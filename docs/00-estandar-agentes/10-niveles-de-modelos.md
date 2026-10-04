# Niveles de modelos, benchmark por nivel y ejecución sin bloqueo de configuración

> **Estado: aprobado por Victor el 2026-10-04.** Define tres políticas: (1) los **cinco niveles de modelos** según su consumo de tokens, (2) el **benchmark por nivel** que se corre antes de asignar un modelo a una tanda, y (3) la **vía para ejecutar el modelo que el nivel pida sin que la configuración lo impida**, incluso con dos planes simultáneos.
>
> Complementa a [`09-orquestacion-y-modelos.md`](09-orquestacion-y-modelos.md), que sigue siendo la fuente de verdad de **roles, esfuerzo y Jev**. Este archivo no repite esa tabla: solo ordena los modelos por consumo y dice cómo ejecutar cada nivel.

## Por qué existe

El 2026-10-03 y el 2026-10-04 hubo que trabajar con dos Orquestadores distintos sobre los mismos roles y con modelos distintos, porque el modelo de cada agente vive en un archivo de configuración compartido que se resuelve al arrancar el proceso. De ahí salieron dos problemas, ambos medidos: el Worker más barato disponible no era el que estaba configurado, y un segundo plan no podía elegir su propio modelo sin tocar el archivo que el primero estaba usando. Las tres políticas de abajo quitan los dos problemas.

## Política 1 — Los cinco niveles de modelos

### Qué define el nivel

El nivel de un modelo es **su precio por token consumido**, medido, no supuesto:

```
USD por millón de tokens = costo total de las sesiones del modelo / tokens totales de esas sesiones × 1 000 000
```

Tokens totales = entrada + salida + razonamiento + caché de lectura + caché de escritura. La fuente es la base de opencode (`%USERPROFILE%\.local\share\opencode\opencode.db`, tabla `session`), que trae costo y tokens por sesión, incluidos los subagentes. Script: [`scripts/niveles-modelos.py`](../../scripts/niveles-modelos.py).

**Nivel 1 es lo que menos consume; nivel 5, lo que más.** Las bandas por defecto:

| Nivel | USD por millón de tokens | Para qué |
|---|---|---|
| **1** | < 0,02 | Tarea simple, mecánica o de documentación acotada |
| **2** | 0,02 – 0,06 | Worker de código bien especificado, sin decisiones de diseño |
| **3** | 0,06 – 0,20 | Tanda con análisis, dependencias o varios archivos y flujos |
| **4** | 0,20 – 1,00 | Razonamiento sobre regla de negocio nueva o migración |
| **5** | ≥ 1,00 | Solo con aprobación de Victor, por riesgo o ambigüedad reales |

Bandas por escala logarítmica, no por cuartiles: el salto real de precio entre modelos va de 0,011 a 1,97 USD por millón, casi tres órdenes de magnitud. Un modelo con costo 0 (free) cae en **nivel 1** aunque consuma muchos tokens.

### La tabla medida (2026-10-04, base de opencode, 227 sesiones del 2026-10-01 al 2026-10-04)

| Nivel | Modelos medidos | USD/millón | Sesiones | USD por sesión |
|---|---|---|---|---|
| **1** | `space-bunny-free` (y su variante `max`), `big-pickle`, `mimo-v2.6-flash-free`, `deepseek-v4.1-flash` y `deepseek-v4.1-flash [high]` | 0,0000 – 0,0128 | 16, 7, 2, 9, 16, 4 | 0,00 – 0,12 |
| **2** | `qwen3.8-flash`, `glm-5.3-flash`, `deepseek-v4-pro [high]` | 0,0302 – 0,0563 | 14, 16, 21 | 0,04 – 0,26 |
| **3** | `deepseek-v4-flash`, `qwen3.7-plus`, `mimo-v2.6-flash` | 0,0847 – 0,1442 | 10, 31, 1 | 0,00 – 0,58 |
| **4** | `deepseek-v4-pro` (default), `minimax-m3`, `qwen3.8-max [medium]`, `mimo-v2.6-pro`, `kimi-k2.7-code` | 0,3015 – 0,8423 | 3, 2, 1, 1, 2 | 0,01 – 3,06 |
| **5** | `glm-5.3`, `qwen3.8-max` (default), `kimi-k3` | 1,0895 – 1,9683 | 2, 3, 1 | 0,04 – 0,09 |

