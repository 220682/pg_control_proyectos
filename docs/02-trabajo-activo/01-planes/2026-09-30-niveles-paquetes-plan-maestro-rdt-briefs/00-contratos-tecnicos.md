# Contratos técnicos compartidos (índice)

Su propósito: que los cuatro carriles construyan **a la vez** contra formas acordadas, sin esperar el código de otro. Cada contrato está en **su propio archivo**; tu brief nombra cuál leer. **No leas los demás.** Un carril no cambia un contrato por su cuenta: si lo necesita, se detiene y devuelve la pregunta al Orquestador. Lo marcado «por confirmar» lo verifica el Worker en el código. Verificado en el código de la app (`main` `45c9e0a`, solo lectura, 2026-09-30).

| Archivo | Contenido | Dueño | Lo leen |
|---|---|---|---|
| `contrato-c1-niveles.md` | Roles, mapa de niveles, `NodoEstructura`, bloqueo de recarga | carril 1 | F1-A, F1-B, F2-A; F5-A |
| `contrato-c2-paquetes.md` | Vínculos, `paquete_trabajo_vinculos`, clave de reporte, API de Paquetes, regla del 100 % | carril 3 | F2-A; F5-A |
| `contrato-c3-plan-maestro.md` | Líneas del Plan Maestro, asignaciones, API, totales y caso de 4 semanas | carril 2 | F3-A, F3-B, F4-A; F5-A |
| `contrato-c4-real-por-clave.md` | `realPorClaveReporte` y su fuente | carril 4 (lo consume el 2) | F3-A, F3-B, F4-A; F5-A |
| `contrato-c5-rdt.md` | Columnas del vínculo del RDT, catálogo, validación, permisos vigentes | carril 4 | F4-A, F4-B; F5-A |
| `contrato-c6-interfaz.md` | Reglas de interfaz: lógica en módulos puros, «Crear paquete», paneles, asistente | todos (solo lectura) | las tandas de pantalla; F5-A |
