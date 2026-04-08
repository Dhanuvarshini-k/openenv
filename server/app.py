import json
from fastapi import FastAPI, Body
from helpdesk_env.env import HelpdeskEnv
from helpdesk_env.models import HelpdeskAction

app = FastAPI()

# initialize environment
env = HelpdeskEnv(task_name="easy", seed=42)
current_obs = env.reset()


@app.get("/")
def root():
    return {"status": "ok", "env": "helpdesk_openenv"}


@app.get("/health")
def health():
    return {"status": "healthy"}

# ✅ RESET (GET)
@app.get("/reset")
def reset_get():
    global current_obs
    current_obs = env.reset()
    return {
        "observation": current_obs.model_dump()
    }


# ✅ RESET (POST) — IMPORTANT FIX
@app.post("/reset")
def reset_post(payload: dict = Body(default={})):
    global current_obs

    task_name = payload.get("task_name", "easy")

    global env
    env = HelpdeskEnv(task_name=task_name, seed=42)
    current_obs = env.reset()

    return {
        "observation": current_obs.model_dump()
    }


# ✅ STEP (GET)
@app.get("/step")
def step_get(action: str = None):
    global current_obs

    if action:
        try:
            action_dict = json.loads(action)
            act = HelpdeskAction(**action_dict)
            obs, reward, done, info = env.step(act)
            current_obs = obs
            return {
                "observation": obs.model_dump(),
                "reward": reward,
                "done": done,
                "info": info
            }
        except:
            return {"error": "invalid action format"}

    return {"error": "send action via POST or add ?action=... query param"}


# ✅ STEP (POST)
@app.post("/step")
def step_post(payload: dict = Body(default={})):
    global current_obs

    action_data = payload.get("action", {"action_type": "noop", "value": None})

    act = HelpdeskAction(**action_data)
    obs, reward, done, info = env.step(act)
    current_obs = obs

    return {
        "observation": obs.model_dump(),
        "reward": reward,
        "done": done,
        "info": info
    }


# ✅ REQUIRED BY OPENENV
def main():
    return app


# ✅ REQUIRED ENTRYPOINT
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000)
