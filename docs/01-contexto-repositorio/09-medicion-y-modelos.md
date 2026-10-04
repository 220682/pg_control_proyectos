# Medición, modelos y ahorro de tokens en este repositorio

Aplica `../00-estandar-agentes/08-medicion-y-relevo.md`. Decisiones de Victor del 2026-10-01.

## Cómo se trabaja

- **Todo en terminal**, con Claude Code o con Cursor. Un Orquestador y sus subagentes (Planner, Workers, Auditor, Analista del flujo). No se usan chats con nombre ni aplicaciones de escritorio o web para coordinar.
- **Trabajo remoto:** la laptop de Victor queda encendida con las sesiones corriendo y él entra a ella con un medio de control remoto externo (cuál: por confirmar). Consecuencias para los agentes: el avance real vive en git y en el progreso, nunca en una sesión; una consulta al Responsable humano puede tardar, y se registra y se espera sin improvisar; nada asume que Victor está frente a la pantalla.

## Modelos por rol

**No se usa Opus.** Ver política completa en `../00-estandar-agentes/09-orquestacion-y-modelos.md` y los cinco niveles de consumo en `../00-estandar-agentes/10-niveles-de-modelos.md`.

| Trabajo | Modelo |
|---|---|
| Orquestador | `opencode-go/qwen3.7-plus` (nivel 3); lo elige Victor al abrir la sesión |
| Planner y Documentador | Los hace el Orquestador o el agente `general` (`opencode-go/space-bunny-free`, nivel 1): **no existe un subagente `planner` ni `documenter`** en este harness |
| Workers de código | `worker-flash` → `opencode-go/deepseek-v4.1-flash` (nivel 1) · `worker-plus` → `opencode-go/deepseek-v4-pro` variante `high` (nivel 2) |
| Auditor | `opencode-go/space-bunny-free` (nivel 1) |
| Analista del flujo | Agente `general` |
| Worker git (y tareas puramente mecánicas) | `worker-flash` (nivel 1) |

Si un rol falla de forma repetida con el modelo asignado, el Orquestador lo anota en la medición y lo consulta con Victor; no cambia de modelo por su cuenta.

## Dónde vive la configuración de modelos, y qué la limita

Verificado el 2026-10-04 con `opencode debug config`, `opencode agent list` y una corrida real (opencode 1.18.34):

| Tema | Hecho |
|---|---|
| Fuente de verdad | El archivo **global** `~/.config/opencode/opencode.jsonc` (decisión de Victor del 2026-10-03, OP7 del Lote 3). `.opencode/config.json` de este repositorio **no define modelos** |
| Override por proyecto | Un `opencode.json` **en la raíz** del proyecto **sí** pisa al global. El mismo override en `.opencode/config.json` **no** lo pisa (probado sin BOM) |
| Tanda puntual | `opencode run --model <proveedor/modelo> --dir <worktree>` pisa el modelo en la invocación, sin tocar ningún archivo. Es la vía que usa la política de niveles |
| Límite de la sesión abierta | La configuración se resuelve al arrancar el proceso: un cambio de modelo **no** afecta a las sesiones ya abiertas. Por eso el Worker 4 del Lote 3 no pudo lanzar |
| Config muerta | El bloque `agent.roles` de los dos archivos (con `qwen3.8-plus`, que no existe en el proveedor) no lo lee ningún agente. Pendiente de que Victor lo retire |
| Dos planes a la vez | Cada plan usa su directorio y su override, o lanza cada tanda con `--model`. Ninguno edita el config global |

Detalle y las tres políticas: `../00-estandar-agentes/10-niveles-de-modelos.md`.

## Agentes por nivel (los seis de este repositorio)

`opencode.json` en la raíz del proyecto define un agente por nivel, para no depender del config global y para que dos planes no se pisen: `n0` gratis (documentación, Auditor, Documentador) · `n1` `deepseek-v4.1-flash` (por defecto) · `n2` `deepseek-v4-pro` **variante `high`** · `n3` `qwen3.7-plus` · `n4` `qwen3.8-max` variante `medium` · `n5` `qwen3.8-max` (requiere aprobación de Victor). Se eligen por nivel, nunca por nombre de modelo. Tabla y medidas: `../00-estandar-agentes/10-niveles-de-modelos.md`.

## Medición

- **Fuente real en este entorno: la base de opencode**, `%USERPROFILE%\.local\share\opencode\opencode.db`, tabla `session`: trae `model`, `cost`, `tokens_input/output/reasoning/cache_read/cache_write`, `parent_id` (subagentes) y `directory` por sesión. Es lo que hace posible medir por modelo. Hallazgo V-M5 del Lote 3.
- Script de niveles: `python scripts/niveles-modelos.py` (reparte los modelos medidos en los cinco niveles de consumo; `--niveles N`, `--modelo <subcadena>`, `--dir <ruta>`, `--json`). Creado el 2026-10-04.
- Script: `scripts/medir.py` (`python scripts/medir.py 8` lista las 8 sesiones más recientes). Lee los registros locales de sesión de Claude Code en `%USERPROFILE%\.claude\projects`, en las carpetas de este repositorio y de la app. Probado el 2026-10-01. Para sesiones de Cursor: por confirmar.

