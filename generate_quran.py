import urllib.request, json
url = "https://api.alquran.cloud/v1/quran/quran-uthmani"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    import os
    os.makedirs("applet/app/src/main/assets", exist_ok=True)
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        with open("applet/app/src/main/assets/quran.txt", "w", encoding="utf-8") as f:
            for surah in data['data']['surahs']:
                chapter = surah['number']
                for ayah in surah['ayahs']:
                    verse = ayah['numberInSurah']
                    text = ayah['text']
                    f.write(f"{chapter}|{verse}|{text}\n")
    print("Success")
except Exception as e:
    print("Error:", e)
