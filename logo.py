"""Recrea el logo de Cabañas 4 Elementos en SVG (f/logo.svg).

El texto sale de Alfa Slab One (OFL) convertido a trazos: el SVG no depende
de ninguna fuente instalada. La ilustración y los glifos están dibujados a mano
sobre el original (rombo ocre, mitad inferior llena con tierra/agua/aire/fuego).
Uso: python logo.py  (requiere fonttools)
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = Path(__file__).parent
FONT = TTFont(ROOT / "_media/fonts/AlfaSlabOne.ttf")
CMAP, GLYPHS, HMTX = FONT.getBestCmap(), FONT.getGlyphSet(), FONT["hmtx"]
CAP = 700  # alto de mayúscula aproximado en unidades de la fuente (UPM 1000)

OCRE = "#B27314"
CREMA = "#F4EEDC"
GRIS = "#7C7770"


def text_path(txt, cx, baseline, width, track=40):
    """Devuelve (d, alto) del texto centrado en cx, estirado a `width` px de ancho."""
    advances = [HMTX[CMAP[ord(ch)]][0] + track for ch in txt]
    raw_w = sum(advances) - track
    s = width / raw_w
    x = cx - width / 2
    pen = SVGPathPen(GLYPHS)
    for ch, adv in zip(txt, advances):
        if ch != " ":
            # la fuente crece hacia arriba; el SVG hacia abajo → escala y negativa
            GLYPHS[CMAP[ord(ch)]].draw(TransformPen(pen, (s, 0, 0, -s, x, baseline)))
        x += adv * s
    return pen.getCommands(), CAP * s


def lines():
    out = []
    for txt, base, w in (("CABAÑAS", 256, 292), ("4 ELEMENTOS", 306, 432), ("HUACALERA JUJUY", 340, 418)):
        d, _ = text_path(txt, 300, base, w)
        out.append(d)
    return out


ILUSTRACION = f"""
  <g class="lg-illus" fill="none" stroke="{OCRE}" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="330" cy="104" r="19" fill="{OCRE}" stroke="none"/>
    <path d="M200 184 L246 132 L258 142 L296 92 L314 114 L326 104 L376 160 L400 184" fill="#fff" stroke-width="4.5"/>
    <path d="M283 110 L296 124 L304 112 M318 118 L326 128" stroke-width="3.5"/>
    <path d="M228 174 L240 128 L252 174 Z M232 158 H248 M235 144 H245" fill="{OCRE}" stroke-width="2"/>
    <path d="M352 164 L362 124 L372 164 Z M355 150 H369 M357 138 H367" fill="{OCRE}" stroke-width="2"/>
    <path d="M262 166 L300 134 L340 166" stroke-width="8"/>
    <path d="M272 166 V180 H328 V166" fill="#fff" stroke-width="4"/>
    <rect x="292" y="164" width="12" height="10" fill="{OCRE}" stroke="none"/>
    <path d="M330 164 L350 148 L370 164" stroke-width="7"/>
    <rect x="344" y="162" width="10" height="9" fill="{OCRE}" stroke="none"/>
    <path d="M196 196 Q300 176 404 196" stroke-width="5"/>
    <path d="M214 206 Q300 192 386 206 Q300 200 214 206 Z" fill="{OCRE}" stroke-width="3"/>
    <path d="M238 214 Q300 207 362 214" stroke-width="3"/>
  </g>"""

# Glifos blancos sobre la mitad ocre: árbol (tierra), olas (agua), viento (aire), llama (fuego)
GLIFOS = """
  <g class="lg-glyph" fill="#fff">
    <path d="M194 450 V414 M194 432 L182 420 M194 426 L206 412" stroke="#fff" stroke-width="6" stroke-linecap="round" fill="none"/>
    <circle cx="186" cy="396" r="12"/><circle cx="202" cy="392" r="13"/><circle cx="194" cy="380" r="12"/>
    <circle cx="180" cy="408" r="9"/><circle cx="208" cy="406" r="10"/><circle cx="194" cy="404" r="11"/>
  </g>
  <g class="lg-glyph" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round">
    <path d="M254 392 q9 -7 18 0 t18 0 t18 0 t18 0 t18 0"/>
    <path d="M254 406 q9 -7 18 0 t18 0 t18 0 t18 0 t18 0"/>
    <path d="M254 420 q9 -7 18 0 t18 0 t18 0 t18 0 t18 0"/>
  </g>
  <g class="lg-glyph" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round">
    <path d="M362 392 H398 a8 8 0 1 0 -8 -8"/>
    <path d="M356 404 H414 a9 9 0 1 1 -9 9"/>
    <path d="M366 416 H392"/>
  </g>
  <path class="lg-glyph" fill="#fff" d="M300 528 C274 528 262 510 266 490 C269 476 278 468 280 454 C288 462 290 472 290 480 C294 468 300 456 298 438 C314 452 334 474 334 496 C334 516 322 528 300 528 Z M300 520 C312 520 318 512 318 502 C318 492 312 484 306 476 C306 486 302 492 298 496 C296 490 294 486 290 482 C286 490 282 496 282 504 C282 514 290 520 300 520 Z" fill-rule="evenodd"/>"""


def build():
    txt = "".join(
        f'<path class="lg-line" d="{d}" fill="{CREMA}" stroke="{GRIS}" stroke-width="3.2" paint-order="stroke" stroke-linejoin="round"/>'
        for d in lines()
    )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" role="img" aria-labelledby="lg-t">
  <title id="lg-t">Cabañas 4 Elementos · Huacalera, Jujuy</title>
  <defs><clipPath id="lg-abajo"><rect x="0" y="360" width="600" height="240"/></clipPath></defs>
  <path class="lg-frame" d="M300 14 L586 300 L300 586 L14 300 Z" fill="#fff" stroke="{OCRE}" stroke-width="12" stroke-linejoin="miter" pathLength="1"/>
  <g clip-path="url(#lg-abajo)"><path class="lg-fill" d="M300 36 L564 300 L300 564 L36 300 Z" fill="{OCRE}"/></g>
  {ILUSTRACION}
  <g>{txt}</g>
  {GLIFOS}
</svg>
"""
    (ROOT / "f/logo.svg").write_text(svg, encoding="utf-8")
    print("f/logo.svg OK", len(svg) // 1024, "KB")


if __name__ == "__main__":
    build()
