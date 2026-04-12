import random
from typing import Tuple

from .models import HelpdeskAction, HelpdeskObservation, HelpdeskInfo
from .dataset import TICKETS
from .tasks import TASKS
from .graders import grade_easy, grade_medium, grade_hard


class HelpdeskEnv:
    """
    HelpdeskEnv — an OpenEnv-compatible environment simulating a real-world
    customer support ticket triage and resolution workflow.

    Unique mechanic: SLA-aware priority escalation.
    Premium customers have a 6-hour SLA. If fewer than 2 hours remain and the
    agent has NOT set priority to 'high', a penalty is applied. This forces the
    agent to react to urgency signals, not just message content.
    """

    def __init__(self, task_name: str = "easy", seed: int = 42):
        self.task_name = task_name
        self.seed = seed
        self.rng = random.Random(seed)

        self.ticket = None
        self.step_count = 0
        self.max_steps = TASKS[task_name]["max_steps"]
        self.state_dict = {}
        self.last_action_error = None
        self._base_sla = 24  # overridden on reset

    def reset(self) -> HelpdeskObservation:
        self.ticket = self.rng.choice(TICKETS)
        self.step_count = 0
        self.last_action_error = None
        self._base_sla = 6 if self.ticket["customer_tier"] == "premium" else 24

        self.state_dict = {
            "category": None,
            "priority": None,
            "team": None,
            "reply": "",
            "status": "open",
        }

        return HelpdeskObservation(
            task_name=self.task_name,
            ticket_id=self.ticket["ticket_id"],
            customer_tier=self.ticket["customer_tier"],
            message=self.ticket["message"],
            status="open",
            sla_hours_left=self._base_sla,
            history="",
        )

    def state(self) -> dict:
        return dict(self.state_dict)

    def _compute_score(self) -> float:
        if self.task_name == "easy":
            return grade_easy(self.state_dict, self.ticket)
        elif self.task_name == "medium":
            return grade_medium(self.state_dict, self.ticket)
        elif self.task_name == "hard":
            return grade_hard(self.state_dict, self.ticket)
        return 0.0

    def _sla_hours_left(self) -> int:
        return max(0, self._base_sla - self.step_count)

    def step(self, action: HelpdeskAction) -> Tuple[HelpdeskObservation, float, bool, dict]:
        self.step_count += 1
        self.last_action_error = None
        reward = 0.0
        expected = self.ticket
        sla_left = self._sla_hours_left()

        # ---------- ACTION HANDLING ---------- #

        if action.action_type == "noop":
            reward -= 0.05

        elif action.action_type == "set_category":
            if action.value:
                self.state_dict["category"] = action.value
                if action.value == expected["category"]:
                    reward += 0.10
                else:
                    reward -= 0.10
            else:
                self.last_action_error = "Missing category value"
                reward -= 0.05

        elif action.action_type == "set_priority":
            if action.value:
                self.state_dict["priority"] = action.value
                if action.value == expected["priority"]:
                    reward += 0.10
                else:
                    reward -= 0.15
                # SLA escalation mechanic: premium customers with <2h SLA need high priority
                if sla_left < 2 and action.value != "high":
                    reward -= 0.20
                    self.last_action_error = "SLA breach: priority should be high for urgent tickets"
            else:
                self.last_action_error = "Missing priority value"
                reward -= 0.05

        elif action.action_type == "assign_team":
            if action.value:
                if self.state_dict["category"] is None:
                    reward -= 0.20
                    self.last_action_error = "Cannot assign team before setting category"
                else:
                    self.state_dict["team"] = action.value
                    if action.value == expected["team"]:
                        reward += 0.10
                    else:
                        reward -= 0.10
            else:
                self.last_action_error = "Missing team value"
                reward -= 0.05

        elif action.action_type == "send_reply":
            if action.value and len(str(action.value).strip()) >= 10:
                self.state_dict["reply"] = action.value
                reply_lower = action.value.lower()
                # keyword match reward — up to +0.20
                keywords = expected.get("reply_keywords", [])
                if keywords:
                    matched = sum(1 for kw in keywords if kw.lower() in reply_lower)
                    reward += 0.20 * (matched / len(keywords))
                else:
                    reward += 0.10
            else:
                self.last_action_error = "Reply too short or missing"
                reward -= 0.10

        elif action.action_type == "resolve_ticket":
            required = [
                self.state_dict.get("category"),
                self.state_dict.get("priority"),
                self.state_dict.get("team"),
            ]
            if None in required:
                reward -= 0.30
                self.last_action_error = "Resolved before completing full triage workflow"
            else:
                reward += 0.20

            if self.task_name == "hard" and len(self.state_dict.get("reply", "")) < 20:
                reward -= 0.10
                self.last_action_error = "Hard task resolved without a proper customer reply"

            self.state_dict["status"] = "resolved"

        elif action.action_type == "request_info":
            reward += 0.02

        else:
            self.last_action_error = f"Unknown action type: {action.action_type}"
            reward -= 0.10

        # ---------- PROGRESS REWARD ---------- #
        progress = sum([
            self.state_dict.get("category") is not None,
            self.state_dict.get("priority") is not None,
            self.state_dict.get("team") is not None,
        ])
        reward += 0.03 * progress

        # ---------- DONE ---------- #
        done = (
            self.step_count >= self.max_steps
            or self.state_dict["status"] == "resolved"
        )

        # Final score bonus
        final_score = self._compute_score()
        reward += final_score * 0.20
        reward = max(-1.0, min(1.0, reward))

        obs = HelpdeskObservation(
            task_name=self.task_name,
            ticket_id=self.ticket["ticket_id"],
            customer_tier=self.ticket["customer_tier"],
            message=self.ticket["message"],
            status=self.state_dict["status"],
            sla_hours_left=sla_left,
            history=self.state_dict.get("reply", ""),
        )

        info = HelpdeskInfo(
            step_count=self.step_count,
            max_steps=self.max_steps,
            last_action_error=self.last_action_error,
            internal_state=self.state_dict,
        ).model_dump()

        return obs, float(reward), done, info
