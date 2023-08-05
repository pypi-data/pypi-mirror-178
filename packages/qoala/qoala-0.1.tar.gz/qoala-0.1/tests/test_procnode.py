from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Generator, List, Optional, Tuple, Type

import netsquid as ns
from netqasm.lang.instr.core import CreateEPRInstruction, RecvEPRInstruction
from netqasm.lang.parsing import parse_text_subroutine
from netqasm.sdk.build_epr import SER_RESPONSE_KEEP_LEN
from netsquid.components import QuantumProcessor
from netsquid.nodes import Node
from netsquid.qubits import ketstates
from netsquid.qubits.ketstates import BellIndex
from netsquid_magic.link_layer import (
    MagicLinkLayerProtocolWithSignaling,
    SingleClickTranslationUnit,
)
from netsquid_magic.magic_distributor import PerfectStateMagicDistributor
from qlink_interface import ReqCreateBase, ResCreateAndKeep
from qlink_interface.interface import ResCreate

from pydynaa import EventExpression
from qoala.lang.iqoala import (
    AssignCValueOp,
    ClassicalIqoalaOp,
    IqoalaParser,
    IqoalaProgram,
    IqoalaRequest,
    IqoalaSubroutine,
    IQoalaSubroutineParser,
    IqoalaVector,
    ProgramMeta,
    ReceiveCMsgOp,
    RunSubroutineOp,
    SendCMsgOp,
)
from qoala.runtime.config import GenericQDeviceConfig
from qoala.runtime.environment import (
    GlobalEnvironment,
    GlobalNodeInfo,
    LocalEnvironment,
)
from qoala.runtime.program import ProgramInput, ProgramInstance, ProgramResult
from qoala.runtime.schedule import ProgramTaskList
from qoala.sim.build import build_generic_qprocessor
from qoala.sim.csocket import ClassicalSocket
from qoala.sim.egp import EgpProtocol
from qoala.sim.hostinterface import HostInterface
from qoala.sim.memmgr import AllocError, MemoryManager
from qoala.sim.memory import ProgramMemory, SharedMemory, Topology, UnitModule
from qoala.sim.message import Message
from qoala.sim.netstackinterface import NetstackInterface
from qoala.sim.process import IqoalaProcess
from qoala.sim.procnode import ProcNode
from qoala.sim.qdevice import (
    PhysicalQuantumMemory,
    QDevice,
    QDeviceCommand,
    QDeviceType,
)
from qoala.sim.qnosinterface import QnosInterface
from qoala.sim.requests import (
    EprCreateType,
    NetstackCreateRequest,
    NetstackReceiveRequest,
)
from qoala.util.tests import has_multi_state, netsquid_run

MOCK_MESSAGE = Message(content=42)
MOCK_QNOS_RET_REG = "R0"
MOCK_QNOS_RET_VALUE = 7


@dataclass(eq=True, frozen=True)
class InterfaceEvent:
    peer: str
    msg: Message


@dataclass(eq=True, frozen=True)
class FlushEvent:
    pass


@dataclass(eq=True, frozen=True)
class SignalEvent:
    pass


class MockNetstackInterface(NetstackInterface):
    def __init__(
        self,
        local_env: LocalEnvironment,
        qdevice: QDevice,
        memmgr: MemoryManager,
        mock_result: ResCreate,
    ) -> None:
        self._qdevice = qdevice
        self._local_env = local_env
        self._memmgr = memmgr
        self._mock_result = mock_result

        self._requests_put: Dict[int, List[ReqCreateBase]] = {}
        self._awaited_result_ck: List[int] = []  # list of remote ids
        self._awaited_mem_free_sig_count: int = 0

    def put_request(self, remote_id: int, request: ReqCreateBase) -> None:
        if remote_id not in self._requests_put:
            self._requests_put[remote_id] = []
        self._requests_put[remote_id].append(request)

    def await_result_create_keep(
        self, remote_id: int
    ) -> Generator[EventExpression, None, ResCreateAndKeep]:
        self._awaited_result_ck.append(remote_id)
        return self._mock_result
        yield  # to make this behave as a generator

    def await_memory_freed_signal(
        self, pid: int, virt_id: int
    ) -> Generator[EventExpression, None, None]:
        raise AllocError
        yield  # to make this behave as a generator

    def send_qnos_msg(self, msg: Message) -> None:
        return None

    def send_peer_msg(self, peer: str, msg: Message) -> None:
        return None

    def receive_peer_msg(self, peer: str) -> Generator[EventExpression, None, Message]:
        return None
        yield  # to make this behave as a generator

    def reset(self) -> None:
        self._requests_put = {}
        self._awaited_result_ck = []
        self._awaited_mem_free_sig_count = 0


