# Resultados F0-S

## Skills revisados
pg_control_proyectos: cerrar-tanda (usado), seguir-flujo-de-planes y verificar-permisos-por-rol (no aplican: no hay permisos ni cierre de plan). py_control_proyectos_web: sin carpeta de Skills.

## Estados
| ID | Estado | Evidencia |
|---|---|---|
| F0S-1 | Observado (pendiente de revisión visual de Victor) | Leído `WorkspaceShell.tsx` (título «Control de Proyectos» y «Accesos rápidos» en la franja superior de cada panel; anchos w-60/w-64). `paneles-ocultables.html` y `plan-maestro-lienzo.html`: encabezado de panel de 34-38 px; icono absoluto en la esquina superior interior (derecha en el izquierdo, izquierda en el derecho); oculto, sigue en la misma esquina. Sin navegador: revisado por lectura. |
| F0S-2 | Conforme | `design.md` §4.1.2 nueva: 0 % normal, en curso amarillo (`amber-400`), 100 % verde (`emerald-400`) de §4.1.1; solo porcentajes de avance reales; número siempre escrito + leyenda. Sin colores nuevos. |
| F0S-3 | Observado (pendiente de revisión visual) | Lienzo: «Físico acum. (%)» de filas «Real» con color, leyenda y ejemplo 4 (Excavación 90 % amarillo, Eliminación 0 % blanco, Cama de arena y Relleno 100 % verde). Crear RDT: avance de cada partida y paquete con color, marca ✓ al 100 %, leyenda; datos del selector ajustados (Cama de arena y Relleno al 100 %, paquete Banco ducto 62 %). Paquetes (Declarar/Agrupar): no muestran avance, sin cambio. Scripts validados con `node --check`. |
| F0S-4 | Conforme | `design.md` 1.8.0 (§3, §4.1.2, §15), incluye la línea de pantallas existentes fuera de este plan; `mockups/index.html` y `README.md` al día. |
| F0S-5 | Conforme | Este archivo. |

## Handoff
- Falta: que Victor abra `plan-maestro-lienzo.html` (ejemplo 4), `crear-rdt-selector-paquetes.html` (abrir el selector) y `paneles-ocultables.html`.
- Decisión técnica: el color se aplica solo al «Físico acum.» real del lienzo (no al semanal, que es un incremento); comparación con el valor redondeado mostrado.
- Decisión técnica: las tandas de interfaz usan `text-amber-400` / `text-emerald-400` (no hay token propio, §4.1.1).
- Hallazgo: los datos del selector cambiaron (ACUM: cama 50, relleno 80, afirmado 40) para mostrar el 100 %.
- Las maquetas de paneles en Crear RDT no muestran paneles laterales (no se tocó).

## Preguntas para Victor
1. En el lienzo, ¿el color va solo en el «Físico acum.» real (recomendado, muestra el estado de la partida) o también en el «Físico semanal» real? Ejemplo: una semana en que Excavación no avanzó mostraría 0 % en blanco aunque la partida vaya al 90 %.
2. Un avance real entre 99,5 % y 99,99 % que se muestra redondeado como «100,00 %», ¿se pinta amarillo (recomendado: verde solo si de verdad llegó a 100) o verde? Ejemplo: 99,996 % se ve «100,00 %».
3. ¿El total del servicio y los niveles (fila «Total del servicio» Real) también llevan el color? Recomendado: sí, con la misma regla (hoy lo llevan).

## Mejoras de trabajo / reglas de negocio / huérfanos
Reglas de negocio: la regla de color de avance vive en `design.md` §4.1.2 (no es regla de negocio de un flujo). Ninguna mejora de trabajo ni huérfano.

## Llamadas
Aprox. 25.
