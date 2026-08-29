# Fuente de verdad humana: knowledge/reference_assets/FYR_Layout_Specs_v1.md
# Este modulo replica esas medidas como constantes. Si cambia el .md, cambia esto tambien.

CANVAS = {
    "4:5":  {"w": 1080, "h": 1350},
    "9:16": {"w": 1080, "h": 1920},
}

# Zona segura (fracciones del alto)
SAFE_HARD = {"top": 0.125, "bottom": 0.833}
SAFE_PRACTICAL = {"top": 0.152, "bottom": 0.865}

# Assets fijos: nombre de archivo por layout y aspecto
ASSETS = {
    "marco_grande": {
        "4:5": "FYR_ASSET_marco-madera_4x5_v1.png",
        "9:16": "FYR_ASSET_marco-madera_9x16_v1.png",
    },
    "doble_marco": {
        "4:5": "FYR_LAYOUT_doble-marco_4x5_v1.png",
        "9:16": "FYR_LAYOUT_doble-marco_9x16_v1.png",
    },
    "etiqueta_colgante": {
        "4:5": "FYR_LAYOUT_etiqueta-colgante_4x5_v1.png",
        "9:16": "FYR_LAYOUT_etiqueta-colgante_9x16_v1.png",
    },
    "nota_esquina": {
        "4:5": "FYR_LAYOUT_nota-esquina_4x5_v1.png",
        "9:16": "FYR_LAYOUT_nota-esquina_9x16_v1.png",
    },
    "ventana_polaroid": {
        "4:5": "FYR_LAYOUT_ventana-polaroid_4x5_v1.png",
        "9:16": "FYR_LAYOUT_ventana-polaroid_9x16_v1.png",
    },
    "cordel_guia": {
        "4:5": "FYR_LAYOUT_cordel-guia_4x5_v1.png",
        "9:16": "FYR_LAYOUT_cordel-guia_9x16_v1.png",
    },
    "migas_progreso": {
        "4:5": "FYR_LAYOUT_migas-progreso_4x5_v1.png",
        "9:16": "FYR_LAYOUT_migas-progreso_9x16_v1.png",
    },
}

# Ventanas interiores transparentes (px sobre el asset a escala nativa)
WINDOWS = {
    "marco_grande": {
        "4:5":  {"x": 59, "y": 59, "w": 963, "h": 1232, "asset_w": 1080, "asset_h": 1350},
        "9:16": {"x": 72, "y": 66, "w": 938, "h": 1788, "asset_w": 1080, "asset_h": 1920},
    },
    "ventana_polaroid": {
        "4:5":  {"x": 358, "y": 453, "w": 370, "h": 378},
        "9:16": {"x": 333, "y": 702, "w": 413, "h": 420},
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
    # Etiqueta y nota tambien estan rotadas -- medido con medidor_esquinas.html
    # (dos mediciones independientes en 4:5, promediadas para el angulo final).
    # El texto debe rotarse al mismo angulo antes de pegarse, igual que las
    # imagenes de doble_marco.
    "etiqueta_colgante": {
        "4:5":  {"w": 275.4, "h": 347.9, "angle": 11.98, "cx": 742.2, "cy": 898.7},
        "9:16": {"w": 330.9, "h": 411.3, "angle": 10.77, "cx": 762.4, "cy": 1233.3},
    },
    "nota_esquina": {
        "4:5":  {"w": 337.0, "h": 327.7, "angle": 12.08, "cx": 666.6, "cy": 928.0},
        "9:16": {"w": 412.8, "h": 373.8, "angle": 11.66, "cx": 690.7, "cy": 1257.3},
    },
}

# Bounding boxes del contenido opaco (px, escala nativa del asset)
BBOX = {
    "etiqueta_colgante": {
        "4:5":  {"x0": 555, "y0": 160, "x1": 931, "y1": 1141},
        "9:16": {"x0": 541, "y0": 344, "x1": 987, "y1": 1515},
    },
    "nota_esquina": {
        "4:5":  {"x0": 410, "y0": 581, "x1": 924, "y1": 1189},
        "9:16": {"x0": 390, "y0": 854, "x1": 986, "y1": 1556},
    },
    "doble_marco": {
        "4:5":  {"x0": 58, "y0": 86, "x1": 1011, "y1": 1273},
        "9:16": {"x0": 54, "y0": 368, "x1": 1021, "y1": 1556},
    },
    "migas_progreso": {
        "4:5":  {"x0": 95, "y0": 608, "x1": 984, "y1": 759},
        "9:16": {"x0": 74, "y0": 890, "x1": 1002, "y1": 1047},
    },
}

# Zonas de texto Tipo B (fraccion relativa al bbox del asset — primer criterio, Seccion 7 del doc)
# w_frac/h_frac: fraccion del rectangulo ROTATED_WINDOWS asignada al texto.
# El rectangulo medido con medidor_esquinas.html ya excluye el ojal/cordel
# (la medicion empezo justo debajo de esa zona) -- es 100% zona segura, asi
# que la fraccion solo deja el margen estetico minimo (8%), no un margen
# de seguridad extra contra superposicion que no existe.
TEXT_ZONES_TYPE_B = {
    "etiqueta_colgante": {"w_frac": 0.85, "h_frac": 0.85},
    "nota_esquina": {"w_frac": 0.85, "h_frac": 0.85},
}

# Tipografia — roles (Seccion 3 de la arquitectura). Tamanos identicos en ambos aspectos.
import os

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(_THIS_DIR, "..", "..", ".."))
FONTS_DIR = os.path.join(REPO_ROOT, "production", "fonts")
TYPOGRAPHY = {
    "titulo":    {"font": "SourceSerifPro-Regular.ttf", "size": 93, "color": "#E8B84B", "stroke": "#5C3A1E", "stroke_w": 6},
    "subtitulo": {"font": "Lora.ttf", "size": 28, "color": "#5C3A1E", "stroke": None, "stroke_w": 0},
    "cuerpo":    {"font": "Lora.ttf", "size": 40, "color": "#5C3A1E", "stroke": None, "stroke_w": 0},
    "cta":       {"font": "DMSans.ttf", "size": 32, "color": "#5C3A1E", "stroke": None, "stroke_w": 0},
}

PARCHMENT = "#F5ECD7"
OVERLAY_ALPHA = 235  # ~92% opacidad para franja full-bleed

# Clasificacion de layouts (Seccion 0 de la arquitectura)
LAYOUT_TYPES = {
    "marco_grande": "A",
    "doble_marco": "A",
    "etiqueta_colgante": "B",
    "nota_esquina": "B",
    "ventana_polaroid": "B",
    "palabra_acuarela": "C",
    "tachado": "C",
    "cordel_guia": "D",
    "migas_progreso": "D",
    "full_bleed": "BASE",
    "solo_texto": "BASE",
    "texto_lateral": "BASE",
}
