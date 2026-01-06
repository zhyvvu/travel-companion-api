# run_telegram.py - ЗАПУСК ДЛЯ TELEGRAM РАЗРАБОТКИ
import subprocess
import sys
import os
import time
from threading import Thread
import webbrowser

def run_server():
    """Запуск FastAPI сервера для Telegram"""
    print("🚀 Запуск FastAPI сервера...")
    print("🌐 Сервер будет доступен по: http://0.0.0.0:8000")
    print("📖 Документация API: http://localhost:8000/docs")
    os.system("uvicorn main:app --host 0.0.0.0 --port 8000 --reload")

def run_bot():
    """Запуск Telegram бота"""
    print("\n🤖 Запуск Telegram бота...")
    print("⚠️  Убедитесь, что в minimal_bot.py указан реальный BOT_TOKEN!")
    time.sleep(3)
    os.system("python minimal_bot.py")

def run_mini_app():
    """Запуск Mini App для тестирования"""
    print("\n📱 Запуск Mini App для тестирования...")
    print("🌐 Открываю http://localhost:8080 в браузере...")
    time.sleep(2)
    webbrowser.open("http://localhost:8080")
    
    os.chdir("mini_app")
    os.system("python -m http.server 8080")

def check_dependencies():
    """Проверка зависимостей"""
    try:
        import fastapi, sqlalchemy, uvicorn, telegram
        print("✅ Все зависимости установлены")
        return True
    except ImportError as e:
        print(f"❌ Отсутствуют зависимости: {e}")
        print("Установите зависимости: pip install -r requirements.txt")
        return False

def setup_environment():
    """Настройка окружения"""
    print("🔧 Настройка окружения...")
    
    # Создаем базу данных, если её нет
    if not os.path.exists("travel_companion.db"):
        print("📦 Создание базы данных...")
        from database import create_tables
        create_tables()
        print("✅ База данных создана (пустая)")
    
    # Проверяем наличие файлов Mini App
    if not os.path.exists("mini_app"):
        print("❌ Папка mini_app не найдена!")
        return False
    
    return True

def main():
    print("=" * 60)
    print("🚗 TRAVEL COMPANION - TELEGRAM РАЗРАБОТКА")
    print("=" * 60)
    
    # Проверяем зависимости
    if not check_dependencies():
        sys.exit(1)
    
    # Настраиваем окружение
    if not setup_environment():
        sys.exit(1)
    
    print("\n🎯 Выберите режим запуска:")
    print("1. Полный запуск (API + Bot + Mini App)")
    print("2. Только API сервер")
    print("3. Только Telegram Bot")
    print("4. Только Mini App для тестирования")
    print("5. Настройка для публичного доступа")
    
    choice = input("\nВведите номер (1-5): ").strip()
    
    if choice == '1':
        print("\n🔄 Запуск всех компонентов...")
        print("   • API сервер: http://localhost:8000")
        print("   • Telegram Bot: в работе")
        print("   • Mini App: http://localhost:8080")
        print("=" * 60)
        
        try:
            # Запускаем сервер
            server_thread = Thread(target=run_server, daemon=True)
            server_thread.start()
            time.sleep(3)
            
            # Запускаем Mini App
            mini_app_thread = Thread(target=run_mini_app, daemon=True)
            mini_app_thread.start()
            time.sleep(2)
            
            # Запускаем бота
            bot_thread = Thread(target=run_bot, daemon=True)
            bot_thread.start()
            
            print("\n✅ Все компоненты запущены!")
            print("\n📋 Инструкция:")
            print("1. Откройте Telegram и найдите вашего бота")
            print("2. Отправьте команду /start")
            print("3. Нажмите кнопку 'Открыть Travel Companion'")
            print("4. Приложение откроется в Telegram Web App")
            print("\n🔧 Для тестирования в браузере:")
            print("   • API: http://localhost:8000")
            print("   • Mini App: http://localhost:8080")
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
        print("\n📱 Запуск только Mini App для тестирования...")
        run_mini_app()
    
    elif choice == '5':
        print("\n🌐 Настройка публичного доступа...")
        print("\n📋 Для работы с Telegram Mini App нужно:")
        print("1. Разместить Mini App на GitHub Pages или другом хостинге")
        print("2. Разместить API на Heroku, Render или другом хостинге")
        print("3. Настроить Web App URL в @BotFather")
        print("\n🔗 Примеры публичных хостингов:")
        print("   • Mini App: GitHub Pages (бесплатно)")
        print("   • API: Render, Railway, Heroku (есть бесплатные тарифы)")
        print("\n📝 После настройки укажите URL в:")
        print("   • minimal_bot.py: MINI_APP_URL")
        print("   • app.js: API_BASE_URL")
        
        input("\nНажмите Enter для возврата...")
        main()
    
    else:
        print("❌ Неверный выбор")

if __name__ == "__main__":
    main()