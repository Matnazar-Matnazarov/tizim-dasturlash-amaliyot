import asyncio
from contextlib import asynccontextmanager

import uvicorn
import uvloop
from fastapi import FastAPI


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("starting up...")
    app.state.db_connection = "connected"

    yield

    # Shutdown logic
    print("shutting down...")
    if hasattr(app.state, "db_connection"):
        app.state.db_connection = None
        print("disconnecting...")
    await asyncio.sleep(5)
    print("terminated")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def home():
    return {"message": "FastAPI working."}


def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")


if __name__ == "__main__":
    main()
