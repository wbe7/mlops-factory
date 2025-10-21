import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# --- 1. Загрузка и подготовка данных ---
# Загружаем данные из нашего CSV, который версионируется с помощью DVC
data = pd.read_csv('data/dataset.csv')

# Разделяем данные на признаки (X) и целевую переменную (y)
X = data.drop('PRICE', axis=1)
y = data['PRICE']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Определяем параметр для обучения
n_estimators = 150

# --- 2. Обучение и логирование с MLflow ---
# mlflow.start_run() создает новый "эксперимент" (run)
with mlflow.start_run():
    # --- Обучение модели ---
    model = RandomForestRegressor(n_estimators=n_estimators, random_state=42)
    model.fit(X_train, y_train)

    # --- Оценка модели ---
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)

    # --- Логирование в MLflow ---
    # Логируем параметр, который мы использовали
    mlflow.log_param("n_estimators", n_estimators)

    # Логируем метрику качества
    mlflow.log_metric("mse", mse)

    # Логируем (сохраняем) и регистрируем саму модель, добавляя пример входа
    # для автоматического определения сигнатуры модели.
    mlflow.sklearn.log_model(
        sk_model=model, 
        name="random-forest-model",
        registered_model_name="california-housing-model",
        input_example=X_train.head(5)
    )

    print(f"Модель обучена. MSE: {mse}")
    print("Модель, параметры и метрики залогированы с помощью MLflow.")