class MockQDevice(QDevice):
    def __init__(self, topology: Topology) -> None:
        self._memory = PhysicalQuantumMemory(topology.comm_ids, topology.mem_ids)

        self._executed_commands: List[QDeviceCommand] = []

    @property
    def typ(self) -> QDeviceType:
        return QDeviceType.GENERIC

    def set_mem_pos_in_use(self, id: int, in_use: bool) -> None:
        pass

    def execute_commands(
        self, commands: List[QDeviceCommand]
    ) -> Generator[EventExpression, None, Optional[int]]:
        self._executed_commands.extend(commands)
        return None
        yield

    def reset(self) -> None:
        self._executed_commands = []


@dataclass
class MockNetstackResultInfo:
    pid: int
    array_id: int
    start_idx: int
    end_idx: int


class MockQnosInterface(QnosInterface):
    def __init__(
        self,
        qdevice: QDevice,
        netstack_result_info: Optional[MockNetstackResultInfo] = None,
    ) -> None:
        self.send_events: List[InterfaceEvent] = []
        self.recv_events: List[InterfaceEvent] = []
        self.flush_events: List[FlushEvent] = []
        self.signal_events: List[SignalEvent] = []

        self._qdevice = qdevice
        self._memmgr = MemoryManager("alice", self._qdevice)

        self.netstack_result_info: Optional[
            MockNetstackResultInfo
        ] = netstack_result_info

    def send_peer_msg(self, peer: str, msg: Message) -> None:
        self.send_events.append(InterfaceEvent(peer, msg))

    def receive_peer_msg(self, peer: str) -> Generator[EventExpression, None, Message]:
        self.recv_events.append(InterfaceEvent(peer, MOCK_MESSAGE))
        return MOCK_MESSAGE
        yield  # to make it behave as a generator

    def send_host_msg(self, msg: Message) -> None:
        self.send_events.append(InterfaceEvent("host", msg))

    def receive_host_msg(self) -> Generator[EventExpression, None, Message]:
        self.recv_events.append(InterfaceEvent("host", MOCK_MESSAGE))
        return MOCK_MESSAGE
        yield  # to make it behave as a generator

    def send_netstack_msg(self, msg: Message) -> None:
        self.send_events.append(InterfaceEvent("netstack", msg))

    def receive_netstack_msg(self) -> Generator[EventExpression, None, Message]:
        self.recv_events.append(InterfaceEvent("netstack", MOCK_MESSAGE))
        if self.netstack_result_info is not None:
            mem = self.memmgr._processes[
                self.netstack_result_info.pid
            ].prog_memory.shared_mem
            array_id = self.netstack_result_info.array_id
            start_idx = self.netstack_result_info.start_idx
            end_idx = self.netstack_result_info.end_idx
            for i in range(start_idx, end_idx):
                mem.set_array_value(array_id, i, 42)
        return MOCK_MESSAGE
        yield  # to make it behave as a generator

    def flush_netstack_msgs(self) -> None:
        self.flush_events.append(FlushEvent())

    def signal_memory_freed(self) -> None:
        self.signal_events.append(SignalEvent())

    @property
    def name(self) -> str:
        return "mock"


