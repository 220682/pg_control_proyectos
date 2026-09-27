> **Nota:** copia de referencia, solo para lectura del usuario. No es el orquestador
> activo de este proyecto ni se integra al sistema — es la versión más actualizada
> de la metodología `raiz.md`, tomada de `pg_dossier_calidad-agente_plan_calidad/gestion_dossier/base/raiz.md`
> (v1.4.0, 2026-09-14).

# Aprendizaje continuo — metodología raíz

> **Qué es este archivo:** la columna vertebral del sistema. Describe *cómo* se diseña un proyecto con memoria MD.
> **Portable:** cópialo a otros repos tal cual. No nombra ninguna empresa,
> cliente ni producto concreto — si acabas escribiendo uno aquí, va al orquestador.
> **Relación:** de aquí nace el orquestador del proyecto (`claude.md o agents.md - solo uno de ambos`), que adapta esta metodología al dominio actual.

---

## 1. Idea central

El cerebro del proyecto **no es el chat**. Son archivos Markdown que se alimentan en cada sesión.

| Concepto                                      | Definición                                                                                                                                                                                                            |
| --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Metodología** (`raiz.md`)          | Reglas universales: carpetas, comandos de sesión, plantillas, ciclo de mejora                                                                                                                                         |
| **Orquestador** (`claude.md`)         | Agente que te habla; nace de`raiz.md` y conoce *este* proyecto                                                                                                                                                     |
| **Dominios**                            | Grandes áreas del negocio (ej. empresa / producto / operación)                                                                                                                                                       |
| **Playbook**                            | MD de una actividad concreta (ej. "creación de videos Facebook")                                                                                                                                                      |
| **Skill** (`base/skills/<nombre>.md`) | Técnica puntual reutilizable — no una actividad completa — que el usuario marca explícitamente como digna de repetir. Vive fuera de los dominios: aplica sin importar en qué dominio o playbook vuelva a aparecer |
| **Salidas / publicidad**                | Productos derivados (imágenes, videos, campañas) — no son el dominio "empresa" ni el "producto"; se agrupan como salidas                                                                                            |
| **Índice generado**                    | `INDICE.md` no se escribe a mano: un script lo regenera desde el frontmatter de cada MD, así el estado real y el catálogo no pueden divergir                                                                       |
| **Fuente de verdad de datos**           | JSON u otro archivo canónico de precios/contacto (si existe); los MD apuntan ahí, no duplican cifras que cambian                                                                                                     |

**Regla de oro:** si ya hay un playbook aprobado, el agente **parte de ese resultado** (mejorar o repetir). No reinventar el procedimiento en cada chat.

---

## 2. Estructura de carpetas (plantilla)

**v1.3.0 — los dominios viven en la RAÍZ del proyecto, no dentro de `base/`.**
`base/` es solo el sistema de memoria (metodología + orquestador + índice); cada
dominio/rama del negocio es una carpeta hermana, con su propio `MEMORIA.md`.
Esto habilita que cada dominio sea también una rama git independiente
(worktree) — ver §9.

```
proyecto/
├── base/                   ← SOLO sistema de memoria
│   ├── raiz.md             ← ESTE archivo (metodología)
│   ├── claude.md           ← orquestador del proyecto (nace de raiz.md)
│   ├── INDICE.md           ← catálogo corto de TODOS los MD (incluye dominios)
│   ├── SESION.md           ← checkpoint de la sesión actual (opcional)
│   ├── skills/                      ← técnicas puntuales reutilizables (§10)
│   │   ├── INDICE.md                ← tabla generada, no a mano
│   │   └── <nombre-skill>.md        ← un archivo por skill
│   └── scripts/
│       ├── generar_indice.py        ← escanea base/ Y cada carpeta de dominio
│       └── generar_indice_skills.py ← arma skills/INDICE.md desde el frontmatter de skills/*.md
│
├── <dominio-a>/            ← ej. empresa/ (carpeta hermana de base/)
│   ├── MEMORIA.md          ← historial, pendientes, últimos merges (obligatorio)
│   ├── <canal-o-tema>.md   ← playbooks del dominio
│   └── <salidas>/          ← publicidad / assets derivados
│
└── <dominio-b>/            ← ej. whatsapp/ o producto/
    ├── MEMORIA.md
    └── ...
```

### Cómo nombra el orquestador al instalarse en un proyecto nuevo

