# Fuente de verdad humana: knowledge/reference_assets/FYR_Layout_Specs_v1.md
# Este modulo replica esas medidas como constantes. Si cambia el .md, cambia esto tambien.

CANVAS = {
    "4:5":  {"w": 1080, "h": 1350},
    "9:16": {"w": 1080, "h": 1920},
}

# Zona segura (fracciones del alto)
SAFE_HARD = {"top": 0.125, "bottom": 0.833}
SAFE_PRACTICAL = {"top": 0.152, "bottom": 0.865}

# Margen minimo puramente estetico para 4:5 -- NO es zona de seguridad.
# El 4:5 (carrusel de feed) no tiene reproductor de video recortando nada,
# a diferencia del 9:16 (reel) donde SAFE_PRACTICAL protege contra la UI
# de la app. El 4:5 debe verse en el feed como el equivalente visual de lo
# que se ve garantizado en un 9:16 -- por eso usa casi el 100% del canvas,
# solo con un margen de aire minimo, no el SAFE_PRACTICAL del video.
SAFE_MINIMAL_4X5 = {"top": 0.03, "bottom": 0.97}


# Recorte de la cuadrilla de perfil de Instagram (11-oct-2026): una portada
# 4:5 (1080x1350) se muestra en 3:4 (1080x1440) y pierde ~34 px por lado
# (33.75), sin recorte vertical. Todo lo clave de la PORTADA 4:5 (titulo,
# marco, logo) debe quedar a >= LATERAL_PORTADA_4X5["objetivo"] del borde.
# No aplica a slides secundarias (la cuadricula solo muestra la portada).
# La cuadricula de reels (3:4 sobre 9:16) recorta 240 px arriba y abajo, que
# coincide con SAFE_HARD (12.5%) -- ya cubierto por la zona segura de 9:16.
LATERAL_PORTADA_4X5 = {"duro": 34, "objetivo": 48}


def usable_zone(aspecto):
    """Devuelve (margen_top_px, margen_bottom_px, alto_util_px) segun el
    aspecto. 4:5 usa SAFE_MINIMAL_4X5 (casi el canvas completo); 9:16 usa
    SAFE_PRACTICAL (proteccion real contra recorte de UI de reels)."""
    h = CANVAS[aspecto]["h"]
    margins = SAFE_MINIMAL_4X5 if aspecto == "4:5" else SAFE_PRACTICAL
    top = h * margins["top"]
    bottom = h * margins["bottom"]
    return top, bottom, bottom - top

# Assets fijos: nombre de archivo por layout y aspecto
ASSETS = {
    "marco_grande": {
        "4:5": "FYR_ASSET_marco-madera_4x5_v1.png",
        "9:16": "FYR_ASSET_marco-madera_9x16_v1.png",
    },
    # marco_grande_portada reutiliza el mismo archivo fisico que marco_grande
    # (ver tipo_a.py::_compose_marco_grande_portada, que llama
    # _load_asset("marco_grande", ...) -- solo cambia el escalado, no el
    # asset). Entrada duplicada aqui a proposito: si una pieza usa
    # marco_grande_portada sin ningun slide marco_grande, el verificador de
    # image_fetcher.py._required_layout_assets() (que filtra por `layout in
    # ASSETS`) debe poder detectar igual que falta el archivo antes del
    # ensamblado, en vez de fallar recien en tipo_a.py.
    "marco_grande_portada": {
        "4:5": "FYR_ASSET_marco-madera_4x5_v1.png",
        "9:16": "FYR_ASSET_marco-madera_9x16_v1.png",
    },
    "marco_grande_cuadrado": {
        # Solo 9:16 -- portadas de reel/video, ventana 1:1 real por diseno
        # (a diferencia de marco_grande, que es rectangular alto). El 4:5
        # sigue usando marco_grande normal (Seccion 0, decision de Johnny:
        # 4:5 vertical / 9:16 cuadrado como default de portada de marca).
        "9:16": "FYR_ASSET_marco-cuadrado_9x16_v1.png",
    },
    "doble_marco": {
        "4:5": "FYR_LAYOUT_doble-marco_4x5_v1.png",
        "9:16": "FYR_LAYOUT_doble-marco_9x16_v1.png",
    },
}

