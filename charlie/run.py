import uvicorn
import sys
import os

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# if __name__ == "__main__":
#     settings = Settings()
#     uvicorn.run(
#         "main:app", host=settings.HOST, port=settings.PORT, reload=settings.RELOAD
#     )
