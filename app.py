import os
import mlflow
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

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
    # Загружаем модель из MLflow Model Registry, используя алиас.
    # Имя модели и алиас (prod, champion, etc) берутся из переменных окружения.
    model_name = os.getenv("MODEL_NAME", "california-housing-model")
    model_alias = os.getenv("MODEL_ALIAS", "prod")
    
    # Устанавливаем URI для подключения к MLflow.
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))

    print(f"Loading model '{model_name}' with alias '{model_alias}'...")
    model_registry["model"] = mlflow.pyfunc.load_model(
        model_uri=f"models:/{model_name}@{model_alias}"
    )
    print("Model loaded successfully.")
    
    yield
    
    # --- Код при остановке ---
    # Очищаем ресурсы, если это необходимо.
    model_registry.clear()
    print("Resources cleaned up.")


# --- 3. Создание приложения FastAPI с lifespan ---
app = FastAPI(title="MLOps Factory Prediction Service", lifespan=lifespan)


# --- 4. Эндпоинт для проверки здоровья (Health Check) ---
@app.get("/health")
def health_check():
    return {"status": "ok"}


# --- 5. Создание эндпоинта для предсказания ---
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
