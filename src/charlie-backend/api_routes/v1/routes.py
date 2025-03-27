from fastapi import APIRouter

router_v1 = APIRouter()


@router_v1.get("/test")
async def test():
    return {"message": "This is a test for the router"}
