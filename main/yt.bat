@echo off

::set /p link="> "

echo Agregador de formatos de download do yt-dlp. Escolha o teu tipo de download abaixo:

set /p numOp="Digite a opcao> "
echo:
	
	if "%numOp%" == "1" (
		echo Escolha de Qualidade:
		echo 1. Recomendado pelo programa, pre-encodado
		echo 2. A melhor possivel
		echo 3. 360p, re-encodado
		echo 4. 480p, re-encodado
		echo 5. 720p, re-encodado
		echo 6. 1080p, re-encodado
		echo 7. A pior possivel
		echo Aviso: as resolucoes especificas talvez nao estejam disponiveis
		echo:
		set /p qualOp="Digite a qualidade> "
		echo:
		
	) else if "%numOp%" == "2" (
		echo DEU BAO
	)