Cuatro lecturas que la tabla da y que no se ven sin medir:

1. **La variante cambia el nivel.** `deepseek-v4-pro [high]` está en nivel 2 (0,056) y `deepseek-v4-pro` default en nivel 4 (0,597): **diez veces**. `qwen3.8-max [medium]` está en nivel 4 y el default en nivel 5. Un modelo no es un modelo: es un modelo **con su variante**.
2. **El precio por token no dice cuánto consume un modelo.** `space-bunny-free [max]` promedió 19,6 millones de tokens por sesión; `deepseek-v4-flash`, 30 600. Por eso el nivel ordena precio y **el consumo por tarea lo mide el benchmark** (Política 2).
3. **Muestra baja.** Con menos de 3 sesiones el nivel es provisional; el script lo marca en la columna «nota». `qwen3.8-max [medium]` (1 sesión, 3,06 USD) es el ejemplo: no se sabe si es de nivel 4 o de nivel 5 hasta tener más datos.
4. **El gasto real está donde están las sesiones largas.** `qwen3.7-plus` acumula 18,11 de los 30,09 USD medidos (31 sesiones, 0,58 por sesión); `deepseek-v4-pro [high]`, 5,40 (21 sesiones). Cambiar el nivel del Orquestador y del Worker base mueve más dinero que cualquier modelo de nivel 5.

### Regla de seguridad: el consumo manda sobre el precio

Si el benchmark muestra que un modelo de nivel bajo consume más tokens por tarea que uno de nivel alto, **la tanda se trata como si fuera del nivel más caro de los dos**. El objetivo es el costo total de la tarea, no el precio de la ficha del modelo.

### Qué nivel usa cada tipo de tarea

| Tipo de tarea | Nivel de partida | Nota |
|---|---|---|
| Documentación acotada, índice, tabla de un flujo, resumen de cierre | 1 | Es lo que más se repite en un plan |
| Worker de código con el brief cerrado, de un archivo acotado | 2 | |
| Tanda con análisis, dependencias o varios archivos y flujos | 3 | |
| Migración con candado, o regla de negocio nueva que hay que redactar | 4 | |
| Razonamiento profundo con riesgo real, o tarea ambigua sin Spec | 5 | **Requiere aprobación de Victor**, y se registra en el plan |
| Orquestador de un plan | 3 – 5 | Lo elige Victor al abrir la sesión; se registra en el plan |

El nivel **sustituye** a los nombres Flash / Plus / Max de `09-orquestacion-y-modelos.md` como forma de clasificar la tarea: el nombre histórico («Plus») y el nivel («3») se anotan juntos en el plan. `09` conserva los criterios de clasificación y las reglas de aprobación; este archivo los traduce a niveles medidos.

### Cuándo se recalculan los niveles

Al abrir un plan, al cambiar de proveedor o al pasar 30 días sin medición. Nunca durante una tanda: cambiar el nivel de un Worker en marcha es un cambio de plan y se registra como tal.

### Los agentes por nivel (`n0` a `n5`)

Para que «usa un agente de nivel 3» sea una orden y no una discusión, este repositorio define **un agente por nivel** en el `opencode.json` de la raíz. Cada uno trae su modelo, su variante y su esfuerzo ya decididos:

| Agente | Modelo | Variante | Nivel | USD/millón (medido) | Para qué |
|---|---|---|---|---|---|
| `n0` | `opencode-go/space-bunny-free` | — | **0** (costo 0) | 0,0000 | Documentación, redacción, revisión de solo lectura, Auditor y Documentador |
| `n1` | `opencode-go/deepseek-v4.1-flash` | — | **1** | 0,0128 | Tarea simple o bien especificada; **por defecto de este repositorio** |
| `n2` | `opencode-go/deepseek-v4-pro` | **`high`** | **2** | 0,0563 | Tanda con análisis o varios archivos, sin regla nueva |
| `n3` | `opencode-go/qwen3.7-plus` | — | **3** | 0,1442 | Regla de negocio nueva, varios flujos, o el Orquestador de un plan |
| `n4` | `opencode-go/qwen3.8-max` | `medium` | **4** | 0,3607 (una sesión) | Riesgo real: migración con candado, decisión de diseño que no se puede deshacer |
| `n5` | `opencode-go/qwen3.8-max` | — | **5** | 1,9526 | **Solo con aprobación de Victor.** Ambigüedad que una Spec no resuelve |

