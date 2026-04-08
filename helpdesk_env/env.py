import random
from typing import Tuple

from .models import HelpdeskAction, HelpdeskObservation, HelpdeskInfo
from .dataset import TICKETS
from .tasks import TASKS
from .graders import grade_easy, grade_medium, grade_hard


class HelpdeskEnv:
    def __init__(self, task_name: str = "easy", seed: int = 42):
        self.task_name = task_name
        self.seed = seed
        self.rng = random.Random(seed)

        self.ticket = None
        self.step_count = 0
        self.max_steps = TASKS[task_name]["max_steps"]

        self.state_dict = {}
        self.last_action_error = None

    def reset(self) -> HelpdeskObservation:
        self.ticket = self.rng.choice(TICKETS)
        self.step_count = 0
        self.last_action_error = None

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
            sla_hours_left=24 if self.ticket["customer_tier"] == "free" else 6,
            history=""
        )

    def state(self):
        return self.state_dict

    def _compute_score(self) -> float:
        expected = self.ticket

        if self.task_name == "easy":
            return grade_easy(self.state_dict, expected)
        elif self.task_name == "medium":
            return grade_medium(self.state_dict, expected)
        elif self.task_name == "hard":
            return grade_hard(self.state_dict, expected)
        return 0.0

    def step(self, action: HelpdeskAction) -> Tuple[HelpdeskObservation, float, bool, dict]:
        self.step_count += 1
        self.last_action_error = None

        reward = 0.0

        if action.action_type == "noop":
            reward -= 0.02

        elif action.action_type == "set_category":
            if action.value:
                self.state_dict["category"] = action.value
                reward += 0.05
            else:
                self.last_action_error = "Missing category value"
                reward -= 0.05

        elif action.action_type == "set_priority":
            if action.value:
                self.state_dict["priority"] = action.value
                reward += 0.05
            else:
                self.last_action_error = "Missing priority value"
                reward -= 0.05

        elif action.action_type == "assign_team":
            if action.value:
                self.state_dict["team"] = action.value
                reward += 0.05
            else:
                self.last_action_error = "Missing team value"
                reward -= 0.05

        elif action.action_type == "send_reply":
            if action.value:
                self.state_dict["reply"] = action.value
                reward += 0.10
            else:
                self.last_action_error = "Missing reply text"
                reward -= 0.05

        elif action.action_type == "resolve_ticket":
            # penalty if resolved without reply in hard task
            if self.task_name == "hard" and len(self.state_dict.get("reply", "")) < 20:
                reward -= 0.10
                self.last_action_error = "Resolved without proper reply"
            self.state_dict["status"] = "resolved"
            reward += 0.10

        elif action.action_type == "request_info":
            reward += 0.02

        else:
            self.last_action_error = "Unknown action"
            reward -= 0.10

        done = False
        if self.step_count >= self.max_steps:
            done = True

        if self.state_dict["status"] == "resolved":
            done = True

        final_score = self._compute_score()

        # reward shaping: small progress toward final score
        reward += (final_score * 0.2)

        # clamp reward
        reward = max(0.0, min(1.0, reward))

        obs = HelpdeskObservation(
            task_name=self.task_name,
            ticket_id=self.ticket["ticket_id"],
            customer_tier=self.ticket["customer_tier"],
            message=self.ticket["message"],
            status=self.state_dict["status"],
            sla_hours_left=24 if self.ticket["customer_tier"] == "free" else 6,
            history=self.state_dict.get("reply", "")
        )

        info = HelpdeskInfo(
            step_count=self.step_count,
            max_steps=self.max_steps,
            last_action_error=self.last_action_error,
            internal_state=self.state_dict
        ).model_dump()

        return obs, float(reward), done, info