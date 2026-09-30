# F0-A · Maquetas de Niveles y de Paquetes de Trabajo

Lee primero `00-reglas-de-contexto.md`. **Carril de diseño**: trabajas en `D:\VICTOR\CLAUDE CODE\pg_control_proyectos` (rama `main`), **sin worktree de la app**. Escribes solo en `docs/05-diseno-y-referencias/**`.
Fase F0 · **Depende de:** nada · **Bloquea:** F1-C y F2-B (no pueden construir interfaz hasta que Victor apruebe estas maquetas). Las tandas de datos y lógica **no** esperan.
**Commit:** en `main` de `pg_control_proyectos`, con `git add` explícito solo de tus archivos.

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| F0A-1 | Maqueta HTML **«Importar DP: confirmación de niveles»**: cuenta de niveles encontrados; lista del presupuesto en orden; una **fila de muestra por grupo de hermanas** con desplegable de rol (Servicio, Área, Subpresupuesto, Paquete de partidas, Partida); roles propuestos por defecto; filas «para revisar»; botón de aprobar; aviso de **recarga bloqueada** (con plan aprobado: bloqueo duro; sin él: lista de lo que se perdería y confirmación). Muestra un presupuesto de 4 niveles y uno de 5 (el nivel 2 propone «Área») | Archivo `mockups/importar-dp-niveles.html` |
| F0A-2 | Maqueta de la confirmación de niveles del **cronograma** con sus roles propios y el mismo patrón | `mockups/cronograma-niveles.html` |
| F0A-3 | Maqueta de **Paquetes, paso «Declarar»**: a un lado el cronograma con jerarquía y **columna Metrado** (desplegable de partida pre-llenado, hitos atenuados con su marca, indicador de restante por partida); al otro el DP **solo partidas, solo consulta**; paneles laterales ocultos. Usa el ejemplo real: 06.03.01 a 06.03.07 (excavación, perfilado, cama de arena, instalación de bancoductos, suministro de afirmado, relleno, eliminación de material excedente) | `mockups/paquetes-declarar.html` |
| F0A-4 | Maqueta de Paquetes, paso **«Agrupar»**: botón «Crear paquete» (no chip); casillas al inicio de cada ítem salvo Servicio; nombre, nivel, guardar; el paquete con **marca visual** (color o borde), selección del paquete completo, **flechas arriba/abajo**, **plegar** (solo nombre); 06.03.01–06.03.06 agrupadas y 06.03.07 directa; una partida repartida entre dos paquetes con sus porciones | `mockups/paquetes-agrupar.html` |
| F0A-5 | Las cuatro maquetas muestran estados vacío, carga y error, versión móvil (390 px) y accesibilidad (`scope` en `th`, foco visible, teclado para mover y plegar) | Capturas o secciones visibles en cada archivo |
| F0A-6 | `design.md`: sección nueva para la **jerarquía en árbol con casillas**, la marca de paquete y el plegado, usando los tokens y componentes existentes (§4, §5, §8); sin inventar nombres de componentes que no existen en el código; versión y §15 actualizados | Diff de `design.md` |
| F0A-7 | `mockups/index.html` y `mockups/README.md` enlazan las cuatro maquetas; `resultados/F0-A.md` lista **preguntas de diseño para Victor** (máx. 6, una decisión por pregunta, sin códigos internos) | Enlaces funcionan |

## Qué mirar antes de dibujar (solo lo necesario)

- `design.md`: §3 (layout), §4 (tokens), §5 (componentes; tablas y selects), §8 (scroll y tablas extensas), §9, §10, §12. Con `offset`/`limit`.
- Un mockup existente como referencia de estilo (`crear-rdts.html`): solo su `<head>` y un bloque de tabla.
- Ejemplos de datos: los del Spec (`…/2026-09-30-niveles-presupuesto-y-cronograma.md` §«Modelo de niveles» y `…/2026-09-30-paquetes-y-plan-maestro-grilla.md` §«Resultado esperado»). Lee solo esas secciones con Grep.
- Flujo 16 §«Política de interfaz nueva» y «Paquetes de trabajo en el panel» (la acción «Crear paquete» del panel ya existe y abre la pantalla en modo crear).

## Qué NO hacer

- No tocar código de la app ni crear ramas. No editar flujos. No crear chips ni pantallas nuevas: Paquetes y la importación ya existen.
- No inventar comportamientos: si algo no está en los Specs, va a la lista de preguntas.
- Datos simulados coherentes con los Specs; nada de datos reales de servicios.
- Sin credenciales. Sin herramientas de navegador para verificar (abre los HTML con lectura y revisa su estructura).

## Cierre

**Skills:** al empezar, lista `.claude/skills/` de `pg_control_proyectos` (hoy: `cerrar-tanda`, `verificar-permisos-por-rol`, `seguir-flujo-de-planes`) y del repositorio de la app (hoy sin carpeta de Skills) y anota «Skills revisados» en tu `resultados/F0-A.md`. **Usa `cerrar-tanda` al terminar** (adaptación de este plan: sus pasos de estados, evidencia y traspaso van en tu `resultados/F0-A.md`, no en el plan ni en el progreso compartidos).

`resultados/F0-A.md` con el estado de F0A-1 a F0A-7, el handoff y las preguntas de diseño. Commit de `docs/05-diseno-y-referencias/**` en `main` (solo tus archivos). Mensaje final: ítems cerrados, pendientes y llamadas usadas. El Orquestador presenta las maquetas a Victor.
