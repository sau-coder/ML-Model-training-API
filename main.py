from fastapi import FastAPI
from app.jobs.route import router as glovbal_router
from app.User.route import router as user_router
import uvicorn

app = FastAPI()

@app.get('/')
def models_info():
    return {"getting started with" : "model training"}

app.include_router(glovbal_router , prefix='/v1')
app.include_router(user_router , prefix='/v1')

if __name__=='__main__':
    uvicorn.run(app)
