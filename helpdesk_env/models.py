from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any


Category = Literal["billing", "technical", "account", "shipping", "security"]
Priority = Literal["low", "medium", "high"]
Team = Literal["billing_team", "tech_team", "account_team", "shipping_team", "security_team"]


class HelpdeskObservation(BaseModel):
    task_name: str
    ticket_id: str
    customer_tier: Literal["free", "premium"]
    message: str
    status: Literal["open", "in_progress", "resolved"]
    sla_hours_left: int
    history: str = ""


class HelpdeskAction(BaseModel):
    action_type: Literal[
        "set_category",
        "set_priority",
        "assign_team",
        "request_info",
        "send_reply",
        "resolve_ticket",
        "noop"
    ]
    value: Optional[str] = None


class HelpdeskInfo(BaseModel):
    step_count: int
    max_steps: int
    last_action_error: Optional[str] = None
    internal_state: Dict[str, Any] = Field(default_factory=dict)