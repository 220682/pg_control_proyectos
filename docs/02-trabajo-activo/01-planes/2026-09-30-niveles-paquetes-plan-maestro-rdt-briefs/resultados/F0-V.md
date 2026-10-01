# Resultados F0-V

Skills revisados: `pg_control_proyectos/.claude/skills/` = cerrar-tanda (usado), verificar-permisos-por-rol y seguir-flujo-de-planes (no aplican: no se tocan permisos ni se cierra un plan). La app no tiene carpeta de Skills (no se tocó la app).

## Estados
| ID | Estado | Evidencia |
|---|---|---|
| F0V-1 | Conforme (verificado por cascade; sin navegador) | Causa: `tr.real td{color:#c3d0e8}` (especificidad 0,1,2) pisaba a `.pct-ej`/`.pct-100` (0,1,0), así que la clase se ponía pero el color no. Corrección en `plan-maestro-tres-paneles.html` línea 169: `tr.real td.pct-ej{color:var(--warn);font-weight:700}` y `tr.real td.pct-100{color:var(--ok);font-weight:700}` (0,2,2, gana). La clase la agrega `recalc()` (línea ~433) a la celda `data-k="<ent>\|r\|<semana>\|fa"` cuando el valor redondeado es >0 y <100 (ámbar) o >=100 (verde, con ✓). Dato: el real solo existe hasta `hoy=2` (S1 y S2); en la vista inicial, S2 «Físico acum.»: Excavación 90 % y Acero 40 % ámbar, Cama de arena y Relleno 100 % verde, Eliminación 0 % blanco. Contraste: #fbbf24 y #34d399 sobre #0a0e18/#0b1222 superan 9:1. El texto de la nota decía «a la semana S4»; corregido a S2 (S3 y S4 quedan en blanco, aún sin RDT). Crear RDT no tenía el problema (`.uni` va antes de `.pct-ej`, mismo peso). **Pendiente solo la mirada de Victor en navegador.** |
| F0V-2 | Conforme | Bloque de barras azuladas (pista #0b1222, pulgar #3d5a8a, hover #5b7fc0, 10 px, `scrollbar-width:thin`; `scrollbar-color` solo bajo `@supports not selector(::-webkit-scrollbar)`) en `marco-tres-paneles.css` (lo usan Cronograma, Importar DP, Paquetes declarar y agrupar), `plan-maestro-tres-paneles.html` y `crear-rdt-selector-paquetes.html`; selector `*`, cubre los contenedores internos. Regla en `design.md` §8 y §15; versión 1.9.1. No se pudo determinar el color anterior: se usó el tono azulado. |
| F0V-3 | Conforme | `importar-dp-niveles.html`: columnas «Und.» (texto, izquierda) y «Met.» (derecha), ancho justo (`w-min`), en las dos tablas: 2 encabezados, 18 filas con valor, 14 filas con guion; nota de alineación actualizada. |
| F0V-4 | Conforme | `plan-maestro-lienzo.html` reescrito como página mínima (685 bytes) con aviso «Reemplazada por la maqueta con los tres paneles», `meta refresh` y enlace. El sistema no lo denegó. |
| F0V-5 | Conforme | `mockups/README.md` e `index.html`: Importar DP, Cronograma, Paquetes (2), Plan Maestro y Crear RDT «aprobada por Victor (2026-09-30)». Se dejó «pendiente de revisión» solo en `paneles-ocultables.html` (no está en las cuatro del brief). |

## Handoff
- Falta: que Victor abra `plan-maestro-tres-paneles.html` y confirme el color y las barras. Luego quedan libres F3-C y F3-D.
- Archivos tocados: `docs/05-diseno-y-referencias/design.md` y `mockups/` (README, index, marco-tres-paneles.css, importar-dp-niveles, plan-maestro-lienzo, plan-maestro-tres-paneles, crear-rdt-selector-paquetes).
- Commit: solo esos archivos; nunca `Trazabilidad.xlsx` (sigue modificado, no es mío). Este archivo lo commitea el Orquestador.

## Mejoras de trabajo
- Una clase de color utilitaria (`.pct-ej`) pierde contra reglas de fila (`tr.real td`): al colorear dentro de tablas con color de fila, calificar el selector (`tr.real td.pct-ej`). Probar el cascade, no solo que la clase se aplique.

## Reglas de negocio nuevas
Ninguna. Huérfanos: ninguno nuevo. Preguntas devueltas: ninguna.

Llamadas: ~22.
