# Plan — Gestión documentaria (documentos pedidos, enviados, observados y aprobados)

## Identificación y estado

- Tema: apartado «Gestión documentaria» en `py_control_proyectos_web`, hermano de «Gestión de interesados».
- Fecha: 2026-10-25.
- Estado: `Planificando` (Spec aprobado; falta el Gate 1 para construir).
- Gate Spec: aprobado por Victor (2026-10-25) — pidió la interfaz, pidió «mejora mi idea», respondió las decisiones de una fila por documento, semáforo ajustable y área primero, y dijo «dale».
- Gate 1: pendiente.
- Gate 2: pendiente.

## Referencia al Spec aprobado

Pedido de Victor (2026-10-25), en sus palabras: otra interfaz, en Planificación, que **extraiga en un cuadro la gestión documentaria** de los correos: qué correo **pide** algo, cuál **responde**, cuál **observa**, cuál **aprueba**; un resumen ordenado de lo que está pendiente de aprobación, emisión, aprobado, etc., con filtros. Decisiones posteriores:

1. **Una fila por documento** (no por correo).
2. **Semáforo:** rojo a los 7 días por defecto, con un desplegable para elegir en cuántos días se enciende; cada documento muestra además una **nota** que dice de qué se trata.
3. Lo primero que se distingue es **a qué área le corresponde** y luego **qué documento es**: una ficha técnica pedida para SSOMA, para Oficina Técnica o para Calidad son documentos distintos.
4. Pocas columnas: cada documento es una ficha compacta que lleva el **correo, el remitente** y otros datos menores.
5. **Áreas:** SSOMA, Medio Ambiente, Oficina Técnica, Calidad, **Administración** (incluye accesos y otros) y **Gerencia** (contratos y compras, por ahora); se afinan después.
6. La contratista usa **un correo por área**; el cliente puede que no. Se trata igual: el área se decide por quién envía, mirando la dirección **y** el nombre.
7. El correo se ve desde esta misma interfaz, en el panel lateral que ya existe; **no** se redirige a Gmail.

## Objetivo, alcance y no alcance

- **Resultado esperado:** una pantalla por servicio que lista cada documento con su área, su tipo, su estado actual, a quién le toca mover, cuántos días lleva esperando (con semáforo) y la nota de qué trata.
- **Alcance:**
  1. Base de datos: documentos, relación nota ↔ documento, tabla «remitente → área» que aprende de las correcciones (`db/120_gestion_documentaria.sql`; el número se confirma al construir).
  2. Servidor: listado con filtros, creación y edición por el administrador, asignación de una nota a un documento, reglas de estado y de «a quién le toca», aprendizaje de remitente → área.
  3. Pantalla: ficha compacta por documento con historial desplegable; resumen por área; filtros; desplegable del semáforo; exportación a Excel.
  4. Carga inicial a partir de las 309 notas ya clasificadas (script local; los datos de correos no van al repositorio).
  5. Chip «Gestión documentaria» en el grupo Planificación, permisos, flujo 24 nuevo y actualización de los flujos 14, 16 y 23.
- **No alcance:** responder correos desde la app; redirigir a Gmail; que el agente Haiku en la nube arme los documentos nuevos (es la tarea posterior ya conversada); definir con detalle qué ve cada área (Victor lo afina luego); el servidor de adjuntos en R2 (otro pendiente del plan de Gestión de interesados).
- **Validación esperada:** pruebas automáticas de las reglas puras (estado, a quién le toca, días y semáforo, área por remitente); `tsc`, `eslint` y `vitest` sin errores nuevos; verificación en la app publicada con Playwright en PS-0002 y PS-0003.

## Diseño propuesto

**Estados del documento:** Solicitado → Enviado → Observado → Levantado → Aprobado. Se derivan de los movimientos de las notas del documento: Solicitud = Solicitado; Enviado = Enviado; Observado = Observado; Enviado después de una observación = Levantado; Aprobado = Aprobado. El administrador puede corregir el estado a mano.

**A quién le toca:** pasa a la parte contraria de quien escribió el último correo. Nosotros = remitente del dominio de la contratista; cliente = cualquier otro. Una solicitud del cliente le toca a la contratista; un envío de la contratista le toca al cliente. Aprobado = a nadie.

**Días esperando:** desde el último movimiento, mientras no esté aprobado. Rojo al llegar al plazo elegido (3, 5, 7, 10, 15 o 30; 7 por defecto), ámbar desde la mitad del plazo, verde antes. El plazo elegido se guarda en el navegador de cada persona.

**Área:** se decide por la dirección del remitente y, si no basta, por su nombre. Con la carga inicial se llena una tabla «remitente → área»; cuando Victor corrige un área, esa corrección queda para los correos que lleguen después. Lo que no se puede decidir queda en «Sin área» para que el administrador lo asigne.

**Ficha (dos líneas, poco ancho):**
- Línea 1: tipo y nombre del documento con revisión, chip del área, chip del estado, semáforo con los días.
- Línea 2: remitente, asunto y fecha del último correo, y «le toca a: nosotros / cliente».
- Debajo, la **nota** que explica de qué se trata.
- Al desplegar: historial de correos del documento (cada uno abre en el panel lateral existente) y adjuntos.

**Filtros:** servicio, área, tipo, estado, «a quién le toca», remitente, fechas, «solo pendientes». Arriba, un resumen por área (por emitir, esperando al cliente, observados, aprobados) que filtra al tocarlo.

**Tipos de documento:** plano, ficha técnica, procedimiento o PETS, informe, trámite, valorización y otros.

**Notas por asignar:** las notas de temas documentales de «Gestión de interesados» que aún no pertenezcan a un documento aparecen en un contador «Por asignar», para vincularlas a un documento existente o crear uno nuevo.

