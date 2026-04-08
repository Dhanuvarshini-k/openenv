import os
import json
import time
from openai import OpenAI

from helpdesk_env.env import HelpdeskEnv
from helpdesk_env.models import HelpdeskAction

API_KEY = os.getenv("HF_TOKEN") or os.getenv("OPENAI_API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"

MAX_STEPS = 10
TASKS = ["easy", "medium", "hard"]

client = OpenAI(
    api_key=API_KEY,
    base_url=API_BASE_URL
)


def fallback_action(obs: dict):
    state = obs.get("current_state", {})
    message = obs.get("message", "").lower()

    if state.get("category") is None:
        if any(x in message for x in ["charge", "refund", "invoice", "billing"]):
            return {"action_type": "set_category", "value": "billing"}
        elif any(x in message for x in ["crash", "error", "bug", "slow", "upload"]):
            return {"action_type": "set_category", "value": "technical"}
        elif any(x in message for x in ["login", "account", "password", "email"]):
            return {"action_type": "set_category", "value": "account"}
        elif any(x in message for x in ["delivery", "order", "package", "shipping"]):
            return {"action_type": "set_category", "value": "shipping"}
        elif any(x in message for x in ["otp", "unauthorized", "security", "hacked"]):
            return {"action_type": "set_category", "value": "security"}
        else:
            return {"action_type": "set_category", "value": "technical"}

    if state.get("priority") is None:
        if obs.get("customer_tier") == "premium":
            return {"action_type": "set_priority", "value": "high"}
        return {"action_type": "set_priority", "value": "medium"}

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

    if obs.get("task_name") == "hard" and state.get("reply") == "":
        cat = state.get("category")
        if cat == "technical":
            reply = "Please update the app, reinstall it, and share crash logs for debugging."
        elif cat == "billing":
            reply = "We will review your transaction and process a refund if necessary."
        elif cat == "shipping":
            reply = "Please check tracking details and we will investigate the delivery."
        elif cat == "account":
            reply = "Please reset your password and verify your account details."
        elif cat == "security":
            reply = "Please secure your account immediately and report unauthorized activity."
        else:
            reply = "We will assist you shortly."
        return {"action_type": "send_reply", "value": reply}

    if obs.get("task_name") in ["easy", "medium"]:
        return {"action_type": "noop", "value": None}
    return {"action_type": "resolve_ticket", "value": None}


def llm_action(obs: dict):
    prompt = f"""
You are a STRICT JSON API.

Return ONLY valid JSON.
No explanation. No extra text.

FORMAT:
{{"action_type": "...", "value": "..."}}

Rules:
1. If current_state.category is null -> set_category
2. If current_state.priority is null -> set_priority
3. If current_state.team is null -> assign_team
4. If task_name == "hard" AND current_state.reply == "" -> send_reply
5. Else -> resolve_ticket

Valid values:
category: billing, technical, account, shipping, security
priority: low, medium, high
team: billing_team, tech_team, account_team, shipping_team, security_team

Observation:
{json.dumps(obs)}
"""

    try:
        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=100
        )

        text = resp.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(text)

        if "action_type" not in parsed:
            return fallback_action(obs)

        if parsed["action_type"] == "send_reply":
            if not parsed.get("value") or len(parsed.get("value").strip()) < 10:
                return fallback_action(obs)

        return parsed

    except Exception:
        return fallback_action(obs)


def run_task(task_name: str):
    env = HelpdeskEnv(task_name=task_name, seed=42)
    obs = env.reset()

    rewards = []
    done = False
    steps = 0

    print(f"[START] task={task_name} model={MODEL_NAME}")

    try:
        while not done and steps < MAX_STEPS:
            steps += 1

            obs_payload = obs.model_dump()
            obs_payload["current_state"] = env.state()

            action_json = llm_action(obs_payload)

            try:
                action = HelpdeskAction(**action_json)
            except Exception:
                action = HelpdeskAction(**fallback_action(obs_payload))

            obs, reward, done, info = env.step(action)
            rewards.append(reward)

            print(f"[STEP] {steps} → {action.action_type}({action.value}) reward={reward:.2f}")

            time.sleep(0.5)

        score = float(env._compute_score())
        score = max(0.001, min(0.999, score))  # ✅ FIX: keep strictly within (0, 1)
        success = score >= 0.7

        print(f"[END] success={success} score={score:.3f}")

    except Exception:
        print(f"[END] success=false score=0.00")


if __name__ == "__main__":
    for t in TASKS:
        run_task(t)
