# 2026-10-17 — Observaciones de Victor, Lote 4 (levantar, desplegar y que Victor revise)

> Lote de trabajo tradicional, sin flujo de Orquestador: Victor pasa las observaciones sobre la app real (`py_control_proyectos_web`); el agente las levanta, las verifica en la app con login real, las despliega a `main` y Victor revisa. Cada observación se registra aquí cuando se atiende.

## Identificación y estado

- Fecha: 2026-10-17
- Estado: **SESIÓN CERRADA el 2026-10-17 y de nuevo el 2026-10-19** (el lote sigue abierto para nuevas observaciones de Victor)
- Despliegue: push a `main` de la app (Vercel despliega desde GitHub)

## Observaciones

| # | Observación (Victor) | Estado | Dónde |
|---|---|---|---|
| L4-1 | En Mano de obra directa del DP y en «Cargos (HH)» los cargos en MES no se convierten a HH: se suman los meses como si fueran horas. Mostrar las HH reales, como la MOI (Cantidad · Meses · HH · Costo), y el total de HH reales | Desplegada (app `5246428`) | DP (C1), descargas Excel y PDF del DP, `/proyectos/{id}/recursos/cargos` |
| L4-2 | PS-108-2026 (PS-0003): las HH del presupuesto no igualan las del listado de insumos (1.699,18 vs 3.140,52 HH directas en HH) | Resuelta y verificada en producción (carga hecha por Victor) | Carpeta `comparar/` del servicio en `01_pg_planeamiento`; DP de PS-0003 |
| L4-3 | Los chips «Alcance» y «Presupuesto» están muertos; no se puede ver, descargar ni eliminar el archivo del checklist; solo el administrador debe cargar y eliminar | Desplegada y verificada en lectura (app `c7b746a` y `69ebf94`); cargar y eliminar sin probar | `/proyectos/{id}/alcance`, `/proyectos/{id}/presupuesto` |
| L4-4 | Botón para mostrar u ocultar la contraseña | Desplegada; verificada en el login local | Login, activación de cuenta, alta de usuarios |
| L4-5 | Obs. 1 (2026-10-19): apartado «Restricciones» (antes «Alertas») en Supervisión operativa, unido al texto «restricciones» del RDT, al banco de fotos y al informe | Implementada y probada de punta a punta en PS-0000 (crear → aviso al administrador → Recepcionado al abrir → Atendido → aviso al creador); **sin commit ni despliegue** (la `db/113` ya la aplicó Victor). Sin probar: excepción del texto «restricciones» del RDT y la tabla del informe | Flujos 04, 06, 14 (nota 17), 16 y 22; app sin versionar |
| L4-6 | Obs. 2 (2026-10-19): partidas transversales (fuera del RDT, avance = % físico del resto) | Desplegada (app `5ed692d`, `db/111` y `db/112` aplicadas). Pendiente de Victor: reimportar DP de servicios existentes y recalcular el PR | Flujos 09, 10, 18, 19, 20, 21 |
| L4-7 | Paquetes → Agrupar: mostrar la descripción de la partida junto a su código | Desplegada (app `99a63d0`) | `PasoAgrupar.tsx` |
| L4-8 | Plan Maestro: los cuadros de días se editan solo en la fila del paquete (metrado de la partida guía); las partidas del paquete derivan sus días por proporción | Desplegada (app `abe31ff`); sin verificar en pantalla por Victor | Flujos 19 y 20; `lienzo-vista.ts`, `LienzoPlanMaestro.tsx` |
| L4-9 | Plan Maestro: las transversales se ven en el lienzo (costo, programado, real) y suman al Total del servicio para llegar al 100 % | Desplegada (app `e0d73af` y `c068f4a`); sin verificar en pantalla por Victor | Flujo 20; `transversales-vista.ts` |

### L4-1 — Detalle

- **Cálculo:** 1 MES = 208 HH, un solo lugar (`src/lib/dp/conversion-hh.ts`); el mismo factor de la MOI. La regla quedó en el [flujo 09](../../04-flujos-de-negocio/09-importar-dp.md) («Mano de obra directa en la vista del DP») y en el [flujo 16](../../04-flujos-de-negocio/16-paneles.md).
- **Verificado (PS-0003, local, login real):** C1 con columnas Cargo · Unid. · Cantidad · HH Contractual · Costo; total 3612,78 HH = 1699,18 HH del DP en HH + 9,20 MES × 208 (1913,60 HH); costo total sin cambio (36719,68). Excel y PDF con la misma tabla y los mismos totales. «Cargos (HH)» con la misma conversión y total, visto con la cuenta de Victor y con la de López Cáceres (sin acceso al DP; ve Cargos sin costos).
- **Efecto en la reconciliación de HH:** las partidas no cuentan los cargos en MES, así que se comparan contra las HH de mano de obra que el DP trae en HH. PS-0003 pasó de «REVISAR 0,54 %» (9,20 meses sumados como horas) a «OK 0,00 %», con los MES mostrados aparte.
- **Pruebas:** `npm test` (1631 pasan), `tsc --noEmit` sin errores. `eslint` marca un `prefer-const` que ya existía en `src/lib/dp/agregacion.ts:64`, fuera de esta tarea.

