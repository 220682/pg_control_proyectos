# Comprobar en la base con la tabla correcta, respaldar antes de borrar y probar con el archivo real

**Origen:** plan `2026-10-14-revision-completa-app.md` (mejoras M1 y M2), 2026-10-14 y 2026-10-15. **Categoría:** `verificación` · `datos`.

## 1. «No se guardó nada» se comprueba en la tabla que lee la pantalla

El 2026-10-15, para asegurar que una prueba de Importar DP no había guardado nada, se consultó `dp_cabecera`, una tabla que no existe. El cliente de Supabase devolvió `data: null` con un conteo vacío, y eso se leyó como «0 filas». La tabla real es `proyecto_dp`, la que lee `proyectos/[id]/dp/page.tsx`. Por esa lectura se le dijo a Victor algo falso, y hubo que corregirlo.

- Antes de afirmar que algo está o no en la base, se busca en el código de la pantalla qué tabla lee (`grep "from('"` en su `page.tsx`) y se consulta esa misma tabla.
- `data: null` no significa «cero filas». Se imprime siempre `error` y se trata `null` como una consulta fallida, no como un vacío.

## 2. Antes de borrar en la base: respaldo completo y borrado servicio por servicio

El 2026-10-14, antes de limpiar los servicios de prueba, se respaldaron las 55 tablas completas en JSON y los archivos de storage de cada servicio, y se borró **un servicio a la vez**. El primer intento falló por el orden de las claves foráneas y no borró nada; con el orden corregido, cada servicio se borró por separado. Así, un error deja intactos los demás y se puede reconstruir desde el respaldo.

## 3. Un importador se prueba con los archivos reales de Victor, no solo con los de prueba

Los presupuestos que mandan los clientes cambian de un archivo a otro: `.xls`, la hoja «PS» con o sin espacio al final, el APU de S10 y archivos separados. El 2026-10-15, las pruebas unitarias estaban en verde y aun así la app no leía ninguno de los tres presupuestos reales. Lo que sirvió:

- Pasar los archivos reales por el parser con una prueba temporal de vitest que escribe a un log del scratchpad (vitest no muestra `console.log` en esta configuración) y se borra al terminar.
- Convertir copias con Excel por COM (`Excel.Application`, `SaveAs` formato 51) para separar dos problemas: el formato del archivo y su contenido.
- En la pantalla, probar solo hasta «Confirmar niveles» (`soloAnalizar`), que no guarda nada, y cancelar.
- Separar los errores del propio Excel (códigos que no coinciden entre la hoja de partidas y el APU, bloques repetidos) de los de la app: los primeros se le reportan a Victor y la app no los corrige por su cuenta.
