import itertools
from typing import Dict, List

import numpy as np
from netsquid.components.instructions import (
    INSTR_CNOT,
    INSTR_CXDIR,
    INSTR_CYDIR,
    INSTR_CZ,
    INSTR_H,
    INSTR_INIT,
    INSTR_MEASURE,
    INSTR_ROT_X,
    INSTR_ROT_Y,
    INSTR_ROT_Z,
    INSTR_X,
    INSTR_Y,
    INSTR_Z,
)
from netsquid.components.models.qerrormodels import DepolarNoiseModel, T1T2NoiseModel
from netsquid.components.qprocessor import PhysicalInstruction, QuantumProcessor
from netsquid.qubits.operators import Operator
from netsquid_magic.link_layer import (
    MagicLinkLayerProtocol,
    MagicLinkLayerProtocolWithSignaling,
    SingleClickTranslationUnit,
)
from netsquid_magic.magic_distributor import (
    DepolariseWithFailureMagicDistributor,
    DoubleClickMagicDistributor,
    PerfectStateMagicDistributor,
)
from netsquid_nv.magic_distributor import NVSingleClickMagicDistributor
from netsquid_physlayer.heralded_connection import MiddleHeraldedConnection

from qoala.runtime.config import (
    DepolariseLinkConfig,
    GenericQDeviceConfig,
    HeraldedLinkConfig,
    LinkConfig,
    NVLinkConfig,
    NVQDeviceConfig,
    ProcNodeConfig,
    ProcNodeNetworkConfig,
)
from qoala.runtime.environment import GlobalEnvironment
from qoala.sim.network import ProcNodeNetwork
from qoala.sim.procnode import ProcNode


# TODO: move this to somewhere else
def fidelity_to_prob_max_mixed(fid: float) -> float:
    return (1 - fid) * 4.0 / 3.0


def build_generic_qprocessor(name: str, cfg: GenericQDeviceConfig) -> QuantumProcessor:
    phys_instructions = []

    single_qubit_gate_noise = DepolarNoiseModel(
        depolar_rate=cfg.single_qubit_gate_depolar_prob, time_independent=True
    )

    two_qubit_gate_noise = DepolarNoiseModel(
        depolar_rate=cfg.two_qubit_gate_depolar_prob, time_independent=True
    )

    phys_instructions.append(
        PhysicalInstruction(
            INSTR_INIT,
            parallel=False,
            duration=cfg.init_time,
        )
    )

    for instr in [
        INSTR_ROT_X,
        INSTR_ROT_Y,
        INSTR_ROT_Z,
        INSTR_X,
        INSTR_Y,
        INSTR_Z,
        INSTR_H,
    ]:
        phys_instructions.append(
            PhysicalInstruction(
                instr,
                parallel=False,
                quantum_noise_model=single_qubit_gate_noise,
                apply_q_noise_after=True,
                duration=cfg.single_qubit_gate_time,
            )
        )

    for instr in [INSTR_CNOT, INSTR_CZ]:
        phys_instructions.append(
            PhysicalInstruction(
                instr,
                parallel=False,
                quantum_noise_model=two_qubit_gate_noise,
                apply_q_noise_after=True,
                duration=cfg.two_qubit_gate_time,
            )
        )

    phys_instr_measure = PhysicalInstruction(
        INSTR_MEASURE,
        parallel=False,
        duration=cfg.measure_time,
    )
    phys_instructions.append(phys_instr_measure)

    electron_qubit_noise = T1T2NoiseModel(T1=cfg.T1, T2=cfg.T2)
    mem_noise_models = [electron_qubit_noise] * cfg.num_qubits
    qmem = QuantumProcessor(
        name=name,
        num_positions=cfg.num_qubits,
        mem_noise_models=mem_noise_models,
        phys_instructions=phys_instructions,
    )
    return qmem