### L4-2 — Detalle

- **Hallazgo:** el listado de insumos de PS-108 es el APU con las «Sub Partidas:» abiertas. Las que tienen APU propio en el mismo archivo reproducen el listado exacto; el pintado de contenedores (4.1 y 4.2) y la limpieza 2.2.8 no tienen APU: su reparto entre actividades es **estimado** (las HH por cargo salen del listado; lo estimado es en qué actividad cae cada hora).
- **Resultado (DP de PS-0003 cargado por Victor, verificado en producción):** 5.054,12 HH directas (3.140,52 en HH + 9,20 MES × 208), 1.248 HH de MOI, BAC 322.877,39 sin cambio, 10 partidas sin mano de obra (antes 19). El costo de mano de obra subió de 36.719,68 a 56.564,88 porque el pintado y otras sub-partidas pasaron de Materiales/Subcontratos a Mano de obra; el total no cambió. Ajustes de cierre netos +92,19 USD (0,30 % en valor absoluto), en una línea «AJUSTE DE CIERRE…» en Materiales.
- **Causa del desconcierto de Victor:** el DP de producción seguía con la importación vieja del 15/10; se comprobó por la fecha y el nombre del archivo importado.
- **Archivos y skills:** `PS-108-2026_presupuesto_base_hh-abiertas.xlsx`, `…_apertura-hh_detalle.xlsx`, `…_reparto-hh.json` (registro de lo estimado) y las skills `comparar-insumos-presupuesto` y `cuadrar-hh-con-insumos` en `01_pg_planeamiento/.claude/skills/`.

### L4-3 — Detalle