class MockHostInterface(HostInterface):
    def __init__(self, shared_mem: Optional[SharedMemory] = None) -> None:
        self.send_events: List[InterfaceEvent] = []
        self.recv_events: List[InterfaceEvent] = []

        self.shared_mem = shared_mem

    def send_peer_msg(self, peer: str, msg: Message) -> None:
        self.send_events.append(InterfaceEvent(peer, msg))

    def receive_peer_msg(self, peer: str) -> Generator[EventExpression, None, Message]:
        self.recv_events.append(InterfaceEvent(peer, MOCK_MESSAGE))
        return MOCK_MESSAGE
        yield  # to make it behave as a generator

    def send_qnos_msg(self, msg: Message) -> None:
        self.send_events.append(InterfaceEvent("qnos", msg))

    def receive_qnos_msg(self) -> Generator[EventExpression, None, Message]:
        self.recv_events.append(InterfaceEvent("qnos", MOCK_MESSAGE))
        if self.shared_mem is not None:
            self.shared_mem.set_reg_value(MOCK_QNOS_RET_REG, MOCK_QNOS_RET_VALUE)
        return MOCK_MESSAGE
        yield  # to make it behave as a generator

    @property
    def name(self) -> str:
        return "mock"


def create_program(
    instrs: Optional[List[ClassicalIqoalaOp]] = None,
    subroutines: Optional[Dict[str, IqoalaSubroutine]] = None,
    requests: Optional[Dict[str, IqoalaRequest]] = None,
    meta: Optional[ProgramMeta] = None,
) -> IqoalaProgram:
    if instrs is None:
        instrs = []
    if subroutines is None:
        subroutines = {}

    if requests is None:
        requests = {}
    if meta is None:
        meta = ProgramMeta.empty("prog")
    return IqoalaProgram(
        instructions=instrs, subroutines=subroutines, meta=meta, requests=requests
    )


def create_process(
    pid: int,
    program: IqoalaProgram,
    unit_module: UnitModule,
    host_interface: HostInterface,
    inputs: Optional[Dict[str, Any]] = None,
) -> IqoalaProcess:
    if inputs is None:
        inputs = {}
    prog_input = ProgramInput(values=inputs)
    instance = ProgramInstance(
        pid=pid,
        program=program,
        inputs=prog_input,
        tasks=ProgramTaskList.empty(program),
    )
    mem = ProgramMemory(pid=0, unit_module=unit_module)

    process = IqoalaProcess(
        prog_instance=instance,
        prog_memory=mem,
        csockets={
            id: ClassicalSocket(host_interface, name)
            for (id, name) in program.meta.csockets.items()
        },
        epr_sockets=program.meta.epr_sockets,
        subroutines=program.subroutines,
        requests=program.requests,
        result=ProgramResult(values={}),
    )
    return process


def create_qprocessor(name: str, num_qubits: int) -> QuantumProcessor:
    cfg = GenericQDeviceConfig.perfect_config(num_qubits=num_qubits)
    return build_generic_qprocessor(name=f"{name}_processor", cfg=cfg)


def create_global_env(
    num_qubits: int, names: List[str] = ["alice", "bob", "charlie"]
) -> GlobalEnvironment:

    env = GlobalEnvironment()
    for i, name in enumerate(names):
        env.add_node(i, GlobalNodeInfo(name, i))
    return env


def create_procnode(
    name: str,
    env: GlobalEnvironment,
    num_qubits: int,
    procnode_cls: Type[ProcNode] = ProcNode,
    asynchronous: bool = False,
) -> ProcNode:
    alice_qprocessor = create_qprocessor(name, num_qubits)

    node_id = env.get_node_id(name)
    procnode = procnode_cls(
        name=name,
        global_env=env,
        qprocessor=alice_qprocessor,
        node_id=node_id,
        asynchronous=asynchronous,
    )

    return procnode


def simple_subroutine(name: str, subrt_text: str) -> IqoalaSubroutine:
    subrt = parse_text_subroutine(subrt_text)
    return IqoalaSubroutine(name, subrt, return_map={})


def parse_iqoala_subroutines(subrt_text: str) -> IqoalaSubroutine:
    return IQoalaSubroutineParser(subrt_text).parse()