def build_nv_qprocessor(name: str, cfg: NVQDeviceConfig) -> QuantumProcessor:

    # noise models for single- and multi-qubit operations
    electron_init_noise = DepolarNoiseModel(
        depolar_rate=cfg.electron_init_depolar_prob, time_independent=True
    )

    electron_single_qubit_noise = DepolarNoiseModel(
        depolar_rate=cfg.electron_single_qubit_depolar_prob, time_independent=True
    )

    carbon_init_noise = DepolarNoiseModel(
        depolar_rate=cfg.carbon_init_depolar_prob, time_independent=True
    )

    carbon_z_rot_noise = DepolarNoiseModel(
        depolar_rate=cfg.carbon_z_rot_depolar_prob, time_independent=True
    )

    ec_noise = DepolarNoiseModel(
        depolar_rate=cfg.ec_gate_depolar_prob, time_independent=True
    )

    electron_qubit_noise = T1T2NoiseModel(T1=cfg.electron_T1, T2=cfg.electron_T2)

    carbon_qubit_noise = T1T2NoiseModel(T1=cfg.carbon_T1, T2=cfg.carbon_T2)

    # defining gates and their gate times

    phys_instructions = []

    electron_position = 0
    carbon_positions = [pos + 1 for pos in range(cfg.num_qubits - 1)]

    phys_instructions.append(
        PhysicalInstruction(
            INSTR_INIT,
            parallel=False,
            topology=carbon_positions,
            quantum_noise_model=carbon_init_noise,
            apply_q_noise_after=True,
            duration=cfg.carbon_init,
        )
    )

    for (instr, dur) in zip(
        [INSTR_ROT_X, INSTR_ROT_Y, INSTR_ROT_Z],
        [cfg.carbon_rot_x, cfg.carbon_rot_y, cfg.carbon_rot_z],
    ):
        phys_instructions.append(
            PhysicalInstruction(
                instr,
                parallel=False,
                topology=carbon_positions,
                quantum_noise_model=carbon_z_rot_noise,
                apply_q_noise_after=True,
                duration=dur,
            )
        )

    phys_instructions.append(
        PhysicalInstruction(
            INSTR_INIT,
            parallel=False,
            topology=[electron_position],
            quantum_noise_model=electron_init_noise,
            apply_q_noise_after=True,
            duration=cfg.electron_init,
        )
    )

    for (instr, dur) in zip(
        [INSTR_ROT_X, INSTR_ROT_Y, INSTR_ROT_Z],
        [cfg.electron_rot_x, cfg.electron_rot_y, cfg.electron_rot_z],
    ):
        phys_instructions.append(
            PhysicalInstruction(
                instr,
                parallel=False,
                topology=[electron_position],
                quantum_noise_model=electron_single_qubit_noise,
                apply_q_noise_after=True,
                duration=dur,
            )
        )

    electron_carbon_topologies = [
        (electron_position, carbon_pos) for carbon_pos in carbon_positions
    ]
    phys_instructions.append(
        PhysicalInstruction(
            INSTR_CXDIR,
            parallel=False,
            topology=electron_carbon_topologies,
            quantum_noise_model=ec_noise,
            apply_q_noise_after=True,
            duration=cfg.ec_controlled_dir_x,
        )
    )

    phys_instructions.append(
        PhysicalInstruction(
            INSTR_CYDIR,
            parallel=False,
            topology=electron_carbon_topologies,
            quantum_noise_model=ec_noise,
            apply_q_noise_after=True,
            duration=cfg.ec_controlled_dir_y,
        )
    )

    M0 = Operator(
        "M0", np.diag([np.sqrt(1 - cfg.prob_error_0), np.sqrt(cfg.prob_error_1)])
    )
    M1 = Operator(
        "M1", np.diag([np.sqrt(cfg.prob_error_0), np.sqrt(1 - cfg.prob_error_1)])
    )

    # hack to set imperfect measurements
    INSTR_MEASURE._meas_operators = [M0, M1]

    phys_instr_measure = PhysicalInstruction(
        INSTR_MEASURE,
        parallel=False,
        topology=[electron_position],
        quantum_noise_model=None,
        duration=cfg.measure,
    )

    phys_instructions.append(phys_instr_measure)

    # add qubits
    mem_noise_models = [electron_qubit_noise] + [carbon_qubit_noise] * len(
        carbon_positions
    )
    qmem = QuantumProcessor(
        name=name,
        num_positions=cfg.num_qubits,
        mem_noise_models=mem_noise_models,
        phys_instructions=phys_instructions,
    )
    return qmem


