from fastapi import FastAPI
import uvicorn
from api_routes.v1.routes import router_v1

app = FastAPI()

app.include_router(router_v1, prefix="/v1")


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8080,
        reload=True
    )
