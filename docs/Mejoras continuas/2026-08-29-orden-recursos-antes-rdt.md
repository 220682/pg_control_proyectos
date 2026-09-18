# Plan de orden — Recursos antes de Crear RDTs y Consolidado

Pedido (29 ago): no inventar personal/cargos/equipos. Usar la data real del **presupuesto de Bancoductos**. Crear tablas. Ir en orden: primero lo que alimenta los desplegables; después Crear RDTs; después Consolidado.

Fuente de verdad para pruebas de punta a punta: carpeta `Informacion para pruebas`, archivo `PS-065-2026 - PROYECTO MOV. TIERRAS, FAB. E INSTALACIÓN DE BANCODUCTOS - AESA v2.xlsx` (hojas `PRESUPUESTO`, `PS`, `APU`, `METRADO`, …). Extraer cargos y equipos del **APU**; partidas/und del presupuesto/PS. El presupuesto no trae nombres ni DNI: trae **cargos** (mano de obra) y **equipos** (HM). Materiales no se catalogan en este lote.

Cuando esa OT tenga DP importado en la app, `dp_partidas` / `dp_recursos` deben coincidir con este Excel. No sembrar ficticios.

App: `py_control_proyectos_web`. Flujo 06 (RDT). Compartido mínimo: `permisos.ts`, `WorkspaceShell.tsx`, nav. Flujo 09 (DP) solo se **lee**, no se reescribe.

---

## Qué hay en el presupuesto (y qué no)

| En el DP de Bancoductos | Tabla hoy | Sirve para |
|---|---|---|
| Partidas (WBS, descripción, **und**, metrado) | `dp_partidas` | Desplegable de actividad / und en Crear RDT |
| Cargos (filas `tipo = mano_obra`) | `dp_recursos` | Desplegable de cargo / filas HH del consolidado |
| Equipos (filas `tipo = equipo`, unidad HM) | `dp_recursos` | Desplegable de equipo / filas HM del consolidado |
| Materiales | `dp_recursos` tipo material | **No** se copia. Ítem Materiales inhabilitado |
| Personas con nombre y DNI | no están en el presupuesto | Salen de los **RDO**, solo nombre y cargo: `Informacion para pruebas/nombres-y-cargos-rdo.md`. No se extraen partidas ni acumulados del RDO. |

Si esa OT aún no tiene DP importado, el paso 0 es importarlo (flujo 09). Sin DP no hay catálogo real.

---

## Orden (no saltar)

### 0. Extraer el presupuesto de `Informacion para pruebas`

Archivo `PS-065-2026 - … BANCODUCTOS - AESA v2.xlsx`. Listar cargos únicos (APU, mano de obra) y equipos únicos (APU, HM). Eso es la semilla. Después, al importar DP en la app, debe coincidir con este Excel.

### 1. Tablas de catálogo (copia del DP, no datos inventados)

SQL nuevo (p. ej. `025_recursos_rdt.sql`). Dos tablas de empresa, pobladas **desde** `dp_recursos` de Bancoductos:

- `recursos_cargos` — descripción, unidad `HH`, origen DP/OT
- `recursos_equipos` — descripción, unidad `HM`, origen DP/OT

Sin tabla de materiales. Sin filas de ejemplo. Script de carga: `INSERT … SELECT DISTINCT` de `dp_recursos` (`mano_obra` / `equipo`). Herramientas `%MO` no entran a equipos de RDT.

Permiso de mantenimiento: administrador y jefe de proyectos (Geren plus).

### 2. Apartado Recursos (pantallas)

Panel izquierdo, mismo criterio que Proyectos: solo admin y jefe de proyectos.

- **Personal** → listado de `recursos_cargos` (encabezados del sistema: filtros/orden en columnas)
- **Equipos** → listado de `recursos_equipos`
- **Materiales** → ítem visible e **inhabilitado**

Hasta que estas dos pantallas muestren la data real de Bancoductos, no se abre Crear RDTs.

### 3. Recién entonces: Crear RDTs

Página completa `/rdts/crear` (mockup PROM-GP-002). Desplegables:

- OT vigente → cliente/proyecto/ubicación
- Partida y **und** desde `dp_partidas` de esa OT
- Cargo / persona-cargo desde `recursos_cargos`
- Equipo desde `recursos_equipos`
- Especialidad, turno, CNC (12 causas PR C5)

Botones: **+ Actividad / + Persona / + Equipo**. **Cargar RDT al sistema**. **Guardar como plantilla**. Quien entra: supervisor operativo + admin + jefe de proyectos.

Aquí sí hacen falta tablas del RDT estructurado (cabecera, actividades, tareo, equipos del día). No se toca `rdts` de Subir.

### 4. Después: Consolidado RDTs

Matriz distinta a los otros consolidados. Filas: partidas, HH (por cargo), HM (por equipo), banda materiales vacía. Cada día cargado = una columna + **Acumulado**. Encabezados del sistema. Datos = lo cargado en el paso 3, no los PDF de Subir.

### 5. Status de RDTs (mismo lote o inmediatamente después)

Como Status RQ: lista los RDT **cargados**. Descarga lista / uno / varios según filtro en formato PROM-GP-002. Subir RDTs queda fuera de este entorno.

---

## Estado (13 sep)

Los cinco pasos están programados y en `main` local, sin subir a producción.

| Paso | Estado |
|---|---|
| 0. Extraer el presupuesto | ✅ |
| 1. Tablas de catálogo | ✅ `025` corrido en Supabase: 13 cargos / 12 equipos / 1 subcontrato |
| 2. Pantallas Personal y Equipos | ✅ vistas y aprobadas por Victor |
| 3. Crear RDTs | ✅ programado — **falta correr `026` en Supabase** |
| 4. Consolidado RDTs | ✅ programado — depende de `026` |
| 5. Status de RDTs + descarga PROM-GP-002 | ✅ programado — depende de `026` |

Sin `db/026_rdt_estructurado.sql` aplicado, las tres pantallas nuevas cargan
pero no encuentran tablas. Es el único bloqueo.

El catálogo de personal (`recursos_personal`, en `026`) es genérico: DNI,
nombre y cargo, sin nada específico de Bancoductos en el código ni en el
esquema. Elegir a alguien del desplegable en Crear RDT jala su DNI y su
cargo. El cargo del consolidado se agrupa tal como está en la base —
no hay ninguna capa aparte tratando de emparejarlo contra el presupuesto.

---

## Decisiones de Victor (13 sep) — valen para los pasos 3, 4 y 5

Resueltas antes de programar Crear RDTs. No volver a preguntarlas.

**1. Materiales: informativo, texto libre, sin catálogo.**
En Crear RDT el supervisor escribe a mano lo que usó ese día. No hay
desplegable ni tabla `recursos_materiales`, no hay cantidad sumable y no entra
al acumulado. En el Consolidado la banda Materiales **sí se muestra** con ese
texto por fecha — es informativa, no cuantificable. Sigue en pie: no se
cataloga materiales en este lote.

**2. El Consolidado RDTs es por OT, con filtro visible.**
Una OT a la vez, no global. El filtro lista las OT vigentes y cada opción se
muestra como `N° OT — Nombre del servicio` (pedido expreso: "para mejor
visualización"). Reutilizar `/api/proyectos/vigentes`, que ya devuelve
`numero`, `nombre` y `cliente`, igual que hace `FormularioSubirRdt`.
Coherente con que las filas de partidas salen del DP de esa OT.

**3. Equipos: al RDT diario solo entran los de unidad HM.**
De los 12 del presupuesto, camioneta pick up y minivan 14 pasajeros son MES y
el alicate crimpador es UND. Esos tres no se tarean por día: son costo fijo o
herramienta, no consumo diario. El desplegable de equipos de Crear RDT filtra
`unidad = 'HM'`. Siguen visibles en la pantalla Equipos del catálogo, que
muestra el presupuesto completo.

---

## Qué no hacer todavía

- No programar Crear ni Consolidado sin el paso 1 y 2 vistos en pantalla
- No sembrar nombres ficticios (Jhonny, Elmer, CAT 320 de ejemplo del mockup)
- No catálogo de materiales
- No borrar Subir RDTs
- No tocar otros flujos; nav/permisos/shell: cambio mínimo + tests + declarar compartido
