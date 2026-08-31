#!/usr/bin/env python3
# main.py -- Orquestador del motor de ensamblado (Seccion 5.2 de la
# arquitectura). Lee un config JSON de pieza, por cada slide clasifica su
# layout, llama al compositor correspondiente, aplica acento si corresponde,
# y exporta el PNG final. Fail loudly segun la tabla de la Seccion 5.3.

import os
import sys
from PIL import Image

from config_loader import load_config
from layout_classifier import classify, get_compositor, get_accent_applier, LayoutError
from layout_specs import CANVAS, PARCHMENT
from compositors.tipo_a import CompositorError as ErrorA
from compositors.tipo_b import CompositorError as ErrorB
from compositors.tipo_c import CompositorError as ErrorC
from compositors.base import CompositorError as ErrorBase
from compositors.acentos import AccentError

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DEFAULT_ASSETS_DIR = os.path.join(REPO_ROOT, "production", "assets_local")
DEFAULT_OUTPUT_DIR = os.path.join(REPO_ROOT, "production", "output")

CompositorErrors = (ErrorA, ErrorB, ErrorC, ErrorBase, AccentError, LayoutError)


def _hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def assemble_slide(slide, aspecto, assets_dir):
    w = CANVAS[aspecto]["w"]
    h = CANVAS[aspecto]["h"]
    canvas = Image.new("RGBA", (w, h), _hex_to_rgb(PARCHMENT) + (255,))

    layout = slide.get("layout")
    compositor = get_compositor(layout)
    result = compositor(canvas, slide, aspecto, assets_dir)
    warnings = list(result.get("warnings", []))

    if "canvas" in result:
        canvas = result["canvas"]

    acento = slide.get("acento")
    if acento:
        applier = get_accent_applier(acento)
        accent_result = applier(canvas, acento, aspecto, assets_dir)
        warnings.extend(accent_result.get("warnings", []))

    return canvas, warnings


def assemble_pieza(config_path, assets_dir=None, output_dir=None, version=1, skip_asset_check=False):
    cfg = load_config(config_path)
    pieza_id = cfg["pieza_id"]
    aspecto = cfg["aspecto"]

    assets_dir = assets_dir or DEFAULT_ASSETS_DIR
    output_dir = output_dir or os.path.join(DEFAULT_OUTPUT_DIR, pieza_id)
    os.makedirs(output_dir, exist_ok=True)

    if not skip_asset_check:
        from image_fetcher import check_assets
        check = check_assets(config_path, assets_dir)
        if not check["listo_para_ensamblar"]:
            faltantes = check["layout_assets_faltantes"] + check["escenas_faltantes"]
            nombres = [f.get("filename", "?") for f in faltantes]
            raise FileNotFoundError(
                f"Assets faltantes antes de ensamblar {pieza_id}: {nombres}. "
                f"Corre image_fetcher.py para el detalle completo de donde buscarlos, "
                f"o usa skip_asset_check=True si ya los verificaste por otra via."
            )

    all_warnings = []
    errors = []
    exported = []

    for slide in cfg["slides"]:
        numero = slide.get("numero", "?")
        layout = slide.get("layout")
        try:
            canvas, warnings = assemble_slide(slide, aspecto, assets_dir)
        except CompositorErrors as e:
            errors.append(f"Slide {numero} ({layout}): {e}")
            print(f"  ✗ Slide {numero} ({layout}): ERROR — {e}")
            continue

        filename = f"{pieza_id}_S{numero}_v{version}.png"
        out_path = os.path.join(output_dir, filename)
        canvas.save(out_path)
        exported.append(out_path)

        status = "✓" if not warnings else "⚠"
        print(f"  {status} Slide {numero} ({layout}) -> {filename}")
        for w in warnings:
            print(f"      advertencia: {w}")
        all_warnings.extend(f"Slide {numero}: {w}" for w in warnings)

    print()
    print(f"Pieza {pieza_id}: {len(exported)}/{len(cfg['slides'])} slides exportados a {output_dir}")
    if all_warnings:
        print(f"Advertencias ({len(all_warnings)}):")
        for w in all_warnings:
            print(f"  - {w}")
    if errors:
        print(f"Errores ({len(errors)}) -- estos slides NO se generaron:")
        for e in errors:
            print(f"  - {e}")

    return {"exported": exported, "warnings": all_warnings, "errors": errors}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 main.py ruta/al/config.json [assets_dir] [output_dir]")
        sys.exit(1)

    config_path = sys.argv[1]
    assets_dir = sys.argv[2] if len(sys.argv) > 2 else None
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None

    result = assemble_pieza(config_path, assets_dir, output_dir)
    sys.exit(1 if result["errors"] else 0)
