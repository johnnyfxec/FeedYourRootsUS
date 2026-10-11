# Cola de render (GitHub Actions)

Un push de un archivo `*.env` en esta carpeta dispara el workflow `Render video`.
Formato (una variable por linea):

    PIEZA=pza-4.2
    VARIANTE=B-e14
    TAIL_LAST=0.35

`TAIL_LAST` es opcional (cierre B = 0.35, cierre A = 0.05).
Tambien se puede lanzar a mano desde la pestana Actions con "Run workflow".

## Carruseles (workflow `Assemble carousel`)

Un push de un archivo `*.env` en `production/queue/carousel/` (o "Run workflow" a mano) baja de Drive las
imagenes que pide el config, corre `assemble/main.py` y deja los PNG como artefacto (7 dias).

    PIEZA=PZA_1.2
    FOLDER_ID=<ID de la carpeta de fecha en Drive, PZA_x.y/AAAA-MM-DD>

El config de la pieza va en `production/queue/carousel/<PIEZA>.json` (misma estructura que el de `assemble.py`).
Las imagenes se buscan por nombre dentro de `FOLDER_ID`; los marcos y layouts fijos salen del repo (`production/assets_local/`).
