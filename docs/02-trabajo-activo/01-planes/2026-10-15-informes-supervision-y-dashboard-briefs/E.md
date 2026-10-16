# Brief — Tanda E: Informes, chips, listado, nuevo y foto de campo

## Rol, modelo y tanda

Worker 3, Sonnet, esfuerzo medio. Tanda E, Ola 3, carril W3 (primera de E → F → Q → L). Subagente «Worker 3 · E». Plan: `docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard.md` (no lo leas completo).

## Ítems de la tanda (Punch List)

- **E1**: `registro-accesos.ts`: el chip pasa a «Informes de supervisión» (informativo, `requiereServicio: 'si'`, panel derecho en Supervisión operativa y panel izquierdo grupo Reportes) y se agrega «Foto de campo» (acción: derecho, Accesos rápidos, Acciones del izquierdo); páginas `/proyectos/[id]/informes` y `/proyectos/[id]/informes/foto`; se conserva el id `informe-servicio` salvo que algo exija cambiarlo (se anota); `next.config.ts`: `geolocation=(self)` **solo si Victor aprueba P7** — prueba: `npm test` (cobertura y humo del registro) y fila en la matriz derivada.
- **E2**: listado con código, tipo, fecha o período, formato, autor, estado, versión, fotos y acciones; filtros; estados vacío, carga y error; tabla con scroll horizontal; los emitidos `COSTOS` no aparecen sin economía.
- **E3**: «Nuevo»: selector de formato (Costos deshabilitado con título), tipo, fecha o período con atajos, Desde/Hasta y resumen (días, trabajados, diarios emitidos, sin diario, columnas por día o semana), avisos de cruce.
- **E4**: «Foto de campo» (móvil): botón grande «Tomar foto» con `<input type="file" accept="image/*" capture="environment">` (un toque tras abrir el chip, P8), reducción a ~1600 px, servicio/actividad/descripción, GPS opcional, mensaje claro y reintento si no hay señal (sin cola sin conexión).

Punto de corte: E1–E2 / E3–E4.

## Rama, worktree y puerto

Rama `local-worker-3`, worktree `D:/VICTOR/CLAUDE CODE/py_control_proyectos_web/.worktrees/local-worker-3`. **W3 parte de `local-worker-3` con `local-worker-1` incorporada (al cerrar D); el Worker git lo hace antes.** Antes de empezar verifica con `git log --oneline -8` y `ls src/lib/informes src/app/api/proyectos/\[id\]/informes` que están `tipos.ts`, `armar-datos-*.ts`, `congelar.ts` y la API de D; si no, **detente y avisa al Orquestador**. Puerto 3013 si levantas la app. Trabaja solo ahí.

## Qué leer, y qué no

1. `src/lib/config/registro-accesos.ts` (helper `inerte(...)`, línea ~234; chip `informe-servicio` ~457; un chip de acción como patrón), `cobertura-pantallas.ts`, `panel-derecho.ts`, `panel-izquierdo.ts`, `nav-proyecto.ts` y sus pruebas (`nav-proyecto.test.ts` cita `informe-servicio`; `registro-humo.test.ts`, `matriz-accesos.test.ts`).
2. `src/lib/informes/tipos.ts` (**contrato congelado de B**), `formatos.ts` (`formatosDisponibles(conEconomia)`), `periodo.ts` (`rangoDeAtajo`, `validarPeriodo`, `resumirPeriodo`, `columnasDelPeriodo`, `avisosDeCruce`, atajos `SEMANA_EN_CURSO`, `SEMANA_ANTERIOR`, `ULTIMAS_2_SEMANAS`, `MES_ANTERIOR`), `estados.ts`.
3. La API de D: `GET/POST /api/proyectos/[id]/informes`, `POST/GET fotos-campo`. **Contrato por confirmar al incorporar D:** forma exacta de la respuesta del listado (campos, `avisos`), del POST y de `fotos-campo`; léelas del código de las rutas, no de este brief.
4. `src/lib/permisos/permisos.ts`: `puedeVerInformes`, `puedeCrearInforme`, `puedeTomarFotoCampo`, `puedeVerInformeCostos`, `puedeCrearInformeCostos`.
5. Diseño: `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/05-diseno-y-referencias/design.md` y la maqueta `.../mockups/informes-supervision.html` (mira solo las vistas `v-lista` Listado, `v-nuevo` Nuevo y `v-movil` Celular; no la copies). Flujos `16-paneles.md` y `14-accesos-y-restricciones.md` en `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/04-flujos-de-negocio/`.

