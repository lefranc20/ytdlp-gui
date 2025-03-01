Um programa pequeno adaptando uma GUI para o yt-dlp. Feito utilizando a interface gráfica nativa do **Python**: **Tkinter**.

# Dependências
Necessita dos seguintes pacotes:
- [yt-dlp](https://github.com/yt-dlp/yt-dlp);
- [ffmpeg](https://github.com/FFmpeg/FFmpeg) e ffprobe;
- [pillow](https://github.com/python-pillow/Pillow) (Biblioteca de Imagem do Python);

# Instalação e Execução
Eles todos podem ser instalados pelo pip (obs: no Linux provavelmente vai ser pip3):
``` bash
pip install -r requirements.txt
```

Ou manualmente especificados abaixo.

## Windows:
``` powershell
python -m pip install pillow ffmpeg ffprobe yt-dlp tk
```

## Linux
``` bash
pip3 install pillow ffmpeg ffprobe yt-dlp tk
```