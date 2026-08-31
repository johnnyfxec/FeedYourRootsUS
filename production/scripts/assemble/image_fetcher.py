# image_fetcher.py -- Verificacion de assets, NO descarga directa.
#
# Este script corre en TERMUX o en Claude Code, pero NO descarga nada de
# Google Drive por si mismo -- Termux no tiene acceso automatizado a Drive,
# y meter credenciales de API en un script plano no es el patron correcto.
#
# En su lugar: dado un config JSON de pieza, revisa que campo de imagen
# necesita cada slide (imagen_escena, imagen_final, etc.) mas los assets
# fijos que requiera cada layout, y reporta cuales YA estan en
# assets_local/ y cuales FALTAN -- con la ruta esperada en Drive segun
# FYR_Asset_Governance_Policy.md, para que quien tenga acceso real a Drive
# (hoy: Claude Code via su Drive MCP) sepa exactamente que buscar y donde.
#
# Flujo real de uso: Claude Code corre check_assets(config) ANTES de
# main.py -- si hay faltantes, usa su propio Drive MCP para descargarlos
# a production/assets_local/, y recien despues corre main.py.

import os
import sys

from config_loader import load_config
from layout_specs import ASSETS

DRIVE_PATHS = {
    "layout_asset": "FYR/01_Brand_Assets/C13_Layout_Elements/",
    "marco_asset": "FYR/01_Brand_Assets/C12_Frames/",
    "narrative_stock": "FYR/06_Narrative_Stock/",
}

MARCO_LAYOUTS = {"marco_grande", "marco_grande_portada", "marco_grande_cuadrado"}


class FetchCheckError(Exception):
    pass


def _drive_path_for_layout_asset(layout_name):
    if layout_name in MARCO_LAYOUTS:
        return DRIVE_PATHS["marco_asset"]
    return DRIVE_PATHS["layout_asset"]


def _required_layout_assets(cfg):
    aspecto = cfg["aspecto"]
    needed = set()
    for slide in cfg["slides"]:
        layout = slide.get("layout")
        if layout in ASSETS and aspecto in ASSETS[layout]:
            filename = ASSETS[layout][aspecto]
            needed.add((layout, aspecto, filename))
    return needed


def _required_scenes(cfg):
    scene_fields = ("imagen_escena", "imagen_escena_1", "imagen_escena_2", "imagen_final")
    needed = set()
    for slide in cfg["slides"]:
        for field in scene_fields:
            value = slide.get(field)
            if value:
                needed.add(value)
    return needed


def check_assets(config_path, assets_dir=None):
    cfg = load_config(config_path)

    if assets_dir is None:
        repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        assets_dir = os.path.join(repo_root, "production", "assets_local")

    layout_assets_faltantes = []
    for layout, aspecto, filename in _required_layout_assets(cfg):
        path = os.path.join(assets_dir, filename)
        if not os.path.exists(path):
            layout_assets_faltantes.append({
                "layout": layout,
                "aspecto": aspecto,
                "filename": filename,
                "drive_path_sugerida": _drive_path_for_layout_asset(layout) + filename,
            })

    escenas_faltantes = []
    for filename in _required_scenes(cfg):
        path = os.path.join(assets_dir, filename)
        if not os.path.exists(path):
            escenas_faltantes.append({
                "filename": filename,
                "narrative_stock_path_sugerida": DRIVE_PATHS["narrative_stock"] + filename,
                "nota": "buscar primero en Narrative Stock por nombre exacto; si no existe, es escena nueva -- generar con Gemini antes de continuar",
            })

    listo = not layout_assets_faltantes and not escenas_faltantes

    return {
        "pieza_id": cfg["pieza_id"],
        "aspecto": cfg["aspecto"],
        "layout_assets_faltantes": layout_assets_faltantes,
        "escenas_faltantes": escenas_faltantes,
        "listo_para_ensamblar": listo,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 image_fetcher.py ruta/al/config.json [assets_dir]")
        sys.exit(1)

    config_path = sys.argv[1]
    assets_dir = sys.argv[2] if len(sys.argv) > 2 else None

    result = check_assets(config_path, assets_dir)

    print(f"Pieza: {result['pieza_id']} ({result['aspecto']})")
    print()

    if result["layout_assets_faltantes"]:
        print(f"Assets de layout faltantes ({len(result['layout_assets_faltantes'])}):")
        for item in result["layout_assets_faltantes"]:
            print(f"  - {item['filename']}  <-  {item['drive_path_sugerida']}")
        print()

    if result["escenas_faltantes"]:
        print(f"Escenas faltantes ({len(result['escenas_faltantes'])}):")
        for item in result["escenas_faltantes"]:
            print(f"  - {item['filename']}")
            print(f"      buscar en: {item['narrative_stock_path_sugerida']}")
            print(f"      {item['nota']}")
        print()

    if result["listo_para_ensamblar"]:
        print("✓ Todo disponible -- listo para correr main.py")
    else:
        print("✗ Faltan assets -- resolver antes de correr main.py")

    sys.exit(0 if result["listo_para_ensamblar"] else 1)
