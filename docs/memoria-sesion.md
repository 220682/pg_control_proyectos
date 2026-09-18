# Memoria de sesión — cierre 29 ago 2026 (madrugada)

Frase de arranque en el chat nuevo: **sigue la memoria de sesión del 29 ago** (ver avance 06/07-sep abajo)

Handoff. Victor (Administrador). Lote 23 ago cerrado en prod. Lote 24 ago **en local, sin commit ni push**. Esta noche se acordó el orden de Crear RDTs / Consolidado: **primero Recursos con data real del presupuesto de Bancoductos**. No programar Crear ni Consolidado hasta que Personal y Equipos muestren esa data.

## Avance 2026-09-06 / 07 — Recursos: paso 0 y paso 1 HECHOS

- **Paso 0 (extracción) HECHO.** De la hoja **APU** del PS-065 Bancoductos, aplicando reglas de Victor:
  **13 cargos (HH) · 12 equipos · 1 subcontrato · 1 excluido (HERRAMIENTAS MANUALES %MO)**.
  Salida: `Informacion para pruebas/cargos-y-equipos-presupuesto.md`. Script versátil en el
  scratchpad de la sesión `71f7a484` (`extraer_recursos.py`, detecta columnas por encabezado).
  Reglas fijadas: descripción normalizada (sin punto final, MAYÚSCULAS); `MES → HH` con
  **8 h/día × 26 días/mes = 208**; del bloque "Equipo:" entra TODO con su unidad tal cual
  (HM/MES/UND), sólo se excluye `%MO`; vehículos quedan en MES; subcontratos SÍ (tabla nueva).
- **Paso 1 (SQL) HECHO, sin correr.** `py_control_proyectos_web/db/025_recursos_rdt.sql`:
  crea `recursos_cargos` / `recursos_equipos` / `recursos_subcontratos` (catálogo de EMPRESA,
  sin `proyecto_id`), RLS lectura-autenticados, semilla Bancoductos idempotente
  (`on conflict do nothing`), query de reconciliación comentada. `db/README.md` línea 25.
  **PENDIENTE: Victor lo pega y ejecuta en el SQL Editor de Supabase.** No hubo commit/push.
- **Siguiente: paso 2** — pantallas del apartado Recursos (Personal / Equipos / Materiales-inhabilitado),
  panel izquierdo, sólo admin + jefe de proyectos.
- Aparte: el parser web `src/lib/dp/parser-apu.ts` NO lee el PS-065 crudo (columnas −2, regex
  WBS `\d{2}\.\d{2}`). Sólo importa si se quiere importar el DP de esta OT en la app; para el
  seed no afecta. Detalle en la auto-memoria `reference-apu-parser-mismatch`.

## Lo primero del chat nuevo

**Extraer datos del presupuesto de pruebas** (cargos / mano de obra, equipos HM, partidas y und). No inventar personas ni equipos. Carpeta:

`pg_control_proyectos/Informacion para pruebas`

Archivo:

`PS-065-2026 - PROYECTO MOV. TIERRAS, FAB. E INSTALACIÓN DE BANCODUCTOS - AESA v2.xlsx`

Hojas: `PRESUPUESTO`, `PS`, `APU`, `PS..`, `GG`, `COMBUSTIBLE`, `METRADO`. La fuente de cargos y equipos es **APU** (mismo criterio que el parser DP). Con eso se prueban el sistema de inicio a fin.

**RDO — solo nombres y cargos** (Victor, 29 ago). Nada de partidas, HH, acumulados ni metrados. Lista: `Informacion para pruebas/nombres-y-cargos-rdo.md` (14 personas, hoja PERSONAL OFFSITE de 26 Excel). Fotos de cantera no se parsearon. El presupuesto sigue siendo la fuente de partidas, und, equipos y cargos de APU.

Plan de orden: `docs/Mejoras continuas/2026-08-29-orden-recursos-antes-rdt.md`.

## Dónde está cada cosa

| Carpeta | Qué es |
|---------|--------|
| `pg_control_proyectos` | Workspace Cursor: dominio, Excel, mockups, **Flujos de trabajo**, **Mejoras continuas**, esta memoria, **Informacion para pruebas** |
| `py_control_proyectos_web` | App real (Next.js). GitHub `220682/py_control_proyectos_web`, rama `main` |

Código: `C:\Users\BRANDY\Downloads\VICTOR\CLAUDE CODE\py_control_proyectos_web`

Producción: https://py-control-proyectos-web.vercel.app

Local: `npm run dev` en la carpeta web → http://localhost:3000 (mismo Supabase que prod).

No migrar a la carpeta web ni tocar código ahí sin autorización explícita.

## Modelo de interfaz (Victor, 24 ago — no mover)

Una interfaz por acción. Dos puertas: chip de Mi entorno + panel derecho (grupos / Accesos rápidos). El rol habilita o corta el chip. Accesos rápidos es la misma segunda puerta, no una tercera. Geren puede entrar a Logística y Supervisión operativa si el rol lo permite.

## Esta noche (28–29 ago) — Crear RDTs, diseño; aún no código de la app

Mockup PROM-GP-002: `docs/visual-companion/crear-rdts.html`. Canvas: `crear-rdts.canvas.tsx`.

Acuerdos:

