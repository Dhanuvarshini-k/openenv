from fastapi import FastAPI
from helpdesk_env.env import HelpdeskEnv
from helpdesk_env.models import HelpdeskAction

app = FastAPI()

env = None

@app.post("/reset")
def reset(payload: dict = {}):   # 👈 THIS IS THE KEY FIX
    global env

    task_name = payload.get("task_name", "easy")

    env = HelpdeskEnv(task_name=task_name, seed=42)
    obs = env.reset()

    return {
        "observation": obs.model_dump()
    }

@app.post("/step")
def step(payload: dict = {}):
    global env

    action_data = payload.get("action", {"action_type": "noop", "value": None})

    action = HelpdeskAction(**action_data)
    obs, reward, done, info = env.step(action)

    return {
        "observation": obs.model_dump(),
        "reward": reward,
        "done": done,
        "info": info
    }