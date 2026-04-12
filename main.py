import json
from fastapi import FastAPI, Body
from helpdesk_env.env import HelpdeskEnv
from helpdesk_env.models import HelpdeskAction

app = FastAPI(
    title="Helpdesk OpenEnv",
    description="OpenEnv-compatible environment for customer support ticket triage and resolution.",
    version="1.0.0",
)

# Global env instance (reset per request)
env: HelpdeskEnv = None
current_obs = None


@app.get("/")
def root():
    return {"status": "ok", "env": "helpdesk_openenv"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/reset")
def reset(payload: dict = Body(default={})):
    global env, current_obs
    task_name   = payload.get("task_name", "easy")
    seed        = payload.get("seed", 42)
    env         = HelpdeskEnv(task_name=task_name, seed=seed)
    current_obs = env.reset()
    return {"observation": current_obs.model_dump()}


@app.post("/step")
def step(payload: dict = Body(default={})):
    global current_obs
    if env is None:
        return {"error": "Call /reset first"}
    action_data = payload.get("action", {"action_type": "noop", "value": None})
    action      = HelpdeskAction(**action_data)
    obs, reward, done, info = env.step(action)
    current_obs = obs
    return {
        "observation": obs.model_dump(),
        "reward":      reward,
        "done":        done,
        "info":        info,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
