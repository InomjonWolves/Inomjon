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
| **1** | Eng yuqori sifat: 4K/8K, 60 fps, HDR (bor boʻlsa) | Standart. Fayl koʻpincha `.mkv` boʻladi |
| **2** | MP4, 1080p gacha (H.264) | Istalgan pleyer, messenjer, televizorda ochilishi kerak boʻlsa |
| **3** | 720p MP4 | Joy va internetni tejash |
| **4** | Faqat audio, M4A, muqova rasmi bilan | Musiqa, podkast |

Yoki Termux'da yozing:

```sh
yt https://youtu.be/…        # sifatni soʻraydi
yt https://youtu.be/… 1      # darhol eng yuqori sifat
yt yangilash                 # yt-dlp va shu skriptni yangilash
yt yordam
```

Pleylist havolasida «faqat shu video» yoki «butun pleylist» soʻraladi. Pleylist alohida papkaga yoziladi; qayta ishga tushirsangiz, yuklangan videolar oʻtkazib yuboriladi.

**Fayllar:** `Download/YouTube` (audio — `Download/YouTube/Audio`). Galereyada «YouTube» albomi boʻlib koʻrinadi.

## 4. Bosh ekran tugmasi (ixtiyoriy)

Havolani nusxalaysiz va bosh ekrandagi qizil tugmani bosasiz: Termux oʻzi ochilib, sifatni soʻraydi.

1. F-Droid'dan yana ikkita kichik ilova oʻrnating (Termux'ni qayerdan olgan boʻlsangiz, oʻsha joydan — aks holda ishlamaydi):
   - **Termux:Widget** — https://f-droid.org/packages/com.termux.widget/
   - **Termux:API** — https://f-droid.org/packages/com.termux.api/ (nusxalangan havolani oʻqish uchun)
2. Termux'da bir marta yozing: `yt tugma` (yangi oʻrnatishda bu oʻzi bajariladi).
3. Bosh ekranni bosib turing → **Vidjetlar** → **Termux:Widget** → **Termux shortcut** ni ekranga torting → **YouTube-yuklash** ni tanlang.
4. Telefon sozlamalari → Ilovalar → Termux → **Boshqa ilovalar ustidan koʻrsatish** → yoqing. Busiz tugma bosilganda Termux oʻzi ochilmaydi (Android 10+).

Ishlatish: YouTube'da **Ulashish → Nusxa olish**, keyin tugmani bosing. Buferda havola boʻlmasa, Termux havolani soʻraydi.

## Bilib qoʻying

- **MKV fayllar.** YouTube 4K ni VP9/AV1 kodekida beradi, ular MP4 ga emas, MKV ga joylanadi. Koʻp telefonlarning galereyasi MKV ni ochadi; ochmasa — **VLC** (Play Market, bepul). Galereyada albatta ochilishi kerak boʻlsa — **2** ni tanlang.
- **4K hajmi katta:** 10 daqiqalik 4K video ~1–2 GB. Yuklashdan oldin taxminiy hajm koʻrsatiladi.
- **Ekran oʻchsa ham** yuklash davom etadi (Termux «wake lock» oladi). Termux'ni yopmang.
- **YouTube oʻzgarsa**, yt-dlp har 5 kunda oʻzi yangilanadi; xato boʻlsa — yangilab, yana bir marta urinadi. Qoʻlda: `yt yangilash`.
- **«Robot emasligingizni tasdiqlang»** xatosi — Wi-Fi'dan mobil internetga (yoki aksincha) oʻting, birozdan keyin qayta urining. VPN boʻlsa, oʻchirib koʻring.
- Yopiq (private), faqat aʼzolar uchun va yosh cheklovi bor videolar hisobsiz yuklanmaydi.
- Instagram, TikTok, Facebook va boshqa saytlar havolalari ham koʻpincha ishlaydi — yt-dlp minglab saytlarni biladi.

## Huquqiy eslatma

Faqat oʻzingiz koʻrish uchun yuklang. Mualliflik huquqi bilan himoyalangan videolarni tarqatmang; YouTube qoidalari yuklab olishni cheklaydi — rasmiy yoʻli YouTube Premium.

## Oʻchirish

```sh
rm -f $PREFIX/bin/yt ~/bin/termux-url-opener ~/.shortcuts/YouTube-yuklash ~/.shortcuts/icons/YouTube-yuklash.png
pip uninstall -y yt-dlp yt-dlp-ejs
```

## Fayllar

| Fayl | Vazifasi |
|---|---|
| `install.sh` | Oʻrnatuvchi: Termux paketlari, `yt`, ulashish tugmasi, xotira ruxsati |
| `yt` | Asosiy buyruq: menyu, sifat tanlash, yuklash, xatolarni tushuntirish, yangilash |
| `termux-url-opener` | «Ulashish → Termux» bosilganda havolani `yt` ga beradi (`~/bin/` ga oʻrnatiladi) |
| `tugma`, `tugma.png` | Bosh ekran tugmasi va uning belgisi (`yt tugma` → `~/.shortcuts/YouTube-yuklash`) |
