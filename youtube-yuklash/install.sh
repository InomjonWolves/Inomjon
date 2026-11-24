#!/usr/bin/env bash
# YouTube yuklovchini Termux'ga oʻrnatish. Termux'da bitta buyruq:
#   curl -fsSL https://raw.githubusercontent.com/InomjonWolves/Inomjon/ccr-dc03c86a-hhey2p/youtube-yuklash/install.sh | bash
#
# Nima qiladi: python, ffmpeg, nodejs paketlari → yt-dlp → «yt» buyrugʻi va
# «Ulashish → Termux» tugmasi (~/bin/termux-url-opener) → xotiraga ruxsat.

# Hammasi funksiya ichida: «curl | bash» da skript oxirigacha oʻqilib, keyin ishlaydi.
main() {
  set -u
  local BASE="${YT_BASE:-https://raw.githubusercontent.com/InomjonWolves/Inomjon/ccr-dc03c86a-hhey2p/youtube-yuklash}"
  local C=$'\e[36m' G=$'\e[32m' R=$'\e[31m' B=$'\e[1m' N=$'\e[0m'
  say() { printf '\n%s\n' "${C}==>${N} ${B}$*${N}"; }
  die() { printf '\n%s\n' "${R}✖ $*${N}" >&2; exit 1; }

  case "${PREFIX:-}" in
    *com.termux*) ;;
    *) [ -n "${YT_TEST:-}" ] || die "Bu oʻrnatuvchi Android'dagi Termux ilovasi uchun." ;;
  esac
  local BIN="$PREFIX/bin"

  say "1/4 Termux paketlari yangilanmoqda (birinchi marta 2–5 daqiqa)…"
  export DEBIAN_FRONTEND=noninteractive
  yes | pkg upgrade -y -o Dpkg::Options::=--force-confnew || die "Paketlarni yangilab boʻlmadi. Internetni tekshirib, qayta urining."

  say "2/4 Python, ffmpeg va Node.js oʻrnatilmoqda…"
  yes | pkg install -y python python-pip ffmpeg curl || die "Paketlarni oʻrnatib boʻlmadi."
  # Node.js — YouTube'ning himoya skriptlarini yechish uchun (busiz eng yuqori sifatlar chiqmaydi).
  if ! command -v node >/dev/null; then
    yes | pkg install -y nodejs-lts || yes | pkg install -y nodejs || die "Node.js ni oʻrnatib boʻlmadi."
  fi

  say "3/4 yt buyrugʻi oʻrnatilmoqda…"
  local tmp f
  tmp=$(mktemp -d)
  for f in yt termux-url-opener mp4; do
    curl -fsSL "$BASE/$f" -o "$tmp/$f" || die "$f ni yuklab boʻlmadi: $BASE/$f"
    bash -n "$tmp/$f" || die "$f buzuq holda keldi — qayta urining."
    chmod +x "$tmp/$f"
    command -v termux-fix-shebang >/dev/null && termux-fix-shebang "$tmp/$f"
  done
  mkdir -p "$HOME/bin"
  local opener="$HOME/bin/termux-url-opener"
  if [ -f "$opener" ] && ! grep -q '"yt"\|/bin/yt' "$opener"; then
    cp "$opener" "$opener.eski" && echo "Avvalgi termux-url-opener saqlandi: $opener.eski"
  fi
  mv -f "$tmp/yt" "$BIN/yt"
  mv -f "$tmp/mp4" "$BIN/mp4"
  mv -f "$tmp/termux-url-opener" "$opener"
  rm -rf "$tmp"
  "$BIN/yt" yangilash-ytdlp || die "yt-dlp ni oʻrnatib boʻlmadi."
  "$BIN/yt" tugma >/dev/null || echo "Bosh ekran tugmasi oʻrnatilmadi — keyin: yt tugma"

  say "4/4 Xotiraga ruxsat…"
  if [ -d /storage/emulated/0/Download ] && [ -w /storage/emulated/0/Download ]; then
    echo "Ruxsat bor."
  elif command -v termux-setup-storage >/dev/null; then
    echo "Chiqqan oynada «Ruxsat berish» (Allow) ni bosing."
    termux-setup-storage
    for _ in $(seq 1 60); do
      [ -w /storage/emulated/0/Download ] && break
      sleep 1
    done
  else
    echo "Keyinroq kerak boʻlsa: termux-setup-storage"
  fi

  printf '\n%s\n\n' "${G}✔ Tayyor!${N}"
  cat <<EOF
${B}Qanday ishlatiladi:${N}
  • YouTube ilovasida videoni oching → ${B}Ulashish${N} → ${B}Termux${N} → sifatni tanlang.
  • Yoki havolani nusxalab, bosh ekrandagi tugmani bosing — sozlash: ${B}yt tugma${N}
  • Yoki Termux'da yozing:  ${B}yt <havola>${N}
  • Fayllar: ${B}Download/YouTube${N} (galereyada ham koʻrinadi).
  • Eski MKV videolarni MP4 ga (sifat oʻzgarmaydi):  ${B}mp4${N}
  • Pinterest videosi:  ${B}yt <pinterest havolasi>${N} yoki bosh ekrandagi ${B}Pinterest-yuklash${N} tugmasi
  • Faqat musiqa (MP3):  ${B}yt <havola> 5${N} yoki bosh ekrandagi ${B}YouTube-MP3${N} tugmasi
  • Yangilash:  ${B}yt yangilash${N}     Yordam:  ${B}yt yordam${N}
EOF
}

main "$@"
