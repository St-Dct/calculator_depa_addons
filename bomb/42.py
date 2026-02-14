import os
import os.path
import urllib.request
import platform
import ctypes
import subprocess

# 🔥 ИЗОБРАЖЕНИЕ (твоя ссылка)
IMAGE_URL = "https://images.genius.com/6c6d9f79236d404764774d75c3ef3500.1000x1000x1.png"

# 🔥 МУЗЫКА (ЗАМЕНИ НА RAW MP3! GitHub raw/soundcloud direct/etc.)
MUSIC_URL = "https://fine.sunproxy.net/file/SmExakg3TFpUZGVTTlZ3a1Ivb3pJLzRPbjY4U3dMUk50SjdDdk1nM3pEUWdUTlRsMGJ5Z3NkRUlTN0MvWFpqdTI3Z21oT2ZiRU5xTlNWeFhqUEZ0dFpkYTQ0cGtUbUZPNDFNY201ajBDNEU9/5opka_6055_-_42_Flamile_Original_Remix_(SkySound.cc).mp3"  # Пример: колокольчик. Поставь свой MP3!

class Addon:
    def __init__(self, app):
        self.app = app
        self.sounds_dir = "sounds"  # Локальная папка для музыки
        if not os.path.exists(self.sounds_dir):
            os.makedirs(self.sounds_dir)
        print("[42-WP+MUSIC] Аддон готов! Ждём 42...")

    def set_wallpaper(self, filepath):
        """Установка обоев по OS"""
        system = platform.system()
        print(f"[42] OS: {system}, wallpaper: {filepath}")
        
        try:
            if system == "Windows":
                SPI_SETDESKWALLPAPER = 20
                ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, filepath, 3)
                print("[42] ✅ Windows wallpaper set!")
            elif system == "Linux":
                # GNOME (ubuntu и т.д.)
                subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", f"file://{filepath}"], check=False)
                print("[42] ✅ Linux GNOME wallpaper!")
            elif system == "Darwin":  # macOS
                subprocess.run(["osascript", "-e", f'tell application "Finder" to set desktop picture to POSIX file "{filepath}"'], check=False)
                print("[42] ✅ macOS wallpaper!")
            else:
                print("[42] OS не поддерживается")
        except Exception as e:
            print(f"[42 WALLPAPER ERROR]: {e}")

    def download_and_play_music(self):
        """Скачать + играть музыку"""
        music_filename = "42-win.mp3"
        music_path = os.path.join(self.sounds_dir, music_filename)
        
        try:
            print(f"[42] Скачиваем музыку: {MUSIC_URL}")
            with urllib.request.urlopen(MUSIC_URL) as response:
                music_data = response.read()
            
            with open(music_path, "wb") as f:
                f.write(music_data)
            
            print(f"[42] 🎵 Играем: {music_path}")
            self.app.play_music(music_path)  # Заменит дефолтную!
            
        except Exception as e:
            print(f"[42 MUSIC ERROR]: {e}")

    def on_eval(self, expression, result):
        if abs(result - 42) < 1e-6:
            self.app.display.setText("🎉 42 — БРАТУХА! 🔥")
            
            try:
                print(f"[42] Скачиваем изображение: {IMAGE_URL}")
                with urllib.request.urlopen(IMAGE_URL) as response:
                    image_data = response.read()
                
                # Desktop
                home = os.path.expanduser("~")
                possible_desktops = [
                    os.path.join(home, "Desktop"),
                    os.path.join(home, r"Рабочий стол"),
                    os.path.join(os.environ.get('USERPROFILE', home), "Desktop")
                ]
                desktop = next((d for d in possible_desktops if os.path.exists(d)), home)
                
                image_filename = "42-meme.png"
                image_path = os.path.join(desktop, image_filename)
                
                with open(image_path, "wb") as f:
                    f.write(image_data)
                
                # 1. Установить обои
                self.set_wallpaper(image_path)
                
                # 2. Скачать/играть музыку (заменит background.mp3)
                self.download_and_play_music()
                
                # Уведомка
                self.app.display.setText(f"🖼️ 42 Обои🎵 42 победа играет!")
                print("[42] ✅ Полный джекпот: обои + музыка!")
                
            except Exception as e:
                self.app.display.setText(f"❌ 42 Error: {str(e)[:50]}")
                print(f"[42 FULL ERROR]: {e}")