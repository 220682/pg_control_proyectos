# Resultados F2-B · Paquetes: pantalla de dos lados, declarar y crear paquete

Carril 3 · rama `local-worker-3` · commit `7038e5e` (sobre `73a8680`). Sin push ni merge. Migraciones 079-081 ya aplicadas (según el encargo); no se escribió ni aplicó ninguna.

## Skills revisados
`pg_control_proyectos/.claude/skills/`: cerrar-tanda (usada: los pasos de estados, evidencia y traspaso van en este archivo), verificar-permisos-por-rol (no aplica: no cambia permisos; solo prueba de las funciones existentes), seguir-flujo-de-planes (lo usa el Orquestador). Repo de la app: sin carpeta de Skills.

## Estado de ítems

| ID | Estado | Evidencia |
|---|---|---|
| F2B-1 | Conforme (render en vivo: Observado, pendiente de F5) | Dos lados: cronograma con jerarquía plegable y columna «Met.» / DP solo partidas, solo consulta (candado). Lógica en `src/lib/paquetes-trabajo/declaracion.ts` y `agrupar.ts`; pruebas en `pantalla-paquetes.test.ts`. Componentes: `src/components/paquetes/PasoDeclarar.tsx`, `PasoAgrupar.tsx`; contenedor `FormularioPaquetesTrabajo.tsx`. Pestañas «Cronograma | DP» bajo `lg`. |
| F2B-2 | Conforme (render: Observado) | Desplegable de partida en la fila, pre-llenado por EDT exacto (etiqueta «auto»; metrado = contractual solo si ese enlace es el único de una partida sin vínculos); metrado por vínculo (varias partidas por actividad con «+»); hitos atenuados con ◆ Hito y sin metrado; restante por actividad y por partida (texto + icono + barra), «Resta / Excede / completa». Pruebas: enlace por EDT, 250 + 170 = 420, hito fuera, exceso. |
| F2B-3 | Conforme (render: Observado) | Botón «Crear paquete» dentro de la pantalla (sin chip); casillas al inicio de cada ítem salvo el Servicio; nombre, nivel, guardar; resumen marca sus hijas libres (casilla parcial incluida). `?accion=crear` abre en «Agrupar» ya en modo crear. Prueba de selección, nivel (profundidad: Bancoductos = 3), cuerpo del POST (sin fechas ni programación) y rechazo de vínculo ya tomado. |
| F2B-4 | Conforme (render: Observado) | Marca visual: borde grueso + fondo tenue + etiqueta «Paquete», dos colores alternos (cian/azul, tokens existentes). Casilla del paquete (o de cualquiera de sus ítems) selecciona el paquete completo. Partida repartida entre dos paquetes: porción «250.00 de 420.00 (60 %) · repartida en 2 paquetes» y vigilancia de Σ = contractual. Subir/bajar con ▲▼ y Alt+↑/↓ (PATCH `MOVER`). Plegado local que se reinicia. Pruebas con el caso de dos paquetes. |
| F2B-5 | Conforme | Diff: se retiran del formulario fechas inicio y fin, «Repartir en días», la lista fecha → metrado, el modo de avance y `repartirAvanceDelPaquete`; guardar un paquete ya no exige programación. Prueba: el cuerpo del POST no contiene «fecha» ni «programación». |
| F2B-6 | Conforme | `npx tsc --noEmit`: 0 errores. `npx vitest run` (con `VITE_CONFIG_NATIVE_IGNORE_WARNING=true`): 73 archivos, 718 pruebas verdes (incl. los 13 roles ven y solo administrador, jefe de proyectos y planner gestionan). `npm run lint`: 27 problemas (9 errores) en el worktree, idénticos a los de F2-A, ninguno en archivos de F2-B (eslint sobre mis rutas: 0). Sin medir `main` (recorre `.worktrees`, ver F2-A). `npx next build --webpack`: compila. Escritura oculta o deshabilitada si `puedeGestionar` es falso. |