1. Leer `raiz.md` (metodología).
2. Crear `base/claude.md` con: objetivo del proyecto, dominios, rutas a INDICE, comandos de sesión.
3. Crear `base/INDICE.md` vacío o con los primeros playbooks.
4. Crear carpetas de dominio **al nivel de la raíz del proyecto** (hermanas de `base/`) según el negocio real — no copiar nombres a ciegas.
5. Cada carpeta de dominio lleva su `MEMORIA.md` desde el primer commit.
6. Registrar la lista de carpetas de dominio en `base/scripts/generar_indice.py` (variable `CARPETAS_DOMINIO`) para que el índice las vea.

---

## 3. Mapa visual del sistema

```text
                    ┌─────────────────────┐
                    │      raiz.md        │
                    │  (metodología)      │
                    └──────────┬──────────┘
                               │ nace / gobierna
                               ▼
                    ┌─────────────────────┐
                    │     claude.md       │
                    │   (orquestador)     │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        ┌──────────┐    ┌──────────┐    ┌──────────────┐
        │ dominio  │    │ dominio  │    │  INDICE.md   │
        │    A     │    │    B     │    │  (catálogo)  │
        └────┬─────┘    └────┬─────┘    └──────────────┘
             │               │
             ▼               ▼
        playbooks        playbooks
        + salidas        + hitos / etc.
```

**Flujo de una tarea**

```text
Usuario → claude.md → ¿existe playbook en INDICE?
                         │
            no ──────────┤────────── sí
            ▼            │           ▼
   "Actividad nueva:     │    Leer playbook
    ¿creo su MD?"        │    Ejecutar / mejorar
                         │    desde lo aprobado
                         ▼
              (al cerrar sesión) actualizar MDs
```

---

## 4. Comandos de sesión (obligatorios)

| Frase del usuario                                    | Qué hace el orquestador                                                                                                                                               |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **inicia sesión** / **iniciar sesión** | Leer`claude.md` + `INDICE.md` (solo nombres/roles). Responder listo + dominios disponibles. **No** leer todos los playbooks aún.                            |
| **cierra sesión** / **cerrar sesión**  | Consolidar aprendizajes, mejoras y decisiones en los MD tocados + actualizar`INDICE.md` + nota breve en `claude.md` si cambió el mapa. Confirmar qué se guardó. |
| Tarea concreta (ej. "crea un video…")               | Buscar playbook → si no hay, proponer crear MD → si hay, ejecutar según ese MD.                                                                                     |

### Checkpoint

Escribir notas crudas en `SESION.md`. **No** reescribir playbooks a medias: la
consolidación real ocurre en **cierra sesión**.

**Se evaluó un cron cada 30 min y se descartó.** Un temporizador no sabe qué pasó
en la conversación: dispararía igual tras una hora de trabajo que tras una de
silencio, y escribiría ruido o nada. El riesgo real no es espaciar los guardados,
es **terminar el chat sin consolidar**.

La solución es un aviso **por evento, no por reloj**: un hook `Stop` que al
terminar la sesión compara la fecha de los entregables con la del `INDICE.md` y
recuerda cerrar sesión si hay cambios sin volcar. Implementación de referencia:
`base/scripts/recordar_cierre.py` + `.claude/settings.json`.

---

## 5. Plantilla de un playbook (actividad)

Todo MD de actividad debería tener:

```markdown
---
id: ejemplo-actividad
dominio: empresa/publicidad
estado: borrador | aprobado | obsoleto
actualizado: YYYY-MM-DD
salida_aprobada: ruta/al/entregable   # obligatorio si estado = aprobado
---

# Título de la actividad

## Objetivo
## Regla de partida        ← qué copiar del resultado ya aprobado
## Entradas (qué leer antes)
## Herramientas que funcionan  ← y cuáles se descartaron, con el motivo
## Procedimiento aprobado
## Criterios de aceptación (lista verificable)
## Trampas conocidas       ← errores ya pagados, para no repetirlos
## Prohibiciones
## Historial de mejoras
```

**`estado: aprobado` exige `salida_aprobada` con un path real.** Sin entregable
que enseñar, el playbook es un borrador por bueno que suene. Esta regla nace de
encontrar un playbook marcado "sin salida en repo" cuando la salida existía, y
que además describía una herramienta que nunca se usó.

**Dos secciones que valen más que el procedimiento:** *Trampas conocidas* (cada
error que ya costó tiempo) y *Herramientas descartadas con el motivo*. Sin ellas
el siguiente chat vuelve a probar lo que ya falló.

---

## 6. Qué va en cada capa (no mezclar)

