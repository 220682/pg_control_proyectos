# T7fix · Worker 7 (código) · Plan Notificaciones

Rama `local-worker-7` (verificada), parte de `85626fd`. Commit nuevo: `9611338`. Sin navegador, sin push ni merge. No se tocaron `permisos.ts`, migraciones, flujos ni `AGENTS.md`.

## Qué cambió

1. **Cantidad vieja tras reenviar.** `AccionesRqEnNotificacion` recibe `onReenviado` (opcional) y lo llama tras «Corregir y reenviar». `ListaNotificaciones.tsx` (bandeja) y `EntornoTrabajoGrupo.tsx` (Mi entorno) suben un contador por aviso (`versionDetalleRq`) que entra en la clave de `DetalleRqNotificacion`, así «Lo solicitado» se vuelve a pedir. La lista ya se recargaba con `onRefrescar`. No se remontan las acciones (conservan el mensaje «Reenviado…»).
2. **Grupo estable.**
   - `avisos-duplicados.ts`: la tarjeta unificada toma el grupo de la fila cuyo rol es de la persona; si coinciden varias, Jefatura primero (el grupo viejo «Proyecto» cuenta como Jefatura); si ninguna coincide, la primera. Tarjeta de una sola fila no cambia. `AvisoAgrupable` gana `grupo_nav?` opcional.
   - `rq.pendiente_aprobacion` se crea siempre con `grupoNav: GRUPO_JEFATURA` en los dos sitios (`POST requerimientos/route.ts`, solo cuando no es directo a Logística, y `reenviarRq` en `cambiar-estado-rq.ts`). En el catálogo pasa a `grupo: 'indicado'` con nota. No cambió el número de llamadas, así que `SITIOS` de `cobertura-avisos.test.ts` queda igual.
   - Pruebas nuevas en `bandeja-avisos.test.ts` (4: dos roles en ambos órdenes, grupo viejo, roles distintos sin Jefatura, fila sola/sin grupo) y una aserción en `devolver-rq-api.test.ts` (los 3 avisos del reenvío salen con `grupo_nav` Jefatura). Todo con doble de base.
3. **Grupo «Proyecto» → «Jefatura».** `TITULO_GRUPO_PROYECTO` ahora vale `'Jefatura'` y los usos literales en `registro-accesos.ts` pasan a la constante. **Solo cambió el rótulo visible:** la clave interna `notificaciones-proyecto` (matriz base del flujo 14, pruebas) y el slug `proyecto` no se renombraron, porque romperían permisos. Pruebas ajustadas: `nav-proyecto.test.ts`, `registro-accesos.test.ts`, `equivalencia-f1b.test.ts` (el argumento de `herramientasPorGrupo` se ignora, se cambió por coherencia). `registro-humo.test.ts` no dependía del rótulo. Los usos de `'Proyecto'` como grupo viejo de avisos guardados (`grupo-proceso.ts`, sus pruebas y `avisar.test.ts`) se dejaron: es compatibilidad con datos antiguos.
4. **Respuestas viejas de la bandeja.** En `cargar()` de ambas pantallas hay un contador de peticiones (`useRef`); una respuesta (éxito, error o fin de carga) de una petición que ya no es la última se descarta.

## Comandos y resultado

- `npm test`: 183 archivos pasan (1 omitido), 2005 pruebas pasan.
- `npm run lint`: 9 errores y 22 avisos, los mismos 9 errores previos; ningún error ni aviso nuevo en archivos tocados.
- `npx tsc --noEmit`: sin errores.
- `npx next build --webpack`: compila bien.

## Dudas / notas

- Los avisos de aprobación ya guardados con grupo «Oficina Técnica» siguen así en la base; solo la tarjeta unificada mostrará Jefatura para quien tenga los dos roles. Los de un solo rol (p. ej. solo jefe de oficina técnica) se verán como «Oficina Técnica» hasta que se reenvíen/recreen. No se tocó la base.
- El filtro de grupo del servidor sigue usando el `grupo_nav` guardado de cada fila; no se cambió.
- Falta verificación visual en vivo de los puntos 1, 2 y 4 (sin navegador en este ajuste).
- La creación de RQ (POST) no tiene prueba de API con avisos; el grupo Jefatura queda cubierto por la ruta de reenvío y el tipo/compilación.
