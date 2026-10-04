# Orquestación y modelos

> **Estado: propuesto por Victor el 2026-10-02. Configurado y verificado el 2026-10-04.**
>
> Este archivo es la fuente de verdad de **roles, esfuerzo y Jev**. El **nivel de consumo de cada modelo** (los cinco niveles) está en [`10-niveles-de-modelos.md`](10-niveles-de-modelos.md), con la tabla medida y la vía para ejecutar un modelo sin depender de la configuración.
>
> **Dónde vive la configuración de verdad:** los modelos por rol están en el archivo **global** `~/.config/opencode/opencode.jsonc` (decisión de Victor del 2026-10-03, hallazgo OP7 del Lote 3). El `.opencode/config.json` de este repositorio **no define modelos**: aporta las claves que no son de modelo (umbrales de contexto, verificador, criterios de nivel) y se fusiona con el global. Un override por proyecto se pone en un `opencode.json` **en la raíz** del proyecto, que sí pisa al global (verificado el 2026-10-04).

## Principio

El Orquestador asigna modelos a los agentes según la complejidad de la tarea, optimizando costo sin sacrificar calidad. Jev valida acciones críticas. Los umbrales de contexto gobiernan el relevo.

## Modelos y niveles de esfuerzo por rol

Verificado el 2026-10-04 con `opencode debug config` (configuración resuelta) y `opencode agent list`. Esta tabla **no se inventa**: es lo que el harness tiene registrado.

| Rol (agente real del harness) | Modelo | Variante | Esfuerzo | Nivel de consumo |
|-----|-------------|----------|----------|------------------|
| Orquestador (`orchestrator`) | `opencode-go/qwen3.7-plus` | default | Medio | 3 |
| Worker base (`worker-plus`) | `opencode-go/deepseek-v4-pro` | **high** | Medio | 2 |
| Worker económico (`worker-flash`) | `opencode-go/deepseek-v4.1-flash` | default | Medio | 1 |
| Documentador (agente `general`) | `opencode-go/space-bunny-free` | default | Medio | 1 |
| Auditor (`auditor`) | `opencode-go/space-bunny-free` | default | Medio | 1 |
| Exploración (`explore`) | `opencode-go/qwen3.8-flash` | default | Medio | 2 |
| Verificador Jev (`jev`) | `typesafe/jev-1.13` | — | — | — |

La columna de nivel viene de [`10-niveles-de-modelos.md`](10-niveles-de-modelos.md) y se recalcula con `python scripts/niveles-modelos.py`.

**Además de los roles, este repositorio define un agente por nivel de consumo** (`n0` a `n5`) en el `opencode.json` de la raíz del proyecto. Se eligen por nivel, no por nombre de modelo, y no tocan el config global. La tabla, las medidas y cómo se lanzan están en [`10-niveles-de-modelos.md`](10-niveles-de-modelos.md).

**Dos advertencias verificadas el 2026-10-04, para que nadie las vuelva a descubrir:**

- **No existe un agente `planner`, ni `documenter`, ni `git`, ni `architect`.** `opencode debug agent planner` responde «Agent planner not found». Los modelos de esos roles no se pueden lanzar como subagentes: el Planner y el Documentador los hace el Orquestador o el agente `general`.
- **El bloque `agent.roles` de los dos archivos de configuración no lo lee nadie.** Sigue nombrando `qwen3.8-plus` y `qwen3.8-max` —`qwen3.8-plus` no existe en el proveedor—, y fue la causa del bloqueo del Worker 4 del Lote 3 (OP1). Está pendiente de que Victor lo retire: es configuración global y no la edita un agente por su cuenta.


### Política de esfuerzo

**Todos los agentes arrancan con esfuerzo medio por defecto.** No existe nivel "bajo".

| Nivel | Default | Cuándo se incrementa |
|-------|---------|----------------------|
| **Medio** | Sí (todos los roles) | — |
| **Alto** | No | Solo si el plan lo autoriza por fase |

### Incremento de esfuerzo

El esfuerzo **alto** no es automático: se solicita y autoriza de manera puntual.