| Capa                                 | Contiene                                                  | No contiene                                 |
| ------------------------------------ | --------------------------------------------------------- | ------------------------------------------- |
| `base/raiz.md`                     | Metodología, comandos, plantillas                        | Precios, copy de marca, un cliente          |
| `base/claude.md`                   | Mapa del proyecto, rutas, reglas locales                  | Procedimiento largo de un video concreto    |
| `<dominio>/MEMORIA.md`             | Historial, pendientes, últimos merges de ESE dominio     | Metodología general, otro dominio          |
| Playbook (`<dominio>/<tema>.md`)   | Cómo producir una salida concreta                        | Estrategia general de la empresa            |
| Skill (`base/skills/<nombre>.md`)  | Una técnica puntual reutilizable, marcada por el usuario | Una actividad completa (eso es un playbook) |
| Archivos reales (HTML, PNG, código) | Entregables                                               | Sustituir a los MD de memoria               |

---

## 7. Ciclo de aprendizaje

1. **Hacer** la tarea con el playbook (o crear uno nuevo).
2. **Aprobar** el humano (explícito o al usar el resultado).
3. **Registrar** en el playbook qué funcionó / qué se rechazó.
4. **Cerrar sesión** para persistir.
5. La próxima vez: **partir de lo registrado**.

Cada proyecto mejora su propio `claude.md` + playbooks; la metodología (`raiz.md`) solo cambia cuando mejoras el *sistema* (no el negocio).

---

## 8. Uso en otros proyectos (checklist)

- [ ] Copiar `base/raiz.md`
- [ ] Crear `base/claude.md` desde esta metodología (dominios del nuevo proyecto)
- [ ] Crear carpetas de dominio
- [ ] Copiar `base/scripts/generar_indice.py` y correrlo → genera `INDICE.md`
- [ ] **Crear `CLAUDE.md` en la RAÍZ del repo** apuntando a `base/claude.md`
- [ ] Copiar `base/scripts/recordar_cierre.py` + `.claude/settings.json` (hook Stop)
- [ ] Opcional: `SESION.md` para notas crudas
- [ ] Opcional: crear `base/skills/` + `base/scripts/generar_indice_skills.py` cuando aparezca el primer skill a guardar (ver §10) — no hace falta crearla vacía de entrada

**El `CLAUDE.md` de la raíz no es opcional en Claude Code:** es el archivo que la
herramienta carga sola al abrir el proyecto. Sin él, `base/claude.md` no se lee
hasta que alguien lo pide a mano, y el sistema entero queda inerte al empezar un
chat. Debe ser corto: apuntar al orquestador y no repetir la metodología.

---

## 9. Manejo de ramas y sincronización (worktrees)

Cuando un proyecto tiene **múltiples ramas de trabajo** (ej. rama `whatsapp/`, rama `facebook/`, cada una con su propia carpeta y worktree), es crítico detectar cuándo un worktree está **desactualizado** por merges posteriores en `main`.

### Estructura MEMORIA.md con historial de merges

Cada carpeta de dominio tiene su `MEMORIA.md` que registra:

```markdown
---
id: whatsapp-memoria
dominio: whatsapp
actualizado: YYYY-MM-DD
---

# WhatsApp — Memoria

## Últimos merges a main
- 2026-09-06: Merge Facebook → cambió número WhatsApp
- 2026-09-05: Merge WhatsApp (este dominio)

## Cambios esta sesión
- ...

## Decisiones
- ...
```

### Cómo detectar desactualización

1. **Al abrir sesión en una rama específica** (ej. "trabajo en WhatsApp"):

   - Leer `main` y ver qué merges ocurrieron después del último merge de esa rama
   - Si hay merges posteriores → avisar: "⚠️ Worktree desactualizado. Hay cambios de otras ramas. ¿Actualizamos?"
2. **Registro en MEMORIA.md**:

   - Cada rama mantiene una lista: "Últimos merges a main"
   - Sirve como histórico: puedo ver qué cambios externos afectaron la rama
3. **Sincronización**:

   - Antes de trabajar en una rama desactualizada, hacer pull/merge de main
   - Resolver conflictos si los datos (ej. número WhatsApp) se duplican

### Regla: Un merge posterior puede afectar tu rama

Ejemplo: trabajas en `facebook/`, cambias el número de WhatsApp. Mergeas a `main`. Otro agente trabaja después en `whatsapp/`, que estaba basado en un main anterior. Ese worktree no ve tu cambio hasta actualizar.

**La detección automática avisa de esto.**

---

## 10. Sistema de skills reutilizables

