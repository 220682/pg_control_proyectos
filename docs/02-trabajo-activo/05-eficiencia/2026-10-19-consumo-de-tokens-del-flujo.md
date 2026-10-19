# Medición y eficiencia — consumo de tokens del flujo (27-sep a 19-oct de 2026)

> Pedido directo de Victor el 2026-10-19: «cómo podemos mejorar el consumo de tokens y qué debemos cambiar… y aplica las mejoras que encuentres a nuestra política». Hecho por el Orquestador en el papel de Analista del flujo, por invocación directa de Victor. No es el informe de un plan: analiza todo el período medido.

## Cómo se midió

- `python scripts/medir.py --resumen --desde 2026-09-27`: 217 sesiones, 10.427 llamadas, 1.657 M de caché leída y 51 M de caché creada.
- Agrupé por rol leyendo la columna «quién» y comparé contra las metas de `08-medicion-y-relevo.md`. El contexto por sesión salió de `scripts/arranque.py --bloques`.
- **Simulación del tope de relevo:** modelo lineal (el contexto crece parejo desde ~56k hasta el máximo medido de la sesión; cada relevo arranca en ~81k). Es una **estimación**, no una medición.
- **Límite:** la salida de los subagentes casi no queda en el registro, así que el análisis es de caché leída y creada. No se convirtió a dinero (sin tabla de precios verificada).

## Resultados

| Rol | Sesiones | Llamadas | Caché leída | % del total | Caché por llamada |
|---|---|---|---|---|---|
| Orquestador | 36 | 4.447 | 885 M | 53 % | 199k |
| Worker | 125 | 4.636 | 515 M | 31 % | 111k |
| Planner | 14 | 606 | 167 M | 10 % | 276k |
| Documentador | 16 | 445 | 62 M | 4 % | 139k |
| Auditor | 4 | 150 | 22 M | 1 % | 148k |
| Worker git | 22 | 143 | 6 M | 0,4 % | 43k |

| Indicador | Valor | Meta o referencia | Causa |
|---|---|---|---|
| Orquestador con contexto máximo sobre 300k | 16 de 36 sesiones; 13 de 23 desde el 1-oct | relevo a ~300k (`08`) | Desde el 1-oct la compactación a 350k frenó los excesos (máximo 318k, antes 596k), pero las sesiones corren pegadas al tope: promedio ~200k por llamada |
| Orquestador en Opus | 5 sesiones, 249 M = 36 % del Orquestador desde el 1-oct y 15 % de todo | «No se usa Opus» (decisión del 2026-10-01) | Las sesiones se abrieron en Opus el 15 y el 17 de octubre; nada en el arranque del flujo lo detecta |
| Planner: dos sesiones grandes | 116 M de 167 M (70 % del Planner); contextos de 685k y 687k | sin meta escrita | La meta de 80 llamadas y 200k solo se escribió para el Worker |
| Subagentes de trabajo fuera de meta | 29 de 159 (18 %), que gastaron 436 M de 766 M (57 %) | 80 llamadas, 200k de contexto, 12 M de caché | Tandas grandes y verificaciones con navegador: la mayor, 249 llamadas y 40 M; otra de 154 llamadas |
| Documentador | 5 sesiones en Sonnet = 49 M; 11 en Haiku = 13 M | por rol, `09` | Las de Sonnet son cierres de tanda e integración de reglas; las de Haiku, cierres mecánicos |
| Resultados de herramienta del propio Orquestador | hasta 1,31 M de caracteres en una sesión (Bash 754k, Read 479k); bloques sueltos de 37k a 47k caracteres | tope de salida (`08`), escrito solo para briefs | Cada resultado se vuelve a pagar en todas las llamadas siguientes |
| Línea base de arranque | 44k a 46k (subagente), 56k a 63k (principal) | medida el 2026-10-02: 40k y 52k | ~32k son prompt del sistema y herramientas; el repositorio no los controla |

**Simulación del tope de relevo del Orquestador (desde el 1-oct, 701 M de caché leída):**

| Tope de relevo | Caché leída | Ahorro | Sesiones (reales: 23) |
|---|---|---|---|
| 300k (la regla actual, cumplida al pie de la letra) | 564 M | 20 % | ~37 |
| 250k | 489 M | 30 % | ~43 |
| **200k** | **450 M** | **36 % (~250 M, 15 % de todo el período)** | **~46** |
| 150k | 385 M | 45 % | ~81 |

De 300k a 200k se ahorra mucho con pocos relevos más; de 200k a 150k casi se duplican los relevos para ganar 9 puntos. El punto de quiebre está en 200k.

## Mejoras propuestas a la política

Victor las aprobó en bloque el 2026-10-19 («aplícalas a nuestra política… a las que corresponda»), salvo tres (5, 7 y 9) que quedaron pendientes de su decisión y las resolvió más tarde el mismo día. Todas están aplicadas.