def create_egp_protocols(node1: Node, node2: Node) -> Tuple[EgpProtocol, EgpProtocol]:
    link_dist = PerfectStateMagicDistributor(nodes=[node1, node2], state_delay=1000.0)
    link_prot = MagicLinkLayerProtocolWithSignaling(
        nodes=[node1, node2],
        magic_distributor=link_dist,
        translation_unit=SingleClickTranslationUnit(),
    )
    return EgpProtocol(node1, link_prot), EgpProtocol(node2, link_prot)


def test_initialize():
    num_qubits = 3
    topology = Topology(comm_ids={0, 1, 2}, mem_ids={0, 1, 2})

    global_env = create_global_env(num_qubits)
    local_env = LocalEnvironment(global_env, global_env.get_node_id("alice"))
    procnode = create_procnode("alice", global_env, num_qubits)
    procnode.qdevice = MockQDevice(topology)

    procnode.host.interface = MockHostInterface()

    mock_result = ResCreateAndKeep(bell_state=BellIndex.B01)
    procnode.netstack.interface = MockNetstackInterface(
        local_env, procnode.qdevice, procnode.memmgr, mock_result
    )

    host_processor = procnode.host.processor
    qnos_processor = procnode.qnos.processor
    netstack_processor = procnode.netstack.processor

    unit_module = UnitModule.default_generic(num_qubits)

    instrs = [AssignCValueOp("x", 3)]
    subrt1 = simple_subroutine(
        "subrt1",
        """
    set R5 42
    """,
    )

    program = create_program(instrs=instrs, subroutines={"subrt1": subrt1})
    process = create_process(
        pid=0,
        program=program,
        unit_module=unit_module,
        host_interface=procnode.host._interface,
        inputs={"x": 1, "theta": 3.14, "name": "alice"},
    )
    procnode.add_process(process)

    host_processor.initialize(process)
    host_mem = process.prog_memory.host_mem
    assert host_mem.read("x") == 1
    assert host_mem.read("theta") == 3.14
    assert host_mem.read("name") == "alice"

    request = NetstackCreateRequest(
        remote_id=1,
        epr_socket_id=0,
        typ=EprCreateType.CREATE_KEEP,
        num_pairs=1,
        fidelity=1.0,
        virt_qubit_ids=[0],
        result_array_addr=0,
    )

    netsquid_run(host_processor.assign(process, instr_idx=0))
    netsquid_run(qnos_processor.assign(process, "subrt1", 0))

    process.shared_mem.init_new_array(0, SER_RESPONSE_KEEP_LEN * 1)
    netsquid_run(netstack_processor.assign(process, request))

    assert process.host_mem.read("x") == 3
    assert process.shared_mem.get_reg_value("R5") == 42
    assert procnode.memmgr.phys_id_for(pid=process.pid, virt_id=0) == 0


def test_2():
    num_qubits = 3
    topology = Topology(comm_ids={0, 1, 2}, mem_ids={0, 1, 2})

    global_env = create_global_env(num_qubits)
    procnode = create_procnode("alice", global_env, num_qubits)
    procnode.qdevice = MockQDevice(topology)

    # procnode.host.interface = MockHostInterface()

    # mock_result = ResCreateAndKeep(bell_state=BellIndex.B01)
    # procnode.netstack.interface = MockNetstackInterface(
    #     local_env, procnode.qdevice, procnode.memmgr, mock_result
    # )

    host_processor = procnode.host.processor
    qnos_processor = procnode.qnos.processor

    unit_module = UnitModule.default_generic(num_qubits)

    instrs = [RunSubroutineOp(None, IqoalaVector([]), "subrt1")]
    subroutines = parse_iqoala_subroutines(
        """
SUBROUTINE subrt1
    params: 
    returns: R5 -> result
    request:
  NETQASM_START
    set R5 42
    ret_reg R5
  NETQASM_END
    """
    )

    program = create_program(instrs=instrs, subroutines=subroutines)
    process = create_process(
        pid=0,
        program=program,
        unit_module=unit_module,
        host_interface=procnode.host._interface,
        inputs={"x": 1, "theta": 3.14, "name": "alice"},
    )
    procnode.add_process(process)

    host_processor.initialize(process)

    netsquid_run(host_processor.assign(process, instr_idx=0))
    netsquid_run(qnos_processor.assign(process, "subrt1", 0))
    host_processor.copy_subroutine_results(process, "subrt1")

    assert process.host_mem.read("result") == 42
    assert process.shared_mem.get_reg_value("R5") == 42


