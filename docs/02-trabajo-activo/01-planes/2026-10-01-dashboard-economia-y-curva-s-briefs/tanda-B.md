# Brief — Tanda B · Dashboard Parcial sin dinero y Completo con costo por recurso

## Rol, modelo y tanda

Worker 1 (código) · modelo **DeepSeek V4.1 Flash** (`opencode-go/deepseek-v4.1-flash`) · tanda **B**, carril único `local-worker-5`. Se lanza como subagente «Worker 1 · B». Depende de A (hecha: commit `d40cd74`).

## Ítems de la tanda (Punch List del plan)

| ID | Ítem | Evidencia mínima |
|---|---|---|
| F03 | Con BD en `COMPLETO`, un rol sin economía abre **Parcial** (el servidor lo fuerza); con rol con economía se respeta la BD | Prueba con BD en COMPLETO y rol sin economía |
| F04 | Parcial no muestra ningún dato monetario (lista cerrada **PD5**), incluso con BD en COMPLETO | Inspección ítem por ítem (captura en D) |
| F05 | Parcial conserva filtros, % avance físico, matriz de partidas sin costo, diagnóstico, PPC/Pareto (Bloque E) y enlace a Curva S | Inspección |
| F06 (parte B) | El interruptor se ve en ambos casos; con economía alterna sin recargar (`router.refresh()`) | Prueba de alternancia (en vivo en D) |
| F07 | Ambos dashboards enlazan a Curva S; desde Parcial sin economía la URL lleva `?modo=fisica` | Inspección + URL |
| F08 | Bloque «Costo real de recursos» **solo en Completo**: filas por recurso, fila «Sin resolver» cuando corresponde, nota del legacy y Total = AC | Suma manual / prueba |
| D01 | La query del Dashboard añade `descripcion` a `pr_recursos` y el bloque la usa | Diff + salida de la consulta |
| D02 | Función de reconciliación con tests: `Σ filas + (AC − Σ) = AC`; con legacy; sin legacy; corrida ≠ 0; diferencia = 0 (no se muestra la fila) | `npm test` |
| D04 | Dashboard sigue leyendo, no recalculando: sin cambios en `evm.ts`, `dashboard.ts` ni funciones SQL | Diff |
| D05 | El Total del bloque es el mismo AC que imprime el KPI AC (misma fuente del PR) | Inspección/captura |
| U03 | Bloque de recursos: tabla con scroll horizontal, encabezado fijo y `scope` en los `th`; sin `max-w-*` en el contenedor de página; paleta de `design.md` | Captura (D) |
| U05 | El ocultado en Parcial no deja huecos de layout ni secciones vacías | Captura (D) |
| E02 | Bloque de recursos sin filas: estado vacío; diferencia = 0: no aparece la fila «Sin resolver» | Prueba/inspección |
| E03 | Carga atenuada sin salto de layout; error de API con mensaje claro (patrón existente) | Revisión del patrón (D) |

Decisiones que aplican: **PD5** (lista cerrada de ocultados en Parcial), **PD6** (Bloque E y enlace a Curva S en ambos), **PD1** (bloque de costo por recurso y reconciliación). El enlace a Curva S en modo físico apunta a `?modo=fisica`; el `?modo=` real de la API es de la Fase C, pero la URL del enlace sí se pone en B.

## Lista cerrada PD5

En **Parcial** se ocultan: cabecera «Costo directo (US$)», resumen ejecutivo (imprime SPI/CPI), chip semáforo (deriva de CPI), dona «Composición del costo», gráfico «Desempeño por partida», columnas PV/EV/AC/SPI/CPI de la matriz de partidas y la opción de orden «mayor desviación de costo».
**Se conservan**: filtros, % avance físico, matriz de partidas sin costo, panel de diagnóstico, PPC/Pareto (Bloque E) y enlace a Curva S.

## Bloque «Costo real de recursos» (PD1)

