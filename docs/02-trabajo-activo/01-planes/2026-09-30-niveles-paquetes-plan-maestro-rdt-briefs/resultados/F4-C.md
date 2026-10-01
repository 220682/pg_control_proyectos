# Resultados F4-C · RDT: pantalla Crear RDT, Consolidado y Status

Carril 4 · rama `local-worker-4` (commit sobre `14bae8d`). Sin push ni merge. Sin migraciones. Sin navegador.

## Skills revisados
`pg_control_proyectos/.claude/skills/`: cerrar-tanda (usada); verificar-permisos-por-rol y seguir-flujo-de-planes no aplican (permisos sin cambio; el segundo es del Orquestador). Repo de la app: sin carpeta de Skills.

## Estado de ítems

| ID | Estado | Evidencia |
|---|---|---|
| F4C-1 | Conforme (código) · Observado en pantalla | Lógica pura `src/lib/rdts/selector-actividad.ts` (`construirSelector`, `elegirLinea`, etiquetas) con pruebas en `selector-actividad.test.ts`. Cuadro `SelectorActividadPm.tsx` (paquetes plegables, directas aparte, búsqueda, role=dialog, Escape, foco). La pantalla existente `FormularioCrearRdt` lo usa en «Partida del DP». Build verde. Verificación visual pendiente de F5. |
| F4C-2 | Conforme (código) · Observado en pantalla | `filasCalculadasDeActividad` usa el mismo reparto que el servidor (`calcularFilasDerivadas`); las filas calculadas se pintan en solo lectura bajo la guía y NO se envían (`parteParaGuardar` no las incluye). Pruebas. |
| F4C-3 | Conforme (código) | C/NC, equipos y materiales abren el mismo selector en modo WBS (solo D declaradas ese día); `claveReporte` viaja por actividad y `materialesClaves[]`. Al quitar/cambiar una D se limpian las referencias huérfanas. Pruebas. |
| F4C-4 | Conforme (código) | Status: columna y filtro «Paquete» (oculta si ningún parte tiene paquete; filtros previos intactos). Consolidado: filtro «Paquete de trabajo» (se combina con el de partidas del DP) y etiqueta del paquete en filas de partidas; sin paquetes, aspecto sin cambios. Módulo `paquetes-consolidado.ts` con pruebas. |
| F4C-5 | Conforme (comandos) · Observado (móvil/accesibilidad reales) | Estados carga (skeleton), error (Reintentar), vacío, «Sin Plan Maestro aprobado» (aviso + bloqueo al guardar con `MENSAJE_SIN_PLAN_MAESTRO`). `npx tsc --noEmit` limpio; `npx vitest run` 74 archivos / 737 pruebas verdes; `npx eslint src` 27 problemas (9 errores) = `main`; `npx next build --webpack` OK. 390 px y lectores: por navegador en F5. |

## Handoff
- Archivos nuevos: `selector-actividad.ts(.test)`, `paquetes-consolidado.ts(.test)`, `SelectorActividadPm.tsx`. Editados: `FormularioCrearRdt`, `TablaStatusRdts`, `TablaConsolidadoRdts`, `parte.ts`, `plantilla.ts`, `partes-listado.ts`, rutas `api/rdts/partes` (GET: paquete por parte) y `api/rdts/consolidado` (devuelve `paquetesTrabajo`). Ajuste de una línea en `partes-paquetes.test.ts` (mock del módulo nuevo).
- Comandos: `npx vitest run`, `npx tsc --noEmit`, `npx eslint src`, `npx next build --webpack`; dev `npm run dev -- --webpack -p 3114`.
- Cambios respecto de la maqueta (a revisar por Victor): las filas calculadas no tienen columna en el tareo (el servidor no recibe horas de derivadas); la fila calculada muestra «↳» en vez de T.
- Al corregir un RDT, la pantalla pide también el catálogo del servicio del RDT para resolver las claves; un C/NC/equipo/material antiguo sin equivalente en el plan queda sin clave y hay que elegirlo de nuevo.

## Comprobaciones para F5 (navegador)
1. Crear RDT con servicio con plan aprobado: abrir el selector, plegar/expandir, buscar, Escape devuelve el foco; colores 0 % blanco / en curso amarillo / 100 % verde con ✓.
2. Elegir paquete «por avance»: aparece la guía, las demás filas calculadas en solo lectura; guardar y ver que Status/PR no duplican.
3. C/NC, equipos y materiales: solo ofrece D declaradas; quitar la D limpia su WBS.
4. Servicio sin plan: aviso y bloqueo; plan vacío; error de red con Reintentar.
5. Corregir (`?editarId=`) un RDT con paquete: carga con claves resueltas. Revisar (`?verId=`) deshabilitado.
6. 390 px: tablas con scroll horizontal, selector casi a pantalla completa.
7. Status y Consolidado con servicio con y sin paquetes.

## Decisiones técnicas (a confirmar con Victor)
- Avance del paquete en el selector: por avance = % de la guía; por partidas = promedio simple de sus partidas. «Avance real (%)» de una partida = Met. acum. del servicio sobre la suma de sus metrados en el plan (si la partida está repartida en varios paquetes, el % es de la partida completa, no del paquete).
- Consolidado: el filtro de paquete de trabajo solo afecta la banda de Partidas (como el de subpresupuestos) y la pertenencia sale del Plan Maestro aprobado más lo reportado.
- Efecto de F4-B visible en Status: «Activ.» cuenta también las filas derivadas.
- No se construyó interfaz para asignar paquete al validar ni para REASIGNAR_PAQUETE (no estaba en F4C; el PATCH ya lo admite).

## Mejoras de trabajo
- Heredoc de Bash con TypeScript/Python vuelve a fallar: escribir el script con Write y ejecutarlo.
- La regla de lint `react-hooks/set-state-in-effect` obliga a derivar el estado de carga (clave servicio+reintento) y a sanear en los manejadores, no en efectos.

## Reglas de negocio detectadas
Ninguna nueva.

## Huérfanos
Ninguno.

## Llamadas
Aproximadamente 60.
