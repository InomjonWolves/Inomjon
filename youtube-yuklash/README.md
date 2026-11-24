# YouTube → telefon (eng yuqori sifatda)

Android telefonda YouTube videolarini **4K/8K va HDR gacha** yuklab olish tizimi — shaxsiy foydalanish uchun.
Hammasi telefonning oʻzida ishlaydi: server, reklama, roʻyxatdan oʻtish yoʻq.

Ichida ikkita ochiq kodli dastur bor:
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — YouTube'dan eng yaxshi video va audio oqimini oladi;
- ffmpeg — ularni bitta faylga birlashtiradi (YouTube 1080p dan yuqorisini video va audio alohida beradi, shuning uchun oddiy yuklovchilar 360p dan nariga oʻtmaydi).

## 1. Termux'ni oʻrnating

Termux — Android uchun buyruqlar oynasi. **Play Market'dagi eski versiyani emas**, shu yerdan oling:
- F-Droid: https://f-droid.org/packages/com.termux/ — sahifa pastidagi «Download APK»;
- yoki GitHub: https://github.com/termux/termux-app/releases — `…arm64-v8a.apk` fayli.

## 2. Bitta buyruq bilan oʻrnating

Termux'ni oching, quyidagini qoʻying va Enter bosing:

```sh
curl -fsSL https://raw.githubusercontent.com/InomjonWolves/Inomjon/ccr-dc03c86a-hhey2p/youtube-yuklash/install.sh | bash
```

5–10 daqiqa ketadi (python, ffmpeg, Node.js va yt-dlp oʻrnatiladi). Oxirida «Xotiraga ruxsat» oynasi chiqadi — **Ruxsat berish** ni bosing.

## 3. Ishlatish

**Eng oson:** YouTube ilovasida videoni oching → **Ulashish** → **Termux** → raqamni tanlang:

