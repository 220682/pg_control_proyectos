# Protocolo de migraciones y credenciales

Lo leen solo los Workers cuya tanda tiene migraciones (F1-B, F2-A, F3-B, F4-A) y el Worker de verificación en vivo (F5-B). Autorizado por Victor el 2026-09-30: **los Workers aplican las migraciones de su rango**; Victor ya dejó las credenciales. Si no se pueden usar, el Worker se detiene y avisa; no improvisa.

## Qué se aplica y en qué orden

La base de datos es una sola y las migraciones no dependen entre sí. Se aplican **de una en una**, de la menos a la más delicada:

| Orden | Carril | Migraciones | Por qué en ese lugar |
|---|---|---|---|
| 1 | Paquetes (F2-A) | 079 a 081 | Solo tablas y columnas nuevas |
| 2 | RDT (F4-A) | 082 a 084 | Columnas nuevas nulas en tablas de RDT |
| 3 | Niveles (F1-B) | 073 a 075 | Reemplaza la función `reemplazar_dp`, que la app usa hoy |
| 4 | Plan Maestro (F3-B) | 076 a 078 | Relaja la restricción de WBS único (autorizado por Victor: una partida se puede repetir) |

La integración (F5-A) espera a que las cuatro estén aplicadas y verificadas; consta en los `resultados/<tanda>.md`.

## Candado: una migración a la vez

Varios Workers pueden terminar a la vez. Antes de aplicar, crea el archivo `resultados/CANDADO-MIGRACIONES.txt` (en esta carpeta, con el comando `set -o noclobber; echo "<tanda> <hora>" > …`): si ya existe, **no apliques**; sigue con otros ítems y vuelve a intentar al final de tu tanda. Bórralo al terminar, aunque falle. Si el candado tiene más de 30 minutos, no lo rompas: avisa al Orquestador.

## Antes de aplicar cada archivo

1. Comprueba la conexión con una consulta trivial (`select 1`).
2. Comprueba que el archivo es **aditivo e idempotente**: solo `create table if not exists`, `add column if not exists`, `create or replace function` con la **misma firma**; nada de borrar ni renombrar tablas o columnas, ni `delete`/`update` de datos. Única excepción: la relajación de la restricción de WBS único en 076 a 078.
3. Anota los conteos de filas de las tablas que toca (por ejemplo `dp_partidas`, `plan_maestro_partidas`, `rdt_actividad_partidas`, `paquetes_trabajo`).
4. Si el archivo tiene otra cosa, **detente** y avisa.

## Cómo aplicar (sin exponer credenciales)

- Fuente: la carpeta `C:\Users\BRANDY\Downloads\DIARIO`, archivo `entorno_variable.txt`. Nombres de variable: `PR_DB_URL` (conexión directa) y `SUPABASE_ACCESS_TOKEN` (API de administración). El `.env.local` de la app **no sirve**: solo trae URL y llaves REST, que no crean tablas.
- Un script de un solo uso (Python con `psycopg2`, ya instalado en esta máquina), guardado **fuera del repositorio** (carpeta temporal de la sesión) y **borrado al terminar**. Lee el valor de la variable dentro del proceso; **no lo imprime, no lo pasa como argumento de línea de comandos** y limpia los mensajes de error antes de mostrarlos.
- **Nunca abras, muestres ni copies** `entorno_variable.txt`: ni `cat`, ni `grep` con valores, ni lo pegues en un resultado, brief, log, captura o commit. Solo se usan los nombres.
- Cada archivo va **dentro de una transacción**: si falla, se revierte solo.
- **Vía alterna**, solo si la directa es inalcanzable (antecedente de IPv6 en `docs/03-aprendizaje-continuo/2026-09-21-acceso-postgres-sin-ipv6.md`): la API de administración de Supabase con `SUPABASE_ACCESS_TOKEN`; el identificador del proyecto sale de la parte inicial de `NEXT_PUBLIC_SUPABASE_URL`, que no es secreta.

## Después de aplicar

1. Comprueba con consultas que la tabla o columna existe y que `reemplazar_dp` (si la tocaste) tiene **una sola** firma, sin sobrecargas huérfanas.
2. Compara los conteos de antes y después: los datos existentes **no cambian**.
3. Anota en tu `resultados/<tanda>.md`: archivo, vía usada (directa o API), hora, verificación y resultado, conteos antes y después. **Sin ningún valor secreto.**
4. Borra el script temporal y el candado. Comprueba con `git status` que no quedó nada con credenciales.
5. Cada migración incluye, al final, un comentario con cómo deshacerla. **No se ejecuta** sin autorización de Victor.

## Detente y avisa (no improvises) si

- No ves las credenciales o ninguna vía conecta: escribe «no veo las credenciales» o «ninguna vía conecta» en tu resultado y avisa al Orquestador, que avisa a Victor.
- La migración falla, la verificación no coincide o hace falta borrar, renombrar o cambiar datos existentes.
- Alguien más tiene el candado y no se libera.

No busques otras credenciales, no uses la llave de servicio REST para forzar cambios de estructura y no toques datos de ningún servicio que no sea el de prueba del plan.
