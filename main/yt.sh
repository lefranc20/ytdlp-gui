#!/bin/bash

echo "Agregador de formatos de download do yt-dlp. Escolha o tipo de download:"
echo "1. Recomendado pelo programa, pre-encodado (-f mp4)"
echo "2. A melhor possível (\"-f bestvideo+bestaudio/bestvideo+bestaudio --merge-output-format mp4\")"
echo "3. Audio MP3"
echo "4. Audio M4A"
echo "5. 360p, re-encodado (\"-f bestvideo[height<=360]+bestaudio/best[height<=360] --merge-output-format mp4\")"
echo "6. 480p, re-encodado (\"-f bestvideo[height<=480]+bestaudio/best[height<=480] --merge-output-format mp4\")"
echo "7. 720p, re-encodado (\"-f bestvideo[height<=720]+bestaudio/best[height<=720] --merge-output-format mp4\")"
echo "8. 1080p, re-encodado (\"-f bestvideo[height<=1080]+bestaudio/best[height<=1080] --merge-output-format mp4\")"
echo "9. A pior possível"
read -p "Digite a opção> " op

if [ "$op" = "1" ]; then
    dl="-f mp4"
elif [ "$op" = "2" ]; then
    dl="-f bestvideo+bestaudio/bestvideo+bestaudio --merge-output-format mp4"
elif [ "$op" = "3" ]; then
    dl="-f bestaudio --extract-audio --audio-format mp3 --audio-quality 192k"
elif [ "$op" = "4" ]; then
    dl="-f bestaudio --extract-audio --audio-format m4a --audio-quality 128k"
elif [ "$op" = "5" ]; then
    dl="-f bestvideo[height<=360]+bestaudio/best[height<=360] --merge-output-format mp4"
elif [ "$op" = "6" ]; then
    dl="-f bestvideo[height<=480]+bestaudio/best[height<=480] --merge-output-format mp4"
elif [ "$op" = "7" ]; then
    dl="-f bestvideo[height<=720]+bestaudio/best[height<=720] --merge-output-format mp4"
elif [ "$op" = "8" ]; then
    dl="-f bestvideo[height<=1080]+bestaudio/best[height<=1080] --merge-output-format mp4"
elif [ "$op" = "9" ]; then
    dl="-f worst"
else
    echo "ESSA OPÇÃO NÃO EXISTE"
    exit 1
fi

echo "Escolha de metadados:"
echo "1. Apenas Metadados imbutidos"
echo "2. Metadados escritos e imbutidos (os arquivos estarão no mesmo local do arquivo do link)"
read -p "Digite a opção> " op

if [ "$op" = "1" ]; then
    meta="--embed-metadata --embed-chapters --all-subs --embed-subs --embed-thumbnail"
elif [ "$op" = "2" ]; then
    meta="--embed-metadata --embed-chapters --all-subs --embed-subs --embed-thumbnail --write-thumbnail --write-description --write-info-json --write-annotations --write-comments"
else
    echo "ESSA OPÇÃO NÃO EXISTE"
    exit 1
fi

echo "Escolha de formato (a barra simboliza um diretório):"
echo "1. Video/Audio: \"TITULO_DO_VIDEO\" [\"DATA_DE_UPLOAD\"] [\"ID/URL\"].\"EXTENSÃO\""
echo "2. Playlist com índice: \"TITULO_DA_PLAYLIST\"/\"INDICE_DA_PLAYLIST\"-\"TITULO_DO_VIDEO\" [\"DATA_DE_UPLOAD\"] [\"ID/URL\"].\"EXTENSÃO\""
echo "3. Playlist sem índice: \"TITULO_DA_PLAYLIST\"/\"TITULO_DO_VIDEO\" [\"DATA_DE_UPLOAD\"] [\"ID/URL\"].\"EXTENSÃO\""
read -p "Digite a opção> " op

if [ "$op" = "1" ]; then
    formato="-o \"%(title)s [%(upload_date)s] [%(id)s].%(ext)s\""
elif [ "$op" = "2" ]; then
    formato="-o \"%(playlist_title)s/%(playlist_index)s-%(title)s [%(upload_date)s] [%(id)s].%(ext)s\""
elif [ "$op" = "3" ]; then
    formato="-o \"%(playlist_title)s/%(title)s [%(upload_date)s] [%(id)s].%(ext)s\""
else
    echo "ESSA OPÇÃO NÃO EXISTE"
    exit 1
fi

read -p "Cole o link aqui> "
echo
yt-dlp $dl $meta $formato $url