- **Subir RDTs** queda fuera de este entorno: no carga datos ni alimenta consolidado. Más adelante se puede quitar. No borrar ahora.
- **Crear RDTs** (página completa `/rdts/crear`): supervisor operativo + **Geren plus** (administrador y jefe de proyectos). Jefe de OT **no** crea. Botones: **+ Actividad / + Persona / + Equipo** (sin + Material). **Cargar RDT al sistema** (no “Guardar RDT”). **Guardar como plantilla**.
- **Consolidado RDTs** deja de ser la copia de Status. Matriz: filas partidas / HH / HM / materiales (vacío); cada día cargado = una columna + **Acumulado**. Encabezados del sistema (filtros/orden en columnas, `CabeceraPagina`).
- **Status de RDTs** será como Status RQ: lista los RDT **cargados**; descarga lista / uno / varios según filtro en formato **PROM-GP-002**.
- **Apartado Recursos** (panel izquierdo, mismo criterio que Proyectos): solo admin y jefe de proyectos. Ítems: Personal (cargos), Equipos, Materiales **inhabilitado**.
- El presupuesto **no trae nombres ni DNI**: trae cargos (mano de obra) y equipos. No sembrar ficticios del mockup.

**Orden (no saltar):** ~~(0) presupuesto en `Informacion para pruebas`~~ ✅ → ~~(1) extraer y tablas `recursos_cargos` / `recursos_equipos`~~ ✅ (SQL creado, falta correrlo) → **(2) pantallas Recursos ← acá va lo siguiente** → (3) Crear RDTs → (4) Consolidado → (5) Status.

**No está en la app.** No hay commit de este lote.

## Lote 24 ago — código local, sin commit/push

Ficha: `docs/Mejoras continuas/2026-08-24-status-entorno-apartado-proyectos.md`

HEAD remoto/prod sigue en `bb3f751`. Todo lo de ese lote está **uncommitted** en `main` local.

Al commitear (solo si Victor lo pide): `src/` del lote 24. **No** incluir borrados de `docs/Flujos de trabajo/` ni `?? .cursor/` del repo web.

## Cerrado en prod (23 ago)

Lote 22 ago 14/14 OK. Lote 23 ago 3/3 OK. HEAD `bb3f751`.

## Qué queda fuera (no programar hasta que Victor lo pida)

- **Pasar responsabilidades a**
- OT (flujo 13) no está en UI. No es RDT; solo se cruzan por N° OT.
- Crear RDTs / Consolidado matriz / Recursos — acordado, **esperar extracción del presupuesto** (arriba).
- Plantillas de RDT (misma cuadrilla) — van con Crear RDTs.
- Parsear fotos RDO de cantera (nombres/cargos ya salieron de los Excel)
- Quitar Subir RDTs

## Cómo registrar las mejoras

Una mejora **no está hecha** hasta que está en **todas** las pantallas que la usan.

Lo acordado se guarda en `docs/Mejoras continuas/` **aquí**. Al tocar un flujo, no modificar otros. Archivo compartido: cambio mínimo + tests + declarar “compartido”.

## SQL en Supabase

| Script | Estado |
|--------|--------|
| `022_rq_estados_adjuntos.sql` | Aplicado (sondeado 21 ago) |
| `023_rol_supervisor_ssoma.sql` | Victor dijo que lo corrió. No se volvió a sondear |
| `024_rdts.sql` | Igual |
| `025_recursos_rdt.sql` | **Creado 06-sep. PENDIENTE que Victor lo pegue y ejecute en Supabase** |
| RDT estructurado (cabecera/actividades/tareo) | **No existe todavía** (va con Crear RDTs, paso 3) |

## Conceptos que no hay que mezclar

- **Status RQ** = una fila por cabecera. PDF **PROM-GP-008**.
- **Consolidado RQ** = una fila por ítem. PDF **PROM-GP-004**.
- **Crear RDTs** = llenar PROM-GP-002. **Subir RDTs** = foto/PDF (fuera de este flujo). Listado PDF viejo = **PROM-GP-0006**; descarga de RDT cargado = **PROM-GP-002**.
- **Geren** = administrador + jefe_de_oficina_tecnica + jefe_de_proyectos.
- **Geren plus** (Recursos y Crear RDTs) = administrador + jefe_de_proyectos. Jefe de OT no.
- Importar DP y generar PR son flujos independientes. OT ≠ RDT (solo se cruzan por N° OT).
- Borrar RQ solo Status, solo admin.

## 2026-09-17 — 4 flujos nuevos + pendiente de acceso a Supabase

Se crearon los flujos **14-accesos-y-restricciones**, **15-cronograma**,
**16-paneles** y **17-chat-agentico** en `docs/Flujos de trabajo/` (ver
README de esa carpeta). Cronograma Fase 1 ya está en main
(`py_control_proyectos_web`, migración `036` corrida); los otros 3 son
solo visión de Victor, sin construir.

**Pendiente de decisión — acceso directo a Postgres para Claude.** Hoy
Claude solo tiene las llaves de la API REST de Supabase (`.env.local`:
`NEXT_PUBLIC_SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY`), que sirven
para leer/escribir filas de tablas ya existentes pero NO para correr
migraciones (`CREATE TABLE`, etc.) — por eso Victor sigue pegando y
corriendo el SQL él mismo en el editor de Supabase. Si en algún momento
Victor quiere que Claude corra migraciones directo, haría falta agregar
a `.env.local` la cadena de conexión directa de Postgres (Project
Settings → Database → Connection string en el dashboard de Supabase) —
decisión de Victor, no tomada todavía. Aun con esa llave, Claude
confirmaría con Victor antes de correr cada migración (cambio difícil de
deshacer).
