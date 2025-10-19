import joblib
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

# --- 1. Создание приложения FastAPI ---
# Аналог: Инициализация веб-сервера (как Nginx или Apache).
app = FastAPI(title="MLOps Factory Prediction Service")

# --- 2. Загрузка модели при старте ---
# Модель загружается один раз при запуске приложения, а не на каждый запрос.
# Аналог: Инициализация пула соединений с базой данных.
# Это экономит время и ресурсы.
model = joblib.load('model.pkl')

# --- 3. Определение формата входных данных ---
# Мы используем Pydantic для валидации данных.
# Аналог: Определение схемы в OpenAPI/Swagger или .proto файле для gRPC.
# Это гарантирует, что на вход API придут корректные данные, и избавляет нас
# от написания кучи проверок вручную.
class HouseFeatures(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float

# --- 4. Создание эндпоинта для предсказания ---
@app.post("/predict")
def predict(features: HouseFeatures):
    """
    Принимает на вход признаки дома и возвращает предсказанную цену.
    """
    # Преобразуем входные данные в DataFrame, т.к. модель обучалась на них.
    # Важно, чтобы порядок колонок совпадал с тем, что был при обучении.
    data_for_prediction = pd.DataFrame([features.dict()])
    
    # Вызов метода predict.
    # Аналог: Выполнение основного бизнес-логического метода в вашем микросервисе.
    prediction = model.predict(data_for_prediction)
    
    # Возвращаем результат в формате JSON.
    return {"predicted_price": prediction[0]}
