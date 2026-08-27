import os

app_env = os.getenv("APP_ENV", "development")

print(f"CloudForge application is running in {app_env} environment!")