**Permisos (provisorio, igual que Gestión de interesados):** ver = administrador, jefe de proyectos, jefe de oficina técnica y supervisor de oficina técnica; gestionar = administrador (y jefe de proyectos según la nota ¹⁹ del flujo 14, hasta que se aplique la decisión final de «todos ven, solo el administrador edita»).

## Entorno, repositorios, ramas y worktrees

Trabajo directo en `main`, sin worktree (como en el plan anterior). Código en `py_control_proyectos_web`; documentación aquí. No se hace push hasta que la migración esté aplicada en Supabase (si no, la pantalla falla en producción); Victor aplica el SQL y se le da la ruta completa del archivo.

## Skills aplicables

`seguir-flujo-de-planes` (activación y antes del cierre), `cerrar-tanda` (al terminar cada tanda), `trasladar-hallazgos` (tanda final), `verificar-permisos-por-rol` (permisos del chip y de la ruta).

## Fases y dependencias

| Fase | Contenido | Depende de |
|---|---|---|
| F1 | Migración y tipos | — |
| F2 | Reglas puras con pruebas: estado, a quién le toca, días y semáforo, área por remitente | F1 |
| F3 | Rutas API (listar, crear, editar, asignar nota, exportar) | F2 |
| F4 | Pantalla, chip, permisos y matriz base | F3 |
| F5 | Carga inicial desde las 309 notas (script local) | F1, F2 |
| F6 | Flujo 24, flujos 14, 16 y 23, índices, evidencia y verificación en producción | F4, F5 |

## Equipo del plan

Orquestador (esta sesión, Sonnet 5.5). Sin Workers separados: el alcance es acotado y se construye en tandas pequeñas desde la sesión. Documentador en Haiku para la tanda final si hace falta.

## Archivos / componentes afectados

Nuevos: `db/120_gestion_documentaria.sql`, `src/lib/gestion-documentaria/*`, `src/app/api/gestion-documentaria/**`, `src/app/(workspace)/proyectos/[id]/gestion-documentaria/page.tsx`, `src/components/gestion-documentaria/*`, script local de carga inicial (fuera del repositorio o excluido de git si contiene datos). Modificados: `permisos.ts`, `registro-accesos.ts`, `matriz-base-flujo14.ts`, `cobertura-pantallas.ts` y sus pruebas, `db/README.md`. Documentación: flujo 24 (nuevo), flujos 14, 16 y 23, índice de flujos, `docs/README.md` (conteo de flujos), Matriz de permisos (artefacto; esta cuenta no lo abre, ver memoria).

## Punch List embebida

| # | Ítem | Verificación |
|---|---|---|
| 1 | Migración y tipos | SQL revisado, Victor lo aplica; tipos compilan |
| 2 | Reglas puras | `vitest` verde con casos de cada estado y del semáforo |
| 3 | Rutas API con permisos | Sin sesión 401; rol sin permiso 403; administrador 200 |
| 4 | Pantalla | Playwright: ficha compacta, nota visible, desplegable de semáforo, filtros, correo en panel lateral, ancho de Victor |
| 5 | Carga inicial | Conteo de documentos por área y por estado revisado con Victor |
| 6 | Permisos por rol | `verificar-permisos-por-rol` |
| 7 | Documentación | Flujo 24 y flujos 14, 16, 23 coherentes; Matriz anotada |

## Riesgos y bloqueos

- **Agrupar correos en documentos** exige juicio (qué correos son el mismo documento). La carga inicial la hace el Orquestador y Victor la revisa; los nuevos quedan en «Por asignar» hasta que exista el agente Haiku.
- **Áreas por remitente:** un mismo correo puede servir a varias áreas; se resuelve con la corrección manual que queda aprendida.
- **Matriz de permisos** sin acceso desde esta cuenta: se anota el chip nuevo en el flujo 14 y se avisa a Victor.
- **Migración:** hasta que Victor aplique el SQL no se empuja el código.

## Registro de decisiones

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-10-25 | Interfaz nueva «Gestión documentaria» en Planificación, junto a Gestión de interesados | Victor |
| 2026-10-25 | Una fila por documento; rojo a los 7 días con plazo elegible; la ficha lleva una nota de qué trata | Victor |
| 2026-10-25 | Primero el área y luego el tipo de documento; áreas: SSOMA, Medio Ambiente, Oficina Técnica, Calidad, Administración (accesos y otros) y Gerencia (contratos y compras, por ahora); se afinan después | Victor |
| 2026-10-25 | El área se decide por quien envía (dirección y nombre), igual para contratista y cliente; el correo se ve en el panel lateral, sin redirigir a Gmail | Victor |
| 2026-10-25 | AESA queda fuera de los 4 servicios | Victor |

## Enlaces a progreso y evidencia homónimos

Aún no creados; se crean al iniciar la construcción (`02-progreso/` y `03-evidencia/` con este mismo nombre).

## Libro de hallazgos

### Mejoras (de trabajo)

Ninguna.

### Reglas de negocio acordadas en esta tarea

Las del apartado «Referencia al Spec aprobado» y «Diseño propuesto»; se integran directo en el flujo 24 al cerrar. Contradicciones con lo ya escrito: ninguna detectada hasta ahora (el flujo 23 solo habla de temas y notas, no de documentos).

### Observaciones sobre la política

Ninguna.

### Carpetas/archivos huérfanos

Ninguna.

## Informe de Auditoría

Pendiente.

## Mensaje de cierre

Pendiente.

## Elementos postergados propuestos para planes futuros

- Agente Haiku en la nube que arme y actualice los documentos desde los correos nuevos.
- Afinar qué ve y qué hace cada área.
- Alertas cuando un documento pase a rojo.
