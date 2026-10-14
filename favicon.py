"""Genera los favicons reales (raíz del sitio): favicon.svg, favicon.ico, apple-touch-icon.png, icon-192/512.png.

Google no lee favicons incrustados (data:), necesita archivos que pueda descargar,
de un múltiplo de 48 px. El logo completo no se lee a 16 px, así que esto es una
versión reducida: rombo del logo, techo arriba y mitad ocre abajo.
Uso: python favicon.py  (requiere Pillow)
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).parent
OCRE = (178, 115, 20, 255)      # #B27314, el ocre del logo
WHITE = (255, 255, 255, 255)

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">
  <title>Cabañas 4 Elementos</title>
  <path d="M24 1.5L46.5 24L24 46.5L1.5 24Z" fill="#B27314"/>
  <path d="M24 6L42 24L24 42L6 24Z" fill="#fff"/>
  <path d="M9 27H39L24 42Z" fill="#B27314"/>
  <path d="M13 21L24 11L35 21" fill="none" stroke="#B27314" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""


def draw(size, pad=0.0, bg=None):
    """Dibuja el ícono a `size` px (supermuestreado 8x). `pad` = margen relativo; `bg` = fondo opaco."""
    k = size * 8 / 48
    im = Image.new("RGBA", (size * 8, size * 8), bg or (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s = 1 - 2 * pad
    o = size * 8 * pad

    def P(*pts):
        return [(o + x * k * s, o + y * k * s) for x, y in pts]

    d.polygon(P((24, 1.5), (46.5, 24), (24, 46.5), (1.5, 24)), fill=OCRE)
    d.polygon(P((24, 6), (42, 24), (24, 42), (6, 24)), fill=WHITE)
    d.polygon(P((9, 27), (39, 27), (24, 42)), fill=OCRE)
    roof = P((13, 21), (24, 11), (35, 21))
    w = 3.6 * k * s
    d.line(roof, fill=OCRE, width=round(w))
    for x, y in roof:  # puntas y vértice redondeados
        d.ellipse((x - w / 2, y - w / 2, x + w / 2, y + w / 2), fill=OCRE)
    return im.resize((size, size), Image.LANCZOS)


if __name__ == "__main__":
    (ROOT / "favicon.svg").write_text(SVG, encoding="utf-8")
    draw(48).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    draw(192).save(ROOT / "icon-192.png")
    draw(512).save(ROOT / "icon-512.png")
    # iOS no admite transparencia: fondo crema de la web y margen
    draw(180, pad=0.1, bg=(243, 241, 236, 255)).convert("RGB").save(ROOT / "apple-touch-icon.png")
    for n in ("favicon.svg", "favicon.ico", "icon-192.png", "icon-512.png", "apple-touch-icon.png"):
        print(f"{n:22} {(ROOT / n).stat().st_size} B")
