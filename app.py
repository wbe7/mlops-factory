import os
import mlflow
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from contextlib import asynccontextmanager

# --- 1. Определение формата входных данных ---
class HouseFeatures(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float

# Словарь для хранения нашей модели
model_registry = {}

# --- 2. Контекстный менеджер для жизненного цикла приложения ---
# Это современный способ в FastAPI для выполнения кода при старте и остановке.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Код при старте ---
    # Загружаем модель из MLflow Model Registry.
    # Имя модели и стадия (Prod, Staging) берутся из переменных окружения.
    # Это позволяет менять модели без изменения кода.
    model_name = os.getenv("MODEL_NAME", "california-housing-model")
    model_stage = os.getenv("MODEL_STAGE", "Production")
    
    # Устанавливаем URI для подключения к MLflow.
    # В Docker-контейнере это будет внутренний адрес сервиса MLflow.
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))

    print(f"Loading model '{model_name}' stage '{model_stage}'...")
    model_registry["model"] = mlflow.pyfunc.load_model(
        model_uri=f"models:/{model_name}/{model_stage}"
    )
    print("Model loaded successfully.")
    
    yield
    
    # --- Код при остановке ---
    # Очищаем ресурсы, если это необходимо.
    model_registry.clear()
    print("Resources cleaned up.")


# --- 3. Создание приложения FastAPI с lifespan ---
app = FastAPI(title="MLOps Factory Prediction Service", lifespan=lifespan)


# --- 4. Создание эндпоинта для предсказания ---
@app.post("/predict")
def predict(features: HouseFeatures):
    """
    Принимает на вход признаки дома и возвращает предсказанную цену.
    """
    # Преобразуем входные данные в DataFrame.
    data_for_prediction = pd.DataFrame([features.dict()])
    
    # Берем модель из нашего хранилища и делаем предсказание.
    prediction = model_registry["model"].predict(data_for_prediction)
    
    # Возвращаем результат в формате JSON.
    return {"predicted_price": prediction[0]}
