# Dashboard Fase 3 (Agente C): los dos Dashboards — Parcial mejorado y Completo construido

**Estado (2026-09-21):** PLAN INICIAL — **pendiente de aprobación de Victor** (plan + Punch List). Sin checklist aprobado, la implementación no arranca. Trabaja en paralelo con [Curva S / Fase 3 (Agente D)](2026-09-21-curva-s-fase-3-agente-d.md).

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

- **Rama propia en `py_control_proyectos_web`**, no directo a `main`. Rama sugerida: `feat/dashboard-fase-3-evm`. Al llegar al 100% del checklist, abre un **PR** para que Victor lo revise antes de mergear.
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

- [ ] C0 · Confirmado que no hace falta ninguna migración (o consultado a Victor si falta una columna)
- [ ] C1 · Dashboard movido a `(workspace)`, URL intacta, sin colisión de rutas, enlaces revisados
- [ ] C2 · Estructura de página con el orden acordado, sin `max-w-*`, espaciado de una sola medida por bloque
- [ ] C3 · Fila única de filtros arriba, `<select>` nativos con label, opciones dinámicas, scopean todo lo de abajo
- [ ] C4 · Fila de KPI con contexto, variación con icono + signo, rótulos `(US$, CD)`, "Pendiente" sin Plan Maestro
- [ ] C5 · Dona revisada + barras de desviación por partida, SVG sin dependencias, hover en cada marca, paleta validada, sin doble eje
- [ ] C6 · Matriz de partidas con pre-vuelo §11 respondido, sticky de celda, `flex-1 min-h-0`, `scope="col"`, alerta de sobre-ejecución
- [ ] C7 · Panel de diagnóstico con los cuatro puntos y camino a la pantalla que corrige
- [ ] C8 · Bloque E del Completo: PPC (separado de SPI, rotulado como LPS) + Pareto de CNC ordenado por frecuencia, con "Otras" y hover; enlace a Curva S
- [ ] C9 · Toggle `tipo_dashboard` funcional, matiz visual del Completo, aviso viejo retirado, permiso sin cambios
- [ ] C10 · Resumen ejecutivo de dos líneas, al final, en los dos Dashboards
- [ ] C11 · `11-dashboard.md` reescrito con los dos Dashboards; `design.md` solo si Victor aprueba la regla nueva; este archivo actualizado con decisiones y vueltas del loop
- [ ] C12 · tsc, eslint, tests y build limpios
- [ ] C13 · **Autoverificación Playwright en loop hasta cerrar: Punch List 100 % Completado, sin ítems abiertos ni observados**
- [ ] C14 · Informe de limpieza entregado

## Punch List — a aprobar ANTES de implementar

Se carga en la Punch List de Mejoras como checklist nuevo: **"Dashboard Fase 3 — Dashboard profesional con EVM real"**.

