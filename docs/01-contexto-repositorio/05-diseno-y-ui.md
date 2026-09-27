# Diseño y UI

## Lectura obligatoria para cambios de interfaz

`docs/05-diseno-y-referencias/design.md` es la fuente de verdad visual (layout, tokens, componentes, tablas, accesibilidad) y es **lectura obligatoria** antes de cualquier cambio de interfaz — no opcional, aunque el cambio parezca menor.

## Mockups

`docs/05-diseno-y-referencias/mockups/` fija cómo se ve y cómo se llama cada pantalla (nomenclatura, campos). Es referencia de UI, no una lista de pendientes.

## Reglas de interfaz

Como este repositorio no contiene la implementación visual en ejecución, estas reglas se toman como directrices documentadas y no como inventario de componentes reales en código:

- Mantener consistencia visual con el sistema ya descrito en la documentación.
- No crear una segunda interfaz sin referirse primero a los flujos y pantallas existentes.
- Priorizar reutilización sobre nuevas construcciones aisladas.
- Mantener separación entre paneles de trabajo, estado operativo y resúmenes ejecutivos.
- Usar scroll horizontal en tablas largas sin perder contexto.
- No convertir un paquete operativo en una partida contractual sin validación.
- No declarar avances reales sin una fuente documentada de ejecución validada.
- **Si no existe un componente real en el repo, no inventar su nombre ni su comportamiento.**

## No inventar componentes

Si un mockup o `design.md` no cubre una pantalla o un componente concreto, se anota como hallazgo (o se pregunta al Responsable humano si bloquea la tarea) en vez de inventar un nombre o un comportamiento de UI que no está documentado.
