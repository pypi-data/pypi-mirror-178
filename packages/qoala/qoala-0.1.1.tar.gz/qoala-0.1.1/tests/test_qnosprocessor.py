from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Generator, List, Optional, Tuple

import pytest
from netqasm.lang.parsing import parse_text_subroutine

from pydynaa import EventExpression
from qoala.lang.iqoala import IqoalaProgram, IqoalaSubroutine, ProgramMeta
from qoala.runtime.program import ProgramInput, ProgramInstance, ProgramResult
from qoala.runtime.schedule import ProgramTaskList
from qoala.sim.memmgr import AllocError, MemoryManager
from qoala.sim.memory import ProgramMemory, Topology, UnitModule
from qoala.sim.message import Message
from qoala.sim.process import IqoalaProcess
from qoala.sim.qdevice import PhysicalQuantumMemory, QDevice
from qoala.sim.qnosinterface import QnosInterface
from qoala.sim.qnosprocessor import GenericProcessor, QnosProcessor
from qoala.util.tests import yield_from

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


class MockQDevice(QDevice):
    def __init__(self, topology: Topology) -> None:
        self._memory = PhysicalQuantumMemory(topology.comm_ids, topology.mem_ids)

    def set_mem_pos_in_use(self, id: int, in_use: bool) -> None:
        pass


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


def create_program(
    subroutines: Optional[Dict[str, IqoalaSubroutine]] = None,
    meta: Optional[ProgramMeta] = None,
) -> IqoalaProgram:
    if subroutines is None:
        subroutines = {}
    if meta is None:
        meta = ProgramMeta.empty("prog")
    return IqoalaProgram(instructions=[], subroutines=subroutines, meta=meta)


def create_process(
    pid: int, program: IqoalaProgram, unit_module: UnitModule
) -> IqoalaProcess:
    instance = ProgramInstance(
        pid=pid,
        program=program,
        inputs=ProgramInput({}),
        tasks=ProgramTaskList.empty(program),
    )
    mem = ProgramMemory(pid=pid, unit_module=unit_module)

    process = IqoalaProcess(
        prog_instance=instance,
        prog_memory=mem,
        csockets={},
        epr_sockets=program.meta.epr_sockets,
        subroutines=program.subroutines,
        requests={},
        result=ProgramResult(values={}),
    )
    return process


def create_process_with_subrt(
    pid: int, subrt_text: str, unit_module: UnitModule
) -> IqoalaProcess:
    subrt = parse_text_subroutine(subrt_text)
    iqoala_subrt = IqoalaSubroutine("subrt", subrt, return_map={})
    meta = ProgramMeta.empty("alice")
    meta.epr_sockets = {0: "bob"}
    program = create_program(subroutines={"subrt": iqoala_subrt}, meta=meta)
    return create_process(pid, program, unit_module)


def execute_process(processor: GenericProcessor, process: IqoalaProcess) -> int:
    subroutines = process.prog_instance.program.subroutines
    netqasm_instructions = subroutines["subrt"].subroutine.instructions

    instr_count = 0

    instr_idx = 0
    while instr_idx < len(netqasm_instructions):
        instr_count += 1
        instr_idx = yield_from(processor.assign(process, "subrt", instr_idx))
    return instr_count


def execute_multiple_processes(
    processor: GenericProcessor, processes: List[IqoalaProcess]
) -> None:
    for proc in processes:
        subroutines = proc.prog_instance.program.subroutines
        netqasm_instructions = subroutines["subrt"].subroutine.instructions
        for i in range(len(netqasm_instructions)):
            yield_from(processor.assign(proc, "subrt", i))


def setup_components(
    topology: Topology,
    netstack_result: Optional[MockNetstackResultInfo] = None,
    asynchronous: bool = False,
) -> Tuple[QnosProcessor, UnitModule]:
    qdevice = MockQDevice(topology)
    unit_module = UnitModule.from_topology(topology)
    interface = MockQnosInterface(qdevice, netstack_result)
    processor = QnosProcessor(interface, asynchronous)
    return (processor, unit_module)


def verify_native(subrt_text: str, num_instr: int) -> bool:
    # check that the instructions in the subroutine text do not expand
    # to additional instructions when parsed and compiled
    parsed_subrt = parse_text_subroutine(subrt_text)
    assert len(parsed_subrt.instructions) == num_instr


def test_set_reg():
    processor, unit_module = setup_components(Topology(comm_ids={0}, mem_ids={1}))

    subrt = """
    set R0 17
    """
    process = create_process_with_subrt(0, subrt, unit_module)
    processor._interface.memmgr.add_process(process)
    execute_process(processor, process)
    assert process.prog_memory.shared_mem.get_reg_value("R0") == 17


