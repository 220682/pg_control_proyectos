# Informes: Avance por nivel completo y Plantilla Promcoser

Fecha: 2026-11-06. Estado: `Implementando` (código desplegado en `main`; faltan la revisión de Victor en producción y los Pendientes; sesión cerrada el 2026-11-06).

Lote de trabajo tradicional por orden directa de Victor. No siguió el flujo con Orquestador ni tuvo Gates.

## Objetivo, alcance y no alcance

- **Resultado esperado:** el bloque «Avance por nivel» de los informes muestra siempre todo el presupuesto (niveles, paquetes y partidas), sin recortarlo; los informes emitidos los ve el equipo del servicio; hay una plantilla de empresa predeterminada.
- **Alcance:** «Avance por nivel» (hoja, PDF, Word, Excel y barra de sección), Plantilla Promcoser en «Nuevo informe», flujo 22.
- **No alcance:** declarar o quitar partidas transversales (Victor, 2026-11-06: no se tocan las de PS-108); cambiar la regla de acceso por servicio; migraciones.

## Repositorios

| Repositorio | Commit | Estado |
|---|---|---|
| `py_control_proyectos_web` | `04f9b18` | en `main`, desplegado a pedido de Victor |
| `pg_control_proyectos` | sin commit | flujo 22 y este plan modificados en el equipo local |

## Avance

- [x] Causa de las partidas que no salían (leída de los datos reales de PS-108, solo lectura): los subpresupuestos 1 (preliminares) y 4 (pintado exterior) traen partidas directas, sin paquete de partidas, y los modos de paquetes solo mostraban paquetes. No era un tema de transversales.
- [x] «Avance por nivel»: los tres modos de paquetes y «Niveles del presupuesto» incluyen niveles, paquetes y partidas sueltas, en orden de WBS. Modos renombrados «Presupuesto completo…».
- [x] Plantilla Promcoser (de la empresa, predeterminada) basada en «Standar 2» de Victor, sin fotos, firma, logo del cliente ni textos de un día. No exige migración.
- [x] Informes emitidos: ya los ven todos los roles con el servicio asignado; los dos informes de PS-108 siguen en borrador.
- [x] Flujo 22 actualizado.

## Evidencia

- Tipos limpios y 696 pruebas de informes y API pasan; pruebas nuevas de partidas sueltas y de la plantilla.
- No se revisó en pantalla ni en producción con sesión iniciada.

## Pendientes

1. Victor revisa en producción «Presupuesto completo (HH y avance)» en PS-108: deben salir los niveles 1 y 4 con sus partidas.
2. Victor emite los informes `PS-108-2026-ID-1` e `ID-2` (siguen en borrador) y asigna al servicio a los roles que deben verlos (PS-108 solo tiene 2 miembros).
3. Victor confirma que «pronto ser» era **Promcoser** y si la plantilla debe llevar sus fotos, firmas y logo del cliente.
4. Decidir si «Mis formatos» debe poder compartirse con otros usuarios del servicio (hoy son individuales por diseño).
5. Subir a `main` los cambios de `pg_control_proyectos` (flujo 22 y este plan).

## Mejoras (de trabajo)

- Extraídas a [`2026-11-06-leer-datos-reales-antes-de-suponer-la-causa.md`](../../03-aprendizaje-continuo/2026-11-06-leer-datos-reales-antes-de-suponer-la-causa.md).

## Reglas de negocio acordadas en esta tarea

Integradas en el flujo 22: «Avance por nivel» muestra el presupuesto completo (niveles, paquetes y partidas fuera de paquetes) en todos los modos; Plantilla Promcoser de la empresa, predeterminada; «Mis formatos» individuales y plantillas del RDT compartidas por servicio.

## Observaciones sobre la política

- Ninguna.

## Carpetas/archivos huérfanos

- `py_control_proyectos_web`: `db/095_cerrar_lectura_directa.sql`, `db/114_personal_datos_contacto.sql`, `scripts/cargar-rq-ps108-fase2.mjs`, `scripts/revision/zz-agrupar.mjs`, `zz-docs.mjs`, `zz-reclasificar-ps131.mts` sin versionar y ajenos a este lote. Sin borrar.
- `pg_control_proyectos`: imágenes sueltas en la raíz (`estado-ps0002.png`, `fabricaciones-*.png`, `fuente-whatsapp-nuevo.png`, `gestion-interesados-panel.png`, `login-ojo-contrasena.png`, `prueba-sello-T3.jpg`, `restricciones-admin.png`), varias carpetas de evidencia y archivos de `Informacion para pruebas/` sin versionar, y `Formato Requerimiento.xlsx` modificado. Sin borrar.
