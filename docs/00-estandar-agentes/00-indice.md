# Índice del estándar de agentes

Qué leer según tu rol y el tipo de solicitud. No leas la carpeta completa por defecto: usa esta tabla para ir directo a lo que aplica.

## Por tipo de solicitud

| Tipo de solicitud | Qué leer |
|---|---|
| Chat normal (pregunta, análisis, corrección puntual) | No activa este flujo. Basta el contexto del repositorio (`01-contexto-repositorio/`) que aplique. |
| Spec/SDD | `04-flujo-sdd-y-planes.md` (pasos 1–4) + `06-plantillas/01-spec-sdd.md`. |
| Implementación (Worker) | Su brief, que ya trae su tramo del estándar y de `02-roles-y-delegacion.md` § Worker copiado (no abre esos documentos salvo ante un conflicto de negocio) + **solo** los flujos de negocio que su parte toca, elegidos por su línea `Lee si:` + `05-diseno-y-ui.md` del contexto del repositorio si es UI. |
| Planificación | `04-flujo-sdd-y-planes.md` (pasos 5–7) + `06-plantillas/02-plan.md` y `06-plantillas/05-punch-list.md` + el **índice de flujos** + solo los flujos que el plan declare afectados. La lista completa, únicamente con las dos excepciones de D10. |
| Auditoría | `04-flujo-sdd-y-planes.md` (paso 12) + `06-plantillas/06-informe-auditoria.md` (el informe se guarda en `02-trabajo-activo/04-auditoria/`) + el **índice de flujos** + solo los flujos que el plan declara afectados. La lista completa, únicamente con las dos excepciones de D10. |
| Acción irreversible o reservada a una puerta (merge, push, borrar, migrar, crear o borrar ramas) | `07-verificador-de-acciones.md` (borrador por probar) + `01-principios-y-seguridad.md`. |
| Asignar modelos a agentes, clasificar complejidad de tareas, decidir relevo por contexto, o consultar umbrales de esfuerzo | `09-orquestacion-y-modelos.md` + `10-niveles-de-modelos.md` (qué nivel corresponde a la tarea) + la configuración que corresponda: `opencode.json` en la raíz del proyecto, o `~/.config/opencode/opencode.jsonc` (global). |
| Elegir modelos por consumo de tokens, correr un benchmark antes de asignar, o dejar de depender de la configuración para lanzar un Worker | `10-niveles-de-modelos.md` (las tres políticas) + `scripts/niveles-modelos.py`. |
| Medir sesiones, relevar al Orquestador o medir la eficiencia de un plan | `08-medicion-y-relevo.md` + `06-plantillas/10-medicion-y-eficiencia.md`. Para ver de dónde viene el contexto de una sesión, `scripts/arranque.py` con `--bloques`. |
| Cierre / handoff | `04-flujo-sdd-y-planes.md` (pasos 13–18) + `03-sesiones-contexto-y-handoff.md` + `06-plantillas/07-handoff.md` o `06-plantillas/09-cierre.md` según corresponda. |

## Qué lee, dónde trabaja y dónde deja su entrega cada rol

Ver el detalle por paso en `04-flujo-sdd-y-planes.md` (columna «Qué debe leer antes»). Regla: **todo archivo nuevo nace enlazado** desde el índice o README de su carpeta y desde el plan o el progreso; ninguno queda suelto.

| Rol | Lee | Trabaja en | Deja su entrega o evidencia en |
|---|---|---|---|
| Responsable humano | Nada obligatorio: aprueba en las puertas con lo que el rol correspondiente le presenta | — | El Orquestador registra sus respuestas en el registro de decisiones del plan |
| Orquestador | Este estándar; el plan, el progreso y la evidencia del tema; el índice de flujos y los que el Spec o el plan indican afectados; solo el índice de aprendizaje continuo | Progreso (medición, roles), registro de decisiones y libro de hallazgos del plan, briefs y su índice, handoff | Progreso, informe de avance, mensaje de cierre en el plan, prompt de relevo |
| Planner | El Spec aprobado; `02-plan.md` y `05-punch-list.md`; el índice de flujos y los que el plan declara afectados; solo el índice de aprendizaje | El archivo del plan y la carpeta `-briefs/` | El plan listo para el Gate 1, con la tabla de cambios a flujos y las pre-autorizaciones |
| Worker de código | Su brief, que ya trae su tramo del estándar y las reglas de su rol copiados; los flujos que su parte toca, elegidos por su `Lee si:`; `design.md` si es interfaz | Su rama y su worktree en el repositorio de código | `resultados/<tanda>.md` con los hallazgos en cinco grupos |
| Documentador | Los cuatro apartados del libro de hallazgos; la tabla del Gate 1; los resúmenes de cierre; los flujos afectados | Flujos de negocio, aprendizaje continuo, artefactos derivados e índices | Su resumen de cierre y la lista para el Auditor |
| Worker git | La instrucción puntual del Orquestador | Git de ambos repositorios | Una línea por operación en el progreso |
| Auditor | El plan, el progreso y la evidencia; el índice de flujos y los que el plan declara afectados; el libro de hallazgos | `02-trabajo-activo/04-auditoria/` | El informe de auditoría |
| Analista del flujo | El README de `02-trabajo-activo/05-eficiencia/` y solo lo que necesite | `02-trabajo-activo/05-eficiencia/` | Su informe de eficiencia |

No se replica el contenido de las políticas acá: cada fila apunta al documento que las tiene.