**Verifica con `grep` los nombres reales.** **No leas** el plan completo ni otros flujos.

## Qué puede trabajar

Crear o editar: `src/lib/config/registro-accesos.ts` y las pruebas de `src/lib/config/` que lo cubren, `src/app/(workspace)/proyectos/[id]/informes/**`, `src/components/informes/**`, sus pruebas. `next.config.ts` **solo** si Victor aprueba P7 (si no consta la aprobación, no lo toques y anótalo).

**No toca:** `src/lib/informes/tipos.ts`, `src/lib/informes/**` salvo archivos nuevos que haga falta (pregunta), `api/proyectos/[id]/informes/**` y `fotos-campo/**` (son de W1), `permisos.ts`, `src/lib/pdf/hoja.ts`, `db/**`, `db/095*` (sin seguimiento: no lo agregues a ningún commit), `src/lib/rdts/**` y `api/rdts/**`, `package.json`, flujos, `AGENTS.md`, el archivo del plan, ni otros worktrees. **No aplica migraciones.**

## Dónde deja su entrega y su evidencia

- Código: commit y push a `local-worker-3` (nunca a `main`) al cerrar E1–E2 y al cerrar E3–E4. `git add <ruta>` por nombre, nunca `git add -A`. Mensaje en español con `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.
- Resumen de cierre: `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard-briefs/resultados/E.md`. **Lee y usa la plantilla** `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/00-estandar-agentes/06-plantillas/12-resumen-de-cierre-de-tanda.md` (cinco grupos de hallazgos). No hagas commit en el repositorio de documentación.

## Contrato técnico verificado

- Hoy `informe-servicio` es un chip inerte (`inerte('informe-servicio', 'Informe de servicio', 'Supervisión operativa', FileBarChart, ...)`); `Permissions-Policy` de `next.config.ts` trae `camera=(), geolocation=()`. La cámara con `capture` puede no depender de esa cabecera (**no verificado**; lo confirma Victor en un celular real, P8); el GPS sí (P7).
- Ver informes: los 13 roles; crear: administrador, jefe de proyectos, jefe de oficina técnica, supervisor operativo; foto de campo: esos 4. `COSTOS` lo ven y crean los 5 roles con economía (no los restrinjas a 3, P30).
- Toda interfaz o acceso nuevo exige fila en la matriz derivada del registro; **no edites el flujo 14 ni el artefacto**: anota las filas en el resumen para el Documentador (tanda M).
- Migraciones 098 a 102 pueden no estar aplicadas (P33): la pantalla se prueba con datos simulados; sin cuentas de prueba (P36), las capturas y el inicio de sesión quedan «Observado» y los cierra la tanda L.

## Skills y verificación

`cerrar-tanda` al terminar (`D:/VICTOR/CLAUDE CODE/pg_control_proyectos/.claude/skills/cerrar-tanda/SKILL.md`; el commit de documentación lo hace el Orquestador). E1 toca menús y accesos por rol: **aplica `verificar-permisos-por-rol`** (`.claude/skills/verificar-permisos-por-rol/SKILL.md`) con la prueba del registro por los 13 roles; lo observado en vivo lo cierra L. Comandos: `npm test` (si solo cambia por fin de línea el `.snap` de curva-s, restaurarlo con `git checkout`); `npx tsc --noEmit`; `npm run lint` (9 errores y 22 avisos **preexistentes**: no agregar nuevos, anota el conteo); `npx next build --webpack`. `.env.local`: copiar el principal al worktree (autorizado siempre).

## Límites y preguntas

80 llamadas como meta; a las ~60 cierra el ítem en curso, commit, push y traspaso. Si hallas un conflicto con una regla de negocio o algo que el brief no decide (por ejemplo cambiar el id del chip), **detente y devuélvelo como pregunta al Orquestador**.

## Criterios de salida

E1–E4 en `Conforme` u `Observado` con causa; pruebas, `tsc`, lint (sin errores nuevos) y build webpack en verde; commits comprobados con `git branch --contains`; árbol limpio salvo `db/095*`; resumen escrito. Respuesta final en <= 25 líneas: estado por ítem, commits, resultado de los comandos, preguntas abiertas.
