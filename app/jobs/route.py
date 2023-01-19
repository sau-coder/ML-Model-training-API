from fastapi import FastAPI , APIRouter , UploadFile , File , Form , status , BackgroundTasks
from fastapi.responses import JSONResponse
from uuid import uuid4
from database.db import SessionLocal
import pandas as pd
from app.jobs.schema import Model_types , PredictData
from sklearn.linear_model import LinearRegression , LogisticRegression
import pickle
import os
import numpy as np
from app.jobs.model import JobData
from app.User.model import UserData
from fastapi import HTTPException

db = SessionLocal()
router = APIRouter()

authorized_models = ['Linear Regression', 'Logistic Regression', 'SVM']

@router.post('/upload/')
async def create_upload_file(file: UploadFile ,indepandant_columns: str = Form(...), depandant_column: str = Form(...), model_name : str = Form(...) , user_name : str = Form(...) , bg_task : BackgroundTasks):
    db_query = db.query(UserData).filter(UserData.user_name == user_name).first()
    if db_query is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Please create user first")

    if not file.filename.endswith('.csv'):
        raise ValueError("Invalid file type, expected CSV.")

    data = pd.read_csv(file.file)
    input_columns = indepandant_columns.split(',')
    csv_columns = data.columns.tolist()


    if set(input_columns) == set(csv_columns) & depandant_column:
        X = data.drop(depandant_column)
        Y = data(depandant_column)
        if model_name not in authorized_models:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail = "invalid model_name")
        
        try:
            global model
            if data.model_name == Model_types.linear_regression:
                model = LinearRegression()

            elif data.model_name == Model_types.logistic_regression:
                model = LogisticRegression(solver='lbfgs', max_iter=100)

            bg_task.add_task(model.fit(X , Y))

            model_id = str (uuid4())

            model_directory = "models"
            if not os.path.exists(model_directory):
                os.makedirs(model_directory)

            model_path = os.path.join(model_directory, f"{model_id}.pkl")

            new_job = JobData(
                job_id = model_id,
                job_name = model_name,
                user_name = user_name
            )
            db.add(new_job)
            db.commit()

            pickle.dump(model , open(model_path , 'wb'))
            model_info = {"model_id" : model_id , "model_name" : data.model_name , "info" : "model is trained and created successfully"}

        except Exception as e:
            return {"status" : f"error while training: {e}"}
    

    return JSONResponse(content = model_info)



        

   

@router.post('/predict')
def predict(predict_data : PredictData):
    loaded_model = pickle.load(open(f'models/{predict_data.model_id}.pkl' , 'rb'))
    prediction = loaded_model.predict(predict_data.input)
    return {"prediction" : prediction}







    

