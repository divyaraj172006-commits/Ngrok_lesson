from fastapi import FastAPI
from routes import user_routes
from models import Base
from db import engine

app = FastAPI()

# Auto-create database tables on startup
Base.metadata.create_all(bind=engine)

app.include_router(user_routes.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="[IP_ADDRESS]", port=8000)