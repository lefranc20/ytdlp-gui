@echo off

echo "Musica no formato m4a em 128k"
echo "Formato: %%(title)s [%%(id)s].%%(ext)s"
set /p link="Digite o link para baixar um audio no formato m4a em 128k: "

::Música no formato m4a em 128k:
yt-dlp -f bestaudio --extract-audio --audio-format m4a --audio-quality 128k --embed-metadata --embed-thumbnail -o "%%(title)s [%%(id)s].%%(ext)s" %link%