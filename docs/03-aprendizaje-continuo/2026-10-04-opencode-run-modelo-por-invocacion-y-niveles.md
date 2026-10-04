# Opencode: correr cualquier modelo por invocación, medirlo por nivel y no chocar con la configuración

**Origen:** plan `2026-10-02-observaciones-victor-lote-3-plan.md` (Enmienda E1), 2026-10-04. **Categoría:** `modelos/config` · `harness`. **Estado:** las tres políticas ya viven en `docs/00-estandar-agentes/10-niveles-de-modelos.md`; aquí queda el aprendizaje de trabajo.

## 1. El modelo del subagente no se elige en la llamada

La herramienta de subagentes acepta el **tipo de agente**, no el modelo. El modelo sale del agente en la configuración, y la configuración se resuelve **al arrancar el proceso**: un cambio posterior no afecta a las sesiones ya abiertas. De ahí vinieron dos bloqueos reales del Lote 3: el Worker 4 no pudo arrancar porque el config del repo apuntaba a `qwen3.8-plus` (modelo que no existe en el proveedor), y el Worker de la Tanda V corrió con otro modelo del que creía.

## 2. `opencode run --model` sí manda sobre el config

```powershell
opencode run --agent build --model opencode-go/deepseek-v4.1-flash --dir "<worktree>" --title "<etiqueta>" "<instrucción>"
```

Comprobado el 2026-10-04: la corrida arranca con ese modelo y el encabezado lo confirma (`build · deepseek-v4.1-flash`). Sirve para lanzar un Worker externo sin tocar ningún archivo de configuración, y `--dir` aíla el carril. Cada corrida queda en la base de opencode con su costo y sus tokens: eso es lo que hace posible medir después.

## 3. Dónde sí manda un override, y dónde no

| Archivo | ¿Pisa el modelo de un agente que ya está en el global? |
|---|---|
| `opencode.json` **en la raíz** del proyecto | **Sí** |
| `.opencode/config.json` | **No** (sí se fusiona, pero el global gana en `agent.<nombre>.model`) |
| `~/.config/opencode/opencode.jsonc` | Es la fuente de verdad compartida |

Medido con `opencode debug config` en un directorio de prueba, con el archivo **sin BOM** (con BOM el resultado es otro y el diagnostico sale mal).

## 4. La trampa que detiene a un Worker: el directorio externo

Un Worker lanzado con `opencode run --dir <worktree>` **no puede** leer con la herramienta de lectura un archivo fuera de ese directorio: el permiso se rechaza solo, sin humano que lo apruebe, y el Worker se detiene. Pasó dos veces el 2026-10-04: con el brief de la Tanda R6a (en el repositorio de documentación) y con el protocolo de migraciones.

**Dos|workarounds, y uno de ellos no vale para lo que creías:**

- **Brief o documento de apoyo:** copiarlo dentro del worktree y borrarlo al terminar. Es lo que se hizo con `_protocolo-migraciones.md`.
- **Credenciales de la base:** no hay workaround. El archivo está fuera del worktree y el permiso no se concede solo. Lo aplica **el Orquestador**, no el Worker, aunque el protocolo diga que lo aplica el Worker. Un brief de tanda con migraciones tiene que prever ese corte **desde el principio**, o la tanda se queda a medias.

## 5. El precio por token no predice el costo por tarea

Tres modelos con la misma tarea de resultado conocido:

| Nivel | Modelo | USD | Tokens | Min | Acierto |
|---|---|---|---|---|---|
| 1 | `deepseek-v4.1-flash` | 0,0369 | 1 467 458 | 2,8 | 8/8 |
| 2 | `deepseek-v4-pro` (`high`) | 0,0858 | 809 909 | 2,2 | 7/8 |
| 3 | `qwen3.7-plus` | 0,0477 | 325 972 | 2,3 | 7/8 |

El más barato por token consumió **cuatro veces más tokens** que el nivel 3 y ganó en calidad. La regla que sale de aquí: **el nivel ordena el precio, y el consumo por tarea lo mide el benchmark**; si un modelo barato consume más, la tarea se trata como del modelo caro. Otra vez: con `n=1` no se ordena por latencia (el mismo modelo dio 18,3 s y 61,8 s en dos corridas el día anterior).

## 6. Instrumento

`scripts/niveles-modelos.py`: lee la base de opencode en modo solo lectura, agrega por modelo y variante, y reparte en cinco bandas de USD por millión de tokens. Marca la muestra baja y el «solo subagentes». Con `--json` alimenta a otro script.