| # | Ítem | Resultado esperado | Estado | Evidencia |
|---|---|---|---|---|
| 1 | Abrir el Dashboard de PS-0004 | Aparece dentro del shell (nav izquierda y panel derecho), misma URL que antes | Pendiente | |
| 2 | Fila de KPI | BAC, PV, EV, AC, SPI, CPI y % avance físico con valores reales y su línea de contexto | Pendiente | |
| 3 | SPI y CPI contra cálculo a mano | Coinciden con el valor calculado manualmente para una partida | Pendiente | |
| 4 | Rótulos | Todo dice costo directo y USD; SPI/CPI con nombre, fórmula y unidad | Pendiente | |
| 5 | PS-0002 (sin Plan Maestro) | PV, SV y SPI dicen "Pendiente", con el aviso de por qué. Ningún 0 inventado | Pendiente | |
| 6 | Filtro de fecha de corte | Cambia KPIs, gráficos, tabla y diagnóstico a la vez; los números concuerdan entre sí | Pendiente | |
| 7 | Filtro que deja la tabla vacía | Estado "sin resultados" explícito, sin tabla en blanco ni error | Pendiente | |
| 8 | Recarga por filtro | El contenido anterior se mantiene atenuado; sin salto de layout ni parpadeo | Pendiente | |
| 9 | Gráficos | Dona y barras con leyenda, hover con valor en cada marca, y ningún gráfico de doble eje | Pendiente | |
| 10 | Matriz de partidas con scroll | Encabezado sticky visible al final de la tabla; barra de scroll horizontal alcanzable sin bajar la página | Pendiente | |
| 11 | Partida sobre-ejecutada | Alerta visible con icono + texto en `1.3` y `2.1.5` de PS-0004 (dato real, no forzado) | Pendiente | |
| 12 | Panel de diagnóstico | Muestra sobre-ejecutadas, sin actividad, recursos sin tarifa y HH de MOI (horas, sin costo) | Pendiente | |
| 13 | Cambiar el toggle a `COMPLETO` | La pantalla pasa al Dashboard Completo sin recargar a mano ni quedar en estado intermedio; el aviso viejo de "no construido" ya no aparece | Pendiente | |
| 14 | Permiso del toggle | Lo edita quien ya podía editar el proyecto; una cuenta sin ese permiso no puede cambiarlo | Pendiente | |
| 15 | PPC en el Completo | Se muestra con nombre, fórmula y unidad, **separado de SPI** y rotulado como indicador LPS | Pendiente | |
| 16 | PPC contra cálculo a mano | Coincide con `(actividades − actividades con CNC) / actividades` de PS-0004 | Pendiente | |
| 17 | Pareto de CNC | Barras ordenadas de mayor a menor frecuencia (no alfabético), con acumulado y agrupación "Otras" | Pendiente | |
| 18 | Pareto contra los datos reales | Las causas y conteos coinciden con los CNC de los RDT validados de PS-0004 | Pendiente | |
| 19 | Enlace a Curva S desde el Completo | Lleva a la pantalla del Agente D; no hay curva embebida en el Dashboard | Pendiente | |
| 20 | Los dos matices | Parcial y Completo se distinguen visualmente pero usan los mismos tokens y componentes; ningún color fuera del sistema | Pendiente | |
| 21 | Rollup de portafolio | Sigue funcionando igual que antes de esta fase | Pendiente | |
| 22 | Resumen ejecutivo | Dos líneas, al final de la página, en los dos Dashboards, sin repetir los números de arriba | Pendiente | |
| 23 | Móvil | Las dos páginas se recorren sin desbordes ni columnas cortadas | Pendiente | |
| 24 | Teclado | Los `<select>` y el toggle se operan con teclado y el foco es visible | Pendiente | |
| 25 | Cuenta sin permisos de administración | Ve lo que le corresponde, sin filtrar datos de más ni romperse | Pendiente | |

**Cierre de esta Punch List:** se cierra **en loop** (ver protocolo, paso 5). El agente verifica, corrige y vuelve a verificar hasta que los 25 ítems estén en **Completado**, con evidencia real de la app. No se entrega con ítems abiertos ni observados; si uno no se puede cerrar, se consulta a Victor en vez de dejarlo a medias.

## Coordinación con el Agente D

| | Agente C (Dashboard) | Agente D (Curva S) |
|---|---|---|
| **Pantalla** | `(workspace)/proyectos/[id]/dashboard` | pantalla nueva, chip propio |
| **Archivos propios** | `dashboard/page.tsx`, `src/lib/dashboard/dashboard.ts` | módulo de serie temporal + su pantalla |
| **Flujo que edita** | `11-dashboard.md` | su propio archivo de flujo |
| **No toca** | Curva S, serie temporal, `evm.ts` | Dashboard, `dashboard.ts`, `evm.ts` |
| **Migraciones** | ninguna (ver C0) | `07x` si hace falta |

**Compartido y fijo para los dos:** la paleta PV azul / AC naranja / EV aqua, el rótulo de costo directo en USD, y el patrón "Pendiente" cuando no hay Plan Maestro aprobado. Si uno de los dos necesita cambiarlo, se acuerda con Victor y se escribe en los dos archivos.

**Prohibido para los dos:** `src/lib/pr/evm.ts`, el motor de RDT del Agente A, y la pantalla del PR.

## Informe de limpieza (entregable obligatorio al cerrar)

Al terminar, antes de dar la fase por cerrada, el agente escribe en este archivo una sección `## Archivos y código que quedaron viejos`, con cuatro datos por ítem: **qué es**, **por qué quedó viejo**, **qué lo reemplaza** y **quién más lo referencia hoy**.

Reglas:

- **El agente no borra nada.** Reporta y Victor decide (AGENTS.md).
- **Ninguna columna de base de datos se borra ni se renombra** sin plan de migración aparte.
- Cada "esto quedó sin uso" se sostiene con una **búsqueda real de referencias en el código**, no de memoria.

Dos cosas que esta fase tiene que mirar sí o sí:

- **La carpeta `src/app/proyectos/`** tras mover el Dashboard: queda vacía. Reportarla.
- **Los componentes y helpers de la pantalla vieja** que la versión nueva ya no use.

## Decisiones y convenciones acordadas durante la ejecución

*(El agente escribe aquí, conforme ocurren, las decisiones nuevas tomadas con Victor: convenciones visuales, nombres, comportamientos de filtro, cualquier cosa que un agente futuro no deba volver a preguntar.)*

## Mejoras a flujos

Ver tarea C9.