Dos avisos que están en el propio archivo, porque son los que hacen fallar la elección:

- **`n2` solo es nivel 2 con la variante `high`.** El mismo modelo en `default` costó 0,597: diez veces más. Si alguien quita la variante sin querer, el nivel cambia solo.
- **`n4` es provisional**: una sola sesión medida. Para una migración, `n2` sale más barato y ya lo aplicó un Worker sin incidentes (Tanda M del Lote 3).

Cómo se lanza un nivel:

```powershell
# como subagente, en una sesión nueva (la lista de subagentes incluye n0 a n5)
opencode run --agent n3 --dir "<worktree>" "<instrucción>"

# o por invocación, sin depender de ningún archivo de configuración
opencode run --agent build --model opencode-go/qwen3.7-plus --dir "<worktree>" "<instrucción>"
```

**Este `opencode.json` no toca el config global.** Es un archivo del proyecto con claves nuevas, y la precedencia verificada (hecho 2) hace quechanging un nivel aquí no afecte a otro proyecto ni a otro plan que estén corriendo. Los roles del config global (`worker-flash`, `worker-plus`, `orchestrator`, `auditor`) siguen como estaban.

## Política 2 — Benchmark por nivel antes de asignar

### Qué se pide

Cuando Victor dice «busca modelos de nivel N» o al abrir un plan con más de tres Workers, el Orquestador corre un benchmark **de los modelos del nivel pedido** antes de asignarlos. No se asigna un modelo sin haberlo medido en una tarea parecida a la que va a hacer.

### Cómo se corre

Cada modelo es una invocación suelta, con la tarea completa en el prompt y sin depender de la configuración de roles:

```powershell
opencode run --agent build --model opencode-go/<modelo> --variant <high|default> `
  --dir "<worktree>" --title "bench-<nivel>-<modelo>" "<la tarea, con su resultado esperado>"
