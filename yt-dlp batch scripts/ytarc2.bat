@echo off

echo Formato: %%(uploader)s/%%(playlist_title)s/%%(title)s [%%(upload_date)s] [%%(id)s].%%(ext)s
set /p link="Digite um link para arquivar um canal do youtube: "

::Arquivação de uma qualidade qualquer em mp4 de um canal completo:
yt-dlp -f mp4 --all-subs --embed-subs --write-annotations --write-comments --embed-thumbnail --write-thumbnail --embed-metadata --embed-chapters --write-description --write-info-json -o "%%(uploader)s/%%(playlist_title)s/%%(title)s [%%(upload_date)s] [%%(id)s].%%(ext)s" %link%