@echo off

::set /p link="> "

echo "Baixar um video de uma qualidade pré-definida em mp4"
set /p link="Digite o link> "


yt-dlp -f mp4 --embed-metadata --embed-chapters --all-subs --embed-subs --embed-thumbnail -o "%%(title)s [%%(upload_date)s] [%%(id)s].%%(ext)s" %link%

