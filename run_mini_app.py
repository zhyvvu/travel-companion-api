# run_mini_app.py - ДЛЯ ЗАПУСКА MINI APP ОТДЕЛЬНО
import http.server
import socketserver
import webbrowser
import os

PORT = 8080
DIRECTORY = "mini_app"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run_mini_app():
    print("🌐 Запуск Mini App сервера...")
    print(f"📂 Папка: {os.path.abspath(DIRECTORY)}")
    print(f"🌐 Ссылка: http://localhost:{PORT}")
    print("📱 Открываю в браузере...")
    
    # Открываем в браузере
    webbrowser.open(f"http://localhost:{PORT}")
    
    # Запускаем сервер
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"✅ Сервер запущен на порту {PORT}")
        print("🛑 Для остановки нажмите Ctrl+C")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Остановка сервера...")

if __name__ == "__main__":
    print("=" * 60)
    print("📱 TRAVEL COMPANION MINI APP")
    print("=" * 60)
    run_mini_app()