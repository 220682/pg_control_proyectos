# 16 — Paneles

**No implementado como visión completa** (partes ya existen por separado, pero no bajo este diseño de conjunto). Pedido por Victor el 2026-09-16: 3 paneles que organizan los chips de acceso a la interfaz.

1. **Panel derecho** — divide las acciones en apartados por grupo/rol (Proyecto, Planificación, Supervisión operativa, SSOMA, etc.), cada uno con sus chips. Acceso rápido a la interfaz. Ya existe parcialmente: `NAV_PROYECTO` (`nav-proyecto.ts`) + `GruposAccordion` (`PanelSecciones.tsx`), renderizado en `WorkspaceShell.tsx`.
2. **Panel central** — el "entorno del usuario" (`/mi-entorno`): muestra los apartados/chips a los que el usuario tiene acceso, no solo los de su propio rol. Ya existe: `EntornoTrabajoGrupo.tsx` + `herramientasPorGrupo` (`grupo-proceso.ts`). También abarca otras funciones además de chips (ej. crear usuario, según permiso).
3. **Panel izquierdo — NO EXISTE TODAVÍA.**
   - Sin servicio seleccionado: recursos de la empresa (catálogo, no por proyecto) — por ahora 3 campos: cargos de personal, maquinaria, herramientas.
   - Con un servicio seleccionado: cambia a mostrar los chips PROPIOS de ese servicio (no un desplegable de OT — ya se entiende que es "su alcance"): Alcance, Presupuesto, Cronograma, Cargos (HH), Equipos (HM), Planos, PETS, Consolidado RDTs, RQ.
   - Dos tipos de chip, separados visualmente: **informativos** (solo ver + descargar, sin modificar) y **acciones** (van debajo, disparan una acción sobre ESE servicio sin opción de cambiar de servicio — ej. Generar RQ, Crear RDTs ya fijados al servicio actual).

Flujo relacionado: 14 (Accesos y restricciones) — la tabla de roles×accesos se deriva de estos mismos paneles.
