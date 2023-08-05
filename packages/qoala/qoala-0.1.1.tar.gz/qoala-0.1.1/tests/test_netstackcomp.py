from __future__ import annotations

from typing import Generator

import netsquid as ns
from netsquid.nodes import Node

from pydynaa import EventExpression
from qoala.runtime.environment import (
    GlobalEnvironment,
    GlobalNodeInfo,
    LocalEnvironment,
)
from qoala.sim.message import Message
from qoala.sim.netstackcomp import NetstackComponent
from qoala.sim.netstackinterface import NetstackInterface


class MockNetstackInterface(NetstackInterface):
    def __init__(self, comp: NetstackComponent, local_env: LocalEnvironment) -> None:
        super().__init__(comp, local_env, None, None, None)


def create_netstackcomp(num_other_nodes: int) -> NetstackComponent:
    node = Node(name="alice", ID=0)
    env = GlobalEnvironment()

    node_info = GlobalNodeInfo(node.name, node.ID)
    env.add_node(node.ID, node_info)

    for id in range(1, num_other_nodes + 1):
        node_info = GlobalNodeInfo(f"node_{id}", id)
        env.add_node(id, node_info)

    return NetstackComponent(node, env)


def test_no_other_nodes():
    comp = create_netstackcomp(num_other_nodes=0)

    # should have qnos_in, qnos_out, qnos_mem_in, qnos_mem_out ports
    assert len(comp.ports) == 4
    assert "qnos_in" in comp.ports
    assert "qnos_out" in comp.ports
    assert "qnos_mem_in" in comp.ports
    assert "qnos_mem_out" in comp.ports


def test_one_other_node():
    comp = create_netstackcomp(num_other_nodes=1)

    # should have 4 qnos ports + 2 peer ports
    assert len(comp.ports) == 6
    assert "qnos_in" in comp.ports
    assert "qnos_out" in comp.ports
    assert "qnos_mem_in" in comp.ports
    assert "qnos_mem_out" in comp.ports

    assert "peer_node_1_in" in comp.ports
    assert "peer_node_1_out" in comp.ports

    # Test properties
    assert comp.peer_in_port("node_1") == comp.ports["peer_node_1_in"]
    assert comp.peer_out_port("node_1") == comp.ports["peer_node_1_out"]


def test_many_other_nodes():
    comp = create_netstackcomp(num_other_nodes=5)

    # should have 4 qnos ports + 5 * 2 peer ports
    assert len(comp.ports) == 14
    assert "qnos_in" in comp.ports
    assert "qnos_out" in comp.ports
    assert "qnos_mem_in" in comp.ports
    assert "qnos_mem_out" in comp.ports

    for i in range(1, 6):
        assert f"peer_node_{i}_in" in comp.ports
        assert f"peer_node_{i}_out" in comp.ports
        # Test properties
        assert comp.peer_in_port(f"node_{i}") == comp.ports[f"peer_node_{i}_in"]
        assert comp.peer_out_port(f"node_{i}") == comp.ports[f"peer_node_{i}_out"]


def test_connection():
    alice = Node(name="alice", ID=0)
    bob = Node(name="bob", ID=1)
    env = GlobalEnvironment()

    alice_info = GlobalNodeInfo(alice.name, alice.ID)
    env.add_node(alice.ID, alice_info)
    bob_info = GlobalNodeInfo(bob.name, bob.ID)
    env.add_node(bob.ID, bob_info)

    alice_comp = NetstackComponent(alice, env)
    bob_comp = NetstackComponent(bob, env)

    alice_comp.peer_out_port("bob").connect(bob_comp.peer_in_port("alice"))
    alice_comp.peer_in_port("bob").connect(bob_comp.peer_out_port("alice"))

    class AliceNetstackInterface(MockNetstackInterface):
        def run(self) -> Generator[EventExpression, None, None]:
            self.send_peer_msg("bob", Message("hello"))

    class BobNetstackInterface(MockNetstackInterface):
        def run(self) -> Generator[EventExpression, None, None]:
            msg = yield from self.receive_peer_msg("alice")
            assert msg.content == "hello"

    alice_intf = AliceNetstackInterface(alice_comp, LocalEnvironment(env, alice.ID))
    bob_intf = BobNetstackInterface(bob_comp, LocalEnvironment(env, bob.ID))

    alice_intf.start()
    bob_intf.start()

    ns.sim_run()


def test_three_way_connection():
    alice = Node(name="alice", ID=0)
    bob = Node(name="bob", ID=1)
    charlie = Node(name="charlie", ID=2)
    env = GlobalEnvironment()

    alice_info = GlobalNodeInfo(alice.name, alice.ID)
    env.add_node(alice.ID, alice_info)
    bob_info = GlobalNodeInfo(bob.name, bob.ID)
    env.add_node(bob.ID, bob_info)
    charlie_info = GlobalNodeInfo(charlie.name, charlie.ID)
    env.add_node(charlie.ID, charlie_info)

    alice_comp = NetstackComponent(alice, env)
    bob_comp = NetstackComponent(bob, env)
    charlie_comp = NetstackComponent(charlie, env)

    alice_comp.peer_out_port("bob").connect(bob_comp.peer_in_port("alice"))
    alice_comp.peer_in_port("bob").connect(bob_comp.peer_out_port("alice"))
    alice_comp.peer_out_port("charlie").connect(charlie_comp.peer_in_port("alice"))
    alice_comp.peer_in_port("charlie").connect(charlie_comp.peer_out_port("alice"))
    bob_comp.peer_out_port("charlie").connect(charlie_comp.peer_in_port("bob"))
    bob_comp.peer_in_port("charlie").connect(charlie_comp.peer_out_port("bob"))

    class AliceNetstackInterface(MockNetstackInterface):
        def run(self) -> Generator[EventExpression, None, None]:
            self.send_peer_msg("bob", Message("hello bob"))
            self.send_peer_msg("charlie", Message("hello charlie"))

    class BobNetstackInterface(MockNetstackInterface):
        def run(self) -> Generator[EventExpression, None, None]:
            msg = yield from self.receive_peer_msg("alice")
            assert msg.content == "hello bob"

    class CharlieNetstackInterface(MockNetstackInterface):
        def run(self) -> Generator[EventExpression, None, None]:
            msg = yield from self.receive_peer_msg("alice")
            assert msg.content == "hello charlie"

    alice_intf = AliceNetstackInterface(alice_comp, LocalEnvironment(env, alice.ID))
    bob_intf = BobNetstackInterface(bob_comp, LocalEnvironment(env, bob.ID))
    charlie_intf = CharlieNetstackInterface(
        charlie_comp, LocalEnvironment(env, charlie.ID)
    )

    alice_intf.start()
    bob_intf.start()
    charlie_intf.start()

    ns.sim_run()


if __name__ == "__main__":
    test_no_other_nodes()
    test_one_other_node()
    test_many_other_nodes()

    test_connection()
    test_three_way_connection()
