# Progreso — Contexto de arranque de los agentes: cerrar las fugas de lectura

Plan: [`../01-planes/2026-10-02-contexto-de-arranque-de-agentes.md`](../01-planes/2026-10-02-contexto-de-arranque-de-agentes.md)
Estado: F0 a F4 aplicadas. Falta F5 (medición con la política nueva), el Documentador y el Auditor.

## Medición

### Línea base antes de los cambios — 2026-10-02, 28 sesiones del 2026-09-30 al 2026-10-01

Con `python scripts/arranque.py 28`:

| | Contexto de 1ª llamada | Creció por su cuenta | Llamadas | Contexto máx |
|---|---|---|---|---|
| Subagentes (n=8) | min 40k · mediana 40k · max 41k | +24k a +195k | 10 a 125 | 64k a 237k |
| Sesión principal (n=4) | min 52k · mediana 52k · max 55k | +12k a +228k | 14 a 102 | 63k a 283k |

Descomposición de los 40k del arranque: ~32k prompt del sistema y herramientas (fuera del alcance de este repositorio) · 5.1k `AGENTS.md` · 3.0k bloque de Skills, de los cuales 1.5k eran 15 Skills ya borrados que seguían inyectándose.

Casos que motivaron el plan: el Planner del plan de permisos creció 195k en 34 llamadas (leyó los 21 flujos por `Bash`); un Worker con dos flujos que tocar creció 36k; hubo bloques de resultado de herramienta de 54k caracteres (`Read`), 36k (`Artifact`) y 19k (`Bash`).

## Fases

| Fase | Estado | Qué |
|---|---|---|
| F0 — Higiene del entorno | **Hecha** | 15 Skills retirados movidos de `~/.claude/skills/.trash/` a `~/.claude/skills_retirados_2026-10-02/` (movidos, no borrados). `scripts/arranque.py` creado y registrado en `scripts/README.md` |
| F1 — Cambios 1, 2, 3, 6 | **Hecha** | D10 en 4 archivos; el brief lleva el tramo del rol; se saca la regla de listar Skills; la medición del arranque entra al estándar |
| F2 — Cambio 4 | **Hecha** | Línea `Lee si:` en los 21 flujos (todas ≤ 200 caracteres) y tabla de disparadores en `04-flujos-de-negocio/README.md` |
| F3 — Cambio 5 | **Hecha** | § Tope de salida de herramientas en los briefs, en `08-medicion-y-relevo.md` |
| F4 — Cambio 7 | **Hecha** | `AGENTS.md` línea de inicio de sesión ya no manda leer todos los flujos |
| F5 — Verificación | **Pendiente** | Requiere un plan real que use la política nueva (V10) |

## Commits

| Commit | Qué |
|---|---|
| `42dcad9` | Plan, Gate Spec y Gate 1 aprobados, tabla de 7 cambios, `scripts/arranque.py` |
| `3df6055` | Los 7 cambios aplicados: D10, disparadores, brief, regla de Skills, topes, línea base, `AGENTS.md` |

Commits de otros planes que se cruzaron en `main` entre ambos (`b02e5f1`, `ddc0275`, `7ff0925`): verificados como ancestros, nada se perdió.

## Validaciones ejecutadas

| Qué | Resultado |
|---|---|
| `grep` de reglas de lectura viejas en `AGENTS.md`, el estándar, el contexto y el índice de flujos | 3 coincidencias, **ninguna es la regla**: dos son «se implementa en todos los afectados» y una es la nota histórica de `09-medicion-y-modelos.md` |
| `grep` de `lista el contenido de` en el estándar | 0 coincidencias: la regla desapareció |
| Flujos con `Lee si:` | 21 de 21 |
| `scripts/verificar-referencias.py` | 44 archivos, 0 huérfanos, **0 enlaces rotos**. Las 2 «menciones sin archivo» son previas y ajenas a este plan (`convenciones-de-trabajo.md`) |
| Longitud de `AGENTS.md` | 182 líneas, dentro de su propia regla de menos de 200 |
| `git diff` de los 21 flujos | `2 +` por archivo, una sola línea insertada cada uno; ningún contenido eliminado |
| `scripts/arranque.py` | Corre en los dos repositorios |

## Desviación del flujo que el Auditor debe conocer

**El primer chequeo del Auditor no se cumple.** Las fases F1 a F4 las aplicó la sesión del Planner, no un Worker en su propia sesión ni su rama propia, porque Victor lo ordenó directamente el 2026-10-02 con los Gates ya aprobados. Todo fue a `main` del repositorio de documentación, que es lo que el Gate 1 pre-autorizó, pero no hubo separación de sesiones ni de ramas. Queda registrado en el § Registro de decisiones del plan.

## Skills revisados

`seguir-flujo-de-planes` (leído al activar el flujo), `trasladar-hallazgos` y `cerrar-tandas` apply a las fases siguientes. Ninguno aplica a las ediciones de política ya feitas, que son texto del estándar.

## Pendientes

1. **Victor**: en la próxima sesión, contar las entradas del bloque de Skills. Debe bajar de 29 a 14 (V1).
2. **Documentador**: trasladar H1 a H3 de `03-aprendizaje-continuo/` y clasificar O1 a O6.
3. **Auditor**: el prompt está en el § Prompt del Auditor del plan. El punto crítico es V7 —abrir 5 flujos al azar y comprobar que su `Lee si:` no promete algo que el flujo no tiene— y la desviación de arriba.
4. **Opcional, con autorización aparte**: registrar el hook de Jev, y decidir sobre el piloto de contradicciones por flujo.
5. **No autorizado**: retirar los 10 Skills de redes sociales de `~/.claude/skills/`. Siguen ahí.

## Handoff

Objetivo: reducir el contexto que un agente carga al arrancar y el que lee de más por la política. Estado: F0-F4 aplicadas y pusheadas; falta F5, Documentador y Auditor. Rama `main` del repositorio de documentación, `origin/main...main = 0 0`. Lo único que no se pudo verificar es el V1, que depende de que Victor abra una sesión nueva. El primer plan que use la política nueva debe medir su arranque con `python scripts/arranque.py` y comparar contra la línea base de la tabla de arriba (V10).