```

Verificado el 2026-10-04: `--model` pisa lo que diga la configuración del agente, y el encabezado de la salida confirma con qué modelo corrió (`build · deepseek-v4-flash`). El script `niveles-modelos.py` mide después lo que esa corrida dejó en la base.

### Qué se mide y qué se registra

Por modelo: **USD de la corrida**, **tokens**, **minutos**, **si el resultado es correcto** y **cuántas llamadas tomó**. Con eso se responde: ¿el modelo más barato del nivel acertó la tarea? La respuesta se escribe en el plan, en la tabla de asignación de las tandas.

```
Nivel pedido: 3
| Modelo | USD | Tokens | Min | Correcto | Llamadas | Veredicto |
|---|---|---|---|---|---|---|
| deepseek-v4-flash | … | … | … | sí/no | … | va / no va |
```

### Tres reglas que el benchmark no puede saltarse

1. **La tarea tiene resultado conocido.** Sin un resultado contra el que comparar, el benchmark mide latencia y nada más. El 2026-10-03 uno con 10 modelos y 4 preguntas dio 10 aciertos: no discriminó.
2. **Con n=1 no se ordena por latencia.** El mismo modelo dio 18,3 s y 61,8 s en dos corridas idénticas (2026-10-03, `glm-5.3-flash`). Dos corridas por modelo es el mínimo para hablar de tiempo.
3. **Un modelo que no existe no entra al benchmark.** La lista real sale de `opencode models <proveedor>`, no de la memoria ni de la tabla de este archivo. El 2026-10-03, `qwen3.8-plus` no existía en el proveedor y bloqueó seis roles.

## Política 3 — La configuración no es una limitación

### Los cinco hechos verificados (2026-10-04, opencode 1.18.34)

| # | Hecho | Cómo se comprobó |
|---|---|---|
| 1 | **La herramienta de subagentes no acepta modelo.** El modelo del subagente viene del agente en la configuración; en la llamada solo se elige el tipo de agente | Definición de la herramienta `task` de esta sesión: no tiene parámetro de modelo |
| 2 | **`opencode.json` en la raíz del proyecto sí pisa al global.** Un override de `agent.worker-flash.model` en la raíz se resolvió con el modelo del proyecto | `opencode debug config` en un directorio de prueba |
| 3 | **`.opencode/config.json` no pisa el modelo de un agente ya definido en el global.** El mismo override en esa ruta dejó ganar al global (probado sin BOM) | `opencode debug config`, dos rutas comparadas |
| 4 | **`opencode run --model` pisa todo en la llamada**, sin tocar ningún archivo de configuración | Corrida real: `opencode run --agent build --model opencode-go/deepseek-v4-flash` respondió `build · deepseek-v4-flash` |
| 5 | **La configuración se resuelve al arrancar el proceso.** Un cambio posterior no afecta a las sesiones ya abiertas | Nota vigente en el propio archivo global, y el Worker 4 del Lote 3 no pudo lanzar por un cambio de modelo no aplicado |

### Qué hacer en cada caso

| Necesidad | Vía | Coste |
|---|---|---|
| Asignar un modelo por rol, para todas las sesiones de un proyecto | `opencode.json` **en la raíz** de ese proyecto (hecho 2) | Un archivo por proyecto, versionable |
| Correr **una** tanda con un modelo puntual, sin cambiar nada | `opencode run --model` (hecho 4) | Ninguno: es explícito en la invocación |
| Cambiar el modelo de un subagente **de esta sesión ya abierta** | No se puede (hechos 1 y 5) | La sesión se cierra y se abre otra, o el Worker se lanza con `opencode run` |
| Cambiar el modelo de un rol para todas partes | Pregunta a Victor | Él decide si se edita el config global |

### Dos (o más) planes a la vez

El conflicto de origen venía de que el modelo de cada rol vivía en un único archivo compartido: un segundo plan necesitaba el suyo y pisaba el del primero. Con los hechos de arriba **el conflicto desaparece sin tocar el archivo global**:

1. **Cada plan trabaja en su directorio**, y el override va en el `opencode.json` de ese directorio (hecho 2). Un plan en el worktree del repositorio de código y otro en el repositorio de documentación no se ven.
2. **Si dos planes comparten directorio**, no se edita la configuración: cada tanda se lanza con `opencode run --model … --dir …` (hecho 4). El modelo viaja en la invocación, que es donde debe estar si hay más de un Orquestador.
3. **El agente que más se repita es el que se declara en la configuración**, para que el Worker se pueda lanzar como subagente (herramienta `task`). Si es un nivel raro, se usa `opencode run` y el subagente no se usa para ese caso.
4. **El config global no se edita para acomodar un plan.** Es la fuente de verdad compartida entre proyectos; si un plan necesita un modelo distinto, lo lanza con `--model` y lo deja registrado en el plan.

### La regla corta

> El nivel decide **qué modelo**; la invocación decide **con cuál se corre**. Un plan nunca se frena porque el modelo que necesita no esté en la configuración: se lanza con `opencode run --model`.

## Lo que no se hace

- **No se inventa un nivel** por nombre de modelo. El nivel se lee del script; si el proveedor cambia los precios, se vuelve a correr.
- **No se asigna un modelo sin benchmark** cuando la tarea no se parece a ninguna ya medida.
- **No se sube a un nivel 5 por comodidad.** La subida se justifica con riesgo o ambigñedad concretos y se registra; el criterio del estándar es que el nivel alto es excepcional, no la regla.
- **No se mide calidad con una tarea de respuesta conocida si todos la acertan.** El instrumento no discrimina, y se dice.
- **No se edita el config global sin que Victor lo pida.** Dos planes simultáneos se resuelven con overrides por directorio o con `--model`.

## Referencias

- Roles, esfuerzo y Jev: [`09-orquestacion-y-modelos.md`](09-orquestacion-y-modelos.md)
- Medición de sesiones y relevo: [`08-medicion-y-relevo.md`](08-medicion-y-relevo.md)
- Rol del Orquestador y prohibiciones: [`02-roles-y-delegacion.md`](02-roles-y-delegacion.md)
- Fuente de medición en este repositorio: [`../01-contexto-repositorio/09-medicion-y-modelos.md`](../01-contexto-repositorio/09-medicion-y-modelos.md)
- Instrumento: [`scripts/niveles-modelos.py`](../../scripts/niveles-modelos.py)
