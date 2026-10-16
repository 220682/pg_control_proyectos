# Brief — Tanda F: Informes, editor y vista

## Rol, modelo y tanda

Worker 3, Sonnet, esfuerzo medio. Tanda F, Ola 3, carril W3 (después de E). Subagente «Worker 3 · F». Plan: `docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard.md` (no lo leas completo).

## Ítems de la tanda (Punch List)

- **F1**: editor por bloques con vista previa de hoja A4 y los bloques de datos del sistema.
- **F2**: quitar, ocultar, agregar y reordenar bloques con botones y teclado (no solo arrastrar).
- **F3**: bloques libres: texto, fotos (del banco del día), tabla, clima y turno, firmas.
- **F4**: período cambiable desde la barra, guardado automático del borrador, descarga (pdf/docx/xlsx; completo, resumen, fotos).
- **F5**: «Mis formatos» (guardar y usar).
- **F6**: vista de informe emitido (solo lectura), versiones, «Reemplazado» consultable, botones Emitir y Nueva versión con sus permisos.

Punto de corte: F1–F3 / F4–F6.

## Rama, worktree y puerto

Rama `local-worker-3`, worktree `D:/VICTOR/CLAUDE CODE/py_control_proyectos_web/.worktrees/local-worker-3`, continuando tras E (verifica con `git log --oneline -5`). **W3 parte de `local-worker-3` con `local-worker-1` incorporada (al cerrar D); el Worker git lo hace antes.** La descarga (F4) usa la ruta de la tanda G (W1, en paralelo): si G aún no está incorporada, el botón apunta a la URL del contrato y se anota «Observado». Puerto 3013 si levantas la app. Trabaja solo ahí.

## Qué leer, y qué no

1. `src/lib/informes/tipos.ts` (**contrato congelado de B**: `Informe`, `Bloque`, `TipoBloque`, `TipoBloqueDatos`, `TipoBloqueLibre`, `FotoCampo`, `FotoFija`, `FormatoUsuario`, `BloquePlantilla`), `formatos.ts` (`FORMATOS`, `bloquesPermitidos`, `esBloqueEconomico`), `periodo.ts` (`validarPeriodo`, `columnasDeTabla`, `resumirPeriodo`), `estados.ts` (`esEditable`, `puedeEditarInforme`, `puedeNuevaVersion`).
2. La API de D: `informes/[informeId]` (GET, PATCH, DELETE), `emitir`, `nueva-version`, `formatos-usuario`, `fotos-campo`. **Contrato por confirmar al incorporar D:** forma exacta de las respuestas (cómo llegan los datos de cada bloque en un borrador, `avisos`, códigos de error 400/403/404/409); léela de las rutas y sus pruebas.
3. Lo de E (`src/components/informes/**`, páginas de `informes/`) para reutilizar; no dupliques.
4. `src/lib/permisos/permisos.ts`: `puedeEmitirInforme`, `puedeEmitirInformeCostos`, `puedeNuevaVersionInformeAjeno`, `puedeDescargarInforme`, `puedeVerInformeCostos`.
5. Diseño: `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/05-diseno-y-referencias/design.md` y la maqueta `.../mockups/informes-supervision.html` (mira solo la vista `v-editor`: «Bloques del informe», «Agregar bloque», «Banco de fotos del día»; no la copies).

**Verifica con `grep` los nombres reales.** **No leas** el plan completo ni otros flujos.

## Qué puede trabajar

Crear o editar: `src/app/(workspace)/proyectos/[id]/informes/**` (página del editor y de la vista del emitido), `src/components/informes/**`, sus pruebas. Los bloques de datos se muestran con lo que entrega la API; no recalcules cifras en el navegador.

**No toca:** `src/lib/informes/tipos.ts`, `api/proyectos/[id]/informes/**` y `fotos-campo/**` (son de W1; si falta algo en la API, pregunta), `permisos.ts`, `registro-accesos.ts` (salvo lo que ya dejó E), `next.config.ts`, `src/lib/pdf/hoja.ts`, `db/**`, `db/095*` (sin seguimiento: no lo agregues a ningún commit), `src/lib/rdts/**`, `api/rdts/**`, `package.json`, flujos, `AGENTS.md`, el archivo del plan, ni otros worktrees. **No aplica migraciones.**

## Dónde deja su entrega y su evidencia

- Código: commit y push a `local-worker-3` (nunca a `main`) al cerrar F1–F3 y al cerrar F4–F6. `git add <ruta>` por nombre, nunca `git add -A`. Mensaje en español con `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.
- Resumen de cierre: `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard-briefs/resultados/F.md`. **Lee y usa la plantilla** `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/00-estandar-agentes/06-plantillas/12-resumen-de-cierre-de-tanda.md` (cinco grupos de hallazgos). No hagas commit en el repositorio de documentación.

## Contrato técnico verificado

- Borrador ajeno = 404; PATCH sobre `EMITIDO` = 409; DELETE solo borrador propio; `COSTOS` sin economía = 403. La interfaz oculta lo que el rol no puede, pero **el servidor es quien decide**.
- Emitir: autor (`puedeEmitirInforme`); `COSTOS` exige `puedeEmitirInformeCostos` (los 5 roles con economía, P30). Nueva versión: autor, administrador, jefe de proyectos.
- Los formatos `COSTOS` y los bloques `COSTOS_INDICADORES`, `PERSONAL_VALORIZADO`, `EQUIPOS_VALORIZADOS`, `COSTO_PARTIDA` no se ofrecen, ni en «Agregar bloque» ni en «Mis formatos», a quien no tiene economía.
- Reordenar con botones y teclado (no solo arrastrar); guardado automático con aviso de estado (guardando, guardado, error) y sin perder cambios al fallar.
- Un emitido se muestra desde su foto fija (solo lectura); el `REEMPLAZADO` es consultable.
- Migraciones 098 a 102 pueden no estar aplicadas (P33); sin cuentas de prueba (P36): capturas y sesión quedan «Observado» y los cierra la tanda L.

## Skills y verificación

`cerrar-tanda` al terminar (`D:/VICTOR/CLAUDE CODE/pg_control_proyectos/.claude/skills/cerrar-tanda/SKILL.md`; el commit de documentación lo hace el Orquestador). F6 muestra Emitir y Nueva versión según rol: **aplica `verificar-permisos-por-rol`** (`.claude/skills/verificar-permisos-por-rol/SKILL.md`) con pruebas de componente o de ruta por rol; el recorrido en vivo lo cierra L. Comandos: `npm test` (si solo cambia por fin de línea el `.snap` de curva-s, restaurarlo con `git checkout`); `npx tsc --noEmit`; `npm run lint` (9 errores y 22 avisos **preexistentes**: no agregar nuevos, anota el conteo); `npx next build --webpack`. `.env.local`: copiar el principal al worktree (autorizado siempre).

## Límites y preguntas

80 llamadas como meta; a las ~60 cierra el ítem en curso, commit, push y traspaso. Si hallas un conflicto con una regla de negocio o algo que el brief no decide, **detente y devuélvelo como pregunta al Orquestador**.

## Criterios de salida

F1–F6 en `Conforme` u `Observado` con causa; pruebas, `tsc`, lint (sin errores nuevos) y build webpack en verde; commits comprobados con `git branch --contains`; árbol limpio salvo `db/095*`; resumen escrito. Respuesta final en <= 25 líneas: estado por ítem, commits, resultado de los comandos, preguntas abiertas.
