# F5-B · Servicio de prueba dedicado y verificación en vivo (niveles, paquetes, Plan Maestro)

Lee primero `00-reglas-de-contexto.md`. **Carril de integración** · rama `local-worker-1` (con los cuatro carriles integrados), puerto 3111. **Solo este carril usa el navegador** en este momento.
Fase F5 · **Depende de:** F5-A cerrada **y de que las migraciones 073 a 084 estén aplicadas y verificadas por sus carriles** (constan en sus `resultados/`; el Orquestador te lo confirma en el prompt de lanzamiento; sin eso, no empieces).
**Punto de commit:** solo el `resultados/F5-B.md`, que lo commitea el Orquestador; si hay ajustes de código menores, en `local-worker-1`.

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| F5B-1 | Se crea el **servicio de prueba dedicado** (nombre marcado `PRUEBA-…`, con el portafolio que indique el Orquestador) — autorizado por Victor — y se le importa un **DP de 5 niveles** (real si existe; si no, el sintético de F1-A, rotulado) | Captura de la ficha y URL |
| F5B-2 | Importación con **confirmación de niveles**: cuenta los niveles, propone roles (nivel 2 = Área), fila de muestra que se propaga, filas «para revisar»; luego se importa el **cronograma** con su propio mapa | Capturas + snapshot de texto |
| F5B-3 | **Paquetes**: declarar actividad → partida → metrado (pre-llenado por EDT), marcar un hito, crear dos paquetes con **una partida repartida entre ambos** (suma 100 %), marca visual, seleccionar completo, mover y plegar; «Crear paquete» desde el panel abre en modo crear | Capturas + comprobación del restante en 0 |
| F5B-4 | **Plan Maestro**: lienzo con columnas fijas y días, semanas plegables, seis columnas; repartir todos los metrados; el botón de crear solo se habilita al 100 %; aprobar; los totales coinciden con el cálculo de la lógica; el PV aparece en la **Curva S** | Capturas + números comparados |
| F5B-5 | **Recarga**: con Plan Maestro aprobado, cargar de nuevo el DP o el cronograma queda bloqueado; con solo un borrador, se permite tras el aviso y la confirmación | Capturas + resultado de la API |

## Contrato técnico verificado (2026-09-30)

- Navegador: herramientas `mcp__playwright__*` (si no están, `claude-in-chrome`; si tampoco, lo demás queda `Observado`). Escritorio 1440 px. Encadena las navegaciones una a una. Lee con `textContent()`. Una captura por ítem como máximo, guardada en `docs/02-trabajo-activo/03-evidencia/capturas/niveles-paquetes-plan-maestro-rdt/<ID>.jpg` (ancho ≤ 1440).
- Cuentas de prueba: solo en la memoria del agente (`cuentas-prueba.md`; léelo con `Read`, sin `grep`/`sed`/`cat`). **No tomes snapshot de la pantalla de login con el formulario relleno.** Agrupa todo lo de la cuenta A.
- Escrituras: **solo** en el servicio de prueba dedicado y con registros marcados `PRUEBA-…`. Ningún servicio real se toca.
- Archivos de prueba: `docs/06-material-de-apoyo/Informacion para pruebas/` (Excel de presupuesto y cronograma); no los copies a la app.
- El Plan Maestro aprobado de prueba reemplaza nada real: el servicio es nuevo.

## Qué NO hacer

- No escribas en ningún servicio que no sea el de prueba. No apliques migraciones. No cambies permisos. Sin push.
- No borres datos: la limpieza es F5-C, con autorización expresa.
- Ante lo que falle: detén el ítem como `Observado` con el síntoma exacto y continúa con los demás.

## Cierre

**Skills:** al empezar, lista `.claude/skills/` de `pg_control_proyectos` (hoy: `cerrar-tanda`, `verificar-permisos-por-rol`, `seguir-flujo-de-planes`) y del repositorio de la app (hoy sin carpeta de Skills) y anota «Skills revisados» en tu `resultados/F5-B.md`. **Usa `cerrar-tanda` al terminar** (adaptación de este plan: sus pasos de estados, evidencia y traspaso van en tu `resultados/F5-B.md`, no en el plan ni en el progreso compartidos).

`resultados/F5-B.md` (estado de F5B-1 a F5B-5, evidencia, hallazgos, handoff, llamadas). Mensaje final: cerrados, pendientes y llamadas.