def test_add():
    processor, unit_module = setup_components(Topology(comm_ids={0}, mem_ids={1}))

    subrt = """
    set R0 2
    set R1 5
    add R2 R0 R1
    """
    process = create_process_with_subrt(0, subrt, unit_module)
    processor._interface.memmgr.add_process(process)
    execute_process(processor, process)
    assert process.prog_memory.shared_mem.get_reg_value("R2") == 7


def test_alloc_qubit():
    processor, unit_module = setup_components(Topology(comm_ids={0}, mem_ids={1}))

    subrt = """
    set Q0 0
    qalloc Q0
    """
    process = create_process_with_subrt(0, subrt, unit_module)
    processor._interface.memmgr.add_process(process)
    execute_process(processor, process)

    assert processor._interface.memmgr.phys_id_for(process.pid, 0) == 0
    assert processor._interface.memmgr.phys_id_for(process.pid, 1) is None


def test_free_qubit():
    processor, unit_module = setup_components(Topology(comm_ids={0}, mem_ids={1}))

    subrt = """
    set Q0 0
    qalloc Q0
    qfree Q0
    """
    process = create_process_with_subrt(0, subrt, unit_module)
    processor._interface.memmgr.add_process(process)
    execute_process(processor, process)

    assert processor._interface.memmgr.phys_id_for(process.pid, 0) is None
    assert processor._interface.memmgr.phys_id_for(process.pid, 1) is None


def test_free_non_allocated():
    processor, unit_module = setup_components(Topology(comm_ids={0}, mem_ids={1}))

    subrt = """
    set Q0 0
    qfree Q0
    """
    process = create_process_with_subrt(0, subrt, unit_module)
    processor._interface.memmgr.add_process(process)

    with pytest.raises(AllocError):
        execute_process(processor, process)


def test_alloc_multiple():
    processor, unit_module = setup_components(Topology(comm_ids={0}, mem_ids={1}))

    subrt = """
    set Q0 0
    set Q1 1
    qalloc Q0
    qalloc Q1
    """
    process = create_process_with_subrt(0, subrt, unit_module)
    processor._interface.memmgr.add_process(process)
    execute_process(processor, process)

    assert processor._interface.memmgr.phys_id_for(process.pid, 0) == 0
    assert processor._interface.memmgr.phys_id_for(process.pid, 1) == 1


def test_alloc_multiprocess():
    processor, unit_module = setup_components(Topology(comm_ids={0}, mem_ids={1}))

    subrt0 = """
    set Q0 0
    qalloc Q0
    """
    subrt1 = """
    set Q1 1
    qalloc Q1
    """
    process0 = create_process_with_subrt(0, subrt0, unit_module)
    process1 = create_process_with_subrt(1, subrt1, unit_module)
    processor._interface.memmgr.add_process(process0)
    processor._interface.memmgr.add_process(process1)
    execute_multiple_processes(processor, [process0, process1])

    assert processor._interface.memmgr.phys_id_for(process0.pid, 0) == 0
    assert processor._interface.memmgr.phys_id_for(process0.pid, 1) is None
    assert processor._interface.memmgr.phys_id_for(process1.pid, 0) is None
    assert processor._interface.memmgr.phys_id_for(process1.pid, 1) == 1

    assert processor._interface.memmgr._physical_mapping[0].pid == process0.pid
    assert processor._interface.memmgr._physical_mapping[1].pid == process1.pid


def test_alloc_multiprocess_same_virt_id():
    processor, unit_module = setup_components(Topology(comm_ids={0, 1}, mem_ids={0, 1}))

    subrt0 = """
    set Q0 0
    qalloc Q0
    """
    subrt1 = """
    set Q0 0
    qalloc Q0
    """

    process0 = create_process_with_subrt(0, subrt0, unit_module)
    process1 = create_process_with_subrt(1, subrt1, unit_module)
    processor._interface.memmgr.add_process(process0)
    processor._interface.memmgr.add_process(process1)
    execute_multiple_processes(processor, [process0, process1])

    assert processor._interface.memmgr.phys_id_for(process0.pid, 0) == 0
    assert processor._interface.memmgr.phys_id_for(process0.pid, 1) is None
    assert processor._interface.memmgr.phys_id_for(process1.pid, 0) == 1
    assert processor._interface.memmgr.phys_id_for(process1.pid, 1) is None

    assert processor._interface.memmgr._physical_mapping[0].pid == process0.pid
    assert processor._interface.memmgr._physical_mapping[1].pid == process1.pid


