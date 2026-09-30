> Parte de los contratos técnicos compartidos (índice: `00-contratos-tecnicos.md`). Un carril **no cambia** un contrato por su cuenta: si lo necesita, se detiene y devuelve la pregunta al Orquestador. Lo marcado «por confirmar» lo verifica el Worker en el código. Verificado en `main` `45c9e0a`, solo lectura, 2026-09-30.

## C6 · Interfaz

- Sin pruebas de componentes (`vitest`: `environment: 'node'`, `include: src/**/*.test.ts`): **toda la lógica de la pantalla vive en módulos puros con prueba**; el componente solo la pinta.
- Ningún chip ni acceso nuevo. La acción «Crear paquete» del panel (`registro-accesos.ts`, id `crear-paquete`, `/paquetes-trabajo?proyectoId=&accion=crear`) **se conserva**; ya llega a la pantalla como `abrirNuevoAlInicio` y debe abrirla en modo «crear» (casillas activas).
- Paneles ocultables: control del shell (`WorkspaceShell.tsx`: asides de escritorio `lg:flex`, izquierdo `w-60` y derecho `w-64`), recordado por usuario; en móvil los paneles ya son un cajón. El icono flotante del asistente (abajo a la derecha, dentro del `main`) no debe tapar columnas del lienzo.
- `design.md` (lectura por secciones: §3, §5, §8, §9, §10, §12) y las maquetas aprobadas de F0 mandan en la interfaz; si falta un componente, se anota como hallazgo, no se inventa.