- **Pantallas:** `/proyectos/{id}/alcance` y `/proyectos/{id}/presupuesto` muestran el archivo de la fila `alcance` o `presupuesto_proyecto` del checklist: Ver, Descargar y, solo para el administrador, Cargar/Reemplazar y Eliminar (con confirmación). Un archivo por servicio. API: `GET …/documentos/[documentoId]/archivo?modo=ver|descargar` (URL firmada de 60 s) y `DELETE …/documentos/[documentoId]`; el `POST` quita de Storage el archivo anterior al reemplazar con otro nombre.
- **Decisiones de Victor:** la subida del checklist **convive** con la pantalla; solo él (administrador) carga y elimina; los demás ven y descargan.
- **Interpretación mía por confirmar:** el Presupuesto lo ven y descargan solo los roles que ven el DP (trae precios); Victor dijo «los demás». Quedó escrito así en el flujo 14, nota 13.
- **No se construyó:** pantalla para otros documentos («y demás») ni borrar el DP importado (cargar un DP nuevo ya lo reemplaza).
- **Pruebas:** `npm test` (1637 pasan), `tsc --noEmit` y `eslint` de los archivos tocados sin errores; en producción: ambas pantallas cargan, el Presupuesto de PS-0003 muestra `PROPUESTA_ECONOMICA.xls` y la descarga entrega el archivo (131.584 bytes); la consola quedó sin errores tras corregir una advertencia de hidratación (#418).

## Reglas de negocio acordadas en esta tarea

| Regla | Dónde quedó |
|---|---|
| Los cargos de mano de obra en MES se muestran convertidos a HH reales (1 MES = 208 HH) junto a la cantidad en su unidad, con total de HH reales, en el DP (pantalla, Excel y PDF) y en «Cargos (HH)» | Flujo 09, sección «Mano de obra directa en la vista del DP: HH reales»; flujo 16, «Recursos del servicio» |
| La reconciliación de HH compara partidas contra las HH de mano de obra en HH; los cargos en MES van aparte | Flujo 09 (misma sección) |
| Alcance y Presupuesto del servicio tienen pantalla propia: cargar, reemplazar y eliminar el archivo solo el administrador; ver y descargar según el permiso de cada pantalla (Alcance los 13 roles; Presupuesto los roles que ven el DP, por confirmar); la subida del checklist convive | Flujo 14 (tablas 1 y 2, nota 13), flujo 12 (Grupos de acción), flujo 16 (Implementado) |
| El programado diario de un paquete se escribe sobre su partida guía (en su unidad) y las demás partidas lo reciben por proporción; se guarda por línea, así que PV, PR y Curva S siguen sumando por partida y cada partida cuadra con su metrado (100 %) | Flujo 20 («Programación diaria de un paquete»), flujo 19 |
| Las transversales se ven en el lienzo como filas «Transversal» de solo lectura y **suman al Total del servicio**; no se programan día por día. Criterio de Victor: lo agrupado vuelve a la estructura inicial del presupuesto y todo suma 100 % en metrado, HH y costo | Flujo 20 (párrafo de transversales). Los cambios de los flujos 19 y 20 de esta sesión están **sin commit** en este repositorio |

## Mejoras (de trabajo)

Trasladadas el 2026-10-17 a [`docs/03-aprendizaje-continuo/2026-10-17-lote-4-aprendizajes-de-trabajo.md`](../../03-aprendizaje-continuo/2026-10-17-lote-4-aprendizajes-de-trabajo.md): comprobar que el archivo se aplicó antes de revisar el cálculo; parche filtrado por hunk para comitear solo lo propio; hidratación con `toLocaleString`; límites del modo automático con login y escritura en producción; claves de prueba visibles al leer su archivo; heredocs en Windows; skills de cuadre de HH.

## Observaciones sobre la política

- Sin entradas todavía.

## Carpetas/archivos huérfanos

- `py_control_proyectos_web/db/095_cerrar_lectura_directa.sql`: archivo sin versionar que ya estaba en el árbol antes de este lote. No se tocó; lo decide Victor.
- `pg_control_proyectos/.playwright-mcp/`: carpeta sin versionar con capturas, logs y descargas de pruebas anteriores (esta sesión sumó más). No se borró nada.
- Carpeta `comparar/` de PS-108 (en `01_pg_planeamiento`): el `_comparado.xlsx` que generé ya no está (no figura borrado por el agente); se regenera con la skill `comparar-insumos-presupuesto` si Victor lo quiere. Hay dos copias de `presupuesto_base.xls` con las mismas celdas y distinto binario, y el `INDICE.md` del servicio lista archivos que ya no están (anotado en «Por confirmar»).
- `docs/02-trabajo-activo/01-planes/2026-10-07-plan-maestro-tres-paneles.md` y `2026-10-14-revision-completa-app.md`: sin versionar desde antes de este lote. No se tocaron.
- 2026-10-19: `login-ojo-contrasena.png` y `prueba-sello-T3.jpg` en la raíz de este repositorio (capturas de pruebas anteriores, sin versionar). No se borraron.
- 2026-10-19: el dato de prueba `PS-0000-RE-1` (restricción) sigue en el servicio PS-0000. No se borró.

## Pendientes de decisión de Victor

1. **Presupuesto: ¿lo descargan los 13 roles o solo los que ven el DP?** (hoy, solo los que ven el DP). Cambio pequeño en `puedeVerPresupuestoServicio` y en la fila de la tabla 1 del flujo 14.
2. **Reparto estimado del pintado 4.1/4.2 y de 2.2.8** de PS-108: confirmar con planeamiento.
3. **FLETE (1.270,58 USD):** Material en la app, Subcontratos en el listado.
4. **Que el lector del DP abra solo las «Sub Partidas:» con APU propio** (hoy la app las cuenta como Materiales): cambio de regla del flujo 09, posible observación de seguimiento.
5. **INDICE de PS-108:** el listado dice sumar 320.701,97 y suma 322.877,39; el INDICE lista archivos que ya no están.
6. **«Y demás»** (cronograma y otros documentos con pantalla propia) y **borrar el DP importado**: sin construir; Victor decide si los quiere.
7. **Matriz de permisos (artefacto):** la actualiza Victor con las filas de Alcance y Presupuesto (esta cuenta no la abre).
8. **Equipos (C2) con unidad MES** (camioneta pick up, minivan): siguen bajo «HM Contractual» con el valor en meses. Falta definir cuántas horas-máquina vale un mes antes de convertirlos.
9. **GPS de la foto de campo:** Victor probó la captura y las coordenadas no salen en el sello. Revisión aplazada por él; ver `leerGps` en `FotoCampo.tsx`, el POST de `fotos-campo` y el dibujo del sello.
10. **Matriz de permisos (artefacto):** Victor debe sumar las filas nuevas del flujo 14 de Restricciones (nota 17).
11. **Restricciones (L4-5):** DESPLEGADO el 2026-10-21 (app `ddb18ee` en `main`, Vercel; 2146 pruebas y build en verde; `db/113` ya aplicada). **Pendiente de verificación en producción:** la restricción escrita en una actividad del RDT, el aviso y la tabla del informe. Se verifica con el caso del día 3 de la [prueba v2](../06-pruebas/04-prueba-rdt-ps0001-v2-guion.md) (plan [Correcciones de la prueba del RDT en PS-0001](2026-10-21-correcciones-prueba-rdt-ps0001.md), Lote 0).
