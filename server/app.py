from fastapi import FastAPI
import subprocess
import sys

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/run")
def run():
    import subprocess, sys
    result = subprocess.run(
        [sys.executable, "inference.py"],
        capture_output=True,
        text=True
    )
    return {
        "stdout": result.stdout,
        "stderr": result.stderr
    }
def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()