def build_procnode(cfg: ProcNodeConfig, global_env: GlobalEnvironment) -> ProcNode:
    if cfg.qdevice_typ == "nv":
        qdevice_cfg = cfg.qdevice_cfg
        if not isinstance(qdevice_cfg, NVQDeviceConfig):
            qdevice_cfg = NVQDeviceConfig(**cfg.qdevice_cfg)
        qprocessor = build_nv_qprocessor(f"qdevice_{cfg.name}", cfg=qdevice_cfg)
        procnode = ProcNode(
            cfg.name,
            global_env=global_env,
            qprocessor=qprocessor,
            qdevice_type="nv",
            node_id=cfg.node_id,
        )
    elif cfg.qdevice_typ == "generic":
        qdevice_cfg = cfg.qdevice_cfg
        if not isinstance(qdevice_cfg, GenericQDeviceConfig):
            qdevice_cfg = GenericQDeviceConfig(**cfg.qdevice_cfg)
        qprocessor = build_generic_qprocessor(f"qdevice_{cfg.name}", cfg=qdevice_cfg)
        procnode = ProcNode(
            cfg.name,
            global_env=global_env,
            qprocessor=qprocessor,
            qdevice_type="generic",
            node_id=cfg.node_id,
        )
        # TODO: do this in constructor?
        procnode.qnos.processor.instr_latency = cfg.instr_latency
    return procnode


def build_ll_protocol(
    config: LinkConfig, proc_node1: ProcNode, proc_node2: ProcNode
) -> MagicLinkLayerProtocolWithSignaling:
    if config.typ == "perfect":
        link_dist = PerfectStateMagicDistributor(
            nodes=[proc_node1.node, proc_node2.node], state_delay=0
        )
    elif config.typ == "depolarise":
        link_cfg = config.cfg
        if not isinstance(link_cfg, DepolariseLinkConfig):
            link_cfg = DepolariseLinkConfig(**config.cfg)
        prob_max_mixed = fidelity_to_prob_max_mixed(link_cfg.fidelity)
        link_dist = DepolariseWithFailureMagicDistributor(
            nodes=[proc_node1.node, proc_node2.node],
            prob_max_mixed=prob_max_mixed,
            prob_success=link_cfg.prob_success,
            t_cycle=link_cfg.t_cycle,
        )
    elif config.typ == "nv":
        link_cfg = config.cfg
        if not isinstance(link_cfg, NVLinkConfig):
            link_cfg = NVLinkConfig(**config.cfg)
        link_dist = NVSingleClickMagicDistributor(
            nodes=[proc_node1.node, proc_node2.node],
            length_A=link_cfg.length_A,
            length_B=link_cfg.length_B,
            full_cycle=link_cfg.full_cycle,
            cycle_time=link_cfg.cycle_time,
            alpha=link_cfg.alpha,
        )
    elif config.typ == "heralded":
        link_cfg = config.cfg
        if not isinstance(link_cfg, HeraldedLinkConfig):
            link_cfg = HeraldedLinkConfig(**config.cfg)
        connection = MiddleHeraldedConnection(name="heralded_conn", **link_cfg.dict())
        link_dist = DoubleClickMagicDistributor(
            [proc_node1.node, proc_node2.node], connection
        )
    else:
        raise ValueError

    return MagicLinkLayerProtocolWithSignaling(
        nodes=[proc_node1.node, proc_node2.node],
        magic_distributor=link_dist,
        translation_unit=SingleClickTranslationUnit(),
    )


def build_network(
    config: ProcNodeNetworkConfig, global_env: GlobalEnvironment
) -> ProcNodeNetwork:
    proc_nodes: Dict[str, ProcNode] = {}
    link_prots: List[MagicLinkLayerProtocol] = []

    for cfg in config.nodes:
        proc_nodes[cfg.name] = build_procnode(cfg, global_env)

    for (_, s1), (_, s2) in itertools.combinations(proc_nodes.items(), 2):
        s1.connect_to(s2)

    for cfg in config.links:
        proc_node1 = proc_nodes[cfg.node1]
        proc_node2 = proc_nodes[cfg.node2]
        link_prot = build_ll_protocol(cfg, proc_node1, proc_node2)
        proc_node1.assign_ll_protocol(proc_node2.node.ID, link_prot)
        proc_node2.assign_ll_protocol(proc_node1.node.ID, link_prot)

        link_prots.append(link_prot)

    return ProcNodeNetwork(proc_nodes, link_prots)
