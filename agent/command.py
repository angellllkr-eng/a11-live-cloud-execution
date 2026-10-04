from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class AgentOperatorCommand(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    action: str = Field(min_length=1)
    input: dict[str, Any]
    context: dict[str, Any] | None = None
    requested_by: str | None = None
    evidence_required: bool | None = None


def parse_agent_operator_command(value: Any) -> AgentOperatorCommand:
    return AgentOperatorCommand.model_validate(value)
