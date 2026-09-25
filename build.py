"""Genera index.html: src.html + widget REAL de Operon Reservas, tematizado + logo inline.

El widget se pega tal cual desde la skill web-hustler; solo se completa su CONFIG
(ORG_SLUG y WA_NUMBER) y se pisa la paleta con un <style> posterior (nunca su CSS).
Unidades, tarifas y disponibilidad salen del backend central (tenant ORG_SLUG),
dado de alta con provision-tenant.sql.
"""
from pathlib import Path

ROOT = Path(__file__).parent
ASSET = Path.home() / ".claude/skills/web-hustler/assets/booking-widget.html"

ORG_SLUG = "cabanas-4-elementos"
WA_NUMBER = "5493885186442"

widget = ASSET.read_text(encoding="utf-8")

CONFIG_OLD = (
    "    ORG_SLUG:     'CAMBIAR-por-el-slug-del-cliente',   // <<< cambiar\n"
    "    WA_NUMBER:    '549XXXXXXXXXX',                      // <<< cambiar (sin +, sin espacios)"
)
for old in (CONFIG_OLD, "<h3>Reservá online</h3>"):
    assert old in widget, f"El asset cambió, no encuentro: {old[:40]}"

widget = (widget
    .replace(CONFIG_OLD, f"    ORG_SLUG:     '{ORG_SLUG}',\n    WA_NUMBER:    '{WA_NUMBER}',")
    .replace("<h3>Reservá online</h3>", "<h3>Elegí tus fechas</h3>"))

THEME = """
<style>
  .bkw{
    --bkw-primary:#0B7A68;   /* = CTA primario (turquesa de las sillas) */
    --bkw-accent:#8A6A12;    /* = ocre hondo: seña y bordes en hover */
    --bkw-bg:#FFFFFF;        /* inputs: se despegan del fondo cal de la tarjeta */
    --bkw-bg-2:#E8E4DB;
    --bkw-text:#25221F;
    --bkw-text-soft:#5B554E;
    --bkw-white:#FFFFFF;     /* texto sobre el turquesa: 5,3:1 */
    --bkw-line:rgba(37,34,31,.18);
    --bkw-radius:6px;
    --bkw-font-display:'Barlow Condensed', system-ui, sans-serif;
    --bkw-font-body:'Barlow', system-ui, sans-serif;
  }
  .bkw h3,.bkw .bk-unit h4{text-transform:uppercase;letter-spacing:.01em}
  .bkw h3{font-size:1.9rem;font-weight:800;line-height:1}
  .bkw .bk-unit h4{font-size:1.3rem;font-weight:700}
  .bkw .btn-primary{font-family:var(--bkw-font-display);text-transform:uppercase;letter-spacing:.06em;font-size:1.02rem}
  .bkw .field input,.bkw .field select,.bkw .field textarea{border-radius:var(--bkw-radius)}
  .bkw .bk-summary,.bkw .bk-code,.bkw .bk-unit{border-radius:var(--bkw-radius)}
</style>
"""

src = (ROOT / "src.html").read_text(encoding="utf-8")
assert "<!--BOOKING-->" in src and "<!--LOGO-INTRO-->" in src
# la intro anima el logo por partes (.lg-frame, .lg-line, .lg-glyph…): va inline, no como <img>
logo = (ROOT / "f/logo.svg").read_text(encoding="utf-8").replace('role="img"', 'aria-hidden="true"', 1)
(ROOT / "index.html").write_text(
    src.replace("<!--BOOKING-->", widget + THEME).replace("<!--LOGO-INTRO-->", logo),
    encoding="utf-8")
print("index.html OK")
