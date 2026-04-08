import os
import json
from openai import OpenAI

from helpdesk_env.env import HelpdeskEnv
from helpdesk_env.models import HelpdeskAction

API_KEY = os.getenv("HF_TOKEN") or os.getenv("OPENAI_API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"

MAX_STEPS = 10

client = OpenAI(
    api_key=API_KEY,
    base_url=API_BASE_URL
)

TASKS = ["easy", "medium", "hard"]


def llm_action(obs: dict):
    prompt = f"""
You are an AI agent in a customer support ticket triage environment.

You MUST respond with exactly ONE JSON object.
No explanation. No extra text.

Allowed action_type values:
- set_category (value must be one of: billing, technical, account, shipping, security)
- set_priority (value must be one of: low, medium, high)
- assign_team (value must be one of: billing_team, tech_team, account_team, shipping_team, security_team)
- send_reply (value must be a helpful reply)
- resolve_ticket (value must be null)
- request_info (value must be a short question)
- noop (value must be null)

Strict decision rules (follow exactly):
1. If current_state.category is null -> output set_category
2. Else if current_state.priority is null -> output set_priority
3. Else if current_state.team is null -> output assign_team
4. Else if task_name == "hard" AND current_state.reply is empty -> output send_reply
5. Else -> output resolve_ticket

Important:
- Never output send_reply if current_state.reply is already filled.
- resolve_ticket should be the final action.

Observation:
{json.dumps(obs, indent=2)}

Return ONLY valid JSON.
"""

    resp = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=200
    )

    text = resp.choices[0].message.content.strip()

    try:
        parsed = json.loads(text)
        return parsed
    except Exception:
        return {"action_type": "noop", "value": None}


def run_task(task_name: str):
    env = HelpdeskEnv(task_name=task_name, seed=42)
    obs = env.reset()

    rewards = []
    done = False
    steps = 0

    print(f"[START] task={task_name} env=helpdesk_openenv model={MODEL_NAME}")

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

            action_str = f"{action.action_type}({action.value})"
            err = info.get("last_action_error")

            if err is None:
                err_out = "null"
            else:
                err_out = err

            print(f"[STEP] step={steps} action={action_str} reward={reward:.2f} done={str(done).lower()} error={err_out}")

        score = float(env._compute_score())
        success = score >= 0.7

        rewards_str = ",".join([f"{r:.2f}" for r in rewards])
        print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}")

    except Exception:
        rewards_str = ",".join([f"{r:.2f}" for r in rewards])
        print(f"[END] success=false steps={steps} score=0.00 rewards={rewards_str}")


if __name__ == "__main__":
    for t in TASKS:
        run_task(t)