def test_alloc_multiprocess_same_virt_id_trait_not_available():
    processor, unit_module = setup_components(Topology(comm_ids={0}, mem_ids={0, 1}))

    subrt0 = """
    set Q0 0
    qalloc Q0
    """
    subrt1 = """
    set Q0 0
    qalloc Q0
    """

    process0 = create_process_with_subrt(0, subrt0, unit_module)
    process1 = create_process_with_subrt(1, subrt1, unit_module)
    processor._interface.memmgr.add_process(process0)
    processor._interface.memmgr.add_process(process1)

    with pytest.raises(AllocError):
        execute_multiple_processes(processor, [process0, process1])


def test_no_branch():
    processor, unit_module = setup_components(Topology(comm_ids={0}, mem_ids={0}))

    subrt = """
    set R3 3
    set R0 0
    beq R3 R0 LABEL1
    set R1 1
    add C0 R3 R1
LABEL1:
    """
    verify_native(subrt, 5)

    process = create_process_with_subrt(0, subrt, unit_module)
    processor._interface.memmgr.add_process(process)
    instr_count = execute_process(processor, process)

    assert instr_count == 5
    assert process.prog_memory.shared_mem.get_reg_value("C0") == 4


def test_branch():
    processor, unit_module = setup_components(Topology(comm_ids={0}, mem_ids={0}))

    subrt = """
    set R3 3
    set C3 3
    beq R3 C3 LABEL1
    set R1 1
    add C0 R3 R1
LABEL1:
    """
    verify_native(subrt, 5)

    process = create_process_with_subrt(0, subrt, unit_module)
    processor._interface.memmgr.add_process(process)
    instr_count = execute_process(processor, process)

    assert instr_count == 3
    assert process.prog_memory.shared_mem.get_reg_value("C0") == 0


def test_array():
    processor, unit_module = setup_components(Topology(comm_ids={0}, mem_ids={0}))

    subrt = """
    set C10 10
    array C10 @0
    set R4 4
    set C8 8
    store C8 @0[R4]
    """
    verify_native(subrt, 5)

    process = create_process_with_subrt(0, subrt, unit_module)
    processor._interface.memmgr.add_process(process)
    instr_count = execute_process(processor, process)

    assert instr_count == 5
    array = process.prog_memory.shared_mem.get_array(0)
    assert len(array) == 10
    assert all(
        process.prog_memory.shared_mem.get_array_value(0, i) is None
        for i in range(10)
        if i != 4
    )
    assert process.prog_memory.shared_mem.get_array_value(0, 4) == 8


# TODO: decide on role of create_epr and recv_epr in qnosprocessor

# def test_create_epr():
#     processor, unit_module = setup_components(Topology(comm_ids={0}, mem_ids={0}))

#     qubit_array = 0
#     arg_array = 1
#     result_array = 2

#     qubit_id = 8
#     create_type = 2  # RSP
#     epr_count = 6
#     rot_x_remote2 = 1

#     remote_id = 2
#     epr_sck_id = 4

#     pid = 0
#     # fidelity = 0.75

#     subrt = f"""
#     array 1 @{qubit_array}
#     store {qubit_id} @{qubit_array}[0]
#     array 20 @{arg_array}
#     store {create_type} @{arg_array}[{SER_CREATE_IDX_TYPE}]
#     store {epr_count} @{arg_array}[{SER_CREATE_IDX_NUMBER}]
#     store {rot_x_remote2} @{arg_array}[{SER_CREATE_IDX_ROTATION_X_REMOTE2}]
#     array 10 @{result_array}
#     create_epr({remote_id}, {epr_sck_id}) 0 1 2
#     """
#     process = create_process_with_subrt(pid, subrt, unit_module)
#     processor._interface.memmgr.add_process(process)
#     execute_process(processor, process)

#     expected_request = NetstackCreateRequest(
#         remote_id=remote_id,
#         epr_socket_id=epr_sck_id,
#         typ=EprCreateType.REMOTE_STATE_PREP,
#         num_pairs=epr_count,
#         fidelity=1.0,  # TODO: fix hardcoded only allowed value
#         virt_qubit_ids=[8],
#         result_array_addr=result_array,
#     )

#     assert process.prog_memory.requests[0] == expected_request

#     mem = process.prog_memory.shared_mem
#     assert mem.get_array_value(qubit_array, 0) == qubit_id
#     assert mem.get_array_value(arg_array, SER_CREATE_IDX_TYPE) == create_type
#     assert mem.get_array_value(arg_array, SER_CREATE_IDX_NUMBER) == epr_count
#     assert (
#         mem.get_array_value(arg_array, SER_CREATE_IDX_ROTATION_X_REMOTE2)
#         == rot_x_remote2
#     )


# def test_create_epr_async():
#     processor, unit_module = setup_components(
#         Topology(comm_ids={0}, mem_ids={0}), asynchronous=True
#     )

