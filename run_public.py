# run_public.py - ЗАПУСК API С ПУБЛИЧНЫМ ДОСТУПОМ
import subprocess
import sys
import os
import time
from threading import Thread

def run_server_public():
    """Запуск FastAPI сервера с публичным доступом"""
    print("🚀 Запуск FastAPI сервера с публичным доступом...")
    print("🌐 Сервер будет доступен по адресу: http://0.0.0.0:8000")
    print("📱 Для доступа из локальной сети используйте ваш локальный IP")
    
    # Получаем локальный IP
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # не нужно отправлять пакет
        s.connect(('10.255.255.255', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    
    print(f"🔗 Локальный IP: http://{local_ip}:8000")
    print(f"📖 Документация: http://{local_ip}:8000/docs")
    print(f"📊 Статистика: http://{local_ip}:8000/stats")
    
    os.system("uvicorn main:app --host 0.0.0.0 --port 8000 --reload")

def run_ngrok():
    """Запуск ngrok для публичного доступа"""
    print("\n🌐 Запуск ngrok для публичного доступа в интернет...")
    print("⚠️  Убедитесь, что ngrok установлен и настроен!")
    print("📦 Установка: https://ngrok.com/download")
    print("🔑 Настройка: ngrok config add-authtoken <ваш_токен>")
    
    try:
        import requests
        # Проверяем, запущен ли уже ngrok
        response = requests.get('http://localhost:4040/api/tunnels')
        if response.status_code == 200:
            print("✅ Ngrok уже запущен")
            tunnels = response.json()['tunnels']
            for tunnel in tunnels:
                print(f"🔗 Публичный URL: {tunnel['public_url']}")
            return
    except:
        pass
    
    # Запускаем ngrok
    print("🔄 Запускаю ngrok...")
    os.system("ngrok http 8000")

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

def main():
    print("=" * 60)
    print("🚗 TRAVEL COMPANION - ПУБЛИЧНЫЙ ДОСТУП")
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
    print("1. Только локальный сервер (http://127.0.0.1:8000)")
    print("2. Публичный доступ в локальной сети (http://ваш-ip:8000)")
    print("3. Публичный доступ через ngrok (https://ваш-домен.ngrok.io)")
    
    choice = input("\nВведите номер (1-3): ").strip()
    
    if choice == '1':
        print("\n🔧 Запуск в локальном режиме...")
        os.system("uvicorn main:app --host 127.0.0.1 --port 8000 --reload")
    
    elif choice == '2':
        print("\n🌐 Запуск с доступом в локальной сети...")
        # Запускаем сервер в отдельном потоке
        server_thread = Thread(target=run_server_public)
        server_thread.daemon = True
        server_thread.start()
        
        time.sleep(3)
        
        print("\n✅ Сервер запущен!")
        print("📱 Чтобы подключить Mini App:")
        print("1. В файле app.js замените API_BASE_URL на ваш локальный IP")
        print("2. В Telegram Mini App настройте Web App URL")
        print("\n🛑 Для остановки нажмите Ctrl+C")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Остановка сервера...")
    
    elif choice == '3':
        print("\n🚀 Запуск с полным публичным доступом...")
        
        # Запускаем сервер в отдельном потоке
        server_thread = Thread(target=run_server_public)
        server_thread.daemon = True
        server_thread.start()
        
        time.sleep(3)
        
        # Запускаем ngrok в отдельном потоке
        ngrok_thread = Thread(target=run_ngrok)
        ngrok_thread.daemon = True
        ngrok_thread.start()
        
        print("\n✅ Система запущена!")
        print("📱 Чтобы подключить Mini App:")
        print("1. Дождитесь появления публичного URL от ngrok")
        print("2. В файле app.js замените API_BASE_URL на этот URL")
        print("3. В Telegram Bot настройте Web App URL на этот же URL")
        print("\n🛑 Для остановки нажмите Ctrl+C")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Остановка системы...")
    
    else:
        print("❌ Неверный выбор")

if __name__ == "__main__":
    main()