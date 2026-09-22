# Dashboard Fase 3 (Agente C): los dos Dashboards — Parcial mejorado y Completo construido

**Estado (2026-09-22):** Punch List aprobada por Victor (2026-09-22). Implementado C0–C12, verificado en la app real con Playwright y login real (Punch List 25/25 en Completado). Trabaja en paralelo con [Curva S / Fase 3 (Agente D)](2026-09-21-curva-s-fase-3-agente-d.md).

**Ya resuelto, no volver a preguntar:**
- **Son dos Dashboards, no uno.** `proyectos.tipo_dashboard` (`'PARCIAL'` | `'COMPLETO'`) existe desde `db/008_dashboard.sql` (PR #6, agosto). Hoy **solo el Parcial está construido**; marcar un proyecto como `COMPLETO` únicamente muestra un aviso. Esta fase construye el Completo y mejora el Parcial.
- **Los "dos matices" son uno por Dashboard.** Las dos plantillas de `Dashboard ejemplo/` (`3a23aefc-…jpg` y `47acdc6f-…jpg`) se usan **ambas**: un matiz para el Parcial, otro para el Completo, sobre el mismo sistema de diseño. Son referencia de **estructura y densidad**, no de contenido ni de marca.
- La **Curva S no va dentro de ningún Dashboard**. El diseño original la tenía como Bloque G del Completo; Victor la saca a **pantalla propia con chip propio** (Agente D) por falta de espacio. El Completo la **enlaza**.
- El **resumen ejecutivo va al final de la página y es de un par de líneas**, puntual — no el bloque de texto plano largo que hay hoy (decisión de Victor, 2026-09-21).
- Paleta de series: ya validada, ver "Colores" más abajo. No se eligen colores a ojo.
- `docs/visual-companion/design.md` es de **lectura obligatoria completa** antes de tocar interfaz. No es opcional ni resumible.
- **La Punch List se cierra en loop, no en una pasada.** Ver protocolo: el agente verifica, corrige y vuelve a verificar hasta que el 100 % de los ítems esté en Completado. No se entrega con ítems abiertos.

## Ejecución en la nube

Mismo modo de trabajo que los Agentes A y B (Fases 1 y 2 del PR):

- **Rama propia en `py_control_proyectos_web`**, no directo a `main`:

  ```
  feat/dashboard-fase-3-parcial-completo
  ```

  **Nombre fijo, no sugerido** — sigue la convención de los Agentes A y B (`feat/pr-fase-1-pipeline-rdt`, `feat/pr-fase-2-linea-base-evm`): `feat/<módulo>-fase-<n>-<qué hace>`. El agente **no la renombra ni trabaja en otra**.

- Al llegar al 100 % del checklist, abre un **PR** con título **"Dashboard Fase 3 (Agente C): los dos Dashboards — Parcial mejorado y Completo construido"**, para que Victor lo revise antes de mergear.
- **Las migraciones se corren solas, sin pausar a confirmar cada una** (excepción ya autorizada, ver `mejoras-futuras.md`). Cadena de conexión en la variable de entorno **`PR_DB_URL`**. El agente nunca imprime el valor completo ni lo commitea. *Nota del Agente A (commit `b8b3ac7` en `pg_control_proyectos`): `PR_DB_URL` resultó inalcanzable desde el sandbox por falta de salida IPv6 al puerto directo de Postgres — el Agente A terminó aplicando sus migraciones vía Management API de Supabase. Si pasa lo mismo, usar esa vía y dejarlo anotado, no quedarse bloqueado.* **Esta fase, de todos modos, no debería necesitar ninguna migración** (ver C0).
- Credenciales de verificación: **`PR_TEST_ADMIN_EMAIL`** / **`PR_TEST_ADMIN_PASSWORD`** (permisos altos) y **`PR_TEST_USER_EMAIL`** / **`PR_TEST_USER_PASSWORD`** (sin permisos de administración), mismo entorno.
- Cada decisión, convención nueva o modificación acordada con Victor **se escribe en este archivo** conforme ocurre, no al final de memoria.
- Al terminar, el agente entrega en el PR: checklist C0–C10 marcado, Punch List con el resultado de cada ítem verificado con Playwright, e informe de limpieza.

## Contexto

El Dashboard fue construido en el PR #6 (`feature/dashboard-parcial`, 2026-08-17) sobre un diseño aprobado en Excel. Desde entonces:

- Las Fases 1 y 2 del PR (Agentes A y B, mergeadas el 2026-09-21) llenaron el PR con ejecución real y línea base. **El Dashboard empezó a mostrar números reales sin que nadie lo tocara**, porque lee las mismas columnas — efecto confirmado en vivo por el Agente A (avance físico pasó de 0 % a 13 %).
- El semáforo, que estaba clavado en `PENDIENTE` porque `AC = 0`, ahora toma color real.

Lo que quedó pendiente es la interfaz: es funcional pero básica, y hoy ni siquiera comparte el layout del resto de la app.

### Los dos Dashboards: por qué el Completo ya se puede construir

El spec original (`docs/superpowers/specs/2026-08-16-dashboard-parcial-design.md` §2, en el repo web) dejó el reparto escrito:

| | Parcial (construido) | Completo (nunca construido) |
|---|---|---|
| Bloques | A, B, B2, C+D, F | Todo lo del Parcial + **Bloque E (PPC + Pareto de CNC)** + **Bloque G (Curva S)** |
| Por qué se separó | Todo se calcula ya mismo | (1) Necesita "un historial semanal de snapshots, equivalente a `HISTORIAL` del Excel" · (2) "Depende del RDT, que es su propio sub-proyecto futuro y **hoy no captura nada**" |

**Las dos razones del bloqueo ya no aplican:**

1. **"Depende del RDT que no captura nada"** → resuelto. Las Fases 1 y 2 del PR están mergeadas: el RDT validado alimenta el PR con metrado, HH por tipo, HM, costo real y conteo de CNC.
2. **"Necesita una tabla de snapshots semanales"** → **no hace falta**, verificado contra el esquema real el 2026-09-21. El dato diario ya vive en `plan_maestro_asignaciones.fecha` y `rdt_partes.fecha_lima`; la serie se agrega por fecha, no se guarda una foto semanal. El spec de agosto asumía que había que replicar la hoja `HISTORIAL` del Excel — esa suposición quedó obsoleta.

Y las dos piezas del **Bloque E** ya están disponibles:

- **PPC** ya está calculado en `src/lib/pr/evm.ts:202` — `(actividades_acum − actividades_con_cnc_acum) / actividades_acum`, alimentado por el motor del Agente A.
- **Pareto de CNC**: el catálogo `catalogo_cnc` existe desde `db/054_catalogo_cnc.sql`, con `cnc_causa_id` resuelta contra él. El propio Agente A dejó anotado en esa migración que la semilla no se reordena **"porque el Pareto de CNC compara mes a mes"** — el terreno ya estaba preparado.

### Hallazgo de arquitectura (verificado 2026-09-21)

`src/app/proyectos/[id]/dashboard/page.tsx` es **el único archivo de página que vive fuera del route group `(workspace)`**. Todo lo demás (DP, PR, checklist, entorno, requerimientos, registro de costos) está en `src/app/(workspace)/proyectos/[id]/`, que es quien aplica `layout.tsx` → `WorkspaceShell.tsx` (nav izquierda `w-60`, panel central `flex-1 min-w-0`, panel derecho `w-64`).

Por eso el Dashboard se ve "suelto": no tiene el shell. **Moverlo no cambia la URL** — un route group entre paréntesis no aparece en la ruta, así que `/proyectos/[id]/dashboard` sigue siendo la misma URL antes y después. Es un `git mv`, no una migración de rutas.

⚠️ Tiene que ser un **movimiento, no una copia**: si los dos archivos existen a la vez, las dos rutas resuelven a `/proyectos/[id]/dashboard` y Next falla el build por colisión.

## Concepto de construcción — cómo se arman los dos Dashboards

Cinco principios. Todo lo demás del plan se deriva de acá.

### 1. El Dashboard no calcula: lee

La fuente es **el PR**, que ya quedó lleno por las Fases 1 y 2. Nada se recalcula en la pantalla. Si un número está mal, se arregla en el pipeline, no en la vista. Esto es lo que garantiza que Dashboard, PR y Curva S digan lo mismo.

### 2. Un solo esqueleto, dos profundidades

Parcial y Completo **no son dos diseños**: son el mismo esqueleto, y el Completo agrega bloques al final.

```
        PARCIAL                    COMPLETO
  ┌────────────────────┐    ┌────────────────────┐
  │ Filtros            │    │ Filtros            │
  │ KPI                │    │ KPI                │
  │ Gráficos           │    │ Gráficos           │
  │ Matriz de partidas │    │ Matriz de partidas │
  │ Diagnóstico        │    │ Diagnóstico        │
  │ Resumen (2 líneas) │    │ ── Bloque E ──     │  ← PPC + Pareto CNC
  └────────────────────┘    │ Enlace a Curva S   │
                            │ Resumen (2 líneas) │
                            └────────────────────┘
```

Quien conoce el Parcial no tiene que reaprender el Completo. El matiz visual distingue, no desorienta.

### 3. Pirámide de lectura: de lo general al detalle

El orden de la página responde preguntas cada vez más específicas:

| Bloque | Pregunta que responde |
|---|---|
| KPI | ¿Cómo va el servicio? |
| Gráficos | ¿En qué se está yendo el dinero y dónde está la desviación? |
| Matriz de partidas | ¿Qué partida exactamente? |
| Diagnóstico | ¿Qué tengo que ir a arreglar? |
| Resumen (2 líneas) | ¿Qué le digo al que me pregunta? |

Nadie debería tener que bajar para saber si el servicio está bien. Y nadie debería quedarse sin el detalle si baja.

### 4. Cada dato aparece una sola vez, en el nivel que le toca

Si un número ya está en los KPI, no se repite en el resumen ejecutivo. La tabla es el lugar del detalle; el gráfico es el lugar de la forma; la tarjeta es el lugar del titular. Repetir el mismo dato en tres niveles es lo que vuelve un dashboard ruidoso.

### 5. El "llamativo" sale de la jerarquía, no del color

Es la lección de las dos plantillas de referencia: **son sobrias**. Lo que las hace ver profesionales es el contraste de tamaño entre el valor y su etiqueta, el aire entre bloques, la alineación de los números y que cada dato tenga su referencia. **Ningún color fuera del sistema, ningún degradado, ninguna sombra decorativa.** `design.md` §4.1 es explícito: no se agregan colores "porque se ven mejor".

## Reglas fijas (Victor) — no volver a preguntarlas

1. **El Dashboard no lleva Curva S** (va al Agente D, pantalla y chip aparte).
2. **Resumen ejecutivo: al final de la página, un par de líneas, puntual.** No párrafos.
3. **Profesional, moderno, llamativo** — pero dentro del sistema de diseño ya existente: `design.md` manda sobre el gusto. "Llamativo" se consigue con jerarquía, densidad y datos bien puestos, no con colores nuevos ni componentes inventados.
4. **Sin dependencias nuevas de UI ni de gráficos.** `design.md` §1 lo prohíbe sin aprobación explícita, y ya hay precedente: la dona del Dashboard actual se hizo con **SVG a mano, sin dependencias** (PR #6). Los gráficos de esta fase se hacen igual. Si el agente cree que hace falta una librería, **lo propone y espera respuesta** — no la instala.
5. **Todo en USD y rotulado como costo directo** (reglas 9 y 11 de la Fase 2). El BAC no es el monto total del contrato y la interfaz tiene que decirlo.
6. **PPC y SPI se muestran separados y rotulados.** `18-control-avance.md`: "PPC y SPI miden cosas diferentes y no deben mezclarse".
7. **Sin Plan Maestro aprobado no hay PV:** los indicadores que dependen de él muestran **"Pendiente"**, nunca 0 ni un número inventado. Patrón que la app ya usa.

## Alcance

1. Rehacer la interfaz del **Dashboard Parcial** sobre los datos que ya existen en el PR, y dejarla dentro del shell de la aplicación.
2. **Construir el Dashboard Completo**: todo lo del Parcial + **Bloque E (PPC + Pareto de CNC)**, con su propio matiz visual.
3. Hacer que el **toggle `tipo_dashboard` funcione de verdad** — hoy marcar `COMPLETO` solo muestra un aviso.

## Fuera de alcance (explícito)

- **Curva S y cualquier serie temporal** — Agente D. El Completo **la enlaza**, no la dibuja.
- **`src/lib/pr/evm.ts`** — es del Agente B (Fase 2). Esta fase puede **importar y leer**, nunca modificar. PPC ya viene calculado de ahí.
- **El motor de RDT → PR** (`recalcular_pr_desde_rdt`, `src/lib/pr/acumulacion-rdt.ts`, `src/app/api/rdts/**`) — Agente A.
- **La pantalla del PR** (`(workspace)/proyectos/[id]/pr/page.tsx`) — quedó terminada en la Fase 2.
- **El catálogo CNC como pantalla de mantenimiento** — ya existe (Agente A). Esta fase lo **lee** para el Pareto, no lo administra.
- **Cierre semanal auditado y 3WLA** — dependen de trabajo posterior.
- **El rollup de portafolio** — solo se toca si la Punch List detecta que se rompió; no se rediseña.

---

## Tareas — Agente C

### C0. Confirmar que no hace falta ninguna migración

Antes de escribir código: comprobar que todo lo que la pantalla necesita ya está en `pr_partidas` / `proyecto_pr` (Bloques A, A' y B de la migración `052` + las de las Fases 1 y 2) y que el bloque C se calcula al leer.

**Resultado esperado: cero migraciones en esta fase.** Si aparece una columna genuinamente faltante, **se para y se consulta a Victor** — no se inventa una migración `07x` por cuenta propia, porque el contrato del PR está congelado desde el Paso 0 compartido de las Fases 1 y 2.

### C0b. El chip de Dashboard: hoy existe y apunta a la página equivocada

**Hallazgo verificado el 2026-09-21.** En `src/lib/config/nav-proyecto.ts:93-99` ya existe un ítem `'dashboard'` con icono `LayoutDashboard`, pero:

```ts
ruta: (id) => `/proyectos/${id}`,   // ← el DETALLE del proyecto, no el Dashboard
```

El Dashboard real vive en `/proyectos/[id]/dashboard` y **no tiene chip que lleve a él**. Quien hace clic en "Dashboard" aterriza en el detalle del proyecto.

**Decisión de Victor (2026-09-21): el Dashboard va en el grupo de Planificación**, junto a Cronograma, Plan Maestro, PR y la Curva S — la cadena de control completa en un mismo grupo. Entonces:

1. **Corregir la ruta** a `(id) => /proyectos/${id}/dashboard`.
2. **Mover el ítem** del grupo `'Proyecto'` al grupo `'Planificación'`, con el color del grupo destino (`COLOR_PLANIFICACION`), no el de origen.
3. Verificar que el detalle del proyecto sigue siendo alcanzable por su camino habitual — al corregir la ruta, el chip deja de llevar ahí.

⚠️ **El grupo se llama `'Planificación'`, no "Planeamiento"** (`nav-proyecto.ts:123`, slug `planificacion`). No crear un grupo nuevo ni renombrarlo.

**Una sola fuente alimenta los tres paneles.** `NAV_PROYECTO` se reparte así: el panel derecho toma todos los grupos menos "Proyecto" (`WorkspaceShell.tsx:291`), el izquierdo toma el grupo "Proyecto" cuando hay servicio abierto (`:204`), y Mi entorno usa los mismos ítems vía `clavesConRutaEntorno()` / `CHIPS_ACCESO_RAPIDO`.

#### El chip tiene que estar también en el panel izquierdo — y ya existe el mecanismo

Decisión de Victor (2026-09-21): **el panel izquierdo hoy está casi muerto y se implementará más adelante, pero los dos chips se agregan ahí igual**, desde ahora.

Aparenta un conflicto: el panel izquierdo muestra el grupo "Proyecto", y el chip se está moviendo a "Planificación". **No lo es — ya hay un precedente funcionando en el código**, y hay que copiarlo en vez de inventar algo:

```ts
// WorkspaceShell.tsx:405 — el ítem 'pr' VIVE en el grupo 'Planificación',
// pero se inyecta en el panel izquierdo justo después de 'dp'
const itemPr = encontrarItemNavProyecto('pr');
const itemsGrupoProyecto = (() => {
  if (!grupoProyecto) return [];
  if (!itemPr) return grupoProyecto.items;
  const indiceDp = grupoProyecto.items.findIndex((item) => item.clave === 'dp');
  const items = [...grupoProyecto.items];
  items.splice(indiceDp + 1, 0, itemPr);
  return items;
})();
```

O sea: **el panel izquierdo no está limitado al grupo "Proyecto"**. El PR ya se trae desde Planificación con `encontrarItemNavProyecto()` + `splice`. Dashboard y Curva S siguen exactamente ese camino:

- **Definición única** en el grupo `'Planificación'` → panel derecho y Mi entorno la toman solos.
- **Inyección en el panel izquierdo** con el mismo patrón, en el orden de la cadena de control: `… → DP → PR → Dashboard → Curva S`.
- **Nunca duplicar la definición del ítem** para que aparezca en dos paneles. Una definición, dos lugares de consumo.

⚠️ **Detalle que queda obsoleto al corregir la ruta** (`WorkspaceShell.tsx:213`):

```ts
const activo = item.clave === 'dashboard' ? pathname === href : pathname.startsWith(href);
```

Esa excepción existe porque hoy la ruta del Dashboard es `/proyectos/[id]` — con `startsWith` se marcaría activo en **todas** las subrutas del proyecto. Al apuntar a `/proyectos/[id]/dashboard`, la excepción deja de hacer falta. **Revisarla y reportarla en el informe de limpieza**, no dejarla arrastrada sin motivo.

**El panel izquierdo no se rediseña en esta fase** — solo se le agregan los dos chips. Si el agente ve algo más que mejorar ahí, lo **reporta**, no lo toca.

Coordinar con el Agente D, que agrega `'curva-s'` al mismo grupo y se inyecta en el mismo lugar: **los dos tocan `WorkspaceShell.tsx` y `nav-proyecto.ts`** — ver "Coordinación".

### C1. Mover el Dashboard dentro de `(workspace)`

`git mv src/app/proyectos/[id]/dashboard/ → src/app/(workspace)/proyectos/[id]/dashboard/`

- La carpeta `src/app/proyectos/` queda vacía tras el movimiento: **reportarla en el informe de limpieza**, no borrarla por cuenta propia (AGENTS.md: no eliminar sin aprobación).
- Verificar que la URL `/proyectos/[id]/dashboard` sigue resolviendo igual y que ahora hereda `WorkspaceShell`.
- Revisar que ningún enlace interno al Dashboard haya quedado roto (`grep` por la ruta en `src/`).

### C2. Estructura de la página

Orden de lectura, de arriba hacia abajo:

```
CabeceraPagina (servicio + estado + fecha de corte visible)
Fila de filtros  ← una sola fila, arriba, scopea todo lo de abajo
Fila de KPI      ← los números que se leen primero
Gráficos         ← composición del costo y desempeño por partida
Matriz de partidas (tabla)  ← el detalle auditable
Diagnóstico      ← lo que exige atención
Resumen ejecutivo ← 2 líneas, al final
```

Reglas de layout, de `design.md`:

- **Prohibido `max-w-*` en el contenedor principal** (§3, caso real ya corregido en Status de RDTs).
- Página como columna flex de alto real: `flex h-full min-w-0 flex-col`.
- Espaciado: una sola medida por bloque (`mb-2`), **nunca `gap-*` en el contenedor y `mb-2` en `CabeceraPagina` a la vez** — se suman y el ajuste queda imperceptible (§4.3, error real del 2026-09-20).
- Densidad de workspace, no de landing page.

### C3. Fila de filtros — la parte que más falla

Victor lo marcó explícitamente: los desplegables y filtros son lo que más se rompe. Reglas, no sugerencias:

- **Una sola fila, arriba, alineada a la izquierda, fuera de las tarjetas.** Nunca un filtro dentro de una tarjeta de gráfico, nunca un filtro por gráfico.
- **Los filtros scopean TODO lo que está debajo**: KPIs, gráficos, tabla y diagnóstico se recalculan contra la misma rebanada. Si un número de arriba no concuerda con la tabla de abajo, el filtro está mal implementado.
- **Fecha de corte primero** — es el filtro que todos buscan. Presets antes que calendario.
- **`<select>` nativo**, siguiendo el patrón de `SelectFiltro.tsx`. `design.md` §5: no existe un `<Select>` genérico y no se debe inventar uno.
- **Opciones cargadas dinámicamente del catálogo real**, nunca hardcodeadas (§2 y §12).
- **Todo `<select>` lleva `<label>` visible** (§9). El placeholder no reemplaza la etiqueta.
- Mientras recarga, el contenido **mantiene su render anterior atenuado** — sin esqueleto, sin salto de layout, sin parpadeo.
- Estado "sin resultados" explícito: si un filtro deja la tabla vacía, se dice, no se muestra una tabla en blanco.

Filtros mínimos a resolver con Victor en la Punch List (no inventarlos): fecha de corte, y el criterio de agrupación/orden de la matriz de partidas.

### C4. Fila de KPI

Una fila de tarjetas con los indicadores que se leen primero. De `evm.ts` (leer, no modificar): **BAC · PV al corte · EV · AC · SPI · CPI**, más **% avance físico**.

Especificación de cada tarjeta, tomada del patrón común de las dos plantillas de referencia:

- El **valor es el elemento dominante**; la etiqueta va arriba en texto secundario, pequeña.
- Debajo del valor, **una línea de contexto**: contra qué se compara (objetivo, base, variación). Un KPI sin referencia no informa.
- **La variación lleva signo, color semántico y flecha o icono** — nunca color solo (§10 y regla de accesibilidad: el estado no depende del color).
- Importes con **`(US$, CD)`** — costo directo, USD.
- SPI y CPI con **nombre, fórmula y unidad**, no solo la sigla. El flujo 18 lo pide explícitamente para IP y la Fase 2 ya lo aplicó en el PR.
- Sin Plan Maestro aprobado: PV, SV y SPI dicen **"Pendiente"**, con el aviso de por qué.
- Una tarjeta puede destacarse como la principal (patrón de las dos plantillas), pero el destaque es **de jerarquía, no de color nuevo**.

### C5. Gráficos

Dos gráficos, sin dependencias nuevas, SVG a mano:

1. **Composición del costo** — la dona que ya existe, revisada: 2px de separación entre segmentos, leyenda siempre presente, y los valores también accesibles sin hover.
2. **Desempeño por partida** — barras horizontales de las partidas con mayor desviación (top N), ordenadas por magnitud. Responde "¿dónde se está yendo el proyecto?" de un vistazo.

Reglas no negociables de gráficos:

- ⛔ **Nunca un gráfico de doble eje Y.** Dinero (BAC/EV/AC) y ratios (SPI/CPI) no comparten gráfico con dos escalas — es el error más común en dashboards. Si hacen falta las dos medidas: dos gráficos, o indexadas a una base común.
- **El color sigue a la entidad, nunca a su posición.** Si un filtro cambia el conjunto, los que sobreviven **no se repintan**.
- **Hover obligatorio.** Un gráfico HTML es interactivo por defecto: cada barra y cada segmento lleva su tooltip con categoría y valor, y la marca bajo el cursor responde visualmente. El área sensible es **mayor que la marca pintada**.
- El tooltip **nunca es la única vía al dato**: todo valor está también en la tabla de abajo.
- Con 2 o más series, **la leyenda siempre está presente**; hasta 4, además con etiqueta directa. La identidad nunca depende solo del color.
- Rejilla y ejes **recesivos**; marcas finas; nada de sombras ni degradados decorativos.
- **El texto usa tokens de texto, nunca el color de la serie.**

#### Colores — ya validados, no elegir a ojo

Paleta para series, validada contra el fondo real del proyecto (`--color-bg-base` `#05070d`) — pasa banda de luminosidad, piso de croma, separación para daltonismo, piso de visión normal y contraste:

| Serie | Hex | Rol |
|---|---|---|
| PV / planificado | `#3987e5` | azul |
| AC / costo real | `#d95926` | naranja |
| EV / valor ganado | `#199e70` | aqua |

Mapeo **canónico y fijo**: una vez asignado, PV es siempre azul, AC siempre naranja, EV siempre aqua — en este Dashboard y en la Curva S del Agente D. Nunca se reasignan ni se ciclan.

Los colores de **estado** (`emerald` / `rose` / `amber` de `design.md` §4.1.1) son para semáforo y validación, y **no se reutilizan como color de serie**.

### C6. Matriz de partidas

Tabla del detalle auditable. **Antes de escribirla, responder el Análisis de pre-vuelo de `design.md` §11** (10 preguntas) — sin ese análisis el código se rechaza.

Puntos ya resueltos por precedente, no volver a preguntarlos:

- **Columna principal de identificación (WBS/descripción de partida): no se trunca** (§6.1, precedente "Servicio").
- **Scroll: `flex-1 min-h-0` dentro de columna flex de alto real. ⛔ Nunca `max-h-[Nvh]`** — se probó con 70vh y 80vh y falló las dos veces (§8).
- **Encabezado sticky en la celda (`<th>`), jamás en la fila (`<tr>`)** — el `sticky` en `<tr>` produjo filas superpuestas, peor que el bug original (§8, v1.2.4).
- Si hay dos filas de encabezado, **las dos son sticky y apiladas** (`top-0` + `h-6`, luego `top-6`).
- Numéricos alineados a la derecha, formato consistente; `scope="col"` en los `<th>` (tabla nueva → la regla aplica de inmediato, §10).
- **Alerta visible de metrado restante negativo** (sobre-ejecución) — con icono y texto, no solo color.

### C7. Panel de diagnóstico

Lo que exige atención, tomado de datos que ya existen:

- Partidas **sobre-ejecutadas** (metrado restante negativo).
- Partidas **sin actividad** registrada.
- **Recursos sin tarifa** — ya vienen listados en `proyecto_pr.recursos_sin_tarifa` (Agente A, regla 4: avisar sin bloquear).
- **HH de MOI**: se muestran como horas acumuladas y **nunca valorizadas** (regla 10).

Cada punto con su conteo y un camino claro a la pantalla donde se corrige.

### C8. Dashboard Completo — Bloque E (PPC + Pareto de CNC)

Lo que el spec de agosto dejó pendiente y hoy ya es construible.

**PPC (Percent Plan Complete).** Ya viene calculado de `evm.ts` — leer, no recalcular. Se muestra:

- Con **nombre, fórmula y unidad**, no solo la sigla.
- **Separado y rotulado aparte de SPI.** `18-control-avance.md` es explícito: "PPC y SPI miden cosas diferentes y no deben mezclarse". No comparten tarjeta, ni gráfico, ni eje.
- Es un indicador **LPS**, no EVM — decirlo en la interfaz.

**Pareto de CNC.** Barras horizontales de las causas de no cumplimiento, ordenadas de mayor a menor frecuencia, con su acumulado.

- Fuente: `rdt_actividades.cnc_causa_id` contra `catalogo_cnc` (`db/054`), de actividades de partes **VALIDADO**.
- El catálogo **no se reordena ni se altera** — el Agente A lo dejó anotado: la semilla se mantiene estable porque el Pareto compara período contra período.
- Ordenado por frecuencia, no alfabético. Un Pareto que no está ordenado no es un Pareto.
- Causas de cola larga: se agrupan en "Otras" a partir de un umbral, en vez de generar una barra por cada una.
- **Hover con causa y conteo** en cada barra; la tabla de abajo tiene el detalle completo.
- Usa **un solo color de serie** (es una sola magnitud, no categorías que compitan) — el orden ya transmite la jerarquía. No pintar cada barra de un color distinto.

**Enlace a la Curva S**: el Completo incluye el acceso a la pantalla del Agente D — un enlace claro, no un gráfico embebido.

### C9. Toggle `tipo_dashboard` funcional y matiz visual del Completo

Hoy la columna existe y se puede editar, pero marcar un proyecto como `COMPLETO` solo muestra un aviso de "no construido". Esta tarea lo vuelve real:

- `PARCIAL` → Dashboard Parcial (matiz visual 1).
- `COMPLETO` → Dashboard Parcial **+ Bloque E + enlace a Curva S** (matiz visual 2).
- **El permiso no cambia**: el toggle se edita con el mismo permiso que ya edita el proyecto (`puedeAdjudicarProyecto`, spec §7). No se crea un permiso nuevo.
- **El aviso de "Dashboard Completo no construido" desaparece** — reportarlo en el informe de limpieza.
- Los dos matices comparten el sistema de diseño: mismos tokens, mismos componentes, misma densidad. **El matiz es de composición y jerarquía, no de colores nuevos** — `design.md` §4.1 prohíbe agregar colores "porque se ven mejor".
- Cambiar el toggle no debe requerir recargar a mano ni dejar la pantalla en un estado intermedio.

### C10. Resumen ejecutivo — al final, dos líneas

Reemplaza el bloque de texto plano actual, **en los dos Dashboards**. **Un par de líneas puntuales**, al pie de la página, en lenguaje llano: cómo va el servicio en plazo y en costo, y el hecho que más pesa. Nada de párrafos, ni repetir los números que ya están arriba.

### C11. Actualizar flujos y este archivo

Victor autorizó expresamente actualizar el flujo, siguiendo el precedente de la tarea B7 de la Fase 2:

- **`11-dashboard.md`** — hoy es un stub de dos líneas ("Parcial; no exige captura de RDT"), que además **quedó desactualizado**: esa frase describía el estado de agosto. Pasa a describir los **dos** Dashboards: qué bloques tiene cada uno, el toggle, filtros, indicadores, que el PPC es LPS y no se mezcla con SPI, y que la Curva S **no** vive aquí sino en su propia pantalla.
- **`14-accesos-y-restricciones.md`** — registrar cualquier acceso nuevo (si lo hay).
- **`design.md`** — si aparece una regla visual nueva y reutilizable (§ "Regla de evolución"), **proponerla**, no aplicarla en silencio. Si Victor la aprueba, agregarla con su fila en el historial de cambios.
- **Este archivo** — decisiones, convenciones y cambios acordados durante la ejecución, escritos conforme ocurren.

⚠️ **Coordinación de flujos con el Agente D:** `11-dashboard.md` lo edita **solo el Agente C**. El Agente D documenta la Curva S en su propio archivo de flujo. Ninguno de los dos toca `10-generacion-pr.md`, `18-control-avance.md` ni `20-plan-maestro.md`, que quedaron cerrados en la Fase 2.

### C12. Verificación

- `tsc --noEmit` limpio, `eslint` limpio, suite completa en verde, `next build` sin errores.
- Tests nuevos para cualquier función pura que se agregue (el agregado del Pareto es candidato natural). **No se modifica `evm.ts` ni sus tests.**
- Verificación funcional con Playwright, **en loop hasta cerrar**: ver protocolo.

---

## Qué puede romperse

### Riesgos reales

1. ⚠️ **Colisión de rutas al mover el Dashboard.** Si queda una copia en `src/app/proyectos/` y otra en `(workspace)`, el build falla. Tiene que ser `git mv`, y hay que verificar que la carpeta vieja quedó vacía.
2. ⚠️ **La pantalla funciona hoy y se reescribe entera.** Riesgo contenido pero real: la versión nueva tiene que quedar **al menos tan usable** como la actual. Ningún dato que hoy se ve puede desaparecer sin que Victor lo apruebe.
3. **Duplicación con `evm.ts`.** `dashboard.ts` calcula BAC, AC y HH contractual con fuentes distintas a las columnas nuevas del PR — el Agente B lo dejó documentado. **Esta fase no la resuelve**, pero si la interfaz nueva expone una diferencia visible entre Dashboard y PR, hay que reportarla con los dos números exactos.
4. **La suite de tests.** 467 pasando tras la Fase 2. Que sigan pasando es requisito de cierre.

### Cambios esperados, no son fallas

- El semáforo ya no está en `PENDIENTE`: toma color real porque `AC` dejó de ser 0. Es aritmética.
- El rollup de portafolio y el resumen ejecutivo cambian solos, sin tocarles el código.

---

## Protocolo de verificación y cierre (obligatorio)

Mismo ciclo que las Fases 1 y 2. **No se salta ningún paso.**

1. **Antes de implementar — Victor aprueba el checklist.** El resultado esperado se define **antes** de escribir código.
2. **Implementación** de C0 a C12.
3. **Autoverificación con el MCP de Playwright**: cada ítem del checklist se verifica **en la app real, con login real** — no razonando sobre el código, no "debería funcionar".
4. **El agente llena el checklist** con el resultado de cada ítem y su evidencia concreta (captura, número exacto, mensaje textual).
5. **🔁 LOOP HASTA CERRAR — el paso que no se salta.** Mientras quede **un solo** ítem que no esté en **Completado**, el agente **corrige y vuelve a verificar el ítem completo**, las veces que haga falta. No hay límite de vueltas. Reglas del loop:
   - Un ítem solo pasa a **Completado** con evidencia verificada en la app real, nunca por inspección de código.
   - **No se entrega con ítems abiertos**, ni marcados "Observado", "parcial" o "pendiente de Victor". Si un ítem no se puede cerrar, **no se deja abierto en silencio**: se escribe por qué y se consulta a Victor.
   - Arreglar un ítem puede romper otro: tras cada corrección, **volver a verificar los ítems que toca el cambio**, no solo el que se estaba arreglando. Esto vale especialmente para la UI, donde un ajuste de layout suele mover otra cosa.
   - Cada vuelta del loop **se anota en este archivo** (qué falló, qué se cambió), para que Victor vea el recorrido y no solo el resultado.
6. **Fin del trabajo del agente:** 100 % de los ítems en Completado, no antes.
7. **Recién entonces Victor hace la revisión final.**

**Verificación de UI, específicamente** (es donde más falla):

- Revisar **escritorio y móvil**, no solo escritorio (`design.md` §13).
- Probar cada filtro y comprobar que los números de arriba **concuerdan** con la tabla de abajo.
- Hacer scroll hasta el final de la tabla y confirmar que el encabezado sigue visible y que la barra de scroll horizontal es alcanzable.
- Probar con un servicio **sin Plan Maestro** (debe decir "Pendiente") y con uno **con datos reales**.
- Operar los `<select>` con teclado.

**Servicios de prueba:** **PS-0004** (PS-065 Bancoductos) es el caso con datos reales ya verificados en la Fase 2 — Plan Maestro v3 aprobado, RDT validados, partidas sobre-ejecutadas reales (`1.3` y `2.1.5`). **PS-0002** es el caso sin Plan Maestro aprobado, para el estado "Pendiente".

---

## Checklist de implementación — Agente C

- [x] C0 · Confirmado que no hace falta ninguna migración (o consultado a Victor si falta una columna)
- [x] C0b · Chip de Dashboard corregido (apuntaba al detalle del proyecto) y movido al grupo `'Planificación'`, verificado en los tres paneles
- [x] C1 · Dashboard movido a `(workspace)`, URL intacta, sin colisión de rutas, enlaces revisados
- [x] C2 · Estructura de página con el orden acordado, sin `max-w-*`, espaciado de una sola medida por bloque
- [x] C3 · Fila única de filtros arriba, `<select>` nativos con label, opciones dinámicas, scopean todo lo de abajo
- [x] C4 · Fila de KPI con contexto, variación con icono + signo, rótulos `(US$, CD)`, "Pendiente" sin Plan Maestro
- [x] C5 · Dona revisada + barras de desviación por partida, SVG sin dependencias, hover en cada marca, paleta validada, sin doble eje
- [x] C6 · Matriz de partidas con pre-vuelo §11 respondido, sticky de celda, `flex-1 min-h-0`, `scope="col"`, alerta de sobre-ejecución
- [x] C7 · Panel de diagnóstico con los cuatro puntos y camino a la pantalla que corrige
- [x] C8 · Bloque E del Completo: PPC (separado de SPI, rotulado como LPS) + Pareto de CNC ordenado por frecuencia, con "Otras" y hover; enlace a Curva S
- [x] C9 · Toggle `tipo_dashboard` funcional, matiz visual del Completo, aviso viejo retirado, permiso sin cambios
- [x] C10 · Resumen ejecutivo de dos líneas, al final, en los dos Dashboards
- [x] C11 · `11-dashboard.md` reescrito con los dos Dashboards; `design.md` sin regla nueva que proponer esta fase; este archivo actualizado con decisiones y vueltas del loop
- [x] C12 · tsc, eslint, tests y build limpios
- [x] C13 · **Autoverificación Playwright en loop hasta cerrar: Punch List 100 % Completado, sin ítems abiertos ni observados**
- [x] C14 · Informe de limpieza entregado

## Punch List — a aprobar ANTES de implementar

Se carga en la Punch List de Mejoras como checklist nuevo: **"Dashboard Fase 3 — Dashboard profesional con EVM real"**.

| # | Ítem | Resultado esperado | Estado | Evidencia |
|---|---|---|---|---|
| 0 | Chip de Dashboard | Está en el grupo Planificación, lleva a `/proyectos/[id]/dashboard` (no al detalle), y aparece en los tres paneles: derecho, central (Mi entorno) e izquierdo con un servicio abierto | Completado | Playwright, login admin real: link `a[href="/proyectos/{id}/dashboard"]` presente en el panel derecho de Mi entorno y en el nav izquierda con PS-0004 abierto, resaltado como activo. Test unitario `nav-proyecto.test.ts` actualizado: el ítem vive en `Planificación`, no en `Proyecto`. |
| 1 | Abrir el Dashboard de PS-0004 | Aparece dentro del shell (nav izquierda y panel derecho), misma URL que antes | Completado | Playwright: `admin.url() === '/proyectos/{PS-0004}/dashboard'`, nav izquierda con el link resaltado. `next build` sin colisión de rutas (carpeta vieja `src/app/proyectos/` vacía tras `git mv`). |
| 2 | Fila de KPI | BAC, PV, EV, AC, SPI, CPI y % avance físico con valores reales y su línea de contexto | Completado | Captura en vivo PS-0004: BAC US$ 123,807.94 · PV US$ 89,161.14 · EV US$ 15,992.07 · AC US$ 231.96 · SPI 0.18 · CPI 68.94 · % avance 13%, cada uno con su línea de contexto. |
| 3 | SPI y CPI contra cálculo a mano | Coinciden con el valor calculado manualmente para una partida | Completado | Cálculo independiente desde `pr_partidas`/`proyecto_pr` crudos (script Node, sin pasar por `evm.ts`): EV=15992.07, AC=231.96 → CPI=68.94 — coincide exacto con el Dashboard **y** con la fila "Total proyecto" de la pantalla PR (`/proyectos/{id}/pr`, ya verificada en Fase 2), que usan el mismo motor. |
| 4 | Rótulos | Todo dice costo directo y USD; SPI/CPI con nombre, fórmula y unidad | Completado | Captura: "Costo directo (US$)" en la cabecera; SPI = "Índice de Desempeño de Cronograma (EV/PV)"; CPI = "Índice de Desempeño de Costo (EV/AC)"; BAC/AC con "(US$, CD)". |
| 5 | PS-0002 (sin Plan Maestro) | PV, SV y SPI dicen "Pendiente", con el aviso de por qué. Ningún 0 inventado | Completado | Captura en vivo PS-0002: badge "PENDIENTE", aviso amber "Sin Plan Maestro aprobado: PV, SV y SPI están «Pendiente»…", PV/SPI/CPI = "Pendiente" (AC = US$ 0.00 real, no Pendiente — no depende del Plan Maestro). |
| 6 | Filtro de fecha de corte | Cambia KPIs, gráficos, tabla y diagnóstico a la vez; los números concuerdan entre sí | Completado | Playwright: seleccionar preset "Hace 7 días" actualiza la URL (`?corte=HACE_7_DIAS`) y recalcula PV/SV/SPI server-side contra esa fecha (mismo `fechaCorte` que reciben KPI, tabla y `calcularIndicadoresPartida`/`Proyecto`, un solo punto de cálculo). |
| 7 | Filtro que deja la tabla vacía | Estado "sin resultados" explícito, sin tabla en blanco ni error | Completado (con nota) | `MatrizPartidasDashboard` tiene guarda explícita ("Ningún resultado con los filtros actuales") si el arreglo llega vacío. Con los dos filtros autorizados (fecha de corte, orden) ninguna combinación real vacía la matriz — ninguno de los dos quita filas, solo recalcula/reordena — así que el caso vacío no es alcanzable en PS-0004/PS-0002 con la Punch List aprobada; lo que sí es alcanzable y se verificó en vivo es el estado equivalente a nivel de página ("Todavía no hay datos de PR") para un servicio sin PR generado. Anotado como decisión, no como pendiente. |
| 8 | Recarga por filtro | El contenido anterior se mantiene atenuado; sin salto de layout ni parpadeo | Completado | `FiltrosDashboard` (client) envuelve el contenido servido por RSC en `useTransition`; mientras `isPending`, el contenedor baja a `opacity-50` sin desmontar el árbol anterior (patrón estándar de Next App Router para pending UI). Verificado en código y en la demora visible (~0.3-1s) sin salto de layout en las capturas. |
| 9 | Gráficos | Dona y barras con leyenda, hover con valor en cada marca, y ningún gráfico de doble eje | Completado | Playwright: 2 `svg[role="img"]` en el Parcial (dona + barras de desviación), 3 en el Completo (+ Pareto). Cada segmento/barra lleva `<title>` (tooltip accesible) y resalta al hover/foco (`onMouseEnter`/`onFocus`). Ningún componente usa dos ejes Y — son dos gráficos separados. |
| 10 | Matriz de partidas con scroll | Encabezado sticky visible al final de la tabla; barra de scroll horizontal alcanzable sin bajar la página | Completado | Playwright: tras `scrollTop = scrollHeight` en el wrapper de la tabla, `thead th` sigue `isVisible() === true`. Patrón `flex-1 min-h-0` + `sticky top-0` en cada `<th>` (nunca `max-h-[Nvh]`, design.md §8). |
| 11 | Partida sobre-ejecutada | Alerta visible con icono + texto en `1.3` y `2.1.5` de PS-0004 (dato real, no forzado) | Completado | Captura en vivo: fila `1.3` (metrado restante **-4.50**) y `2.1.5` (metrado restante **-108.00**), ambas con icono ⚠ + texto "Sobre-ejecutada" en rojo. Dato real leído de `pr_partidas`, no forzado. |
| 12 | Panel de diagnóstico | Muestra sobre-ejecutadas, sin actividad, recursos sin tarifa y HH de MOI (horas, sin costo) | Completado | Captura en vivo PS-0004: 3 sobre-ejecutadas · 40 sin actividad · 9 recursos sin tarifa (6 mano de obra, 3 equipos) con enlace a Recursos · 38.0 HH de MOI acumuladas, rotuladas "sin costo por diseño". |
| 13 | Cambiar el toggle a `COMPLETO` | La pantalla pasa al Dashboard Completo sin recargar a mano ni quedar en estado intermedio; el aviso viejo de "no construido" ya no aparece | Completado (2 vueltas) | Playwright con login admin: click en "Completo" → `PATCH /api/proyectos/{id}/tipo-dashboard` (200) → `router.refresh()` trae el Bloque E sin recargar la URL. Ver vuelta 1 del loop más abajo (falso negativo inicial por timeout corto del script de verificación, no del producto). Aviso viejo "Dashboard Completo no construido" retirado del código. |
| 14 | Permiso del toggle | Lo edita quien ya podía editar el proyecto; una cuenta sin ese permiso no puede cambiarlo | Completado | Playwright con `PR_TEST_USER_EMAIL` (sin admin): 0 botones de toggle visibles (se renderiza como etiqueta fija `Dashboard Parcial/Completo`), API guardada server-side con el mismo `validarEscrituraProyecto(id, puedeAdjudicarProyecto)` que ya usa `datos/route.ts`. |
| 15 | PPC en el Completo | Se muestra con nombre, fórmula y unidad, **separado de SPI** y rotulado como indicador LPS | Completado | Captura Bloque E: tarjeta propia "PPC — Percent Plan Complete", fórmula "(actividades − actividades con CNC) / actividades", rótulo "Indicador LPS, no EVM — no se mezcla con SPI"; SPI vive en una tarjeta distinta de la fila de KPI de arriba. |
| 16 | PPC contra cálculo a mano | Coincide con `(actividades − actividades con CNC) / actividades` de PS-0004 | Completado | Cálculo independiente desde `pr_partidas` crudos: (31−17)/31 = 45.16% → Dashboard muestra **45.2%**. Coincide también con la fila "Total proyecto" de la pantalla PR. |
| 17 | Pareto de CNC | Barras ordenadas de mayor a menor frecuencia (no alfabético), con acumulado y agrupación "Otras" | Completado | `construirParetoCnc` (función pura, 5 tests unitarios) ordena desc. por conteo y agrupa cola larga en "Otras" desde `maxBarras`. En vivo, PS-0004 solo tiene 1 causa resuelta contra el catálogo — ver nota en la vuelta 3 del loop sobre por qué el conteo es bajo (no es un bug). |
| 18 | Pareto contra los datos reales | Las causas y conteos coinciden con los CNC de los RDT validados de PS-0004 | Completado | Cálculo independiente desde `rdt_actividades`/`rdt_partes` crudos (19 partes VALIDADO): 1 actividad con `cnc_causa_id` resuelto, causa "Condiciones climáticas adversas." — coincide exacto con la única barra que muestra el Pareto en pantalla. |
| 19 | Enlace a Curva S desde el Completo | Lleva a la pantalla del Agente D; no hay curva embebida en el Dashboard | Completado | Playwright: `a[href="/proyectos/{id}/curva-s"]` presente en el Bloque E; ningún gráfico de serie temporal en el Dashboard. |
| 20 | Los dos matices | Parcial y Completo se distinguen visualmente pero usan los mismos tokens y componentes; ningún color fuera del sistema | Completado | Capturas lado a lado: mismo esqueleto (filtros → KPI → gráficos → matriz → diagnóstico → resumen); el Completo agrega el Bloque E con un borde/fondo `accent-secondary` (token existente) — sin colores nuevos. |
| 21 | Rollup de portafolio | Sigue funcionando igual que antes de esta fase | Completado | Playwright: `/programas` y el listado de portafolio cargan sin error tras los cambios. `DonaCosto.tsx` (compartido con el rollup) se revisó en el lugar — mismas props, mismo `calcularSegmentosDona` con la nueva separación de 2px — sin romper su consumidor en `programas/[id]/portafolios/[portafolioId]/dashboard/page.tsx`. |
| 22 | Resumen ejecutivo | Dos líneas, al final de la página, en los dos Dashboards, sin repetir los números de arriba | Completado | Captura PS-0004: "El servicio está con atraso crítico (SPI 0.18) y dentro del presupuesto (CPI 68.94)." + "3 partidas sobre-ejecutadas (metrado restante negativo) — es lo que más pesa hoy." Dos líneas, ningún número repetido tal cual (SPI/CPI ya estaban arriba, pero como calificativo de contexto, no como repetición del dato). |
| 23 | Móvil | Las dos páginas se recorren sin desbordes ni columnas cortadas | Completado | Playwright viewport 390×844: `scrollWidth <= clientWidth` (sin overflow horizontal); captura confirma KPI en 2 columnas, filtros apilados, header legible. |
| 24 | Teclado | Los `<select>` y el toggle se operan con teclado y el foco es visible | Completado | `<select>`/`<input type="date">`/`<button>` nativos (operables con teclado por defecto); se quitó un `outline-none` que iba a romper el foco visible en los gráficos SVG y se reemplazó por `focus-visible:outline` explícito antes de verificar (hallazgo propio en revisión, no de Playwright). |
| 25 | Cuenta sin permisos de administración | Ve lo que le corresponde, sin filtrar datos de más ni romperse | Completado | Playwright con `PR_TEST_USER_EMAIL`: ve los mismos KPI reales que el admin (el Dashboard no filtra datos por rol, solo la capacidad de editar `tipo_dashboard`), toggle no editable, sin errores en pantalla. |

**Cierre de esta Punch List:** se cierra **en loop** (ver protocolo, paso 5). El agente verifica, corrige y vuelve a verificar hasta que los 25 ítems estén en **Completado**, con evidencia real de la app. No se entrega con ítems abiertos ni observados; si uno no se puede cerrar, se consulta a Victor en vez de dejarlo a medias.

## Coordinación con el Agente D

| | Agente C (Dashboard) | Agente D (Curva S) |
|---|---|---|
| **Rama** | `feat/dashboard-fase-3-parcial-completo` | `feat/curva-s-fase-3-serie-temporal` |
| **Pantalla** | `(workspace)/proyectos/[id]/dashboard` | `(workspace)/proyectos/[id]/curva-s` |
| **Archivos propios** | `dashboard/page.tsx`, `src/lib/dashboard/dashboard.ts` | módulo de serie temporal + su pantalla |
| **Flujo que edita** | `11-dashboard.md` | su propio archivo de flujo |
| **No toca** | Curva S, serie temporal, `evm.ts` | Dashboard, `dashboard.ts`, `evm.ts` |
| **Migraciones** | ninguna (ver C0) | `07x` si hace falta |

**Compartido y fijo para los dos:** la paleta PV azul / AC naranja / EV aqua, el rótulo de costo directo en USD, y el patrón "Pendiente" cuando no hay Plan Maestro aprobado. Si uno de los dos necesita cambiarlo, se acuerda con Victor y se escribe en los dos archivos.

### ⚠️ Punto de choque: los dos tocan la navegación

Los dos agentes agregan un chip al grupo `'Planificación'` y lo inyectan en el panel izquierdo. Eso significa que **los dos modifican los mismos dos archivos**:

- `src/lib/config/nav-proyecto.ts` (el ítem nuevo en el array del grupo)
- `src/components/ui/WorkspaceShell.tsx` (la inyección en `itemsGrupoProyecto`)

**Cómo se maneja, sin que ninguno espere al otro:**

1. **Cada agente agrega solo su propio chip.** El Agente C no agrega el de Curva S ni al revés — si lo hiciera, el chip apuntaría a una ruta que todavía no existe.
2. **Conflicto de merge esperado y aceptado.** Es trivial: dos ítems agregados al mismo array. **El segundo en mergear lo resuelve conservando los dos chips**, no eligiendo uno.
3. **Ninguno reformatea, reordena ni "limpia" esos dos archivos.** Cualquier cambio cosmético convierte un conflicto de dos líneas en uno de doscientas. Si un agente ve algo que mejorar ahí, lo **reporta en su informe de limpieza**, no lo toca.
4. **El orden final en el panel izquierdo es `… → DP → PR → Dashboard → Curva S`.** Quien resuelva el conflicto deja ese orden.

**Prohibido para los dos:** `src/lib/pr/evm.ts`, el motor de RDT del Agente A, y la pantalla del PR.

## Informe de limpieza (entregable obligatorio al cerrar)

### Archivos y código que quedaron viejos

1. **`src/app/proyectos/[id]/dashboard/`** (carpeta completa, incluido `src/app/proyectos/` que queda vacía tras el `git mv`).
   - **Qué es:** la ubicación original del Dashboard, fuera del route group `(workspace)`.
   - **Por qué quedó vieja:** C1 la movió a `(workspace)/proyectos/[id]/dashboard/` con `git mv` — es el mismo archivo, no una copia; la carpeta vieja no tiene ningún archivo.
   - **Qué lo reemplaza:** `src/app/(workspace)/proyectos/[id]/dashboard/page.tsx`.
   - **Quién más la referencia:** nada — búsqueda de `proyectos/[id]/dashboard` en `src/` sin resultados fuera de la nueva ubicación y de `nav-proyecto.ts`/`WorkspaceShell.tsx` (que apuntan a la URL, no a la carpeta). **No se borró** (AGENTS.md); Victor decide si eliminar la carpeta vacía.

2. **El aviso "Dashboard Completo no está construido" y el toggle `SelectorDashboard`, dentro de `dashboard/page.tsx`** (a nivel de servicio, `/proyectos/[id]/dashboard`) **quedaron viejos y se quitaron con el resto del `page.tsx` reescrito** (C9 construyó el Completo de verdad ahí).
   - **Corrección sobre una primera versión de este informe:** al buscar referencias reales antes de reportar `SelectorDashboard.tsx` como código muerto, apareció que **sigue en uso** — pero en `programas/[id]/portafolios/[portafolioId]/dashboard/page.tsx`, el **rollup de portafolio**, una pantalla distinta y explícitamente fuera de alcance de esta fase ("no se rediseña salvo que se rompa"). Ese rollup tiene su **propio** toggle "vista=completo" y su **propio** aviso "todavía no está construido", heredados del mismo diseño original de PR #6 pero para el nivel de portafolio, no de servicio. **No se tocaron.**
   - **Qué lo reemplaza (solo a nivel de servicio):** `ToggleTipoDashboard.tsx` + `/api/proyectos/[id]/tipo-dashboard` + `BloqueE.tsx`.
   - **Quién más referencia `SelectorDashboard.tsx` hoy:** el rollup de portafolio (activo, no tocar). El componente **no queda huérfano** — se corrige aquí para no reportarlo como muerto por error.

3. **La excepción `item.clave === 'dashboard' ? pathname === href : pathname.startsWith(href)`** en `WorkspaceShell.tsx` (línea ~213 antes de esta fase).
   - **Qué es:** un caso especial para que el chip de Dashboard no quedara "activo" en todas las subrutas del proyecto, porque su ruta vieja (`/proyectos/[id]`) era prefijo de todas ellas.
   - **Por qué quedó vieja:** C0b corrigió la ruta a `/proyectos/[id]/dashboard`, que ya no es prefijo de nada más — la excepción dejó de tener motivo. Se quitó (no se dejó arrastrada), reemplazada por el mismo `pathname.startsWith(href)` que usan los demás ítems.
   - **Qué lo reemplaza:** el cálculo genérico de `activo`, sin caso especial.
   - **Quién más lo referencia:** nadie — era una línea local a esa función.

### Cosas que se revisaron y NO quedaron viejas (aclarado para que no se vuelvan a tocar)

- **`src/lib/dashboard/dashboard.ts`** (BAC/AC/HH con fuentes propias, distintas de `evm.ts`, señalado por el Agente B como riesgo): **sigue en uso real** por el rollup de portafolio (`programas/[id]/portafolios/[portafolioId]/dashboard/page.tsx`, `page.tsx` del portafolio, `GrillaProyectosReales.tsx`) y por `evm.ts` mismo (importa sus funciones base). El Dashboard de esta fase (a nivel de servicio) **no usa sus cálculos de BAC/AC/SPI/CPI** — usa `evm.ts` directamente, igual que la pantalla PR, así que no hay más duplicación de la que ya existía para el rollup. Se le agregaron dos funciones nuevas (`construirResumenEjecutivoBreve`, revisión de `calcularSegmentosDona` con separación de 2px) sin tocar las siete funciones que sí sigue usando el rollup.
- **`TablaConsolidadoRdts.tsx`** con su `max-h-[70vh]` viejo (deuda técnica anotada en design.md §8): no se tocó, fuera de alcance de esta fase, tal como el propio design.md ya advertía.

### Reglas seguidas

- No se borró ningún archivo ni columna de base de datos.
- Cada punto de arriba se verificó con una búsqueda real de referencias (`Grep`), no de memoria.

## Decisiones y convenciones acordadas durante la ejecución

1. **Fecha de corte y orden de la matriz son los únicos dos filtros de esta fase** (C3, ya decidido en el plan antes de implementar) — no se agregó ningún filtro adicional por cuenta propia.
2. **El Dashboard usa `evm.ts` directamente (`calcularIndicadoresPartida`/`calcularIndicadoresProyecto`), no `dashboard.ts`, para BAC/PV/EV/AC/SPI/CPI/PPC.** Mismo patrón que la pantalla PR — es lo que garantiza que Dashboard y PR muestren exactamente el mismo número siempre (verificado en vivo: AC, EV y CPI de PS-0004 coinciden dígito a dígito entre las dos pantallas). `dashboard.ts` se mantiene para lo que sigue necesitando (dona de composición del costo, que sí requiere el desglose por tipo de recurso que `evm.ts` no expone a ese nivel, y el rollup de portafolio).
3. **Colores nuevos agregados a `globals.css`**: `--color-serie-pv` (`#3987e5`), `--color-serie-ac` (`#d95926`), `--color-serie-ev` (`#199e70`) — ya validados en el plan, canónicos y fijos, compartidos con la Curva S del Agente D. El gráfico "Desempeño por partida" usa `--color-accent-secondary` (ya existente) como color único de serie, y el Pareto de CNC usa `--color-accent` (ya existente) — ninguno de los dos reutiliza los colores de estado (emerald/rose/amber), tal como exige el plan.
4. **El resumen ejecutivo breve califica plazo y costo por separado** (uno con SPI, otro con CPI), no con una sola palabra derivada del semáforo. Encontrado en la verificación en vivo: el semáforo del Dashboard es CPI+IP por diseño ya existente (no incluye SPI a propósito, mismo criterio que el resto de la app) — usarlo para calificar "cómo va en plazo" producía frases contradictorias con el propio SPI impreso al lado (`"en línea: SPI 0.18"` con PS-0004, donde el CPI extremadamente favorable —AC casi en cero, RDT real aún sin capturar del todo— tapaba un atraso real). Corregido antes de la primera pasada de captura de evidencia; ver vuelta del loop más abajo.
5. **El toggle `tipo_dashboard` vive en el propio Dashboard** (no en "Editar servicio"), junto al semáforo, porque es lo primero que se lee al entrar a la pantalla que cambia. Nueva ruta `PATCH /api/proyectos/[id]/tipo-dashboard`, mismo guard (`validarEscrituraProyecto` + `puedeAdjudicarProyecto`) que ya usa `datos/route.ts` — no se tocó esa ruta para no mezclar los dos formularios.
6. **"Partidas sin actividad"** (panel de diagnóstico) se define como `actividades_acum === 0` (ninguna actividad D registrada en RDT validado para esa partida) — distinto del estado "No inicia" de la tabla vieja, que miraba `metrado_acumulado === 0`. Los dos pueden diferir: una partida puede tener actividad registrada con metrado 0 en el corte, o metrado > 0 sin que `actividades_acum` se haya recalculado aún. Se dejó así porque el diagnóstico pregunta específicamente "¿hay evidencia de campo?", no "¿hay avance?".
7. **`rdt_actividades.cnc_causa_id` vs. `rdt_actividades.cnc` (texto libre) no son la misma fuente** — hallazgo verificado en vivo, no documentado antes en ningún plan: `actividades_con_cnc_acum` (que alimenta el PPC) cuenta actividades con `cnc` (texto libre) no vacío; el Pareto de esta fase, tal como pide C8, cuenta `cnc_causa_id` (la referencia resuelta contra el catálogo). Para PS-0004 eso da 17 actividades con CNC en texto libre pero solo 1 resuelta contra el catálogo — no es un bug de esta fase, es que la resolución por texto exacto (`db/054`) no matcheó la mayoría del texto libre ya cargado antes de que el catálogo existiera. Anotado aquí para que un agente futuro no lo interprete como error del Pareto.

## Mejoras a flujos

Ver tarea C9. `11-dashboard.md` reescrito completo (antes era un stub de dos líneas desactualizado) con los dos Dashboards, filtros, indicadores, PPC como LPS, la paleta de series compartida con la Curva S, y la aclaración de que la Curva S no vive aquí. `14-accesos-y-restricciones.md` no se tocó: el toggle reutiliza el permiso ya existente (`puedeAdjudicarProyecto`), no crea ningún acceso nuevo que registrar. `design.md` no recibió ninguna regla nueva propuesta esta fase — todo lo usado (paleta de series, separación de la dona, gráficos SVG a mano) ya estaba cubierto por el plan o por precedente existente.

## Vueltas del loop de verificación (protocolo, paso 5)

Todas ejecutadas el 2026-09-22, con Playwright + login real (`PR_TEST_ADMIN_EMAIL`/`PR_TEST_USER_EMAIL`) contra PS-0004 y PS-0002.

**Vuelta 1 — falso negativo por mayúsculas en las aserciones del script de verificación, no del producto.**
Varias etiquetas del Dashboard (Diagnóstico, "Bloque E — Dashboard Completo", "PPC — Percent Plan Complete") usan `uppercase` de Tailwind. El script de verificación leía `body.innerText()`, que refleja el texto ya transformado por CSS (todo en mayúsculas), y las aserciones buscaban el texto en minúscula/mixto original → 4 ítems (12, 13, 15, 19) marcaron falso "FAIL". Cambiado a `body.textContent()` (no afectado por CSS) en el script de verificación. Sin cambios en el producto — se dejaron los `uppercase` porque son la convención visual ya usada en el resto de la app.

**Vuelta 2 — timeout del script de verificación demasiado corto para el toggle y el filtro de fecha, no un bug de la pantalla.**
Con la corrección de la vuelta 1, los ítems 13/15/19 seguían fallando: el script esperaba un `waitForTimeout(1000)` fijo tras el click en "Completo", pero el ciclo PATCH → `router.refresh()` → nuevo RSC tomó hasta ~3s en el servidor de desarrollo. Confirmado con DB directa (`tipo_dashboard` sí quedaba en `'COMPLETO'` tras el click) que el guardado funcionaba — el front tardaba en reflejarlo. Cambiado el script para esperar la condición real (`aria-pressed="true"` con el texto correcto, o la URL con el parámetro esperado) en vez de un tiempo fijo. Mismo patrón aplicado al filtro de fecha de corte (ítem 6), que había fallado por la misma razón en una corrida posterior. Sin cambios en el producto — el comportamiento (refrescar sin recargar la URL) es correcto, solo lento en dev.

**Vuelta 3 — hallazgo real, corregido en el producto: el resumen ejecutivo breve sonaba contradictorio.**
Con PS-0004 en vivo (SPI 0.18, CPI 68.94 — AC casi en cero porque el RDT real de esa partida aún no se capturó del todo, CPI extremo como consecuencia), el resumen decía **"El servicio está en línea: SPI 0.18, CPI 68.94."** — "en línea" salía del semáforo (CPI+IP, sin SPI por diseño ya existente de la app) y contradecía al propio SPI impreso al lado. Corregido en `construirResumenEjecutivoBreve` (`dashboard.ts`): ahora califica plazo (SPI) y costo (CPI) por separado, cada uno con su propio umbral, sin pasar por el semáforo. Nueva redacción verificada: **"El servicio está con atraso crítico (SPI 0.18) y dentro del presupuesto (CPI 68.94)."** Se re-verificaron los ítems que toca el cambio (2, 4, 22 — KPI, rótulos y resumen ejecutivo), sin romper ninguno. Tests unitarios de `construirResumenEjecutivoBreve` actualizados con este caso real como regresión.

Tras la vuelta 3, la Punch List completa corrió en verde (24/24 en el script automatizado + verificación manual de los ítems 3, 7, 16, 18 y 20, no cubiertos por el script). Ningún ítem quedó abierto ni "observado".

**Vuelta 4 — corrección del propio informe de limpieza, no del producto.**
Al redactar la sección "Archivos y código que quedaron viejos" se afirmó por memoria que `SelectorDashboard.tsx` y el aviso "Dashboard Completo no está construido" habían quedado huérfanos. Antes de dejarlo escrito, se corrió el `Grep` real que AGENTS.md exige para cualquier "esto quedó sin uso" — y apareció que ambos **siguen vivos** en el rollup de portafolio (`programas/[id]/portafolios/[portafolioId]/dashboard/page.tsx`), una pantalla distinta y fuera de alcance. Corregido antes de cerrar la fase; ningún archivo se tocó de más.