1. **En el Gate 1** (aprobación del plan): el Orquestador declara qué fases requieren esfuerzo alto y por qué. Victor aprueba o rechaza.
2. **Durante la ejecución**: si una fase no contemplada requiere esfuerzo alto, el Orquestador suspende, solicita aprobación y registra el cambio.
3. **En el reporte final**: se listan todas las fases con su esfuerzo real usado (medio o alto).

### Tabla de esfuerzos en el plan

| Fase/Tarea | Esfuerzo default | Esfuerzo usado | Justificación | Aprobación Victor | Timestamp |
|------------|-----------------|----------------|---------------|-------------------|-----------|
| Migración de datos | Medio | Alto | Razonamiento profundo sobre esquema legacy | Aprobada | 2026-10-02 14:30 |
| Actualización flujos 14 y 16 | Medio | Medio | — | — | — |
| Documentación | Medio | Medio | — | — | — |

## Niveles de Worker

El Orquestador clasifica automáticamente cada tarea. Los nombres de abajo son los históricos; el nivel de consumo que hoy se asigna a cada uno está en [`10-niveles-de-modelos.md`](10-niveles-de-modelos.md) y se anota junto al nombre en el plan.

| Nivel | Criterios | Modelo configurado | Nivel de consumo | Esfuerzo | Aprobación |
|-------|-----------|--------|----------|----------|------------|
| **Flash** | Simple, bien especificada, sin ambigüedad, sin dependencias, sin riesgo | `worker-flash` → `deepseek-v4.1-flash` | 1 | Medio | No requiere |
| **Plus** | Requiere análisis, tiene dependencias, o afecta múltiples archivos/flujos | `worker-plus` → `deepseek-v4-pro` (variante `high`) | 2 | Medio | No requiere |
| **Max** | Razonamiento profundo, remoto, o riesgo alto | Sin agente propio: se lanza con `opencode run --model` (ver `10-niveles-de-modelos.md`) | 4 – 5 | Medio (Alto si el plan lo autoriza) | **Requiere aprobación de Victor** |


## Asignación dinámica de Workers durante el plan

### Al aprobar el plan (Gate 1)

Cuando Victor aprueba el plan, el Orquestador debe:

1. **Identificar las fases del plan** que requieren Workers
2. **Asignar el nivel de Worker** (Flash/Plus/Max) para cada fase, según los criterios de complejidad
3. **Declarar explícitamente** en el registro de decisiones:
   - Qué fases usarán Max (y por qué)
   - Qué fases usarán Plus
   - Qué fases usarán Flash
4. **Solicitar aprobación de Victor** para cualquier fase que use Max

**Ejemplo de declaración:**
```
Fase 1: Migración de datos → Worker Max (requiere aprobación)
Fase 2: Actualización de flujos 14 y 16 → Worker Plus
Fase 3: Documentación de cambios → Worker Flash
```

### Cambio de nivel o esfuerzo durante la ejecución

Si durante la implementación una fase requiere cambiar de nivel de Worker (ej: de Flash a Max) o incrementar el esfuerzo (de Medio a Alto):

1. **El Orquestador detecta la necesidad** (por complejidad emergente, dependencias no previstas, o riesgo identificado)
2. **Suspende la fase** hasta obtener aprobación
3. **Solicita aprobación de Victor** indicando:
   - Fase/tarea afectada
   - Nivel o esfuerzo original asignado
   - Nivel o esfuerzo solicitado y justificación
   - Impacto estimado (tiempo, costo)
4. **Registra el cambio** en el plan con:
   - Timestamp
   - Justificación del cambio
   - Aprobación de Victor (o rechazo)
   - Nuevo nivel o esfuerzo asignado

**No se ejecuta la fase con el nuevo nivel o esfuerzo hasta que Victor apruebe.**

### Registro de cambios de nivel

El plan debe incluir una tabla de cambios de nivel de Worker:

| Fase/Tarea | Nivel inicial | Nivel final | Justificación | Aprobación Victor | Timestamp |
|------------|---------------|-------------|---------------|-------------------|-----------|
| Migración de datos | Plus | Max | Dependencias no previstas en esquema legacy | Aprobada | 2026-10-02 14:30 |

### Registro de Max y esfuerzo alto

Todo uso de Max o esfuerzo alto se registra en el plan (con o sin aprobación de Victor). El registro incluye:
- Descripción de la tarea
- Justificación del nivel Max o esfuerzo alto
- Estado de la aprobación (pendiente, aprobada, rechazada)
- Resultado de la tarea