Un **skill** no es un playbook. El playbook cubre una actividad completa ("crear
un video de Facebook", "llenar el protocolo FT-005"); un skill es una **técnica
puntual** — un truco, una receta chica, un procedimiento que resolvió un
problema concreto y que el usuario decide que vale la pena repetir tal cual la
próxima vez que aparezca una situación parecida, sin importar en qué dominio o
playbook vuelva a aparecer. Vive en `base/skills/`, fuera de los dominios.

**Esto es un plus, no un reemplazo.** El sistema de skills no reduce ni
sustituye el ciclo de aprendizaje normal (§7): el agente sigue registrando en
cada `MEMORIA.md` de dominio, en los playbooks y al "cerrar sesión" todo lo que
aprende de las tareas de siempre, se convierta o no en skill. Un skill nace
además de eso, solo cuando el usuario decide que una técnica puntual merece
quedar aparte para reusarse literal — no en lugar de la memoria continua.

### Cuándo se crea o se toca un skill

El agente **no crea skills por su cuenta ni de cualquier tarea**. Se crea (o se
mejora uno existente) solo cuando el usuario señala explícitamente que algo
recién hecho merece quedar como procedimiento repetible — frases como "guardá
esto", "lo que acabamos de hacer conviene que quede", "la próxima vez hacé lo
mismo que ahora", o cuando le pone nombre propio al procedimiento.

Antes de escribir nada, el agente **siempre pregunta**, nunca decide solo:

1. Revisar `base/skills/INDICE.md`. Si ya existe un skill parecido, mostrarlo
   y preguntar si conviene **mejorar ese** en vez de crear uno nuevo.
2. Si no hay uno parecido, confirmar con el usuario el nombre y la
   **instrucción clave** (la frase corta que va a decir para invocarlo
   después) antes de crear el archivo.

Nunca crear ni sobrescribir un skill sin esta confirmación: es contenido que el
usuario va a reusar tal cual más adelante, así que el criterio de qué entra y
cómo se llama es suyo, no una inferencia del agente.

### Estructura de un skill (`base/skills/<nombre>.md`)

```markdown
---
nombre: encabezado-despues-de-una-hoja
instruccion_clave: "encabezado después de una hoja"
descripcion: Repetir un encabezado angosto + numeración Pág. X de Y en las páginas 2+ de un documento
modulo: <dominio o área al que pertenece, ej. Protocolos>
creado: YYYY-MM-DD
actualizado: YYYY-MM-DD
---

# <Nombre legible del skill>

## Cuándo usarlo
## Procedimiento paso a paso
## Trampas conocidas
## Historial de uso            ← dónde se aplicó, con fecha
```

### Índice de skills (`base/skills/INDICE.md`)

No se escribe a mano — igual que `base/INDICE.md`, lo regenera un script
(`base/scripts/generar_indice_skills.py`) leyendo el frontmatter de cada
`base/skills/*.md`, con estas columnas:

| Archivo                               | Instrucción clave                | Descripción                                             | Módulo    |
| ------------------------------------- | --------------------------------- | -------------------------------------------------------- | ---------- |
| `encabezado-despues-de-una-hoja.md` | "encabezado después de una hoja" | Repetir encabezado angosto + Pág. X de Y en páginas 2+ | Protocolos |

Regenerar el índice después de crear o modificar cualquier skill, igual que se
regenera `INDICE.md` general.

---

## 11. Versionado de la metodología

| Versión | Fecha      | Nota                                                                                                                                                                                                                                                                |
| -------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.4.0    | 2026-09-11 | Agregado sistema de skills reutilizables (§10):`base/skills/` con un `.md` por técnica puntual + `INDICE.md` propio generado por script desde el frontmatter. El agente nunca crea o edita un skill sin preguntar primero (nuevo vs. mejorar uno existente) |
| 1.3.0    | 2026-09-06 | Dominios se mueven a la RAÍZ del proyecto (hermanos de`base/`), ya no dentro de `base/`; cada dominio lleva `MEMORIA.md` obligatorio; `generar_indice.py` debe escanear también las carpetas de dominio (`CARPETAS_DOMINIO`)                            |
| 1.2.0    | 2026-09-06 | Agregada sección 9: manejo de worktrees y sincronización; MEMORIA.md ahora registra merges para detección de desactualización                                                                                                                                   |
| 1.1.0    | 2026-09-06 | `CLAUDE.md` raíz obligatorio; `INDICE.md` generado por script; cron sustituido por hook `Stop`; `estado: aprobado` exige `salida_aprobada`; plantilla de playbook con *Trampas conocidas* y *Herramientas descartadas*                               |
| 1.0.0    | 2026-09-06 | Primera definición — Aprendizaje continuo                                                                                                                                                                                                                         |

Cuando cambies reglas universales, sube versión aquí. Los proyectos hijos no necesitan la misma versión de negocio; sí conviene alinear la de metodología.
