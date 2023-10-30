@echo off

::set /p link="> "

echo "Baixar um video da melhor qualidade possivel em um mp4"
set /p link="Digite o link> "


yt-dlp -f bestvideo+bestaudio/bestvideo+bestaudio --merge-output-format mp4 --embed-thumbnail --embed-metadata --embed-chapters --all-subs --embed-subs -o "%%(title)s [%%(upload_date)s] [%%(id)s].%%(ext)s" %link%