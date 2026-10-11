# Cola de render (GitHub Actions)

Un push de un archivo `*.env` en esta carpeta dispara el workflow `Render video`.
Formato (una variable por linea):

    PIEZA=pza-4.2
    VARIANTE=B-e14
    TAIL_LAST=0.35

`TAIL_LAST` es opcional (cierre B = 0.35, cierre A = 0.05).
Tambien se puede lanzar a mano desde la pestana Actions con "Run workflow".
