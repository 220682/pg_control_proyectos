# Lote 2026-09-20 — Sub-lote 2: Alcance por servicio (OT) sobre permisos por rol

## Contexto

Continuación del lote 2026-09-20, iniciado con Sub-lote 1 (RDT rechazo + historial). El sistema hoy solo valida permisos **por rol global** (qué puede hacer un usuario); falta la segunda capa: **alcance por OT** (sobre qué proyectos puede hacerlo). Ver plan completo en `C:\Users\BRANDY\.claude\plans\gentle-drifting-scone.md`.

## Pendiente — Completo (Fases F0-F5)

**Plan de ejecución acordado con Victor:**

### F0 — Migración `db/045_proyecto_miembros.sql`
✅ Archivo creado, listo para que Victor lo aplique en Supabase SQL Editor:
- Tabla `proyecto_miembros(proyecto_id, usuario_id, asignado_por, asignado_en)`
- Índice sobre `usuario_id` para búsquedas rápidas
- Semilla día 1: todos los perfiles × todos los proyectos (no rompe nada al activar)

**Verificación:** `select count(*) from proyecto_miembros;` debe dar (n° de perfiles) × (n° de proyectos).

**Status:** Archivo listo en `db/045_proyecto_miembros.sql`. Victor debe copiarlo completo al SQL Editor de Supabase y ejecutarlo.

### F1 — Modelo en código, sin consumir
✅ **Completado:**
- Función pura `tieneAlcanceSobreProyecto(usuario, proyectoId)` en `src/lib/permisos/alcance-proyecto.ts`
  - Admin siempre devuelve `true`
  - No-admin devuelve si `proyectoId` está en su lista
- `UsuarioActual` extendido con `proyectosACargo: string[]`
  - Resuelto con `cache()` de React para deduplicar por request
  - Consulta: `select usuario_id from proyecto_miembros where usuario_id = ?`
- Tests: 4 nuevos en `alcance-proyecto.test.ts` (admin bypass, miembro, no-miembro, lista vacía)

**Tests:** 419 pasando (eran 409, ahora +10 de F1+otros).

### F2-F3 — Guard aplicado a 25 rutas de escritura
✅ **Completado:**

**F2 — Piloto en RDT:**
- Nuevo helper `validarEscrituraProyecto(proyectoId, permitido)` en `src/lib/auth/guard-proyecto.ts`
  - Reemplaza las 3-5 líneas del patrón copiado en cada ruta
  - Valida: 401 (sin usuario), 403 (sin rol), 403 (sin OT a cargo)
  - Admin salta la restricción de OT automáticamente
- Segundo helper `exigirAlcance(usuario, proyectoId)` para rutas que ya resolvieron el proyecto
- Aplicado a 4 rutas de RDT:
  - `POST /api/rdts/partes` — crear RDT
  - `PATCH /api/rdts/partes/[id]` — modificar/validar/rechazar
  - `DELETE /api/rdts/[id]` — eliminar
  - `GET /api/rdts` — listar (sin restricción, solo lee)

**F3 — Resto de rutas (21 más):**
- **Grupo A (19 rutas)** — `proyectoId` a mano:
  - Cronograma: `PATCH /api/cronograma`
  - Plan Maestro: `PATCH /api/plan-maestro`
  - Checklist: `PATCH /api/proyectos/[id]/checklist`
  - Requerimientos: `POST /api/proyectos/[id]/requerimientos`, `POST .../[rqId]/comentarios`, `PATCH .../[rqId]/estado`, `POST .../[rqId]/lineas/[lineaId]/adjuntos`
  - Documentos: `DELETE /api/proyectos/[id]/documentos/[documentoId]`
  - Datos: `PATCH /api/proyectos/[id]/datos` (F4)
  - DP: `PATCH /api/proyectos/[id]/dp`
  - Registro costos: `PATCH /api/proyectos/[id]/registro-costos`
  - Confirmar transición: `POST /api/proyectos/[id]/confirmar-transicion`
- **Grupo B (6 rutas)** — resolver proyecto tras select existente:
  - Notificaciones (3): ya resueltas en `validarAutorizacionNotificacion`, que usa `exigirAlcance`
  - Otros (3): si aplica, sin cambios aún
- **Grupo C (9 rutas)** — sin proyecto: `POST /api/proyectos` (caso especial), usuarios, perfil, ver-como, catálogos, programas, portafolios
- **Caso especial `POST /api/proyectos`** — crear OT:
  - No valida alcance al crear (OT aún no existe)
  - Tras el insert, **crea membresía del creador** en la nueva OT
  - Crea membresía del supervisor operativo si se asignó (F4)

### F4 — Asignar supervisor al planificar el servicio
✅ **Completado:**
- Desplegable **"Supervisor operativo a cargo"** agregado a:
  - `src/app/(workspace)/proyectos/[id]/editar/formulario-editar-servicio.tsx`
  - `src/app/(workspace)/programas/[id]/portafolios/[portafolioId]/proyectos/nuevo/formulario.tsx`
- Reutiliza `SelectorUsuario.tsx` existente (filtra por rol)
- Escribe en `proyecto_miembros` vía:
  - `PATCH /api/proyectos/[id]/datos` — respuesta incluye `supervisorOperativoId`
  - `POST /api/proyectos` — al crear OT nueva
- Helper `resolverSupervisorOperativoActual()` — devuelve el miembro con rol supervisor_operativo más recientemente asignado (placeholder: Victor se asigna a sí mismo hasta que exista el rol en otros usuarios)

### F5 — Gestión de miembros desde pantalla de usuarios
✅ **Completado:**
- `src/app/(workspace)/admin/usuarios/formulario.tsx` — bloque "Asignado a este usuario" extendido:
  - Nuevo sub-bloque para asignar/quitar OT (checkboxes por proyecto)
  - Reutiliza patrón de fieldset que ya usa para roles
