# Progreso: correcciones de la prueba del RDT en PS-0001

Plan: [2026-10-21-correcciones-prueba-rdt-ps0001.md](../01-planes/2026-10-21-correcciones-prueba-rdt-ps0001.md). Evidencia: [carpeta homónima](../03-evidencia/2026-10-21-correcciones-prueba-rdt-ps0001/README.md).

| Tanda | Contenido | Estado | Resultado |
|---|---|---|---|
| Lote 0 | Restricciones desplegadas | Hecha (2026-10-21) | App `ddb18ee` en `main`; 2146 pruebas y build en verde |
| T1 | Fecha futura y Curva S semanal | Hecha | Pruebas nuevas en `fecha-futura`, `curva-s`, `textos` |
| T2 | Regla de HH de transversales | Hecha, migración por aplicar | `db/116` sin aplicar; IP del día 5 = 0,788 en prueba unitaria |
| T3 y T3b | Cargos sin tarifa, equivalencias del servicio | Hecha | Pantalla «Equivalencias de cargos del servicio» y opción «No se usa» |
| T4 | Formulario, equipos sin partida, rechazo y menores | Hecha | Bloqueo «equipo sin WBS» eliminado |
| T5 | Documentación de flujos | Hecha | Verificador de referencias: 0 huérfanos, 0 rotos |
| T6 | Auditoría | Hecha | [Informe](../04-auditoria/2026-10-21-correcciones-prueba-rdt-ps0001.md); hallazgos «a corregir» atendidos |

Commit de la app: `981b2fd` (local, sin empujar hasta aplicar `db/116`).
