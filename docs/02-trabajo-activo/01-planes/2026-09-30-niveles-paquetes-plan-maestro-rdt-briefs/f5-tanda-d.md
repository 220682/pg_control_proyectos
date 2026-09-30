# F5-D · Documentación: flujos, matriz de permisos y trazabilidad

Lee primero `00-reglas-de-contexto.md`. **Carril de documentación** · trabajas en `pg_control_proyectos` (`main`), **sin worktree de la app**; puedes correr **en paralelo** con F5-B y F5-C.
Fase F5 · **Depende de:** el Gate 1 con la **tabla en bloque de cambios a flujos aprobada por Victor** (plan, sección «Tabla en bloque de cambios a flujos»: léela por Grep de ese título) y F5-A cerrada (para describir lo realmente implementado).
**Commit:** en `main` de `pg_control_proyectos`, `git add` explícito solo de tus archivos.

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| F5D-1 | Flujos **09 y 15** según la tabla aprobada: paso de confirmación de niveles, mapa por servicio y origen, recarga bloqueada, vínculo con metrado que se declara en Paquetes, cronograma solo carga y vista | Diff + casilla «aplicado» en la tabla |
| F5D-2 | Flujos **19 y 20**: paquete sin fechas, partida repartida entre paquetes, lienzo del Plan Maestro, seis columnas, versión nueva con motivo, sin paquete permitido | Diff + casilla |
| F5D-3 | Flujos **06, 18, 10 y 21**: el RDT lista lo del Plan Maestro, real por paquete × partida, columnas fijas del lienzo (sin Tiempo), el PR suma por partida, sin cambio de fórmulas | Diff + casilla |
| F5D-4 | Flujos **14 y 16** y el artefacto **«Matriz de permisos»** (https://claude.ai/artifact/4no1PCEfDb5pYmgmnrP5MT): filas de la tabla 2 (cronograma, paquetes, Plan Maestro, versión nueva), sección «Accesos requeridos para paquetes (pendiente)» reescrita, ocultar paneles, acción «Crear paquete» | Diff + artefacto actualizado |
| F5D-5 | Índices: `04-flujos-de-negocio/README.md`, `02-trabajo-activo/01-planes/README.md` (estado del plan), `06-material-de-apoyo` si aplica; `planes-futuros.md` sin cambios salvo lo que Victor pida | Diff |
| F5D-6 | **Trazabilidad**: para cada flujo de la tabla, el texto final coincide con lo implementado (comprobado contra el código de la rama integrada); las **mejoras de trabajo** del plan (`resultados/*.md`) trasladadas a `03-aprendizaje-continuo/`; las reglas de negocio integradas **en el flujo**, nunca en un archivo aparte | Lista por flujo con el resultado |

## Contrato técnico verificado (2026-09-30)

- Política vigente (`AGENTS.md` § Políticas de coherencia y trazabilidad): la matriz de permisos es la base de los accesos; un cambio que choca con lo escrito se implementa en **todos los afectados**, y el Auditor verifica la trazabilidad antes del Gate 2.
- Las reglas de negocio acordadas en el plan van **directo al flujo**, integradas en su estructura, no al final ni como nota aparte; las mejoras de trabajo van a `03-aprendizaje-continuo/` (una lección sobre cómo se trabaja, nunca una regla del sistema).
- Estructura de las tablas del flujo 14: tabla 1 (interfaces con y sin datos económicos), tabla 2 (acciones); notas al pie numeradas. **No copies** las tablas a otros documentos: referencia por enlace.
- El artefacto se edita con la herramienta de artefactos (Artifact: `read` y luego publicar sobre la misma URL); no se crea otro.
- Sin credenciales. No edites el plan, el progreso ni la evidencia (los consolida el Orquestador).

## Qué NO hacer

- **No edites ningún flujo sin que la fila de la tabla en bloque esté aprobada por Victor.** Una contradicción nueva que no esté en la tabla: detente y devuelve la pregunta.
- No edites código. No borres documentación funcional. No declares nada «aplicado» sin comprobarlo contra el código.

## Cierre

`resultados/F5-D.md` (estado de F5D-1 a F5D-6, la tabla con sus casillas, handoff, llamadas). Commit en `main` de `pg_control_proyectos`, `git add` explícito.
