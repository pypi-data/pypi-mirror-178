from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple, Type, Union

from netqasm.lang import operand
from netqasm.lang.encoding import RegisterName
from netqasm.sdk.shared_memory import Arrays, RegisterGroup, setup_registers


class RegisterMeta:
    @classmethod
    def prefixes(cls) -> List[str]:
        return ["R", "C", "Q", "M"]

    @classmethod
    def parse(cls, name: str) -> Tuple[RegisterName, int]:
        assert len(name) >= 2
        assert name[0] in cls.prefixes()
        group = RegisterName[name[0]]
        index = int(name[1:])
        assert index < 16
        return group, index


class HostMemory:
    """Classical program memory only available to the Host.
    Simple mapping from variable names to values."""

    def __init__(self, pid: int) -> None:
        self._pid = pid

        # Host memory is represented as a mapping from variables to values.
        # Variables have a name (str) and values (int).
        self._mem: Dict[str, int] = {}

    def write(self, loc: str, value: int) -> None:
        self._mem[loc] = value

    def read(self, loc: str) -> int:
        return self._mem[loc]


class SharedMemory:
    """Classical program memory available to both Host and Qnos.
    Implemented as NetQASM arrays and registers.

    TODO: registers should be moved to QnosMemory."""

    def __init__(self, pid: int) -> None:
        self._pid = pid

        register_names: Dict[RegisterName, RegisterGroup] = setup_registers()
        self._registers: Dict[Dict[RegisterName, RegisterGroup], int] = {}
        # TODO fix this abomination of handling registers
        for name in register_names.keys():
            self._registers[name] = {}  # type: ignore
            for i in range(16):
                self._registers[name][i] = 0  # type: ignore
        self._arrays: Arrays = Arrays()

    def set_reg_value(self, register: Union[str, operand.Register], value: int) -> None:
        if isinstance(register, str):
            name, index = RegisterMeta.parse(register)
        else:
            name, index = register.name, register.index
        self._registers[name][index] = value  # type: ignore

    def get_reg_value(self, register: Union[str, operand.Register]) -> int:
        if isinstance(register, str):
            name, index = RegisterMeta.parse(register)
        else:
            name, index = register.name, register.index
        return self._registers[name][index]  # type: ignore

    # for compatibility with netqasm Futures
    def get_register(self, register: Union[str, operand.Register]) -> Optional[int]:
        return self.get_reg_value(register)

    # for compatibility with netqasm Futures
    def get_array_part(
        self, address: int, index: Union[int, slice]
    ) -> Union[None, int, List[Optional[int]]]:
        if isinstance(index, int):
            return self.get_array_value(address, index)
        elif isinstance(index, slice):
            return self.get_array_values(address, index.start, index.stop)

    def init_new_array(self, address: int, length: int) -> None:
        self._arrays.init_new_array(address, length)

    def get_array(self, address: int) -> List[Optional[int]]:
        return self._arrays._get_array(address)  # type: ignore

    def get_array_entry(self, array_entry: operand.ArrayEntry) -> Optional[int]:
        address, index = self.expand_array_part(array_part=array_entry)
        result = self._arrays[address, index]
        assert (result is None) or isinstance(result, int)
        return result

    def get_array_value(self, addr: int, offset: int) -> Optional[int]:
        address, index = self.expand_array_part(
            array_part=operand.ArrayEntry(operand.Address(addr), offset)
        )
        result = self._arrays[address, index]
        assert (result is None) or isinstance(result, int)
        return result

    def get_array_values(
        self, addr: int, start_offset: int, end_offset
    ) -> List[Optional[int]]:
        values = self.get_array_slice(
            operand.ArraySlice(operand.Address(addr), start_offset, end_offset)
        )
        assert values is not None
        return values

    def set_array_entry(
        self, array_entry: operand.ArrayEntry, value: Optional[int]
    ) -> None:
        address, index = self.expand_array_part(array_part=array_entry)
        self._arrays[address, index] = value

    def set_array_value(self, addr: int, offset: int, value: Optional[int]) -> None:
        address, index = self.expand_array_part(
            array_part=operand.ArrayEntry(operand.Address(addr), offset)
        )
        self._arrays[address, index] = value

    def get_array_slice(
        self, array_slice: operand.ArraySlice
    ) -> Optional[List[Optional[int]]]:
        address, index = self.expand_array_part(array_part=array_slice)
        result = self._arrays[address, index]
        assert (result is None) or isinstance(result, list)
        return result

    def expand_array_part(
        self, array_part: Union[operand.ArrayEntry, operand.ArraySlice]
    ) -> Tuple[int, Union[int, slice]]:
        address: int = array_part.address.address
        index: Union[int, slice]
        if isinstance(array_part, operand.ArrayEntry):
            if isinstance(array_part.index, int):
                index = array_part.index
            else:
                index_from_reg = self.get_reg_value(register=array_part.index)
                if index_from_reg is None:
                    raise RuntimeError(
                        f"Trying to use register {array_part.index} "
                        "to index an array but its value is None"
                    )
                index = index_from_reg
        elif isinstance(array_part, operand.ArraySlice):
            startstop: List[int] = []
            for raw_s in [array_part.start, array_part.stop]:
                if isinstance(raw_s, int):
                    startstop.append(raw_s)
                elif isinstance(raw_s, operand.Register):
                    s = self.get_reg_value(register=raw_s)
                    if s is None:
                        raise RuntimeError(
                            f"Trying to use register {raw_s} to "
                            "index an array but its value is None"
                        )
                    startstop.append(s)
                else:
                    raise RuntimeError(
                        f"Something went wrong: raw_s should be int "
                        f"or Register but is {type(raw_s)}"
                    )
            index = slice(*startstop)
        else:
            raise RuntimeError(
                f"Something went wrong: array_part is a {type(array_part)}"
            )
        return address, index


