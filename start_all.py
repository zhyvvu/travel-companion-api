# start_all.py - ГЛАВНЫЙ ФАЙЛ ЗАПУСКА
import subprocess
import sys
import os
import time
from threading import Thread

def run_server():
    """Запуск FastAPI сервера"""
    print("🚀 Запуск FastAPI сервера...")
    # Изменяем хост на 0.0.0.0 для публичного доступа
    os.system("uvicorn main:app --host 0.0.0.0 --port 8000 --reload")

def run_bot():
    """Запуск Telegram бота"""
    print("🤖 Запуск Telegram бота...")
    time.sleep(2)  # Даем серверу запуститься
    os.system("python minimal_bot.py")

def run_mini_app():
    """Запуск Mini App сервера"""
    print("📱 Запуск Mini App сервера...")
    time.sleep(1)
    os.system("python run_mini_app.py")

def check_dependencies():
    """Проверка зависимостей"""
    try:
        import fastapi
        import sqlalchemy
        import uvicorn
        print("✅ Все зависимости установлены")
        return True
    except ImportError as e:
        print(f"❌ Отсутствуют зависимости: {e}")
        print("Установите зависимости: pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🚗 TRAVEL COMPANION - ПОЛНЫЙ ЗАПУСК")
    print("=" * 60)
    
    # Проверяем зависимости
    if not check_dependencies():
        sys.exit(1)
    
    # Проверяем базу данных
    if not os.path.exists("travel_companion.db"):
        print("📦 Создание базы данных...")
        from database import create_tables, seed_test_data
        create_tables()
        seed_test_data()
    
    print("\n🎯 Выберите режим запуска:")
    print("1. Полный запуск (API + Bot + Mini App)")
    print("2. Только API сервер")
    print("3. Только Telegram Bot")
    print("4. Только Mini App для разработки")
    print("5. Публичный доступ (с локальным IP)")
    
    choice = input("\nВведите номер (1-5): ").strip()
    
    if choice == '1':
        print("🔄 Запуск всех компонентов:")
        print("   • FastAPI сервер: http://0.0.0.0:8000")
        print("   • Telegram бот: в работе")
        print("   • Mini App: http://localhost:8080")
        print("=" * 60)
        
        try:
            # Поток для сервера
            server_thread = Thread(target=run_server)
            server_thread.daemon = True
            server_thread.start()
            
            time.sleep(3)
            
            # Поток для Mini App
            mini_app_thread = Thread(target=run_mini_app)
            mini_app_thread.daemon = True
            mini_app_thread.start()
            
            time.sleep(2)
            
            # Поток для бота
            bot_thread = Thread(target=run_bot)
            bot_thread.daemon = True
            bot_thread.start()
            
            print("\n✅ Все компоненты запущены!")
            print("\n🔗 Доступные ссылки:")
            print("1. API сервер: http://127.0.0.1:8000")
            print("2. Документация API: http://127.0.0.1:8000/docs")
            print("3. Статистика: http://127.0.0.1:8000/stats")
            print("4. Mini App: http://localhost:8080")
            print("\n🤖 Telegram Bot: отправьте /start в боте")
            print("\n🛑 Для остановки нажмите Ctrl+C")
            
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n👋 Остановка системы...")
    
    elif choice == '2':
        print("\n🚀 Запуск только API сервера...")
        run_server()
    
    elif choice == '3':
        print("\n🤖 Запуск только Telegram бота...")
        run_bot()
    
    elif choice == '4':
        print("\n📱 Запуск только Mini App для разработки...")
        run_mini_app()
    
    elif choice == '5':
        print("\n🌐 Настройка публичного доступа...")
        print("⚠️  ВАЖНО: Для работы с Telegram Mini App API должен быть доступен по HTTPS")
        print("📦 Рекомендуемые решения:")
        print("   1. Используйте ngrok: https://ngrok.com/")
        print("   2. Разверните на хостинге (Heroku, Render, etc.)")
        print("   3. Настройте reverse proxy (Nginx + Certbot)")
        
        public_ip = input("\nВведите ваш публичный IP или домен: ").strip()
        
        if public_ip:
            print(f"\n🔧 Настройте в app.js:")
            print(f'const API_BASE_URL = "http://{public_ip}:8000";')
            print("\n📝 ИЛИ для HTTPS:")
            print(f'const API_BASE_URL = "https://{public_ip}";')
        
        print("\n🚀 Запуск сервера...")
        run_server()
    
    else:
        print("❌ Неверный выбор")