def test_2_async():
    num_qubits = 3
    topology = Topology(comm_ids={0, 1, 2}, mem_ids={0, 1, 2})

    global_env = create_global_env(num_qubits)
    procnode = create_procnode("alice", global_env, num_qubits, asynchronous=True)
    procnode.qdevice = MockQDevice(topology)

    host_processor = procnode.host.processor
    qnos_processor = procnode.qnos.processor

    unit_module = UnitModule.default_generic(num_qubits)

    instrs = [RunSubroutineOp(None, IqoalaVector([]), "subrt1")]
    subroutines = parse_iqoala_subroutines(
        """
SUBROUTINE subrt1
    params: 
    returns: R5 -> result
    request:
  NETQASM_START
    set R5 42
    ret_reg R5
  NETQASM_END
    """
    )

    program = create_program(instrs=instrs, subroutines=subroutines)
    process = create_process(
        pid=0,
        program=program,
        unit_module=unit_module,
        host_interface=procnode.host._interface,
        inputs={"x": 1, "theta": 3.14, "name": "alice"},
    )
    procnode.add_process(process)

    host_processor.initialize(process)

    def host_run() -> Generator[EventExpression, None, None]:
        yield from host_processor.assign(process, instr_idx=0)

    def qnos_run() -> Generator[EventExpression, None, None]:
        yield from qnos_processor.assign(process, "subrt1", 0)
        # Mock sending signal back to Host that subroutine has finished.
        qnos_processor._interface.send_host_msg(Message(None))

    procnode.host.run = host_run
    procnode.qnos.run = qnos_run
    procnode.start()
    ns.sim_run()

    assert process.host_mem.read("result") == 42
    assert process.shared_mem.get_reg_value("R5") == 42


def test_classical_comm():
    num_qubits = 3

    global_env = create_global_env(num_qubits)

    class TestProcNode(ProcNode):
        def run(self) -> Generator[EventExpression, None, None]:
            process = self.memmgr.get_process(0)
            yield from self.host.processor.assign(process, 0)

    alice_procnode = create_procnode(
        "alice", global_env, num_qubits, procnode_cls=TestProcNode
    )
    bob_procnode = create_procnode(
        "bob", global_env, num_qubits, procnode_cls=TestProcNode
    )

    alice_host_processor = alice_procnode.host.processor
    bob_host_processor = bob_procnode.host.processor

    unit_module = UnitModule.default_generic(num_qubits)

    alice_instrs = [SendCMsgOp("csocket_id", "message")]
    alice_meta = ProgramMeta(
        name="alice",
        parameters=["csocket_id", "message"],
        csockets={0: "bob"},
        epr_sockets={},
    )
    alice_program = create_program(instrs=alice_instrs, meta=alice_meta)
    alice_process = create_process(
        pid=0,
        program=alice_program,
        unit_module=unit_module,
        host_interface=alice_procnode.host._interface,
        inputs={"csocket_id": 0, "message": 1337},
    )
    alice_procnode.add_process(alice_process)
    alice_host_processor.initialize(alice_process)

    bob_instrs = [ReceiveCMsgOp("csocket_id", "result")]
    bob_meta = ProgramMeta(
        name="bob", parameters=["csocket_id"], csockets={0: "alice"}, epr_sockets={}
    )
    bob_program = create_program(instrs=bob_instrs, meta=bob_meta)
    bob_process = create_process(
        pid=0,
        program=bob_program,
        unit_module=unit_module,
        host_interface=bob_procnode.host._interface,
        inputs={"csocket_id": 0},
    )
    bob_procnode.add_process(bob_process)
    bob_host_processor.initialize(bob_process)

    alice_procnode.connect_to(bob_procnode)

    # First start Bob, since Alice won't yield on anything (she only does a Send
    # instruction) and therefore calling 'start()' on alice completes her whole
    # protocol while Bob's interface has not even been started.
    bob_procnode.start()
    alice_procnode.start()
    ns.sim_run()

    assert bob_process.host_mem.read("result") == 1337


