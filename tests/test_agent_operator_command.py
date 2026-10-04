from agent.command import AgentOperatorCommand, parse_agent_operator_command
import pytest


def test_agent_operator_command_accepts_canonical_shape():
    command = parse_agent_operator_command({"id": "cmd-1", "action": "evidence.record", "input": {"key": "value"}, "evidence_required": True})
    assert isinstance(command, AgentOperatorCommand)
    assert command.action == "evidence.record"


def test_agent_operator_command_rejects_unknown_fields():
    with pytest.raises(Exception):
        parse_agent_operator_command({"id": "cmd-1", "action": "x", "input": {}, "extra": True})
