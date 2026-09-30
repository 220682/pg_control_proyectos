# Resultados F0-T · Maqueta del Plan Maestro con los tres paneles reales

Carril de diseño, rama `main`, sin worktree ni puerto. Sin navegador: revisión por lectura y `node --check`.

## Skills revisados

- `pg_control_proyectos/.claude/skills/`: `cerrar-tanda`, `seguir-flujo-de-planes`, `verificar-permisos-por-rol`. Usado: `cerrar-tanda` (estados y traspaso en este archivo). `verificar-permisos-por-rol` no aplica (no cambia permisos); `seguir-flujo-de-planes` es del Orquestador.
- `py_control_proyectos_web`: no tiene `.claude/skills/` (existe `.claude/` sin carpeta de Skills). Ninguno aplica.

## Estado de los ítems

| ID | Estado | Evidencia |
|---|---|---|
| F0T-1 | Conforme (pendiente de revisión de Victor) | `mockups/plan-maestro-tres-paneles.html`: pantalla completa con panel izquierdo (marca, «Todos los servicios», «Servicio actual», «Recursos de empresa» plegado, los 7 grupos de `ESTRUCTURA_IZQUIERDA` con sus rótulos y acciones separadas, pie con Usuarios/Notificaciones/Configuraciones/Cerrar sesión, «Ver como», usuario), centro con el lienzo aprobado (mismo contenido y cálculos de `plan-maestro-lienzo.html`, que no se modificó) y panel derecho («Accesos rápidos» con los 7 chips de `ACCESO_RAPIDO` y «Grupos del servicio» con los 7 grupos plegables, uno abierto a la vez). Rótulos tomados de `WorkspaceShell.tsx`, `panel-izquierdo.ts`, `panel-derecho.ts`, `PanelSecciones.tsx`, `PanelServicioIzquierdo.tsx` y `registro-accesos.ts` (solo lectura). Accesos sin pantalla atenuados (inertes); «Plan Maestro» marcado como la pantalla actual. Sin chip ni acceso nuevo. |
| F0T-2 | Conforme (pendiente de revisión de Victor) | Icono de cada panel en la esquina superior interior de su encabezado (izquierdo a la derecha, junto a «Control de Proyectos»; derecho a la izquierda, junto a «ACCESOS RÁPIDOS»), como `design.md` §3. Barra de la maqueta con 4 estados: tres abiertos, izquierdo oculto, derecho oculto, ambos ocultos; los iconos también alternan y sincronizan la barra. Oculto: tira de 24 px con el icono visible y el centro toma el ancho (`flex:1; min-width:0`). Comprobado por lectura del CSS/JS y `node --check`; no visto en navegador. |
| F0T-3 | Conforme (pendiente de revisión de Victor) | Asistente: botón flotante de 48 px (estilo de `ChatPlaceholder`: fondo elevado, acento) sobre el centro, sin franja reservada. Estados con datos, vacío, cargando y error conservados (los 4 botones de la barra). Móvil (≤1023 px): paneles ocultos, barra superior con ☰ y ◫ que abren cajones (X, fondo o Escape; devuelve el foco), sin el icono de ocultar; a 390 px el lienzo conserva WBS y descripción fijas. |
| F0T-4 | Conforme | `mockups/index.html` (tarjeta nueva) y `mockups/README.md` (fila nueva) enlazan la maqueta como «pendiente de revisión de Victor». `design.md` sin cambios (no hacía falta aclarar nada: versión 1.8.0 intacta). |

Comprobaciones: `node --check` del script extraído: OK. Balance de `<div>` (43/43), `<main>` y `<aside>`. Los constructores de los paneles se ejecutaron en Node: 7 grupos izquierdos, 7 derechos, 7 chips rápidos, sin errores. El archivo usa CRLF como el resto de maquetas.

## Handoff

- Falta: que Victor revise la maqueta en el navegador (abrir `mockups/plan-maestro-tres-paneles.html` a 1440 px y a 390 px; probar los 4 estados de paneles y los 4 estados del lienzo). Nada más pendiente por parte del Worker.
- Retomar: `node --check` sobre el script extraído del HTML; el cambio vive en un solo archivo nuevo más dos enlaces.
- Decisión técnica: los paneles se generan por script desde tablas locales que copian rótulos y orden del registro de la app; si la app cambia un rótulo, hay que actualizar la tabla `R`/`IZQ`/`DER` de la maqueta.
- Hallazgo: en la app real «Consolidado de servicio» va en el grupo Reportes del panel izquierdo y está inerte (sin pantalla); se reprodujo así, no arriba como sugería la captura de Victor.

## Preguntas para Victor (máx. 3)

1. Los iconos de los accesos son glifos de texto (la app usa `lucide-react`): ¿basta para revisar la estructura, o se prefiere dibujar los iconos reales en la maqueta?
2. «Ver como» muestra solo «Mi rol (Administrador)»: ¿quiere ver una variante con un rol de menos permisos (p. ej. Planner) para ver chips deshabilitados?
3. ¿Se deja «Recursos de empresa» plegado (como hace la app con un servicio activo) o se muestra abierto en la maqueta?

## Mejoras de trabajo

- Reutilizar una maqueta aprobada como base y reemplazar solo el marco (shell) con un script de transformación por cortes verificados evita regresiones en el lienzo; conviene comprobar el balance de `<div>` tras cada corte (un corte mal anclado dejó un `</div>` de más que se detectó por conteo).

## Reglas de negocio acordadas en esta tarea

Ninguna.

## Carpetas/archivos huérfanos

Ninguno detectado.

## Número de llamadas

~28 (incluye lecturas de la app y de las maquetas, la construcción, las comprobaciones y el commit).