def test_classical_comm_three_nodes():
    num_qubits = 3

    global_env = create_global_env(num_qubits)

    class SenderProcNode(ProcNode):
        def run(self) -> Generator[EventExpression, None, None]:
            process = self.memmgr.get_process(0)
            yield from self.host.processor.assign(process, 0)

    class ReceiverProcNode(ProcNode):
        def run(self) -> Generator[EventExpression, None, None]:
            process = self.memmgr.get_process(0)
            yield from self.host.processor.assign(process, 0)
            yield from self.host.processor.assign(process, 1)

    alice_procnode = create_procnode(
        "alice", global_env, num_qubits, procnode_cls=SenderProcNode
    )
    bob_procnode = create_procnode(
        "bob", global_env, num_qubits, procnode_cls=SenderProcNode
    )
    charlie_procnode = create_procnode(
        "charlie", global_env, num_qubits, procnode_cls=ReceiverProcNode
    )

    alice_host_processor = alice_procnode.host.processor
    bob_host_processor = bob_procnode.host.processor
    charlie_host_processor = charlie_procnode.host.processor

    unit_module = UnitModule.default_generic(num_qubits)

    alice_instrs = [SendCMsgOp("csocket_id", "message")]
    alice_meta = ProgramMeta(
        name="alice",
        parameters=["csocket_id", "message"],
        csockets={0: "charlie"},
        epr_sockets={},
    )
    alice_program = create_program(instrs=alice_instrs, meta=alice_meta)
    alice_process = create_process(
        pid=0,
        program=alice_program,
        unit_module=unit_module,
        host_interface=alice_procnode.host._interface,
        inputs={"csocket_id": 0, "message": 1337},
    )
    alice_procnode.add_process(alice_process)
    alice_host_processor.initialize(alice_process)

    bob_instrs = [SendCMsgOp("csocket_id", "message")]
    bob_meta = ProgramMeta(
        name="bob",
        parameters=["csocket_id", "message"],
        csockets={0: "charlie"},
        epr_sockets={},
    )
    bob_program = create_program(instrs=bob_instrs, meta=bob_meta)
    bob_process = create_process(
        pid=0,
        program=bob_program,
        unit_module=unit_module,
        host_interface=bob_procnode.host._interface,
        inputs={"csocket_id": 0, "message": 42},
    )
    bob_procnode.add_process(bob_process)
    bob_host_processor.initialize(bob_process)

    charlie_instrs = [
        ReceiveCMsgOp("csocket_id_alice", "result_alice"),
        ReceiveCMsgOp("csocket_id_bob", "result_bob"),
    ]
    charlie_meta = ProgramMeta(
        name="bob",
        parameters=["csocket_id_alice", "csocket_id_bob"],
        csockets={0: "alice", 1: "bob"},
        epr_sockets={},
    )
    charlie_program = create_program(instrs=charlie_instrs, meta=charlie_meta)
    charlie_process = create_process(
        pid=0,
        program=charlie_program,
        unit_module=unit_module,
        host_interface=charlie_procnode.host._interface,
        inputs={"csocket_id_alice": 0, "csocket_id_bob": 1},
    )
    charlie_procnode.add_process(charlie_process)
    charlie_host_processor.initialize(charlie_process)

    alice_procnode.connect_to(charlie_procnode)
    bob_procnode.connect_to(charlie_procnode)

    # First start Charlie, since Alice and Bob don't yield on anything.
    charlie_procnode.start()
    alice_procnode.start()
    bob_procnode.start()
    ns.sim_run()

    assert charlie_process.host_mem.read("result_alice") == 1337
    assert charlie_process.host_mem.read("result_bob") == 42