| | Nima yuklanadi | Qachon |
|---|---|---|
| **1** | Eng yuqori sifat: 4K/8K, 60 fps, HDR — **MP4** da | Standart |
| **2** | Eng yuqori sifat, **MKV** da (asl holicha) | MKV kerak boʻlsa |
| **3** | MP4 1080p (H.264) | Eski telefon, televizor — eng keng mos |
| **4** | 720p MP4 | Joy va internetni tejash |
| **5** | Faqat musiqa — **MP3** (eng yuqori sifat, ~245 kbit/s), muqova rasmi va nomi bilan | Musiqa, podkast |
| **6** | Faqat musiqa — M4A (YouTube'ning asl ovozi, oʻzgarishsiz) | Eng toza ovoz kerak boʻlsa |
| **7** | Pinterest videosi, eng katta oʻlchamda, MP4 | Pinterest havolasi boʻlsa oʻzi tanlanadi (menyu chiqmaydi) |

Yoki Termux'da yozing:

```sh
yt https://youtu.be/…        # sifatni soʻraydi
yt https://youtu.be/… 1      # darhol eng yuqori sifat (MP4)
yt https://youtu.be/… 5      # darhol musiqa (MP3)
yt https://pin.it/…          # Pinterest videosi (menyusiz)
mp4                          # Download/YouTube dagi MKV larni MP4 ga
yt yangilash                 # yt-dlp va skriptlarni yangilash
yt yordam
```

Pleylist havolasida «faqat shu video» yoki «butun pleylist» soʻraladi. Pleylist alohida papkaga yoziladi; qayta ishga tushirsangiz, yuklangan videolar oʻtkazib yuboriladi.

**Fayllar:** `Download/YouTube` (musiqa — `Download/YouTube/Musiqa`, Pinterest — `Download/YouTube/Pinterest`). Galereyada «YouTube» albomi boʻlib koʻrinadi.

## 4. MKV → MP4 (sifat oʻzgarmaydi)

Oldin MKV boʻlib yuklangan videolarni MP4 ga oʻtkazish uchun Termux'da `mp4` deb yozing (yoki bosh ekrandagi yashil **MKV-dan-MP4** tugmasini bosing):

- **Video qayta kodlanmaydi** — oqim MKV ichidan MP4 ichiga aynan koʻchiriladi: 4K/8K, HDR, 60 fps, boblar va nom saqlanadi, bir necha soniyada tugaydi.
- Opus ovoz istalgan pleyerda ochilishi uchun AAC 256 kbit/s ga oʻtkaziladi (YouTube'ning 160 kbit/s ovozidan quloqqa farqsiz). Ovozni ham tegmasdan qoldirish: `mp4 --asl-audio`.
- Har bir natija tekshiriladi (davomiylik, video oqimi); oxirida asl MKV larni oʻchirish soʻraladi — faqat tekshiruvdan oʻtganlari oʻchadi. Soʻramasdan: `mp4 -o` (oʻchirish) yoki `mp4 -k` (saqlash).
- Bitta fayl yoki boshqa papka: `mp4 /storage/emulated/0/Download/video.mkv`.
- Shu nomda boshqa sifatdagi MP4 bor boʻlsa (masalan, 1080p), ustiga yozilmaydi — yangisi `… (2160p).mp4` boʻladi.
- Faqat VP8 kodekli eski videolarni sifat yoʻqotmasdan oʻtkazib boʻlmaydi — ular oʻtkazib yuboriladi.

## 5. Bosh ekran tugmalari (ixtiyoriy)

Qizil **YouTube-yuklash** — nusxalangan havolani yuklaydi (sifatni soʻraydi). Binafsha **YouTube-MP3** — soʻramasdan musiqani MP3 qilib yuklaydi. Yashil **MKV-dan-MP4** — papkadagi MKV larni MP4 ga oʻtkazadi. Pushti **Pinterest-yuklash** — nusxalangan pin havolasidan videoni eng yuqori sifatda yuklaydi.

1. F-Droid'dan yana ikkita kichik ilova oʻrnating (Termux'ni qayerdan olgan boʻlsangiz, oʻsha joydan — aks holda ishlamaydi):
   - **Termux:Widget** — https://f-droid.org/packages/com.termux.widget/
   - **Termux:API** — https://f-droid.org/packages/com.termux.api/ (nusxalangan havolani oʻqish uchun)
2. Termux'da bir marta yozing: `yt tugma` (yangi oʻrnatishda bu oʻzi bajariladi).
3. Bosh ekranni bosib turing → **Vidjetlar** → **Termux:Widget** → **Termux shortcut** ni ekranga torting → **YouTube-yuklash** ni tanlang. Qolgan tugmalar uchun yana bir martadan — **YouTube-MP3**, **MKV-dan-MP4**, **Pinterest-yuklash**.
4. Telefon sozlamalari → Ilovalar → Termux → **Boshqa ilovalar ustidan koʻrsatish** → yoqing. Busiz tugma bosilganda Termux oʻzi ochilmaydi (Android 10+).

Ishlatish: YouTube'da **Ulashish → Nusxa olish**, keyin tugmani bosing. Buferda havola boʻlmasa, Termux havolani soʻraydi.

## Bilib qoʻying

- **4K MP4 va eski qurilmalar.** 4K video VP9 yoki AV1 kodekida boʻladi (YouTube H.264 da 1080p dan yuqorisini bermaydi). Android 10+ telefonlar ularni ochadi; eski televizor yoki pleyer ochmasa — **VLC** yoki **3** (1080p H.264).
- **4K hajmi katta:** 10 daqiqalik 4K video ~1–2 GB. Yuklashdan oldin taxminiy hajm koʻrsatiladi.
- **Ekran oʻchsa ham** yuklash davom etadi (Termux «wake lock» oladi). Termux'ni yopmang.
- **YouTube oʻzgarsa**, yt-dlp har 5 kunda oʻzi yangilanadi; xato boʻlsa — yangilab, yana bir marta urinadi. Qoʻlda: `yt yangilash`.
- **«Robot emasligingizni tasdiqlang»** xatosi — Wi-Fi'dan mobil internetga (yoki aksincha) oʻting, birozdan keyin qayta urining. VPN boʻlsa, oʻchirib koʻring.
- **MP3 haqida.** YouTube ovozni allaqachon siqilgan holda saqlaydi (~128–160 kbit/s), MP3 ga oʻtkazish uni yaxshilamaydi — faqat har qanday pleyerda ochiladigan qiladi. Eng toza ovoz kerak boʻlsa — **6** (M4A).
- **Pinterest.** Pinterest ilovasida pinni oching → **Ulashish** → **Havolani nusxalash** → pushti tugmani bosing. Pinterest videoni bir necha oʻlchamda saqlaydi, eng kattasi yuklanadi — odatda asl yuklangan sifat, lekin undan yuqori boʻlmaydi. Pin faqat rasm boʻlsa, «Bu pinda video yoʻq» deb aytadi. Shaxsiy (yopiq) doskadagi pinlar yuklanmaydi.
- Yopiq (private), faqat aʼzolar uchun va yosh cheklovi bor videolar hisobsiz yuklanmaydi.
- Instagram, TikTok, Facebook va boshqa saytlar havolalari ham koʻpincha ishlaydi — yt-dlp minglab saytlarni biladi.

## Huquqiy eslatma

Faqat oʻzingiz koʻrish uchun yuklang. Mualliflik huquqi bilan himoyalangan videolarni tarqatmang; YouTube qoidalari yuklab olishni cheklaydi — rasmiy yoʻli YouTube Premium.

## Oʻchirish

```sh
rm -f $PREFIX/bin/yt $PREFIX/bin/mp4 ~/bin/termux-url-opener
rm -f ~/.shortcuts/YouTube-yuklash ~/.shortcuts/MKV-dan-MP4 ~/.shortcuts/YouTube-MP3 ~/.shortcuts/Pinterest-yuklash
rm -f ~/.shortcuts/icons/YouTube-yuklash.png ~/.shortcuts/icons/MKV-dan-MP4.png ~/.shortcuts/icons/YouTube-MP3.png ~/.shortcuts/icons/Pinterest-yuklash.png
pip uninstall -y yt-dlp yt-dlp-ejs
```

## Fayllar

| Fayl | Vazifasi |
|---|---|
| `install.sh` | Oʻrnatuvchi: Termux paketlari, `yt`, ulashish tugmasi, xotira ruxsati |
| `yt` | Asosiy buyruq: menyu, sifat tanlash, yuklash, xatolarni tushuntirish, yangilash |
| `termux-url-opener` | «Ulashish → Termux» bosilganda havolani `yt` ga beradi (`~/bin/` ga oʻrnatiladi) |
| `mp4` | MKV/WEBM → MP4: video qayta kodlanmaydi, natija tekshiriladi |
| `tugma`, `tugma.png` | Bosh ekran tugmasi va uning belgisi (`yt tugma` → `~/.shortcuts/YouTube-yuklash`) |
| `tugma-pin`, `tugma-pin.png` | Toʻrtinchi tugma: Pinterest videosi (`~/.shortcuts/Pinterest-yuklash`) |
| `tugma-mp3`, `tugma-mp3.png` | Uchinchi tugma: menyusiz MP3 yuklash (`~/.shortcuts/YouTube-MP3`) |
| `tugma-mp4`, `tugma-mp4.png` | Ikkinchi tugma: papkadagi MKV larni MP4 ga (`~/.shortcuts/MKV-dan-MP4`) |
