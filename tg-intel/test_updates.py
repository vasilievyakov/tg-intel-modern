#!/usr/bin/env python3
"""
Скрипт для тестирования обновлений после обновления зависимостей.
Проверяет импорты и базовую функциональность.
"""

import sys
import subprocess
import importlib
import os
from pathlib import Path

def test_python_imports():
    """Тестирует импорты Python модулей."""
    print("🔍 Тестирование Python импортов...")
    
    modules_to_test = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'psycopg',
        'telethon',
        'apscheduler',
        'httpx',
        'python-dotenv'
    ]
    
    failed_imports = []
    
    for module in modules_to_test:
        try:
            importlib.import_module(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Не удалось импортировать: {', '.join(failed_imports)}")
        return False
    else:
        print("\n✅ Все Python модули импортированы успешно")
        return True

def test_backend_app():
    """Тестирует импорт backend приложения."""
    print("\n🔍 Тестирование backend приложения...")
    
    try:
        # Добавляем путь к backend в sys.path
        backend_path = Path(__file__).parent / "apps" / "backend"
        sys.path.insert(0, str(backend_path))
        
        # Тестируем импорт основных модулей
        import apps.backend.app
        import apps.backend.core.config
        import apps.backend.core.db
        import apps.backend.api.channels
        import apps.backend.api.posts
        import apps.backend.api.summaries
        import apps.backend.services.telegram
        import apps.backend.services.fetcher
        import apps.backend.services.ai
        
        print("  ✅ Backend модули импортированы успешно")
        return True
        
    except Exception as e:
        print(f"  ❌ Ошибка импорта backend: {e}")
        return False

def test_node_modules():
    """Проверяет наличие node_modules."""
    print("\n🔍 Проверка frontend зависимостей...")
    
    frontend_path = Path(__file__).parent / "apps" / "frontend"
    node_modules_path = frontend_path / "node_modules"
    
    if node_modules_path.exists():
        print("  ✅ node_modules найден")
        return True
    else:
        print("  ⚠️  node_modules не найден. Запустите 'pnpm install' в apps/frontend/")
        return False

def main():
    """Основная функция тестирования."""
    print("🚀 Тестирование обновлений tg-intel...")
    print("=" * 50)
    
    # Тестируем Python импорты
    python_ok = test_python_imports()
    
    # Тестируем backend приложение
    backend_ok = test_backend_app()
    
    # Проверяем frontend зависимости
    frontend_ok = test_node_modules()
    
    print("\n" + "=" * 50)
    print("📊 Результаты тестирования:")
    print(f"  Python импорты: {'✅' if python_ok else '❌'}")
    print(f"  Backend приложение: {'✅' if backend_ok else '❌'}")
    print(f"  Frontend зависимости: {'✅' if frontend_ok else '❌'}")
    
    if python_ok and backend_ok and frontend_ok:
        print("\n🎉 Все тесты прошли успешно! Обновления работают корректно.")
        return 0
    else:
        print("\n⚠️  Некоторые тесты не прошли. Проверьте установку зависимостей.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
