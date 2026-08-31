# Valida el JSON de pieza contra el contrato (Seccion 6 de la arquitectura). Fail loudly.
import json
from layout_specs import LAYOUT_TYPES

REQUIRED_BY_LAYOUT = {
    "marco_grande":      ["porcentaje_imagen", "imagen_escena"],
    "marco_grande_portada": ["texto_titulo", "imagen_escena"],
    "marco_grande_cuadrado": ["imagen_escena"],
    "doble_marco":       ["imagen_escena_1", "imagen_escena_2"],
    "etiqueta_colgante": ["texto_cuerpo"],
    "nota_esquina":      ["texto_cuerpo"],
    "ventana_polaroid":  ["imagen_escena"],
    "palabra_acuarela":  ["imagen_final"],
    "tachado":           ["imagen_final"],
    "full_bleed":        ["imagen_escena", "texto_overlay"],
    "solo_texto":        ["texto_cuerpo"],
    "texto_lateral":     ["imagen_escena", "texto_cuerpo"],
}

VALID_ACCENTS = {"cordel_guia", "migas_progreso", None}


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    errors = []
    for key in ("pieza_id", "aspecto", "slides"):
        if key not in cfg:
            errors.append(f"Falta campo raiz obligatorio: {key}")
    if errors:
        raise ValueError("Config invalida:\n" + "\n".join(errors))

    if cfg["aspecto"] not in ("4:5", "9:16"):
        errors.append(f"aspecto debe ser 4:5 o 9:16, recibido: {cfg['aspecto']}")

    for slide in cfg["slides"]:
        n = slide.get("numero", "?")
        layout = slide.get("layout")
        if layout is None:
            errors.append(f"Slide {n}: falta campo layout")
            continue
        if layout not in LAYOUT_TYPES:
            errors.append(f"Slide {n}: layout desconocido: {layout}")
            continue
        if LAYOUT_TYPES[layout] == "D":
            errors.append(f"Slide {n}: {layout} es un acento (Tipo D), no un layout principal — usar campo acento")
            continue
        for req in REQUIRED_BY_LAYOUT.get(layout, []):
            if not slide.get(req):
                errors.append(f"Slide {n} ({layout}): falta campo obligatorio {req}")
        # Tipo A necesita al menos un texto (excepto doble_marco donde es opcional)
        if layout in ("marco_grande", "marco_grande_cuadrado") and not (slide.get("texto_titulo") or slide.get("texto_subtitulo")):
            errors.append(f"Slide {n} ({layout}): requiere texto_titulo o texto_subtitulo")
        acento = slide.get("acento")
        if acento not in VALID_ACCENTS:
            errors.append(f"Slide {n}: acento invalido: {acento}")

    if errors:
        raise ValueError("Config invalida:\n" + "\n".join(errors))
    return cfg


if __name__ == "__main__":
    import sys
    cfg = load_config(sys.argv[1])
    print(f"OK: {cfg['pieza_id']} ({cfg['aspecto']}), {len(cfg['slides'])} slides validados")
