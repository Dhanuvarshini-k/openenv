import json
from fastapi import FastAPI
from helpdesk_env.env import HelpdeskEnv
from helpdesk_env.models import HelpdeskAction

app = FastAPI()

# same env instance
env = HelpdeskEnv(task_name="easy", seed=42)
current_obs = env.reset()

@app.get("/")
def root():
    return {"status": "ok", "env": "helpdesk_openenv"}

@app.get("/reset")
def reset_get():
    global current_obs
    current_obs = env.reset()
    return current_obs.model_dump()

@app.post("/reset")
def reset_post():
    global current_obs
    current_obs = env.reset()
    return current_obs.model_dump()

@app.get("/step")
def step_get(action: str = None):
    """
    For GET you can optionally send action as JSON string in query,
    e.g. ?action={"action_type":"noop","value":null}
    """
    global current_obs
    if action:
        try:
            action_dict = json.loads(action)
            act = HelpdeskAction(**action_dict)
            obs, reward, done, info = env.step(act)
            current_obs = obs
            return {"observation": obs.model_dump(), "reward": reward, "done": done, "info": info}
        except:
            return {"error": "invalid action format"}
    return {"error": "send action via POST or add ?action=... query param"}

@app.post("/step")
def step_post(action: dict):
    global current_obs
    act = HelpdeskAction(**action)
    obs, reward, done, info = env.step(act)
    current_obs = obs
    return {
        "observation": obs.model_dump(),
        "reward": reward,
        "done": done,
        "info": info
    }

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()