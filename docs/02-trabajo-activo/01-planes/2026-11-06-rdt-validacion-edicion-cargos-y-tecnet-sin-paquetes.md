# RDT: validación opcional, editar validados, cargos del presupuesto y Tecnet sin paquetes

Fecha: 2026-11-06. Estado: `Implementando` (código en `main`; falta que Victor aplique db/138, revise en producción y actualice la Matriz de permisos).

Lote de trabajo tradicional por orden directa de Victor. No siguió el flujo con Orquestador ni tuvo Gates.

## Objetivo, alcance y no alcance

- **Resultado esperado:** (a) un cargo no sale dos veces con nombres parecidos en el RDT; (b) el informe y el Dashboard dan el mismo avance; (c) cada servicio elige si sus RDT necesitan validación; (d) un RDT validado se puede editar; (e) Tecnet (PS-167) deja de trabajar por paquetes.
- **Alcance:** Crear RDT y Status de RDTs, bloque «Avance por nivel» de los informes, Plan Maestro (versión «Sin paquetes»), flujos 06, 14, 20 y 22.
- **No alcance:** borrar la fila repetida de Aquino en el RDT de PS-108 del 05-11 (Victor no lo autorizó); renombrar los cargos antiguos ya guardados en RDT y plantillas; los 14 RDT validados de Tecnet se quedan como están (Victor).

## Repositorios

| Repositorio | Commit | Estado |
|---|---|---|
| `py_control_proyectos_web` | `0739b8e`, `6760750` | en `main` (Vercel) |
| `pg_control_proyectos` | este commit | flujos 06, 14, 20, 22 y este plan |

## Avance

- [x] **Causa del cargo doble** (datos reales, solo lectura): las plantillas de RDT de PS-108 tenían el nombre antiguo del catálogo («SUPERVISOR DE CALIDAD»); el RDT del 05-11 salió de una plantilla y luego se volvió a agregar a la misma persona desde la lista, que propone el nombre del presupuesto («INGENIERO DE CALIDAD»). El servidor solo exigía que hubiera tarifa: no renombraba ni impedía repetir a la persona.
- [x] El servidor guarda cada cargo con el nombre del presupuesto; el formulario hace lo mismo al cargar plantillas y borradores; una persona repetida se rechaza en el formulario y en el servidor (`PERSONA_REPETIDA`).
- [x] **Causa del 8.69 % contra 8.76 %:** el chip «Avance medio» del informe era un promedio simple de las filas de «Avance por nivel»; el Dashboard pondera por presupuesto. Se quitó y se agregó la fila «Total del servicio» (EV/BAC = 8.76 % en PS-108).
- [x] «Avance por nivel» en cuatro opciones: metrado por subpresupuesto, metrado completo, HH por subpresupuesto, HH completo. Subpresupuesto y nivel con unidades mezcladas solo muestran avance; todo nivel en negrita.
- [x] Interruptor por servicio «el RDT necesita validación» (admin y JP; por defecto «Sí»; migración `db/138` sin aplicar).
- [x] Editar un RDT validado (admin y JP): motivo, historial, sigue validado, recalcula el Consolidado.
- [x] Plan Maestro: versión «Sin paquetes»; al aprobarla se archivan los paquetes sin uso; cada línea hereda la disciplina de su paquete.
- [x] Tecnet PS-167: versión 4 «Sin paquetes» creada y aprobada (desde la app local, contra la base real).
- [x] Flujos 06, 14, 20 y 22 actualizados.

## Evidencia

- Tipos limpios; 2716 pruebas pasan (una corrida tuvo 2 fallos intermitentes que no se repitieron); lint sin errores nuevos (los 8 que salen son de archivos no tocados).
- Pantalla (Playwright, 1366 px): Status de RDTs con el interruptor (deshabilitado hasta db/138) y el lápiz en filas validadas; informe `PS-108-2026-ID-2` con «Metrado por subpresupuesto» (1: 8.76 %, 2: 0.29 %, 3: 0.00 %, 4: 55.69 %, total 8.76 %; coincide con el Consolidado) y «Metrado completo» con niveles en negrita. El modo del bloque se devolvió a como estaba.
- Tecnet: v4 con 58 líneas, 0 de paquete, 9 partidas; PV por partida y fecha igual a v3 (215 combinaciones, 0 diferencias); Consolidado igual antes y después; 14 RDT reposicionados; 8 paquetes archivados; el catálogo del RDT lista las 9 partidas directas con el acumulado del Consolidado.

## Pendientes

1. Victor aplica `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\db\138_rdt_requiere_validacion.sql` (sin ella el interruptor sale deshabilitado y todo RDT necesita validación).
2. Victor actualiza la Matriz de permisos con las dos filas nuevas del flujo 14.
3. Fila repetida de Aquino en el RDT de PS-108 del 05-11: Victor la corrige con «editar RDT validado» o autoriza borrarla.
4. Decidir si se renombran a nombre del presupuesto los cargos antiguos ya guardados en RDT y plantillas (con respaldo).
5. Título del bloque del informe `PS-108-2026-ID-2`: dice «Avance por nivelñ» (ya estaba así guardado; no se tocó).
6. Victor revisa en producción.

## Mejoras (de trabajo)

- Antes de aprobar un Plan Maestro desde la app, guardar el PV por partida y fecha y el Consolidado, y compararlos después: así se demuestra que la versión nueva no cambió nada que no debía.

## Reglas de negocio acordadas en esta tarea

Integradas en los flujos: validación opcional por servicio y edición de RDT validado (06, 14), cargo con nombre del presupuesto y persona no repetida (06), versión «Sin paquetes» del Plan Maestro (20, 14), «Avance por nivel» en cuatro opciones con total del servicio (22).

## Observaciones sobre la política

- Ninguna.

## Carpetas/archivos huérfanos

- Los mismos del plan [Informes: Avance por nivel completo](2026-11-06-informes-avance-completo-y-plantilla-promcoser.md); ninguno nuevo. Sin borrar.