| N.º | Qué se observó | Propuesta | Documento afectado | Decisión del Responsable humano |
|---|---|---|---|---|
| 1 | El Orquestador pasa la vida cerca del tope y paga ~0,2 M de caché por llamada | Relevo a 200k (verde hasta 150k, amarillo 150k a 200k, rojo desde 200k al terminar la ola); compactación automática de seguridad a 250k | `08-medicion-y-relevo.md`, `09-orquestacion-y-modelos.md`, `01-contexto-repositorio/09-medicion-y-modelos.md`, Skill `seguir-flujo-de-planes` | Aplicada (2026-10-19). Victor cambió su configuración el mismo día (`/autocompact 250k`, para Sonnet 5.5) |
| 2 | Dos sesiones de Planner = 70 % del Planner | El Planner tiene las mismas metas que un Worker; un plan que no cabe se redacta en partes (plan base y briefs por grupo de tandas), un Planner por parte | `08-medicion-y-relevo.md`, `02-roles-y-delegacion.md` | Aplicada (2026-10-19) |
| 3 | El Orquestador llena su contexto con lecturas y consola sin tope | El tope de salida de herramientas también rige al Orquestador; mirar muchos archivos grandes se delega a un subagente que responde en un párrafo; al cerrar cada ola se mide qué herramienta llenó el contexto | `08-medicion-y-relevo.md` | Aplicada (2026-10-19) |
| 4 | Cinco sesiones del Orquestador en Opus pese a la política | Al activar el flujo, el Orquestador declara su modelo y esfuerzo y avisa a Victor si trae Opus | Skill `seguir-flujo-de-planes` | Aplicada (2026-10-19) |
| 5 | Documentador en Sonnet: 31 % de sus sesiones, 79 % de su consumo | Haiku por defecto para cierres de tanda; Sonnet solo para integrar reglas en un flujo. No hay evidencia de calidad que lo respalde ni lo descarte | `09-orquestacion-y-modelos.md` | Aplicada (2026-10-19): Victor: «usemos a Haiku». Queda Haiku por defecto, con Sonnet solo si una tanda debe integrar una regla en un flujo existente |
| 6 | Tandas con navegador que pasan de 80 llamadas (154 y 249) | Partir la verificación por grupos de pantallas desde el brief; la meta ya existe, lo que falta es el cumplimiento | Briefs de cada plan (no un documento del estándar) | No requiere cambio de política; el Planner lo aplica al partir tandas |
| 7 | Los documentos de modelos describen opencode (qwen, deepseek) pero las sesiones medidas desde el 15-oct son de Claude Code (Sonnet y Haiku); la base de opencode se escribió por última vez el 2026-10-17 | Revisar qué parte de `09` y `10` y de `AGENTS.md` (niveles `n0` a `n5`) sigue vigente y agregar el equivalente para Claude Code | `09-orquestacion-y-modelos.md`, `10-niveles-de-modelos.md`, `01-contexto-repositorio/09-medicion-y-modelos.md`, `AGENTS.md` | Aplicada (2026-10-19): Victor: «solo usamos mayormente Claude Code». `09` y `01/09` traen ahora la tabla de Claude Code y dejan opencode como referencia; `AGENTS.md` apunta a `09`; `10` queda marcado como solo opencode |
| 8 | `AGENTS.md` lo lee cada agente en cada llamada (~4,6k tokens; unas 10.400 llamadas = ~48 M) | No se le agregó nada: cada línea nueva se paga en todas las llamadas. Los topes viven en `08` y en el Skill | `AGENTS.md` | Sin cambio, a propósito |
| 9 | Skills de redes sociales y otras herramientas del usuario aparecen en el arranque de cada sesión de este repositorio | Desactivar en este proyecto las que no se usen; no se midió su peso exacto (estimado ≤ 1 % del total) | Configuración local del proyecto (`.claude/settings.local.json`, ignorada por git) | Aplicada (2026-10-19): Victor: no tienen por qué estar vigentes en todos los repositorios. Diez skills puestos en `off` con `skillOverrides` solo en este proyecto; falta comprobar en la sesión nueva que ya no aparecen |

## Qué cambia en cómo trabajamos

1. **El Orquestador releva a los 200k.** Entre olas, con handoff y prompt de relevo. Estimo el doble de relevos que hoy; a cambio gasta ~36 % menos.
2. **Un Planner que no cabe en 80 llamadas se parte**: plan base primero, briefs por grupo de tandas después, un subagente por parte.
3. **Las lecturas grandes las hace un subagente** y devuelve un párrafo, también cuando quien las pide es el Orquestador.
4. **El modelo del Orquestador se declara al activar el flujo.**

## Cómo repetir la medición

`python scripts/medir.py --resumen --desde 2026-09-27` para los totales y `python scripts/arranque.py 15 --bloques` para ver qué herramienta llenó cada contexto. Volver a medir al cierre del siguiente plan para confirmar el ahorro del relevo a 200k.
