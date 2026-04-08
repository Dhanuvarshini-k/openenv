import json

from helpdesk_env.env import HelpdeskEnv
from helpdesk_env.models import HelpdeskAction

MAX_STEPS = 10
TASKS = ["easy", "medium", "hard"]


def llm_action(obs: dict):
    state = obs.get("current_state", {})
    message = obs.get("message", "").lower()

    # 1. CATEGORY
    if state.get("category") is None:
        if any(x in message for x in ["charge", "refund", "invoice", "billing"]):
            return {"action_type": "set_category", "value": "billing"}
        elif any(x in message for x in ["crash", "error", "bug", "slow", "upload"]):
            return {"action_type": "set_category", "value": "technical"}
        elif any(x in message for x in ["login", "account", "password", "email"]):
            return {"action_type": "set_category", "value": "account"}
        elif any(x in message for x in ["delivery", "order", "package", "shipping"]):
            return {"action_type": "set_category", "value": "shipping"}
        elif any(x in message for x in ["otp", "hacked", "unauthorized", "security"]):
            return {"action_type": "set_category", "value": "security"}
        else:
            return {"action_type": "set_category", "value": "technical"}

    # 2. PRIORITY
    if state.get("priority") is None:
        if "urgent" in message or "immediately" in message:
            return {"action_type": "set_priority", "value": "high"}
        elif obs.get("customer_tier") == "premium":
            return {"action_type": "set_priority", "value": "high"}
        else:
            return {"action_type": "set_priority", "value": "medium"}

    # 3. TEAM
    if state.get("team") is None:
        mapping = {
            "billing": "billing_team",
            "technical": "tech_team",
            "account": "account_team",
            "shipping": "shipping_team",
            "security": "security_team"
        }
        return {
            "action_type": "assign_team",
            "value": mapping.get(state.get("category"))
        }

    # 4. HARD → SEND REPLY
    if obs.get("task_name") == "hard" and state.get("reply") == "":
        cat = state.get("category")

        if cat == "technical":
            reply = "Please update the app, reinstall it, and share crash logs."
        elif cat == "billing":
            reply = "We will review the charge and process a refund if needed."
        elif cat == "shipping":
            reply = "Please check tracking details and delivery status."
        elif cat == "account":
            reply = "Please reset your password and verify your login."
        elif cat == "security":
            reply = "Secure your account and report unauthorized activity immediately."
        else:
            reply = "We will assist you shortly."

        return {"action_type": "send_reply", "value": reply}

    # 5. RESOLVE
    return {"action_type": "resolve_ticket", "value": None}


def run_task(task_name: str):
    env = HelpdeskEnv(task_name=task_name, seed=42)
    obs = env.reset()

    rewards = []
    done = False
    steps = 0

    print(f"[START] task={task_name}")

    try:
        while not done and steps < MAX_STEPS:
            steps += 1

            obs_payload = obs.model_dump()
            obs_payload["current_state"] = env.state()

            action_json = llm_action(obs_payload)

            try:
                action = HelpdeskAction(**action_json)
            except Exception:
                action = HelpdeskAction(action_type="noop", value=None)

            obs, reward, done, info = env.step(action)
            rewards.append(reward)

            print(f"[STEP] step={steps} action={action.action_type}({action.value}) reward={reward:.2f}")

        score = float(env._compute_score())
        success = score >= 0.7

        print(f"[END] success={success} steps={steps} score={score:.2f}")

    except Exception:
        print(f"[END] success=false steps={steps} score=0.00")


if __name__ == "__main__":
    for t in TASKS:
        run_task(t)
