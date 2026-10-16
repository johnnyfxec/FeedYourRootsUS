#!/usr/bin/env python3
"""Valida la estructura de pieza_X.json ANTES de gastar los ~5-6 min de TTS+render en Actions
(16-oct-2026: el render es ciego hasta el final -- un JSON mal formado solo se descubria al fallar un
paso tardio, o ni eso, si el paso fallaba en silencio). Corre primero en el workflow, sin red: solo
valida forma y contenido local del JSON, no si los IDs de Drive existen de verdad (eso lo sigue haciendo
fetch_assets.mjs, que si necesita red).

Uso: python3 validate_pieza.py <pieza.json>
Sale con exit code != 0 y un mensaje por cada problema encontrado si algo no cuadra.
"""
import json
import re
import sys

REQUERIDOS_RAIZ = ["pieza_id", "medio", "aspecto", "canvas", "voz", "slides"]
REQUERIDOS_SLIDE = ["n", "layout", "asset", "imagen", "texto_narrado"]  # drive_id se valida aparte (acepta null con mensaje especifico)


def main():
    if len(sys.argv) < 2:
        sys.exit("Uso: validate_pieza.py <pieza.json>")
    ruta = sys.argv[1]
    try:
        pieza = json.load(open(ruta, encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"✗ {ruta}: JSON invalido -- {e}")
    except FileNotFoundError:
        sys.exit(f"✗ {ruta}: no existe")

    errores = []

    for campo in REQUERIDOS_RAIZ:
        if campo not in pieza:
            errores.append(f"falta el campo raiz '{campo}'")

    if pieza.get("medio") != "Video":
        errores.append(f"medio='{pieza.get('medio')}', esperaba 'Video'")

    if pieza.get("aspecto") != "9:16":
        errores.append(f"aspecto='{pieza.get('aspecto')}', esperaba '9:16' (unico soportado por el pipeline de video)")

    canvas = pieza.get("canvas", {})
    if canvas.get("w") != 1080 or canvas.get("h") != 1920:
        errores.append(f"canvas={canvas}, esperaba w=1080 h=1920")

    slides = pieza.get("slides", [])
    if not slides:
        errores.append("'slides' esta vacio")
    elif len(slides) < 4 or len(slides) > 8:
        errores.append(f"{len(slides)} slides -- fuera del rango esperado 4-8 (ver fyr-content Paso 3, numero por Fase Embudo)")

    nombres_imagen = set()
    for s in slides:
        n = s.get("n", "?")
        for campo in REQUERIDOS_SLIDE:
            if campo not in s or s[campo] in (None, ""):
                # subtitulos=false es valido (portada); solo texto_narrado y el resto son obligatorios siempre
                if campo == "texto_narrado" and not s.get("texto_narrado", "").strip():
                    errores.append(f"slide {n}: 'texto_narrado' vacio")
                elif campo != "texto_narrado":
                    errores.append(f"slide {n}: falta '{campo}'")

        drive_id = s.get("drive_id")
        if drive_id is None:
            errores.append(f"slide {n}: drive_id es null -- si es el slide de portada, falta terminar B8 "
                            f"(subir la portada compuesta y escribir su ID aqui) antes de poder renderizar")
        elif drive_id and not re.match(r"^[A-Za-z0-9_-]{10,}$", drive_id):
            errores.append(f"slide {n}: drive_id '{drive_id}' no parece un ID de Drive valido")

        imagen = s.get("imagen", "")
        if imagen:
            if imagen in nombres_imagen:
                errores.append(f"slide {n}: ruta de imagen '{imagen}' duplicada con otro slide")
            nombres_imagen.add(imagen)

        texto = s.get("texto_narrado", "")
        if texto:
            abiertos = texto.count("*")
            if abiertos % 2 != 0:
                errores.append(f"slide {n}: numero impar de '*' en texto_narrado (enfasis sin cerrar) -- '{texto[:60]}...'")

    nums = [s.get("n") for s in slides if "n" in s]
    if nums != list(range(1, len(nums) + 1)):
        errores.append(f"los campos 'n' de los slides no son consecutivos desde 1: {nums}")

    if errores:
        print(f"✗ {ruta}: {len(errores)} problema(s), no se dispara el render:")
        for e in errores:
            print(f"  - {e}")
        sys.exit(1)

    print(f"✓ {ruta}: estructura valida ({len(slides)} slides, pieza_id={pieza['pieza_id']}).")


if __name__ == "__main__":
    main()
