# Resultados F2-C · Paquetes: orden, plegado, edición y estados

Carril 3 · rama `local-worker-3` · commit `d4c5b3b` (sobre `7038e5e`). Sin push ni merge. No se escribió ni aplicó ninguna migración.

## Skills revisados
`pg_control_proyectos/.claude/skills/`: cerrar-tanda (usada; estados, evidencia y traspaso van en este archivo), verificar-permisos-por-rol (no aplica: sin cambio de permisos), seguir-flujo-de-planes (lo usa el Orquestador). Repo de la app: sin carpeta de Skills.

## Qué ya existía de F2-B (no se rehízo)
Flechas ▲▼ y Alt+↑/↓, plegado por paquete, botón «Archivar», estados carga/error/vacío en `FormularioPaquetesTrabajo.tsx` y `PasoAgrupar.tsx`, API `PATCH` con EDITAR/MOVER/ARCHIVAR (F2-A).

## Estado de ítems

| ID | Estado | Evidencia |
|---|---|---|
| F2C-1 | Conforme (render: Observado, pendiente de F5) | Teclado movido a lógica pura `movimientoPorTeclado` (`src/lib/paquetes-trabajo/edicion.ts`). Pruebas: renumeración sin huecos y orden estable al recargar (`edicion.test.ts`); API: `MOVER` escribe `orden` 0..n de todos los vigentes y no actúa sobre un archivado (`paquetes-api.test.ts`, bloque F2C-1). |
| F2C-2 | Conforme (render: Observado) | Nuevo «Plegar todo / Expandir todo» (alterna según lo plegado; `plegarTodos`, `expandirTodos`, `accionPlegadoGlobal`). Plegado = solo el nombre. Pruebas de plegado individual y global. Se reinicia al abrir (regla ya aprobada). |
| F2C-3 | Conforme (render: Observado) | «Editar» en paquete BORRADOR: reutiliza el formulario y las casillas del modo crear (nombre, nivel, modo, partida guía si «Por avance del paquete», vínculos marcando/desmarcando actividades; las propias cuentan como libres, las de otro paquete no). «Archivar» solo en BORRADOR. «Detalle» muestra la trazabilidad paquete → actividad (EDT) → partida (WBS, metrado, unidad) y por partida cuánto toma el paquete, % y reparto. VALIDADO/ARCHIVADO: sin botones y etiqueta «Validado: no se edita»; el servidor rechaza (400). Pruebas: `cuerpoEditarPaquete` (sin fechas ni programación, no roba vínculos de otro paquete, nombre vacío, guía obligatoria), `detalleDePaquete`, API VALIDADO/ARCHIVADO. |
| F2C-4 | Conforme por estructura; navegador: Observado, pendiente de F5 | Carga (`role=status`, `aria-busy`), error (`role=alert` + Reintentar) y vacío (con «Ir a Declarar») ya presentes; tablas con `th scope="col"`, `caption sr-only`, botones con `aria-label`, `aria-expanded`, formulario con `aria-label`, scroll horizontal. Lista para F5 abajo. |
| F2C-5 | Conforme | Prueba cruzada: partida de 10 repartida 5+5 entre dos paquetes → Σ=10, completo; 5+4 → Σ=9, `completo=false`, faltante 1; los dos paquetes se crean sobre la misma partida. `npx tsc --noEmit`: 0 errores. `npx vitest run`: 74 archivos, 733 pruebas verdes. `npm run lint`: 27 problemas (9 errores), idéntico a F2-A/F2-B; eslint sobre mis rutas: 0. `npx next build --webpack`: compila. |

## Handoff
- Falta solo F5: comprobación en navegador. Retomar: `cd <worktree>`; `npm run dev -- --webpack -p 3113`; `/paquetes-trabajo?proyectoId=<id>`.
- **Disciplina: NO implementada** (por instrucción; Victor decide dónde vive el catálogo). Sigue pendiente la decisión.
- Cambios de código: `src/lib/paquetes-trabajo/edicion.ts` (nuevo) y su prueba; `agrupar.ts` (`actividadesLibres` con tercer parámetro opcional `paqueteActualId`; `PaqueteVista` con `modoMedicion?` y `guiaDpPartidaId?`, que el GET ya devuelve); `PasoAgrupar.tsx`; prueba de API ampliada. Sin cambio de contrato.
- Decisión técnica: al editar, la selección es por actividad (igual que al crear); en modo edición las casillas de los demás paquetes quedan deshabilitadas y se oculta la casilla de paquete completo.
- Estados de BD usados por la UI: BORRADOR (editable), el resto solo lectura; el GET excluye ARCHIVADO.

## Comprobaciones de navegador para F5
1. ▲▼ y Alt+↑/↓ mueven el paquete; recargar conserva el orden y los colores alternos.
2. «Plegar todo» deja solo los nombres; el botón pasa a «Expandir todo»; ▾/▸ individual funciona; al reabrir todo está expandido.
3. «Editar» en BORRADOR: precarga nombre, nivel, modo y marcas; cambiar vínculos, guardar, recargar (persisten); error del servidor visible con `role=alert`.
4. Modo «Por avance del paquete»: la guía solo ofrece partidas del paquete; sin guía, error claro.
5. «Archivar» desaparece el paquete y libera sus actividades para otro paquete.
6. «Detalle»: cadena paquete → actividad → partida y reparto (5+5 completo; 5+4 «reparto incompleto» y aviso general).
7. Paquete VALIDADO (si existe): sin Editar/Archivar y con etiqueta; cuenta sin gestión: sin Editar, Archivar, ▲▼ ni Crear.
8. Estados carga, error (Reintentar) y vacío; 390 px con scroll horizontal; foco visible y navegación por Tab.

## Mejoras de trabajo
- Heredocs de bash largos con comillas, apóstrofos o `$` fallan con «unexpected EOF» sin ejecutar nada: escribir ficheros con la herramienta Write y los ajustes de código con un script de Python guardado en archivo (los `assert` en cada reemplazo detectan anclas que no coinciden).

## Reglas de negocio detectadas
Ninguna nueva. Aplicadas: solo BORRADOR se edita o archiva; mover vale en cualquier estado no archivado; el 100 % por partida solo avisa, se exige para abrir el Plan Maestro.

## Huérfanos
Los de F2-B siguen igual (`repartirAvanceDelPaquete`, `validarPartidasDelPaquete`, tablas `paquete_trabajo_partidas`/`paquete_trabajo_programacion`). Nada borrado.

## Llamadas
Aproximadamente 30.
