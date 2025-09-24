#!/usr/bin/env python3
"""
Подробная диагностика проблем с backend
"""
import sys
import os
from pathlib import Path

print("=" * 60)
print("🔍 ДИАГНОСТИКА BACKEND")
print("=" * 60)

# 1. Проверяем текущую директорию
current_dir = Path(__file__).parent.absolute()
print(f"📁 Текущая директория: {current_dir}")
print(f"📁 Рабочая директория: {os.getcwd()}")

# 2. Проверяем структуру проекта
print("\n📂 Структура проекта:")
for item in current_dir.iterdir():
    if item.is_dir():
        print(f"  📁 {item.name}/")
        if item.name == "apps":
            for subitem in item.iterdir():
                if subitem.is_dir():
                    print(f"    📁 {subitem.name}/")
    else:
        print(f"  📄 {item.name}")

# 3. Проверяем Python path
print(f"\n🐍 Python path:")
for i, path in enumerate(sys.path):
    print(f"  {i}: {path}")

# 4. Проверяем переменные окружения
print(f"\n🌍 Переменные окружения:")
print(f"  PYTHONPATH: {os.environ.get('PYTHONPATH', 'НЕ УСТАНОВЛЕНА')}")
print(f"  PWD: {os.environ.get('PWD', 'НЕ УСТАНОВЛЕНА')}")

# 5. Проверяем наличие файлов
print(f"\n📄 Проверка ключевых файлов:")
key_files = [
    "apps/backend/app.py",
    "apps/backend/core/config.py",
    "apps/backend/api/channels.py",
    ".env"
]

for file_path in key_files:
    full_path = current_dir / file_path
    exists = full_path.exists()
    print(f"  {'✅' if exists else '❌'} {file_path}: {'СУЩЕСТВУЕТ' if exists else 'НЕ НАЙДЕН'}")

# 6. Пробуем импортировать модули
print(f"\n🔧 Тестирование импортов:")

try:
    print("  Тестируем импорт config...")
    from apps.backend.core.config import settings
    print("  ✅ config импортирован успешно")
    print(f"    - supabase_url: {settings.supabase_url}")
    print(f"    - tg_api_id: {settings.tg_api_id}")
except Exception as e:
    print(f"  ❌ Ошибка импорта config: {e}")

try:
    print("  Тестируем импорт app...")
    from apps.backend.app import app
    print("  ✅ app импортирован успешно")
    print(f"    - Тип: {type(app)}")
    print(f"    - Название: {getattr(app, 'title', 'Нет названия')}")
except Exception as e:
    print(f"  ❌ Ошибка импорта app: {e}")
    import traceback
    traceback.print_exc()

# 7. Проверяем uvicorn
print(f"\n🚀 Тестирование uvicorn:")
try:
    import uvicorn
    print(f"  ✅ uvicorn версия: {uvicorn.__version__}")
except Exception as e:
    print(f"  ❌ Ошибка импорта uvicorn: {e}")

# 8. Тестируем запуск uvicorn
print(f"\n🧪 Тестирование запуска uvicorn:")
try:
    from fastapi.testclient import TestClient
    client = TestClient(app)
    response = client.get("/healthz")
    print(f"  ✅ Health check: {response.status_code} - {response.json()}")
except Exception as e:
    print(f"  ❌ Ошибка health check: {e}")

print("\n" + "=" * 60)
print("🏁 ДИАГНОСТИКА ЗАВЕРШЕНА")
print("=" * 60)