- Filas = `pr_recursos` de tipos MO (personal, HH) y HM (equipos), con `descripcion` (hoy la query no la trae: **añadirla**).
- Fila «Sin resolver / diferencia» = `AC − Σ filas`, **visible solo si ≠ 0**, con `title` que explica las filas sin resolver (deuda `db/055`).
- El balde `costo_legacy_sin_partida_acum` es **nota informativa, nunca fila sumable** (ya está dentro de las filas de recursos).
- **Total = AC** leído del PR (misma fuente que el KPI AC). Por construcción `Σ ≤ AC`; lo que falte queda en la diferencia, no se fuerza a cero.
- Log de reconciliación en lógica pura con tests (`src/lib/dashboard/costo-recursos.ts` + `.test.ts`, nuevo).

## Rama, worktree y puerto

- Rama `local-worker-5`; worktree `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\local-worker-5`; puerto 3115 (en B **no** se usa navegador).

## Qué leer, y qué no

1. Este brief y `00-reglas-de-contexto.md`.
2. App: `AGENTS.md` y `CLAUDE.md`.
3. `docs/04-flujos-de-negocio/11-dashboard.md` (tablas y reglas del Dashboard) una vez; y la sección de la Curva S (`21-curva-s.md`) solo para el enlace (no implementes C).
4. `docs/05-diseno-y-referencias/design.md` solo las secciones de tablas, colores y componentes que uses.
5. Código: `src/app/(workspace)/proyectos/[id]/dashboard/page.tsx`; `src/components/dashboard/**`; `src/lib/dashboard/**`; `src/lib/pr/**` (solo lectura, para saber de dónde sale AC).
6. Del plan: solo ítems por Grep de su ID.

**No leer**: el plan completo, progreso/evidencia completos, ni los flujos 14/16/21 completos.

## Qué puede trabajar

Editar: `src/app/(workspace)/proyectos/[id]/dashboard/page.tsx` · `src/components/dashboard/**` · `src/lib/dashboard/**` (incluido el archivo nuevo de reconciliación). Crear: el componente del bloque de recursos y su lógica pura.
**No tocar**: `src/lib/permisos/**` (ya cerrado en A salvo corrección necesaria) · `src/lib/config/**` · `src/lib/evm.ts`, `src/lib/dashboard/dashboard.ts` (motor) · `src/lib/curva-s/**` (es C) · `db/**` · `docs/04-flujos-de-negocio/**` (E) · `docs/02-trabajo-activo/**`.

## Contrato técnico verificado (2026-10-02)

- Existen: `src/components/dashboard/{BloqueE,DonaCosto,FiltrosDashboard,GraficoBarrasHorizontales,MatrizPartidasDashboard,PanelDiagnostico,ResumenEjecutivo,SelectorDashboard,TarjetaKpi,ToggleTipoDashboard}.tsx`; `src/lib/dashboard/{dashboard,filtros-dashboard,pareto-cnc}.ts` (+tests).
- La query de `pr_recursos` vive en `dashboard/page.tsx` y hoy selecciona `tipo, costo_contractual, costo_acumulado, cantidad_acumulada` (sin `descripcion`).
- El AC sale del PR (`proyecto_pr`); confirmar la columna exacta en el código antes de usarla.

## Skills que debe usar

- `cerrar-tanda` al final.

## Límites

~80 llamadas. Sin navegador. Sin migraciones. Sin push/merge. Commit solo en `local-worker-5` (`git add` explícito).

## Cómo registra hallazgos y preguntas

A `resultados/tanda-B.md` en los grupos. Conflicto con un flujo o permiso no decidido → detente y devuélvelo al Orquestador.

## Criterios de salida

- Parcial sin ningún dato monetario de la lista PD5; conserva lo listado.
- Bloque «Costo real de recursos» en Completo con total = AC y reconciliación probada (incluido el legacy no sumable).
- Ambos dashboards enlazan a Curva S; desde Parcial sin economía con `?modo=fisica`.
- `npm test` de los módulos tocados verde; `tsc` 0; lint igual al baseline de `main`.
- Commit en la rama y `resultados/tanda-B.md` escrito.
