@echo off

echo "Arquivação na melhor qualidade possível"
echo Formato: %%(uploader)s/%%(playlist_title)s/%%(title)s [%%(upload_date)s] [%%(id)s].%%(ext)s
set /p link="Digite um link para arquivar um canal do youtube: "

::Arquivação da mais alta qualidade para mp4 de canais:
yt-dlp -f bestvideo+bestaudio/bestvideo+bestaudio --merge-output-format mp4  --all-subs --embed-subs --write-annotations --write-comments --embed-thumbnail --write-thumbnail --embed-metadata --embed-chapters --write-description --write-info-json -o "%%(uploader)s/%%(playlist_title)s/%%(title)s [%%(upload_date)s] [%%(id)s].%%(ext)s" %link%