# Dado un nombre de layout, retorna su Tipo (A/B/C/D/BASE) y la funcion
# compositora correspondiente. Punto unico de mapeo layout -> logica.
# Seccion 5.2 de la arquitectura: si se agrega un layout 13, solo se toca
# este archivo + un nuevo modulo en compositors/, nada mas se reescribe.

from layout_specs import LAYOUT_TYPES


class LayoutError(Exception):
    pass


def classify(layout_name):
    """Retorna el Tipo ('A'|'B'|'C'|'D'|'BASE') de un layout.
    Lanza LayoutError si el layout no existe en layout_specs.LAYOUT_TYPES.
    Fail loudly - Seccion 5.3 de la arquitectura."""
    if layout_name not in LAYOUT_TYPES:
        raise LayoutError(f"layout desconocido: {layout_name}")
    return LAYOUT_TYPES[layout_name]


def get_compositor(layout_name):
    """Retorna la funcion compose(slide, aspecto, assets_dir) del modulo
    compositors correcto para este layout. Import perezoso (dentro de la
    funcion) para que cada compositor solo se cargue cuando realmente se usa."""
    tipo = classify(layout_name)

    if tipo == "A":
        from compositors.tipo_a import compose
        return compose
    if tipo == "B":
        from compositors.tipo_b import compose
        return compose
    if tipo == "C":
        from compositors.tipo_c import compose
        return compose
    if tipo == "BASE":
        from compositors.base import compose
        return compose
    if tipo == "D":
        raise LayoutError(
            f"{layout_name} es un acento (Tipo D), no un layout principal — "
            f"no tiene compositor propio, se aplica via compositors/acentos.py "
            f"sobre el resultado de otro layout ya compuesto"
        )
    raise LayoutError(f"Tipo de layout sin compositor asignado: {tipo}")


def get_accent_applier(accent_name):
    """Retorna la funcion apply_accent(canvas, accent_name, aspecto) para
    acentos Tipo D (cordel_guia, migas_progreso). None si no hay acento."""
    if accent_name is None:
        return None
    if LAYOUT_TYPES.get(accent_name) != "D":
        raise LayoutError(f"acento invalido, no es Tipo D: {accent_name}")
    from compositors.acentos import apply_accent
    return apply_accent
