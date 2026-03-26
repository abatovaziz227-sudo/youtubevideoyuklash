import yt_dlp
import os

def download_video(url):
    # Yuklab olish joyi (Downloaded_Videos papkasi yaratiladi)
    output_dir = os.path.join(os.getcwd(), "Downloaded_Videos")
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),   # Video nomi bilan saqlash
        'format': 'bestvideo+bestaudio/best',                       # Eng yuqori sifatli video + audio
        'merge_output_format': 'mp4',                               # Natijani MP4 qilish
        'quiet': False,
        'no_warnings': False,
        'ignoreerrors': True,
        
        # ================== TOKEN / COOKIES SHU YERGA QO'YILADI ==================
        'cookiefile': 'cookies.txt',  8688733724:AAEoV0ztlJ5JvTSyGiRYe_vtIN71gLftDjU        # ← BU YER TOKEN JOYI (cookies.txt fayli)
        
        # Qo'shimcha yaxshi sozlamalar
        'concurrent_fragment_downloads': 8,   # Tezroq yuklash
        'retries': 10,
    }

    print(f"📥 Yuklanmoqda: {url}")
    print("⏳ Biroz kuting...")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("✅ Muvaffaqiyatli yuklandi!\n")
    except Exception as e:
        print(f"❌ Xatolik: {e}\n")


# ====================== DASTURNI ISHGA TUSHIRISH ======================
if __name__ == "__main__":
    print("=== YouTube Video Yuklovchi ===\n")
    
    while True:
        url = input("YouTube linkini kiriting (chiqish uchun 'exit' yozing): ").strip()
        
        if url.lower() == 'exit':
            print("Dastur tugatildi. Xayr!")
            break
        elif url:
            download_video(url)
        else:
            print("Iltimos, to'g'ri link kiriting!\n")