## Handoff
- Falta solo F5: comprobación en navegador (lista abajo). Retomar: `cd <worktree>`; `npm run dev -- --webpack -p 3113`; ruta `/paquetes-trabajo?proyectoId=<id>` (y `&accion=crear`).
- **Cambio de contrato (aditivo) que el Orquestador debe registrar en C2:** `GET /api/paquetes-trabajo` ahora devuelve además `vinculos: { actividadId, dpPartidaId, metrado, paqueteId | null }[]` (todos los vínculos declarados del servicio, con su paquete vigente). Sin él la pantalla no podía precargar «Declarar» ni mostrar las partidas directas. Los demás campos no cambian; hay prueba.
- **Pregunta devuelta (Disciplina):** no existe un catálogo de disciplinas en el código (`grep` en `src` y `db`: sin resultados) ni campo en `paquetes_trabajo` ni en la API. **No incluí el selector de Disciplina** del formulario ni de las partidas directas de la maqueta. Opciones: (a) catálogo + columna nuevos en un carril con migración (recomendado si Victor lo quiere guardado); (b) dejarlo fuera de este plan. Necesito la decisión y dónde vive la lista.
- Decisiones técnicas: modo de medición fijo `POR_PARTIDAS` al crear (la maqueta no ofrece modo ni guía; el modo `AVANCE_PAQUETE` queda soportado por la API pero sin UI); los hitos se envían tal cual están (el PUT los marca; no hay conmutador de hito en la maqueta); la selección es por actividad (una actividad con varias partidas entra completa); el orden con ▲▼ solo existe para paquetes (las directas no tienen `orden` en la API: la maqueta mostraba flechas también en directas, no implementadas).
- «Color del avance real» (design.md 1.9.0): no aplica, esta pantalla declara metrado contractual, no avance real. Alineación de tablas: encabezado alineado con su dato, numéricos y unidades a la derecha, columnas cortas con ancho justo (`w-px`).
- Paneles: el shell ya los oculta con servicio (`WorkspaceShell.tsx`); no se tocó.

## Comprobaciones de navegador para F5
1. «Declarar»: abrir con paneles ocultos; el desplegable de partida sale pre-llenado con «auto» donde el EDT coincide; escribir metrados y ver el restante cambiar en ambos lados; guardar y recargar (persisten).
2. Hitos atenuados con marca, sin campo de metrado; «Guardar declaración» con un hito marcado no falla.
3. Intentar quitar un vínculo que ya está en un paquete: mensaje claro (el PUT lo rechaza).
4. «Agrupar»: «Crear paquete» muestra casillas (no en el Servicio); marcar una resumen marca sus hijas; guardar crea el paquete con marca y color alterno; `?accion=crear` abre ya en modo crear.
5. Partida repartida en dos paquetes: etiqueta de porción y aviso si la suma no llega al 100 %.
6. ▲▼ y Alt+↑/↓ mueven el paquete y recalculan los colores; ▾/▸ pliega y se reinicia al reabrir.
7. Cuenta sin gestión: sin «Crear paquete», sin guardar, sin ▲▼ ni «Archivar», campos deshabilitados; los 13 roles ven la pantalla.
8. Ancho 390 px: pestañas «Cronograma | DP», tablas con scroll horizontal; el icono del asistente no tapa columnas.

## Mejoras de trabajo
- Escribir ficheros largos con la herramienta de escritura y los ajustes pequeños con un script de Python en un `<<'PYEOF'` aparte; un heredoc muy largo con comillas rompió el intérprete (no ejecutó nada y hubo que repetir).
- La herramienta de edición exige haber leído el archivo con `Read` (un `cat` en Bash no cuenta).

## Reglas de negocio detectadas
Ninguna nueva. Aplicada tal cual: la regla del 100 % por partida se exige para abrir el Plan Maestro, no para guardar paquete ni declaración (la pantalla solo avisa).

## Huérfanos
- `repartirAvanceDelPaquete` y `validarPartidasDelPaquete` en `src/lib/paquetes-trabajo/paquetes-trabajo.ts` ya no los usa la pantalla (siguen en sus pruebas); no se borró nada.
- Sigue sin uso `paquete_trabajo_partidas` / `paquete_trabajo_programacion` (por contrato).

## Llamadas
Aproximadamente 45.
