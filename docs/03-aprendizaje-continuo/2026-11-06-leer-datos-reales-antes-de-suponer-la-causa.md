# Leer los datos reales antes de suponer la causa

Fecha: 2026-11-06. Origen: plan [Informes: Avance por nivel completo y Plantilla Promcoser](../02-trabajo-activo/01-planes/2026-11-06-informes-avance-completo-y-plantilla-promcoser.md).

- **Qué pasó:** Victor vio que no aparecían «las transversales» ni el pintado en un bloque de informe y pidió arreglar «el Plan Maestro». La causa real no era el Plan Maestro ni las transversales: dos subpresupuestos tenían partidas directas, sin paquete, y el bloque solo mostraba paquetes.
- **Cómo se resolvió:** una consulta de solo lectura a la estructura real del servicio (encabezados del DP y sus roles) mostró la causa en un paso. Sin eso se habría tocado lo que no debía.
- **Regla de trabajo:** ante «no aparece X», leer primero los datos reales del servicio (solo lectura) y comparar con lo que el código filtra, antes de cambiar reglas o datos.
- **Cuidado operativo:** no lanzar las pruebas en el mismo lote de llamadas que edita los archivos que prueban; el resultado puede salir con el código anterior. Editar, esperar y luego probar.
- **Limpieza:** el script de consulta temporal se crea en `scripts/revision/` con el cliente existente y se borra al terminar.
