from typing import Literal

from pydantic import BaseModel, Field

Outcome = Literal["answered", "escalate", "decline"]


class ModelAnswer(BaseModel):
    """The structured output Claude must return."""

    outcome: Outcome = Field(
        description=(
            "answered: the sources answer the question. "
            "escalate: a human support agent must handle it. "
            "decline: out of scope, not covered by the sources, or not allowed."
        )
    )
    answer: str = Field(description="The reply shown to the customer.")
    cited_sources: list[str] = Field(
        description="IDs of the sources the answer relies on, such as KB-1002 or VG-619."
    )
    escalation_reason: str = Field(
        description="Why a human is needed. Empty unless outcome is escalate."
    )


class Source(BaseModel):
    id: str
    title: str
    type: str


class SupportResponse(BaseModel):
    """What the assistant returns to the API."""

    outcome: Outcome
    answer: str
    escalate: bool
    escalation_reason: str
    sources: list[Source]