def test_epr():
    num_qubits = 3

    global_env = create_global_env(num_qubits)
    alice_id = global_env.get_node_id("alice")
    bob_id = global_env.get_node_id("bob")

    class TestProcNode(ProcNode):
        def run(self) -> Generator[EventExpression, None, None]:
            process = self.memmgr.get_process(0)
            request = process.requests["req"]
            yield from self.netstack.processor.assign(process, request)

    alice_procnode = create_procnode(
        "alice", global_env, num_qubits, procnode_cls=TestProcNode
    )
    bob_procnode = create_procnode(
        "bob", global_env, num_qubits, procnode_cls=TestProcNode
    )

    alice_host_processor = alice_procnode.host.processor
    bob_host_processor = bob_procnode.host.processor

    unit_module = UnitModule.default_generic(num_qubits)

    alice_instrs = [SendCMsgOp("csocket_id", "message")]
    alice_meta = ProgramMeta(
        name="alice",
        parameters=["csocket_id", "message"],
        csockets={0: "bob"},
        epr_sockets={},
    )
    alice_program = create_program(instrs=alice_instrs, meta=alice_meta)
    alice_process = create_process(
        pid=0,
        program=alice_program,
        unit_module=unit_module,
        host_interface=alice_procnode.host._interface,
        inputs={"csocket_id": 0, "message": 1337},
    )
    alice_procnode.add_process(alice_process)
    alice_host_processor.initialize(alice_process)

    bob_instrs = [ReceiveCMsgOp("csocket_id", "result")]
    bob_meta = ProgramMeta(
        name="bob", parameters=["csocket_id"], csockets={0: "alice"}, epr_sockets={}
    )
    bob_program = create_program(instrs=bob_instrs, meta=bob_meta)
    bob_process = create_process(
        pid=0,
        program=bob_program,
        unit_module=unit_module,
        host_interface=bob_procnode.host._interface,
        inputs={"csocket_id": 0},
    )
    bob_procnode.add_process(bob_process)
    bob_host_processor.initialize(bob_process)

    alice_procnode.connect_to(bob_procnode)

    alice_request = NetstackCreateRequest(
        remote_id=bob_id,
        epr_socket_id=0,
        typ=EprCreateType.CREATE_KEEP,
        num_pairs=1,
        fidelity=1.0,
        virt_qubit_ids=[0],
        result_array_addr=0,
    )

    bob_request = NetstackReceiveRequest(
        remote_id=alice_id,
        epr_socket_id=0,
        typ=EprCreateType.CREATE_KEEP,
        num_pairs=1,
        fidelity=1.0,
        virt_qubit_ids=[0],
        result_array_addr=0,
    )

    alice_egp, bob_egp = create_egp_protocols(alice_procnode.node, bob_procnode.node)
    alice_procnode.egpmgr.add_egp(bob_id, alice_egp)
    bob_procnode.egpmgr.add_egp(alice_id, bob_egp)
    alice_process.requests = {"req": alice_request}
    bob_process.requests = {"req": bob_request}

    alice_process.shared_mem.init_new_array(0, 10)
    bob_process.shared_mem.init_new_array(0, 10)

    # First start Bob, since Alice won't yield on anything (she only does a Send
    # instruction) and therefore calling 'start()' on alice completes her whole
    # protocol while Bob's interface has not even been started.
    bob_procnode.start()
    alice_procnode.start()
    ns.sim_run()

    assert alice_procnode.memmgr.phys_id_for(pid=0, virt_id=0) == 0
    assert bob_procnode.memmgr.phys_id_for(pid=0, virt_id=0) == 0

    alice_qubit = alice_procnode.qdevice.get_local_qubit(0)
    bob_qubit = bob_procnode.qdevice.get_local_qubit(0)
    assert has_multi_state([alice_qubit, bob_qubit], ketstates.b00)