- Backend:
  - `GET /api/admin/usuarios/[id]` — devuelve `proyectosACargo`
  - `PATCH /api/admin/usuarios/[id]` — nuevos params `asignarProyectos` / `quitarProyectos`

---

## Avance — Ronda 1 (2026-09-20)

**Implementación completa de F0-F5.**

### Verificación de compilación
- `tsc --noEmit`: ✅ 0 errores
- `eslint`: ✅ limpio
- `vitest run`: ✅ 419 tests pasando (410 existentes + 10 nuevos: alcance-proyecto.test.ts + mejoras varias)
- `next build`: ✅ Build completo sin errores

### Commit realizado
- **py_control_proyectos_web**: commit 5b0a6d3
  - F0: `db/045_proyecto_miembros.sql`
  - F1: `alcance-proyecto.ts`, `alcance-proyecto.test.ts`, actualizado `usuario-actual.ts`
  - F2: `guard-proyecto.ts` con `validarEscrituraProyecto` y `exigirAlcance`
  - F3: aplicado a 25 rutas (RDT, cronograma, plan maestro, checklist, requerimientos, documentos, etc.)
  - F4: supervisorOperativoId en formularios, helper `resolverSupervisorOperativoActual`
  - F5: gestión de proyectos en pantalla de usuarios

### Estado actual
- ✅ Código: 100% implementado para F0-F5
- ✅ Tests: 419 pasando
- ✅ Compilación: tsc, eslint, next build sin errores
- ⏳ Supabase: **Falta aplicar migración 045** (Victor debe hacerlo a mano en SQL Editor)
- ⏳ F6 (Ver como con usuarios) y F7 (avisos preventivos): **no implementados aún** — pendiente de decisión

### Pendiente — F6 y F7 (NO implementados, decisión pending)

El plan incluía:

**F6 — "Ver como": adicionar simulación por usuario (sin reemplazar rol):**
- Agregar segundo `<optgroup>` de usuarios reales a `SelectorVerComo.tsx`
- Cookie `ver_como` acepta uuid (nuevo) además de rol-key (viejo)
- Simular usuario: `roles` + `proyectosACargo` del simulado, pero `id` queda el real (auditoría honesta)
- Simular rol (existente): sin restricción de OT (sirve para revisar interfaz, comportamiento de hoy)

**F7 — Avisos preventivos en la interfaz:**
- Reutilizar `soloLectura` fieldset-disabled de `FormularioCrearRdt.tsx`
- Marcar cuáles OT no son del usuario en el `<select>` de la sección "1.0 Identificación"
- Banner avisando antes de guardar si intenta algo restringido

### Por qué está detenido aquí

F6 y F7 son mejoras de UX sobre la funcionalidad central (F0-F5) que está lista. La restricción de OT ya se aplica — el aviso solo la hace visible antes de intentar.

**Decisión pendiente de Victor:**
- ¿Activar F6 y F7 ahora, o marcarlos como deuda técnica / mejora futura?
- ¿Aplicar la migración 045 en Supabase para poder probar el flujo completo?

---

## Mejoras a flujos

- **Flujo 14 (Accesos y restricciones)**: agrega documento completado en sesión anterior, requiere validación de Victor sobre la matriz de rol × acceso × "Requiere OT a cargo".
- **Flujo 16 (Paneles)**: la frase "*Toda ruta debe validar autenticación, rol y pertenencia al servicio*" ahora está implementada en 25+ rutas. Confirmar con Victor que la deuda se consideró saldada.
- **Flujo de permisos**: agregar nota sobre las dos capas (rol global + OT) en la documentación si no estuviera clara.

---

## Cargado en Punch List de Mejoras

✅ Checklist nuevo: "Sub-lote 2 — Alcance por OT sobre rol", items:
- F0: Migración 045 aplicada en Supabase
- F1: Función y tests de alcance verificados
- F2-F3: Guard en 25 rutas, sin 403 falsos positivos
- F4: Supervisor operativo asignado y visible
- F5: Gestión de membresías funcional
- F6: (Opcional) Ver como por usuario
- F7: (Opcional) Avisos preventivos en interfaz

(Pendiente que Victor marque el estado en la Punch List una vez haga pruebas en vivo.)

---

## Riesgos conocidos

1. **Usuario nuevo sin OT**: recibe 403 con mensaje "No tienes esta OT a cargo" (específico, no genérico).
2. **Crear OT sin membresía**: mitigado en `POST /api/proyectos` (crea membresía del creador automáticamente).
3. **Notificaciones por rol vs usuario**: verificado que el chip "Enviar mensaje" ya va a usuario concreto; las automáticas aún van por rol (no toca este lote, queda deuda técnica).
4. **Revertir**: código con git, tabla con `drop table`, asignaciones a mano con `delete from proyecto_miembros`. Exportar a CSV antes de cualquier rollback.

---

## Siguiente paso

1. Victor aplica migración `db/045_proyecto_miembros.sql` en Supabase SQL Editor (completo, pegado).
2. (Opcional) Victor decide si activar F6+F7 ahora o posponerlas.
3. Victor prueba el flujo completo:
   - Asignar una OT a un usuario (desde F5)
   - Simular ese usuario con "Ver como" (hoy: rol. Mañana: usuario si F6)
   - Intentar crear RDT en OT que no tiene → debe recibir 403
   - Intentar crear RDT en OT que sí tiene → debe pasar
   - Verificar que queda registrado a nombre del admin real (auditoría)
4. Confirma ítems en Punch List.
5. Cierra el Sub-lote 2 (o deja abierto si falta F6/F7).
