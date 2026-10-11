# Dado un nombre de layout, retorna su Tipo (A/BASE) y la funcion
# compositora correspondiente. Punto unico de mapeo layout -> logica.
# Seccion 5.2 de la arquitectura: si se agrega un layout 13, solo se toca
# este archivo + un nuevo modulo en compositors/, nada mas se reescribe.

from layout_specs import LAYOUT_TYPES


class LayoutError(Exception):
    pass


def classify(layout_name):
    """Retorna el Tipo ('A'|'BASE') de un layout.
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
    if tipo == "BASE":
        from compositors.base import compose
        return compose
    raise LayoutError(f"Tipo de layout sin compositor asignado: {tipo}")
