import requests
import os
import sys
import time
from bs4 import BeautifulSoup as bs

data = []

url = input("url: ")

def main():
    global url, judul
    b, y = url.split("https://kiryuu.id/manga/")
    judul = y.rstrip("/")
    if not os.path.exists(judul):
        os.makedirs(judul)
    
    r = requests.get(url)
    bss = bs(r.text, "html.parser")
    div = bss.findAll("li", {"data-num": True})
    
    for i in div:
        link = i.find("a", "dload")
        ch = i.find("span", "chapternum")
        if ch.text == "Chapter {{number}}":
            continue
        data.append({"ch": ch.text, "link": link["href"]})
    
    for d in data[::-1]:
        jud = judul + "-" + d["ch"].replace(" ", "-") + ".zip"
        judl = judul.lower() + "/" + jud
        
        if os.path.exists(judl):
            print(f"File {judl} sudah ada.")
            continue
        
        url = d["link"]
        download(judl, url)

def download(jud, url):
    try_count = 0
    max_attempts = 3
    while try_count < max_attempts:
        try:
            start_time = time.time()
            response = requests.get(url, stream=True)
            size = 0
            total_size = int(response.headers.get('content-length', 0))
            
            with open(jud, 'ab') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        size += len(chunk)
                        f.write(chunk)
                        progress = size / total_size if total_size > 0 else 0
                        progress_message = "{:.1f} MB downloaded".format(size / (1024 * 1024))
                        sys.stdout.write("\r" + progress_message)
                        sys.stdout.flush()
            
            end_time = time.time()
            download_time = end_time - start_time
            print("\nFile " + jud + " berhasil diunduh dalam waktu {:.2f} detik".format(download_time))
            return  # Keluar dari fungsi setelah unduhan selesai
        except Exception as e:
            print("\nTerjadi kesalahan saat mengunduh file:", str(e))
            print("Menunggu 30 detik sebelum mencoba kembali...")
            time.sleep(30)  # Menunggu 30 detik sebelum mencoba kembali
            try_count += 1
    
    print(f"Gagal mengunduh file {jud} setelah {max_attempts} percobaan.")

if __name__ == '__main__':
    main()
