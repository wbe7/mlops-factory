# Развертывание MLflow в Kubernetes

Этот документ описывает процесс развертывания MLflow с использованием Helm-чарта от Bitnami.

## Предварительные требования

Перед установкой чарта необходимо вручную создать секрет `mlflow-s3-creds` в неймспейсе `mlflow`, содержащий ключи для доступа к S3-хранилищу.

```bash
kubectl create secret generic mlflow-s3-creds --namespace mlflow \
  --from-literal=AWS_ACCESS_KEY_ID=<YOUR_ACCESS_KEY> \
  --from-literal=AWS_SECRET_ACCESS_KEY=<YOUR_SECRET_KEY>
```

## Ключевые особенности конфигурации

### 1. Используемый Chart

- **Репозиторий:** `oci://registry-1.docker.io/bitnamicharts/mlflow`
- **Версия:** `5.1.17`

### 2. Проблема с Docker-образами Bitnami

**КЛЮЧЕВАЯ НАХОДКА:** Стандартные образы, указанные в чарте (например, `bitnami/mlflow`), больше не доступны по старым путям. Bitnami перенесла их в репозиторий `bitnamilegacy`. Необходимо переопределить пути для всех используемых образов в `values.yaml`.

Пример из `values.yaml`:
```yaml
# Глобальный образ
image:
  repository: bitnamilegacy/mlflow

# Образ PostgreSQL
postgresql:
  image:
    repository: bitnamilegacy/postgresql

# Образы для init-контейнеров
volumePermissions:
  image:
    repository: bitnamilegacy/os-shell

waitContainer:
  image:
    repository: bitnamilegacy/os-shell
```

### 3. Конфигурация

- **Ingress:** Настроен для хоста `mlflow.cloudnative.space` с TLS через `letsencrypt`.
- **Backend:** Используется PostgreSQL, который разворачивается как sub-chart. Данные хранятся на `freenas-nfs-csi`.
- **Artifact Store:** Используется внешний S3-совместимый сторадж (MinIO). Креды для доступа берутся из секрета `mlflow-s3-creds`, созданного на шаге предварительных требований.

### 4. Аутентификация

Используется **внутренняя система аутентификации MLflow**.

- В `values.yaml` установлен флаг `tracking.auth.enabled: true`.
- **Важно:** Мы не указываем `username` и `password` в `values.yaml` напрямую. При первом деплое чарт автоматически генерирует надежные учетные данные и сохраняет их в секрете. Этот способ оказался наиболее стабильным.

## Процесс развертывания

1.  **Убедитесь, что `values.yaml` соответствует актуальной конфигурации.**

2.  **Выполните установку с помощью Helm:**
    ```bash
    helm upgrade --install mlflow oci://registry-1.docker.io/bitnamicharts/mlflow \
      --version 5.1.17 \
      --namespace mlflow \
      --create-namespace \
      -f helm/mlflow/values.yaml
    ```

## Администрирование

### Получение учетных данных

После установки чарт создаст секрет `mlflow-tracking`. Получить логин и пароль можно командами:

- **Username:**
  ```bash
  kubectl get secret --namespace mlflow mlflow-tracking -o jsonpath="{.data.admin-user}" | base64 -d
  ```
- **Password:**
  ```bash
  kubectl get secret --namespace mlflow mlflow-tracking -o jsonpath="{.data.admin-password}" | base64 -d
  ```

### Анализ конфигурации

Для просмотра `values`, с которыми был задеплоен чарт (полезно для отладки), используйте команду:

```bash
helm get values mlflow -n mlflow
```

Чтобы посмотреть оригинальные `values` из самого чарта для сравнения, используйте:

```bash
helm show values oci://registry-1.docker.io/bitnamicharts/mlflow --version 5.1.17
```

## Доступ

MLflow будет доступен по адресу `https://mlflow.cloudnative.space`. Используйте полученные учетные данные для входа.
