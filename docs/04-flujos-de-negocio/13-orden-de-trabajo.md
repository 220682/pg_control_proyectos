# 13 — Orden de trabajo (OT)
> Lee si: la tarea toca la Orden de Trabajo (OT) o su número. **Hoy no hay UI ni captura estructurada**; no confundir con el RDT (flujo 06).


**No implementado en UI.** El servicio tiene N° OT. RQ y RDT se vinculan por ese número; este flujo (captura estructurada de la OT) aún no se escribe ni se muestra.

**N° OT editable (Victor, 2026-11-03).** El N° OT es el código real del servicio en la empresa, con la forma **`PS-<número>-<año>`** (ej. `PS-108-2026`); se sigue aceptando el correlativo antiguo `PS-0001`. Quien adjudica lo **escribe** al crear el servicio (ya no se propone un correlativo) y se corrige en **Editar servicio** (mismo permiso de editar servicio). El servidor lo pasa a mayúsculas, valida la forma y que no se repita. Al cambiarlo, los RQ, restricciones y adjuntos ya emitidos **conservan su código**; los nuevos usan el N° OT nuevo. Los cuatro servicios reales quedaron con su código: PS-108-2026 (Facilidades de Villa Fase 2), PS-140-2026 (Mantenimiento exterior CCI), PS-167-2026 (Obras civiles detección contraincendios) y PS-131-2025 (Jahuay alcantarillas y enrocados).

No confundir con RDT (flujo 06).

El aviso que recibe el supervisor operativo cuando se le asigna un servicio (y el de cuando se le retira) no es parte de este flujo: lo describe el [flujo 04](04-notificaciones.md) y el cambio de responsable, el [flujo 08](08-programa-portafolio-proyecto.md).