### Reporte final de esfuerzos

Al cerrar el plan, el Orquestador incluye en el reporte final una tabla con los esfuerzos reales usados por fase:

| Fase | Modelo asignado | Nivel de consumo | Esfuerzo default | Esfuerzo usado | Cambio autorizado |
|------|-----------------|------------------|------------------|----------------|-------------------|
| Fase 1 | `opencode-go/deepseek-v4.1-flash` | 1 | Medio | Medio | No |
| Fase 2 | `opencode-go/deepseek-v4-pro` (high) | 2 | Medio | Medio | No |
| Fase 3 | `opencode-go/qwen3.7-plus` | 3 | Medio | Medio | No |

## Acciones críticas (Jev)

Jev (`typesafe/jev-1.13`) valida acciones irreversibles antes de ejecutarlas.

### Cuándo se usa

- `merge` (especialmente a `main`)
- `push` (especialmente `--force` o a `main`)
- `delete` (archivos, ramas, worktrees)
- `migrate` (migraciones de base de datos)
- `branch` (crear o borrar ramas)
- `close` (cierre de plan)

### Umbrales de decisión

| Resultado de Jev | Acción del Orquestador |
|------------------|------------------------|
| ≥ 0.9 | Continuar |
| ≤ 0.1 | Bloquear (corregir y reintentar una vez; segundo bloqueo → escalar a Victor) |
| Entre 0.1 y 0.9 | Escalar al Orquestador para revisión (y a Victor si es necesario) |
| Sin respuesta | Acción destructiva: no ejecutar y escalar. No destructiva: ejecutar y registrar fallo. |

### Qué nunca se envía a Jev

Credenciales, claves, tokens, rutas de archivos de secretos, valores de variables de entorno ni contenido de archivos de configuración sensible.

## Umbrales de contexto

| Zona | Tokens | Acción |
|------|--------|--------|
| Verde | < 200k | Operación normal |
| Amarillo | 200k - 300k | No abrir frentes nuevos; cerrar ola en curso |
| Rojo | > 300k | Relevo del Orquestador al terminar la ola |

## Flujo de decisión del Orquestador

```
1. Victor inicia sesión → elige modelo del Orquestador (Plus o Max)
2. Orquestador lee configuración de roles, modelos y política de esfuerzo (default: medio)
3. Para cada tarea:
   a. Analizar complejidad (Flash/Plus/Max)
   b. Asignar esfuerzo medio por defecto
   c. Si Max o esfuerzo alto → solicitar aprobación de Victor
   d. Asignar agente con modelo y esfuerzo correspondiente
   e. Si la acción es crítica → consultar Jev antes de ejecutar
4. Monitorear contexto:
   a. Verde → continuar
   b. Amarillo → no abrir frentes nuevos
   c. Rojo → preparar relevo
5. Al cerrar el plan → incluir tabla de esfuerzos reales usados
```

## Agente Git

El agente Git ejecuta comandos mecánicos con el Worker económico (`worker-flash`, nivel 1):
- `git status`, `git branch`, `git log`, `git diff`
- `git add`, `git commit` (con mensaje del Orquestador)
- `git push` a rama de trabajo

**Requiere Jev:**
- `git merge` a `main`
- `git push --force`
- `git branch -D` (borrar rama)
- Cualquier operación destructiva

**No requiere aprobación de Victor** para operaciones rutinarias (commit, push a rama de trabajo, merge entre ramas de trabajo).

## Referencias

- Configuración: **global** `~/.config/opencode/opencode.jsonc` (modelos por rol) y, por proyecto, el `opencode.json` de la raíz (agentes por nivel `n0` a `n5` y overrides). `.opencode/config.json`: claves que no son de modelo.
- Niveles de modelos, benchmark por nivel y ejecución sin bloqueo de configuración: [`10-niveles-de-modelos.md`](10-niveles-de-modelos.md)
- Verificador de acciones: `07-verificador-de-acciones.md`
- Jev (detalles técnicos): `../01-contexto-repositorio/07-jev-verificador.md`
- Medición y modelos: `08-medicion-y-relevo.md`, `../01-contexto-repositorio/09-medicion-y-modelos.md`