#     qubit_array = 0
#     arg_array = 1
#     result_array = 2

#     qubit_id = 8
#     create_type = 2  # RSP
#     epr_count = 6
#     rot_x_remote2 = 1

#     remote_id = 2
#     epr_sck_id = 4

#     pid = 0
#     # fidelity = 0.75

#     subrt = f"""
#     array 1 @{qubit_array}
#     store {qubit_id} @{qubit_array}[0]
#     array 20 @{arg_array}
#     store {create_type} @{arg_array}[{SER_CREATE_IDX_TYPE}]
#     store {epr_count} @{arg_array}[{SER_CREATE_IDX_NUMBER}]
#     store {rot_x_remote2} @{arg_array}[{SER_CREATE_IDX_ROTATION_X_REMOTE2}]
#     array 10 @{result_array}
#     create_epr({remote_id}, {epr_sck_id}) 0 1 2
#     """
#     process = create_process_with_subrt(pid, subrt, unit_module)
#     processor._interface.memmgr.add_process(process)
#     execute_process(processor, process)

#     expected_request = NetstackCreateRequest(
#         remote_id=remote_id,
#         epr_socket_id=epr_sck_id,
#         typ=EprCreateType.REMOTE_STATE_PREP,
#         num_pairs=epr_count,
#         fidelity=1.0,  # TODO: fix hardcoded only allowed value
#         virt_qubit_ids=[8],
#         result_array_addr=result_array,
#     )

#     assert processor._interface.send_events[0] == InterfaceEvent(
#         "netstack", Message(expected_request)
#     )

#     mem = process.prog_memory.shared_mem
#     assert mem.get_array_value(qubit_array, 0) == qubit_id
#     assert mem.get_array_value(arg_array, SER_CREATE_IDX_TYPE) == create_type
#     assert mem.get_array_value(arg_array, SER_CREATE_IDX_NUMBER) == epr_count
#     assert (
#         mem.get_array_value(arg_array, SER_CREATE_IDX_ROTATION_X_REMOTE2)
#         == rot_x_remote2
#     )


# def test_recv_epr():
#     processor, unit_module = setup_components(Topology(comm_ids={0}, mem_ids={0}))

#     qubit_array = 0
#     result_array = 2

#     qubit_id = 8

#     remote_id = 2
#     epr_sck_id = 4

#     pid = 0

#     subrt = f"""
#     array 1 @{qubit_array}
#     store {qubit_id} @{qubit_array}[0]
#     array 10 @{result_array}
#     recv_epr({remote_id}, {epr_sck_id}) 0 2
#     """
#     process = create_process_with_subrt(pid, subrt, unit_module)
#     processor._interface.memmgr.add_process(process)
#     execute_process(processor, process)

#     expected_request = NetstackReceiveRequest(
#         remote_id=remote_id,
#         epr_socket_id=epr_sck_id,
#         typ=None,  # TODO: fix recv_epr instruction
#         num_pairs=None,  # TODO: fix recv_epr instruction
#         fidelity=1.0,  # TODO: fix hardcoded only allowed value
#         virt_qubit_ids=[8],
#         result_array_addr=result_array,
#     )

#     assert process.prog_memory.requests[0] == expected_request

#     mem = process.prog_memory.shared_mem
#     assert mem.get_array_value(qubit_array, 0) == qubit_id


def test_wait_all():
    pid = 0
    array_id = 3
    start_idx = 5
    end_idx = 9

    # Let the mock interface write some result to the array such that
    # our "wait_all" instruction will unblock
    netstack_result = MockNetstackResultInfo(
        pid=pid, array_id=array_id, start_idx=start_idx, end_idx=end_idx
    )

    processor, unit_module = setup_components(
        Topology(comm_ids={0}, mem_ids={0}), netstack_result
    )

    subrt = f"""
    array 10 @{array_id}
    wait_all @{array_id}[{start_idx}:{end_idx}]
    """
    process = create_process_with_subrt(pid, subrt, unit_module)
    processor._interface.memmgr.add_process(process)
    execute_process(processor, process)

    mem = process.prog_memory.shared_mem
    assert all(
        mem.get_array_value(array_id, i) is not None for i in range(start_idx, end_idx)
    )


if __name__ == "__main__":
    test_set_reg()
    test_add()
    test_alloc_qubit()
    test_free_qubit()
    test_free_non_allocated()
    test_alloc_multiple()
    test_alloc_multiprocess()
    test_alloc_multiprocess_same_virt_id()
    test_alloc_multiprocess_same_virt_id_trait_not_available()
    test_no_branch()
    test_branch()
    test_array()
    test_wait_all()
