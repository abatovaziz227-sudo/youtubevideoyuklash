import yt_dlp
import os

# ================== TELEGRAM BOT TOKEN ==================
TELEGRAM_TOKEN = "8688733724:AAEoV0ztlJ5JvTSyGiRYe_vtIN71gLftDjU"

def download_video(url):
    # Yuklab olish joyi
    output_dir = os.path.join(os.getcwd(), "Downloaded_Videos")
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),   # Video nomi bilan saqlash
        'format': 'bestvideo+bestaudio/best',                       # Eng yuqori sifat
        'merge_output_format': 'mp4',                               # MP4 formatida
        'quiet': False,
        'no_warnings': False,
        'ignoreerrors': True,
        
        # ================== YOUTUBE COOKIES ==================
        'cookiefile': 'cookies.txt',          # cookies.txt faylidan foydalanadi
        
        # Qo'shimcha sozlamalar
        'concurrent_fragment_downloads': 8,
        'retries': 10,
    }

    print(f"📥 Yuklanmoqda: {url}")
    print("⏳ Biroz kuting...")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("✅ Muvaffaqiyatli yuklandi!\n")
    except Exception as e:
        print(f"❌ Xatolik yuz berdi: {e}\n")


# ====================== DASTURNI ISHGA TUSHIRISH ======================
if __name__ == "__main__":
    print("=== YouTube Video Yuklovchi ===\n")
    print(f"Telegram Token: {TELEGRAM_TOKEN[:15]}... (qo'shilgan)\n")
    
    while True:
        url = input("YouTube linkini kiriting (chiqish uchun 'exit' yozing): ").strip()
        
        if url.lower() == 'exit':
            print("Dastur tugatildi. Xayr!")
            break
        elif url:
            download_video(url)
        else:
            print("Iltimos, link kiriting!\n")
