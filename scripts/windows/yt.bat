@echo off

::set /p link="> "

echo Agregador de formatos de download do yt-dlp. Escolha o teu tipo de download abaixo:

:: 1. Qualidade --->  %dl%  ->  -f mp4
echo Escolha de Download:
echo 1. Recomendado pelo programa, pre-encodado (-f mp4)
echo 2. A melhor possivel ("-f bestvideo+bestaudio/bestvideo+bestaudio --merge-output-format mp4")
echo 3. Audio MP3
echo 4. Audio M4A
echo 5. 360p, re-encodado ("-f bestvideo[height<=360]+bestaudio/best[height<=360] --merge-output-format mp4")
echo 6. 480p, re-encodado ("-f bestvideo[height<=480]+bestaudio/best[height<=480] --merge-output-format mp4")
echo 7. 720p, re-encodado ("-f bestvideo[height<=720]+bestaudio/best[height<=720] --merge-output-format mp4")
echo 8. 1080p, re-encodado ("-f bestvideo[height<=1080]+bestaudio/best[height<=1080] --merge-output-format mp4")
echo 9. A pior possivel
echo:
set /p op="Digite a opcao> "
echo:

if "%op%" == "1" (
	set  dl=-f mp4
) else if "%op%" == "2" (
	set dl=-f bestvideo+bestaudio/bestvideo+bestaudio --merge-output-format mp4
) else if "%op%" == "3" (
	set dl=-f bestaudio --extract-audio --audio-format mp3 --audio-quality 192k
) else if "%op%" == "4" (
	set dl=-f bestaudio --extract-audio --audio-format m4a --audio-quality 128k
) else if "%op%" == "5" (
	set dl=-f bestvideo[height<=360]+bestaudio/best[height<=360] --merge-output-format mp4
) else if "%op%" == "6" (
	set dl=-f bestvideo[height<=480]+bestaudio/best[height<=480] --merge-output-format mp4
) else if "%op%" == "7" (
	set dl=-f bestvideo[height<=720]+bestaudio/best[height<=720] --merge-output-format mp4
) else if "%op%" == "8" (
	set dl=-f bestvideo[height<=1080]+bestaudio/best[height<=1080] --merge-output-format mp4
) else if "%op%" == "9" (
	set dl=-f worst
) else (
	echo ESSA OPCAO NAO EXISTE
)

:: 2. Metadados --->  %meta% -> metadados escritos e imbutidos, ou apenas metadados imbutido
echo Escolha de metadados:
echo 1. Apenas Metadados imbutidos
echo 2. Metadados escritos e imbutidos (os arquivos estarao no mesmo local do arquivo do link)
echo: 
set /p op="Digite a opcao> "
echo:

if "%op%" == "1" (
	set meta=--embed-metadata --embed-chapters --all-subs --embed-subs --embed-thumbnail
) else if "%op%" == "2" (
	set  meta=--embed-metadata --embed-chapters --all-subs --embed-subs --embed-thumbnail --write-thumbnail --write-description --write-info-json --write-annotations --write-comments
) else (
	echo ESSA OPCAO NAO EXISTE
)

:: 3. Formato   --->  %formato% -> -o "%%(title)s [%%(upload_date)s] [%%(id)s].%%(ext)s"
echo Escolha de formato (a barra simboliza um diretorio):
echo 1. Video/Audio: "TITULO_DO_VIDEO" ["DATA_DE_UPLOAD"] ["ID/URL"]."EXTENSAO"
echo 2. Video/Audio em uma pasta: "TITULO_DO_VIDEO"/"TITULO_DO_VIDEO" ["DATA_DE_UPLOAD"] ["ID/URL"]."EXTENSAO"
echo 3. Playlist com indice: "TITULO_DA_PLAYLIST"/"INDICE_DA_PLAYLIST"-"TITULO_DO_VIDEO" ["DATA_DE_UPLOAD"] ["ID/URL"]."EXTENSAO"
echo 4. Playlist sem indice: "TITULO_DA_PLAYLIST"/"TITULO_DO_VIDEO" ["DATA_DE_UPLOAD"] ["ID/URL"]."EXTENSAO"
echo 5. Arquivacao de canais: "UPLOADER"/"TITULO_DA_PLAYLIST"/"TITULO_DO_VIDEO" ["DATA_DE_UPLOAD"] ["ID/URL"]."EXTENSAO" 
echo:
set /p op="Digite a opcao> "
echo:

if "%op%" == "1" (
	set formato=-o "%%(title)s [%%(upload_date)s] [%%(id)s].%%(ext)s"
) else if "%op%" == "2" (
	set formato=-o "%%(title)s/%%(title)s [%%(upload_date)s] [%%(id)s].%%(ext)s"
) else if "%op%" == "3" (
	set formato=-o "%%(playlist_title)s/%%(playlist_index)s-%%(title)s [%%(upload_date)s] [%%(id)s].%%(ext)s"
) else if "%op%" == "4" (
	set formato=-o "%%(playlist_title)s/%%(title)s [%%(upload_date)s] [%%(id)s].%%(ext)s"
) else if "%op%" == "5" (
	set formato=-o "%%(uploader)s/%%(playlist_title)s/%%(title)s [%%(upload_date)s] [%%(id)s].%%(ext)s"
) else (
	echo ESSA OPCAO NAO EXISTE
)
echo:
:: 4. URL
set /p url="Cola o link aquiew> "
echo:
:: 5. Execucao do resultado final
yt-dlp %dl% %meta% %formato% %url%
