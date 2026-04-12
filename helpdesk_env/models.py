from typing import Optional, Any
from pydantic import BaseModel


class HelpdeskAction(BaseModel):
    action_type: str
    value: Optional[Any] = None


class HelpdeskObservation(BaseModel):
    task_name: str
    ticket_id: str
    customer_tier: str
    message: str
    status: str
    sla_hours_left: int
    history: str


class HelpdeskInfo(BaseModel):
    step_count: int
    max_steps: int
    last_action_error: Optional[str] = None
    internal_state: dict
