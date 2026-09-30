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

## Política de interfaz nueva (instrucción para el Worker y el Planner)

Aprobada por Victor el 2026-09-30. La regla del sistema, con sus diez puntos, está en `docs/04-flujos-de-negocio/16-paneles.md`, sección «Política de interfaz nueva»; **no se copia aquí**. Toda pantalla nueva del workspace la cumple sin que Victor tenga que pedirla chip por chip: vive en el shell, se declara una sola vez en el registro único de accesos (o como excepción con motivo, con prueba automática de cobertura), conserva `?proyectoId=`, tiene tipo, muestra deshabilitado con título lo que el rol no puede usar, sale en la matriz del flujo 14 derivada del registro, respeta `design.md` y usa los estados y colores existentes.

El **Planner** copia la plantilla siguiente en toda Punch List con pantalla nueva, sin que Victor la pida. El **Worker** la cumple y aporta la evidencia. (Proponer llevarla al estándar agnóstico `00-estandar-agentes/` es decisión de Victor, a elevar por el Auditor; no se modifica desde aquí.)

| Ítem | Evidencia mínima |
|---|---|
| Existe la entrada del acceso en el registro (o la excepción con motivo) y la prueba de cobertura pasa | `npm test` |
| El chip aparece en los paneles declarados, informativo o acción según corresponda | Captura |
| Abierta desde un servicio, la pantalla conserva `?proyectoId=` en ambos paneles y preselecciona el servicio | Captura + URL |
| Cuenta con permisos altos y cuenta sin permisos de administración: chip habilitado o deshabilitado según el permiso, con título | Tabla + captura |
| URL directa sin permiso: el servidor la rechaza igual que antes | URL + resultado |
| Fila en la matriz derivada del flujo 14 | Diff de la matriz |
| Móvil, scroll horizontal de tablas y estados vacío, carga y error | Capturas |

## No inventar componentes

Si un mockup o `design.md` no cubre una pantalla o un componente concreto, se anota como hallazgo (o se pregunta al Responsable humano si bloquea la tarea) en vez de inventar un nombre o un comportamiento de UI que no está documentado.