class QnosMemory:
    """Classical program memory only available to Qnos.
    Not used at the moment.

    TODO: move NetQASM registers into here."""

    def __init__(self, pid: int) -> None:
        self._pid = pid


class QubitTrait:
    pass


class CommQubitTrait(QubitTrait):
    pass


class MemQubitTrait(QubitTrait):
    pass


class DecorenceQubitTrait(QubitTrait):
    def __init__(self, t1: int, t2: int) -> None:
        self._t1, self._t2 = t1, t2


class GateTrait:
    pass


class SingleGateTrait(GateTrait):
    def __init__(self, depolarizing_factor: float) -> None:
        self._depolarizing_factor = depolarizing_factor


class TwoGateTrait(GateTrait):
    def __init__(self, depolarizing_factor: float) -> None:
        self._depolarizing_factor = depolarizing_factor


@dataclass
class Topology:
    comm_ids: Set[int]
    mem_ids: Set[int]


@dataclass(eq=True, frozen=True)
class UnitModule:
    """
    :param qubit_ids: list of qubit IDs
    :param qubit_traits: map from qubit ID to list of qubit traits
    :param gate_traits: map from list of qubit IDs to list of gate traits
    """

    qubit_ids: List[int]
    qubit_traits: Dict[int, List[Type[QubitTrait]]]
    gate_traits: Dict[List[int], List[GateTrait]]

    @property
    def num_qubits(self) -> int:
        return len(self.qubit_ids)

    @classmethod
    def from_topology(cls, topology: Topology) -> UnitModule:
        all_ids = topology.comm_ids.union(topology.mem_ids)
        traits: Dict[int, List[Type[QubitTrait]]] = {i: [] for i in all_ids}
        for i in all_ids:
            if i in topology.comm_ids:
                traits[i].append(CommQubitTrait)
            if i in topology.mem_ids:
                traits[i].append(MemQubitTrait)
        return UnitModule(qubit_ids=list(all_ids), qubit_traits=traits, gate_traits={})

    @classmethod
    def default_generic(cls, num_qubits: int) -> UnitModule:
        return UnitModule(
            qubit_ids=[i for i in range(num_qubits)],
            qubit_traits={i: [CommQubitTrait, MemQubitTrait] for i in range(num_qubits)},  # type: ignore
            gate_traits={},
        )


class QuantumMemory:
    """Quantum memory only available to Qnos. Represented as unit modules."""

    # Only describes the virtual memory space (i.e. unit module).
    # Does not contain 'values' (quantum states) of the virtual memory locations.
    # Does not contain the mapping from virtual to physical space. (Managed by memmgr)

    def __init__(self, pid: int, unit_module: UnitModule) -> None:
        self._pid = pid
        self._unit_module = unit_module

    @property
    def unit_module(self) -> UnitModule:
        return self._unit_module


class ProgramMemory:
    def __init__(self, pid: int, unit_module: UnitModule) -> None:
        self._pid: int = pid

        self._host_memory = HostMemory(pid)
        self._shared_memory = SharedMemory(pid)
        self._qnos_memory = QnosMemory(pid)
        self._quantum_memory = QuantumMemory(pid, unit_module)

        self._prog_counter: int = 0

    @property
    def host_mem(self) -> HostMemory:
        return self._host_memory

    @property
    def shared_mem(self) -> SharedMemory:
        return self._shared_memory

    @property
    def qnos_mem(self) -> QnosMemory:
        return self._qnos_memory

    @property
    def quantum_mem(self) -> QuantumMemory:
        return self._quantum_memory

    @property
    def prog_counter(self) -> int:
        return self._prog_counter

    def increment_prog_counter(self) -> None:
        self._prog_counter += 1

    def set_prog_counter(self, value: int) -> None:
        self._prog_counter = value