def test_whole_program():
    server_text = """
META_START
    name: server
    parameters: client_id
    csockets: 0 -> client
    epr_sockets: 0 -> client
META_END

remote_id = assign_cval() : {client_id}
run_subroutine(vec<remote_id>) : subrt1

SUBROUTINE subrt1
    params: remote_id
    returns:
    request: req1
  NETQASM_START
    array 10 @0
    recv_epr C15 C0 C1 C0
    wait_all @0[0:10]
  NETQASM_END

REQUEST req1
  role: receive
  remote_id: {client_id}
  epr_socket_id: 0
  typ: create_keep
  num_pairs: 1
  fidelity: 1.0
  virt_qubit_ids: 0
  result_array_addr: 0
    """
    server_program = IqoalaParser(server_text).parse()

    num_qubits = 3
    unit_module = UnitModule.default_generic(num_qubits)
    global_env = create_global_env(num_qubits, names=["client", "server"])
    server_id = global_env.get_node_id("server")
    client_id = global_env.get_node_id("client")

    class TestProcNode(ProcNode):
        def run(self) -> Generator[EventExpression, None, None]:
            process = self.memmgr.get_process(0)
            self.scheduler.initialize_process(process)

            subrt1 = process.subroutines["subrt1"]
            epr_instr_idx = None
            for i, instr in enumerate(subrt1.subroutine.instructions):
                if isinstance(instr, CreateEPRInstruction) or isinstance(
                    instr, RecvEPRInstruction
                ):
                    epr_instr_idx = i
                    break

            for i in range(epr_instr_idx):
                yield from self.qnos.processor.assign(process, "subrt1", i)

            request = process.requests["req1"].request
            print("hello 1?")
            yield from self.netstack.processor.assign(process, request)

            # wait instr
            yield from self.qnos.processor.assign(process, "subrt1", epr_instr_idx + 1)
            print("hello 2?")
            # yield from self.netstack.processor.assign(process, request)

    server_procnode = create_procnode(
        "server", global_env, num_qubits, procnode_cls=TestProcNode
    )
    server_process = create_process(
        pid=0,
        program=server_program,
        unit_module=unit_module,
        host_interface=server_procnode.host._interface,
        inputs={"client_id": client_id, "csocket_id": 0, "message": 1337},
    )
    server_procnode.add_process(server_process)

    client_text = """
META_START
    name: client
    parameters: server_id
    csockets: 0 -> server
    epr_sockets: 0 -> server
META_END

remote_id = assign_cval() : {server_id}
run_subroutine(vec<remote_id>) : subrt1

SUBROUTINE subrt1
    params: remote_id
    returns:
    request: req1
  NETQASM_START
    set C10 10
    array C10 @0
    create_epr C15 C0 C1 C2 C0
    wait_all @0[0:10]
  NETQASM_END

REQUEST req1
  role: create
  remote_id: {server_id}
  epr_socket_id: 0
  typ: create_keep
  num_pairs: 1
  fidelity: 1.0
  virt_qubit_ids: 0
  result_array_addr: 0
    """
    client_program = IqoalaParser(client_text).parse()
    client_procnode = create_procnode(
        "client", global_env, num_qubits, procnode_cls=TestProcNode
    )
    client_process = create_process(
        pid=0,
        program=client_program,
        unit_module=unit_module,
        host_interface=client_procnode.host._interface,
        inputs={"server_id": server_id, "csocket_id": 0, "message": 1337},
    )
    client_procnode.add_process(client_process)

    client_egp, server_egp = create_egp_protocols(
        client_procnode.node, server_procnode.node
    )
    client_procnode.egpmgr.add_egp(server_id, client_egp)
    server_procnode.egpmgr.add_egp(client_id, server_egp)

    client_procnode.connect_to(server_procnode)

    # client_egp._ll_prot.start()
    server_procnode.start()
    client_procnode.start()
    ns.sim_run()

    assert client_procnode.memmgr.phys_id_for(pid=0, virt_id=0) == 0
    assert server_procnode.memmgr.phys_id_for(pid=0, virt_id=0) == 0
    client_qubit = client_procnode.qdevice.get_local_qubit(0)
    server_qubit = server_procnode.qdevice.get_local_qubit(0)
    assert has_multi_state([client_qubit, server_qubit], ketstates.b00)

    # assert client_procnode.memmgr.phys_id_for(pid=0, virt_id=1) == 1
    # assert server_procnode.memmgr.phys_id_for(pid=0, virt_id=1) == 1


if __name__ == "__main__":
    test_initialize()
    test_2()
    test_2_async()
    test_classical_comm()
    test_classical_comm_three_nodes()
    test_epr()
    test_whole_program()
