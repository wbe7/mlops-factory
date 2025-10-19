import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

# --- 1. Загрузка и подготовка данных ---
# Аналог из мира DevOps: Загрузка конфигурации или данных из источника перед запуском сервиса.
# Мы используем встроенный в scikit-learn датасет, чтобы не усложнять первый шаг.
housing = fetch_california_housing()
X = pd.DataFrame(housing.data, columns=housing.feature_names)
y = housing.target

# Разделяем данные на обучающую и тестовую выборки.
# Аналог: Канареечные или blue-green деплойменты, где мы используем часть данных для "тестирования"
# качества нашей модели, прежде чем "выкатывать" ее полностью.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- 2. Обучение модели ---
# RandomForestRegressor - это модель машинного обучения, которая предсказывает числовое значение
# (в нашем случае, цену дома), усредняя прогнозы множества 'деревьев решений',
# что делает её более точной и стабильной.
# Аналог: Запуск сборки артефакта (например, компиляция бинарного файла).
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# --- 3. Сохранение модели ---
# Мы сохраняем обученную модель в файл. Это называется сериализацией.
# Зачем? Чтобы отделить долгий процесс обучения от быстрого процесса предсказания.
# Обучив модель один раз, мы можем многократно использовать этот "бинарный артефакт" в нашем API.
# Это как собрать Docker-образ: вы делаете это один раз, а затем запускаете контейнеры из него.
joblib.dump(model, 'model.pkl')

print("Модель обучена и сохранена в model.pkl")