- Script del arranque: `scripts/arranque.py` (`python scripts/arranque.py 15`, y `--bloques` para ver de qué herramienta vino el contexto). Mide el contexto de la **primera llamada** de cada sesión —la línea base— y cuánto crece por su cuenta. Complementa a `medir.py`, que mide costo y calidad. Creado el 2026-10-02.
- Las sesiones de subagentes quedan dentro de la carpeta de la sesión del Orquestador, en `subagents/`, con un archivo `.meta.json` que trae la descripción.

## Ahorro de tokens

| Medida | Estado |
|---|---|
| Brief de Worker de 8 KB o menos, tope ~80 llamadas, lectura por Grep del ID | Vigente (`03-sesiones-contexto-y-handoff.md`) |
| Relevo del Orquestador medido entre olas | Vigente (`08-medicion-y-relevo.md`) |
| Recortar la salida de herramientas en los briefs: rangos de líneas, `tail`/`grep` en logs largos, subagentes que responden en una línea («operación rama → resultado») | Aplicar en los briefs. **La evidencia guarda el resultado real, no el recortado** |
| Límite de pensamiento (`MAX_THINKING_TOKENS`) | **No sirve**: usa razonamiento adaptativo y ignora ese presupuesto (verificado 2026-10-01). Se regula con el nivel de esfuerzo (`/effort`): ver `../00-estandar-agentes/09-orquestacion-y-modelos.md` |
| Compactación automática por ventana y hooks alrededor de la compactación | Verificados en la documentación oficial (2026-10-01); ver «Contexto y compactación» abajo |
| `AGENTS.md` por debajo de 200 líneas | Hecho el 2026-10-01 (324 a 180). El contenido movido está en `08-arquitectura-funcional-y-datos.md` |
| Lectura de flujos de negocio | **Cambiado el 2026-10-02.** Antes: el Planner y el Auditor leen todos los flujos. Ahora: los cuatro roles leen el índice de flujos y solo los que el Spec o el plan declara afectados, elegidos por su línea `Lee si:`. La lista completa solo con las dos excepciones de D10. Ahorro estimado ~28k tokens por agente, dos veces por plan |
| Tope de salida de herramientas en los briefs | **Promovido a regla del estándar el 2026-10-02** (estaba aquí como nota y no se cumplía). Ver `08-medicion-y-relevo.md` § Tope de salida de herramientas en los briefs |
| Línea base de arranque por sesión | **Medida el 2026-10-02.** `scripts/arranque.py`. Subagentes: 40k tokens de contexto en la primera llamada, muy estable (min 40k, max 41k). Sesión principal del Orquestador: 52k. De esos 40k, ~32k son el prompt del sistema y las herramientas —no los controla este repositorio—, 5.1k `AGENTS.md` y 3.0k el bloque de Skills. El ahorro posible está en el **crecimiento** de la sesión, no en el arranque |

## Git rutinario

`git merge <rama>` desde `main` sin cambiar de rama de trabajo, `git branch -vv` para ver adelantos y atrasos, `git push origin <rama>:<rama>` para subir una rama local. El merge a `main` del código solo lo hace el Orquestador después del paso 15 y con el verificador (`07-jev-verificador.md`).

## Contexto y compactación (verificado en la documentación oficial, 2026-10-01)

| Dato | Valor |
|---|---|
| Ventana del modelo principal | **1.000.000 de tokens** |
| Ventana del modelo de Worker git | **200.000 tokens** (tope duro) |
| Compactación por defecto del modelo principal | Recién a ~**967.000** tokens. Por eso un Orquestador pudo llegar a 564k sin que nada avisara: hasta ahí no se dispara nada |
| Cambiar el umbral | `/autocompact 350k` (se guarda en tu configuración de usuario como `autoCompactWindow`), o `claude --autocompact 350k` para un solo arranque, o la variable `CLAUDE_CODE_AUTO_COMPACT_WINDOW=350000` (solo número entero; manda sobre las otras). Rango: 100k a 1M. `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` (1 a 100) fija el porcentaje de esa ventana; solo puede bajar el umbral, y la documentación dice que aplica a conversaciones principales y subagentes |
| Hooks | `PreCompact` (filtro `auto` o `manual`; puede bloquear), `PostCompact` (solo observa) y `SessionStart` con filtro `compact`, que puede inyectar contexto al reanudar tras compactar |
| Costo | Compactar un contexto grande es en sí una llamada grande; `/clear` no cuesta nada |

**Qué no hay:** un porcentaje oficial a partir del cual el modelo empiece a fallar. La documentación no lo da. Los umbrales de abajo son una propuesta basada en las mediciones de este proyecto y se recalibran con ellas.

## Zonas propuestas

| Zona | Contexto | Qué se hace |
|---|---|---|
| Verde | Hasta 200k (20% de la ventana) | Meta del Worker. Las tandas medidas en 93k a 186k funcionaron bien |
| Amarilla | 200k a 300k | El Orquestador no abre frentes nuevos; cierra la ola en curso |
| Roja | Más de 300k | Relevo del Orquestador al terminar la ola (`08-medicion-y-relevo.md`) |
| Red de seguridad | 350k | Compactación automática, solo por si una ola se alarga y no se llegó al relevo |

Configuración propuesta (pendiente de que Victor la aplique): `/autocompact 350k`, más un hook `SessionStart` con filtro `compact` que recuerde al Orquestador ejecutar el script de medición, escribir el handoff en el progreso y entregar el prompt de relevo antes de seguir. Un Worker no se compacta: cierra su tanda y se lanza uno nuevo.

