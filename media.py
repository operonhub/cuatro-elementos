"""Procesa el material de la clienta (_media/raw) → f/ listo para la web.

Fotos: WebP con nombre según lo que muestran (los nombres de archivo de la
clienta indican cabaña/espacio). Videos: H.264 recomprimido + póster.
Uso: python media.py   (requiere Pillow y ffmpeg en el PATH)
"""
import subprocess
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).parent
RAW = ROOT / "_media/raw"
OUT = ROOT / "f"

FOTOS = {
    # las cuatro cabañas (nombre dado por la clienta)
    "cabanas__cabana-tierra.jpeg": "cab-tierra",
    "cabanas__cabanas-agua.jpeg": "cab-agua",
    "cabanas__cabana-fuego.jpeg": "cab-fuego",
    "cabanas__cabana-aire.jpeg": "cab-aire",
    # el complejo
    "cabanas__wa23-at-1.4.jpeg": "complejo-atardecer",
    "cabanas__wa23-at-1.48.07-pm.jpeg": "complejo-dorado",
    "fotos__espacios-para-compartir.jpeg": "espacios-compartir",
    "fotos__estacionamiento.jpeg": "cardon-piedra",
    "fotos__galeria.jpeg": "galeria-mesa",
    "fotos__wa23-at-1.51.19-pm.jpeg": "galeria-remoto",
    "fotos__wa23-at-1.51.20-pm.jpeg": "pergola-patio",
    # la mesa de Lili (desayuno, salón desayunador)
    "fotos__la-mesa-de-lili.jpeg": "desayuno-ventana",
    "fotos__la-mesa-de-lili-2.jpeg": "desayuno-mesa",
    "salon-desayunador__2.jpeg": "salon-desayunador",
    "salon-desayunador__4.jpeg": "salon-ventana",
    "salon-desayunador__6.jpeg": "desayuno-detalle",
    # el fuego de Luis (comedor y pérgola con parrillas)
    "fotos__wa22-at-2.02.3.jpeg": "asado-estaca",
    "fotos__wa22-at-2.02.33-pm.jpeg": "disco",
    "fotos__quincho.jpeg": "comedor-quincho",
    "fotos__wa22-a.jpeg": "comedor-largo",
    "fotos__wa22-at-2.02.32-pm.jpeg": "comedor-aguayo",
    "fotos__wa22-at-2.02.31-pm.jpeg": "comedor-mesas",
}

VIDEOS = {
    "videos__wa22-at-2.00.35-pm.mp4": ("v-complejo", 20),
    "videos__wa22-at-2.00.35.mp4": ("v-tropico", 5),
    "videos__wa22-at-2.00.36-pm.mp4": ("v-noche", 5),
}


def foto(src, name, max_side=1600, q=80):
    im = ImageOps.exif_transpose(Image.open(RAW / src)).convert("RGB")
    im.thumbnail((max_side, max_side), Image.LANCZOS)
    dst = OUT / f"{name}.webp"
    im.save(dst, "WEBP", quality=q, method=6)
    return dst, im.size


def video(src, name, poster_t):
    dst = OUT / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(RAW / src),
                    "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2", "-c:v", "libx264", "-preset", "slow",
                    "-crf", "30", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k",
                    "-movflags", "+faststart", str(dst)], check=True)
    jpg = OUT / f"{name}.jpg"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(poster_t), "-i", str(RAW / src),
                    "-frames:v", "1", str(jpg)], check=True)
    im = Image.open(jpg).convert("RGB")
    im.save(OUT / f"{name}.webp", "WEBP", quality=78, method=6)
    jpg.unlink()
    return dst


if __name__ == "__main__":
    for src, name in FOTOS.items():
        dst, size = foto(src, name)
        print(f"{dst.name:28} {size[0]}x{size[1]}  {dst.stat().st_size // 1024} KB")
    for src, (name, t) in VIDEOS.items():
        dst = video(src, name, t)
        print(f"{dst.name:28} {dst.stat().st_size // 1024} KB")