# Ventanas interiores transparentes (px sobre el asset a escala nativa)
WINDOWS = {
    "marco_grande": {
        "4:5":  {"x": 59, "y": 59, "w": 963, "h": 1232, "asset_w": 1080, "asset_h": 1350},
        "9:16": {"x": 72, "y": 66, "w": 938, "h": 1788, "asset_w": 1080, "asset_h": 1920},
    },
    "marco_grande_cuadrado": {
        # Medido con medidor_esquinas.html sobre el asset real v2 (con vid
        # y hoja integrados, lienzo completo 1080x1920). Ventana casi
        # cuadrada (722x727.8), angulo -0.23 (ruido de medicion).
        "9:16": {"x": 179.4, "y": 320.3, "w": 722.0, "h": 727.8, "asset_w": 1080, "asset_h": 1920},
    },
}


# Ventanas rotadas (doble_marco): a diferencia de WINDOWS, estas no son
# rectangulos alineados a los ejes -- cada marco esta rotado, por lo que se
# describen como centro + ancho/alto + angulo de rotacion (grados, sentido
# antihorario positivo segun convencion de PIL Image.rotate). Medido a mano
# con production/scripts/tools/medidor_esquinas.html tocando las 4 esquinas
# reales de cada ventana -- lados opuestos verificados consistentes en
# longitud y angulo (diferencia < 0.25 grados), no son valores teoricos.
ROTATED_WINDOWS = {
    "doble_marco": {
        "4:5": {
            "trasero":  {"w": 434.8, "h": 584.4, "angle": -8.47, "cx": 349.1, "cy": 441.8},
            "frontal":  {"w": 448.0, "h": 588.0, "angle": 10.89, "cx": 702.6, "cy": 907.6},
        },
        "9:16": {
            "trasero":  {"w": 439.9, "h": 598.1, "angle": -8.70, "cx": 347.7, "cy": 721.3},
            "frontal":  {"w": 451.8, "h": 589.3, "angle": 10.93, "cx": 704.0, "cy": 1193.1},
        },
    },
}

# Bounding boxes del contenido opaco (px, escala nativa del asset)
BBOX = {
    "doble_marco": {
        "4:5":  {"x0": 58, "y0": 86, "x1": 1011, "y1": 1273},
        "9:16": {"x0": 54, "y0": 368, "x1": 1021, "y1": 1556},
    },
}

# Tipografia — roles (Seccion 3 de la arquitectura). Tamanos identicos en ambos aspectos.
import os

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(_THIS_DIR, "..", "..", ".."))
FONTS_DIR = os.path.join(REPO_ROOT, "production", "fonts")
TYPOGRAPHY = {
    "titulo":    {"font": "SourceSerifPro-Regular.ttf", "size": 93, "color": "#E8B84B", "stroke": "#5C3A1E", "stroke_w": 5, "line_spacing": 0.743},
    "subtitulo": {"font": "Lora-BoldItalic.ttf", "size": 47, "color": "#1A1A1A", "stroke": None, "stroke_w": 0, "line_spacing": 0.777},
    "cuerpo":    {"font": "Lora.ttf", "size": 40, "color": "#5C3A1E", "stroke": None, "stroke_w": 0},
    "cta":       {"font": "DMSans.ttf", "size": 32, "color": "#5C3A1E", "stroke": None, "stroke_w": 0},
}

PARCHMENT = "#F5ECD7"
OVERLAY_ALPHA = 235  # ~92% opacidad para franja full-bleed

# Clasificacion de layouts (Seccion 0 de la arquitectura)
LAYOUT_TYPES = {
    "marco_grande": "A",
    "marco_grande_cuadrado": "A",
    "marco_grande_portada": "A",
    "doble_marco": "A",
    "full_bleed": "BASE",
    "ventana_texto": "BASE",
    "solo_texto": "BASE",
    "texto_lateral": "BASE",
    "lockup_cierre": "BASE",
}

# Anchos medidos para marco_grande_portada (Slide 1/cierre en 4:5, sin
# subtitulo). Medido con medidor_esquinas.html sobre el mockup real de
# portada 9:16 -- el criterio de Johnny es que el ancho de marco+texto en
# 4:5 replica el mismo ancho absoluto que en la portada 9:16, ya que ambos
# canvas comparten el mismo ancho total (1080px).
PORTADA_WIDTHS = {
    "4:5": {"marco_w": 808, "texto_w": 898},
}
