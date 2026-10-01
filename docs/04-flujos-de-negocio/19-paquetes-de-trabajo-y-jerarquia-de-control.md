19 — Paquetes de trabajo y jerarquía de control
Objetivo
Permitir que el usuario agrupe partes de la estructura del servicio en paquetes de trabajo controlables, sin modificar la base contractual. La partida continúa siendo la unidad de trazabilidad y reportabilidad; el paquete es una capa operativa de agrupación.

Estructura y jerarquía
La jerarquía de la estructura viene del **mapa de niveles** confirmado al importar el DP y el cronograma (flujos 09 y 15): de 2 a 5 niveles, con Servicio arriba y Partida en el último. Los paquetes se arman sobre esa estructura y se relacionan con las partidas del DP:

text
Servicio
├── Presupuesto / DP / WBS
│   └── Partidas
└── Paquetes de trabajo
    └── Vínculos (actividad del cronograma × partida, con metrado)
Cadena funcional:

text
Servicio
└── Paquete de trabajo (opcional)
    └── Partida
        └── Actividad del cronograma
            └── Registros RDT
Área, frente, unidad, meta y responsable **ya no son datos del paquete**: se retiraron en el plan niveles-paquetes-plan-maestro-rdt (decisión por defecto de Victor, Gate 1, 2026-09-30). Si hacen falta como columnas en el Plan Maestro, se ofrecen con «Personalizar campos» (flujo 20). La **disciplina** sí se conserva (ver abajo), como catálogo fijo.

El paquete es una unidad concreta que puede planificarse, ejecutarse y medirse, por ejemplo “Cimentación de tanque T-101”. No es un frente ni un nivel rígido de la estructura contractual.

Datos del paquete
- Servicio.
- Nombre (obligatorio).
- **Nivel** (profundidad de la estructura en la que se arma; p. ej. en un presupuesto de 3 niveles, 3).
- **Modo de medición** (ver más abajo).
- **Partida guía** (solo en el modo «por avance del paquete»; debe ser una de las partidas del paquete).
- **Orden** (se sube o baja con ▲▼ o Alt+↑/↓).
- **Disciplina** (obligatoria al crear; catálogo fijo, ver abajo).
- Estado (`BORRADOR`, `VALIDADO`, `ARCHIVADO`).
- Presupuesto y avance calculados, no escritos.

**El paquete no tiene fechas.** No se programa en paquetes: lo programado vive en el lienzo del Plan Maestro (flujo 20) y se edita por línea (actividad × partida). Las fechas del cronograma no se tocan.

Disciplina
- Catálogo **fijo de 5**: Civil, Mecánica, Eléctrica, Instrumentación y Tuberías (tabla `disciplinas`, solo lectura para la app; lectura para cualquier usuario autenticado).
- **Obligatoria al crear el paquete** (la API la exige y la pantalla marca el campo). En un borrador se puede cambiar; en `VALIDADO` o `ARCHIVADO` queda fija.
- **Una partida dentro de un paquete hereda la disciplina del paquete.** La partida directa (sin paquete) define la propia en el Plan Maestro (flujo 20). Los paquetes anteriores a este plan quedan **sin disciplina** y deben elegirla al editarse.

Vínculos y declaración del metrado
El paquete **agrupa vínculos actividad × partida**. El vínculo y su metrado se **declaran en la pantalla de Paquetes** (paso «Declarar»), no en el Cronograma (flujo 15):
- Cada vínculo lleva un **metrado exacto mayor que cero**; una actividad puede tener varias partidas. El enlace por EDT exacto se propone pre-llenado (etiqueta «auto»); si es el único enlace de una partida sin vínculos, el metrado propuesto es el contractual.
- **Hitos:** una tarea marcada como hito (`requiere_partidas = false`) no requiere partida ni metrado y no participa en la regla del 100 %.
- Se muestra el **restante** por actividad y por partida (texto, icono y barra): «Resta / Excede / completa».
- Un vínculo pertenece a **un solo paquete** vigente; no se puede quitar un vínculo que está en un paquete no archivado.
- La regla del 100 % por partida **se exige para crear el Plan Maestro** (flujo 20); en Paquetes solo se avisa, no bloquea guardar la declaración ni el paquete.

Partida repartida entre paquetes
**Una partida repartida entre varios paquetes es la regla general** (ya no una excepción «autorizada»): cada paquete toma una porción de su metrado, la pantalla muestra «250.00 de 420.00 (60 %) · repartida en 2 paquetes» y **la suma de las porciones debe llegar al 100 % del metrado contractual**. Las partidas que no van en ningún paquete son **partidas directas** (sin paquete), permitidas. La clave de reporte de cada línea es `paquete|DIRECTA : partida`, y el PR suma por partida (flujo 10).

Crear paquete
- Botón «Crear paquete» dentro de la pantalla de Paquetes (no es un chip nuevo); el acceso rápido «Crear paquete» abre la pantalla con `?accion=crear`, ya en modo crear (flujo 16).
- En el paso «Agrupar» se marcan con casillas los ítems de la estructura (todos menos el Servicio); marcar un nivel resumen marca sus hijas libres. Se escribe nombre, se confirma el nivel y se elige la disciplina.
- El paquete se marca visualmente con borde, fondo tenue y etiqueta «Paquete», en dos colores alternos.
- Editar y archivar solo en `BORRADOR`; subir o bajar el orden vale en cualquier estado salvo `ARCHIVADO`.
- La pantalla tiene dos lados: cronograma (jerarquía plegable, columna «Met.») y DP (solo partidas, solo consulta); bajo `lg`, pestañas «Cronograma | DP».
- Quién gestiona: administrador, jefe de proyectos y planner; los 13 roles ven (tablas 1 y 2 del [flujo 14](14-accesos-y-restricciones.md)).

Unidades diferentes
Las partidas de un paquete conservan sus unidades originales (m³, kg, m², unidades): no se suman físicamente. El paquete no tiene unidad ni meta propias.

Avance
**Los pesos por partida y el avance ponderado del diseño original quedan superados.** El avance se declara según el modo de medición:
- **Por partida** (`POR_PARTIDAS`): cada partida con su unidad y metrado.
- **Por la guía** (`AVANCE_PAQUETE`): se declara el avance de la partida guía y el mismo % se aplica a todas las partidas del paquete.

Para mostrar un avance del paquete en el selector del RDT: por avance = % de la guía; por partidas = promedio simple de sus partidas. Lo oficial es el **real por paquete × partida**, que se ve en el Plan Maestro (flujos 18 y 20); el real por partida (suma de todos sus paquetes) alimenta al PR. Solo RDT validados alimentan el avance oficial.

Reportabilidad
La cadena de trazabilidad será:

text
Servicio → Paquete → Partida → Actividad → RDT validado → PR → Dashboard
La partida sigue siendo la unidad base para presupuesto, valorización, avance validado, costo y auditoría. El paquete no se convierte en una nueva partida.

## Modo de medición (Fase 1 — implementado 2026-09-23)

El paquete tiene un modo de medición, definido en la columna `paquetes_trabajo.modo_medicion` (migración `072`):

| Modo | Descripción |
|---|---|
| `AVANCE_PAQUETE` | Se declara el avance del paquete como porcentaje de su **partida guía** y ese mismo % se aplica a **todas** las partidas del paquete. La partida guía (`dp_partida_guia_id`) jala su **unidad y metrado** del DP; con eso se calcula `% = metrado_ejecutado / metrado_guía`. Ejemplo: guía cama de arena 10 ml, declaras 5 ml → 50 % → excavación 7.5 m³, cama de arena 5 ml, relleno 7.5 m³. En el RDT (flujo 06) el servidor guarda una fila derivada de solo lectura por cada partida. El metrado de la guía dentro del paquete es la suma de su metrado declarado. |
| `POR_PARTIDAS` | El paquete no tiene unidad propia; el avance se declara **partida por partida**, cada una con su unidad y metrado originales. |

**El modo de medición solo es editable mientras el paquete esté en `BORRADOR`.** Una vez en `VALIDADO` o `ARCHIVADO`, queda fijo. La pantalla de Paquetes crea hoy en `POR_PARTIDAS`; el modo `AVANCE_PAQUETE` lo admite la API y el RDT, sin selector en la pantalla de Paquetes.

La partida guía **no** se elige por peso ni por jerarquía: la selecciona el usuario, y debe ser una de las partidas del paquete.

## Capa operativa (regla fundacional)

El paquete de trabajo **agrupa y secciona** vínculos del DP bajo un nombre propio. Es una **capa operativa** de agrupación; **no reemplaza la partida contractual**. La partida sigue siendo la unidad de trazabilidad, costo, valorización y auditoría.

Selector del presupuesto
Agregar el selector:

text
¿Cómo se controlará este presupuesto?
Opciones:

Control directo por partidas.

Control mediante paquetes de trabajo.

Control mixto.

En control directo no se obliga la creación de paquetes. En control por paquetes, las partidas deben organizarse antes de activar el control. En control mixto, unas partidas pueden controlarse directamente y otras mediante paquetes.

Se recomienda implementar el modo mixto para conservar flexibilidad.

Cuenta de control futura
No será obligatoria en la primera versión. Puede reservarse como relación opcional:

text
Servicio
└── Cuenta de control
    └── Paquetes de trabajo
        └── Partidas
Tiene sentido para consolidar varios paquetes bajo un responsable y controlar PV, EV y AC en un punto intermedio de EVM.

Integración con el sistema
text
Presupuesto / DP (con mapa de niveles)
→ Cronograma (con mapa de niveles)
→ Paquetes opcionales (declaran vínculos con metrado)
→ Plan Maestro (lienzo)
→ Plan semanal / 3WLA
→ RDT validado
→ PR
→ Dashboard
El cronograma debe continuar vinculándose contra DP/WBS y no contra PR. Si una partida tiene varias actividades, la relación debe conservarse a nivel de partida.

Implementación en la app real
La lógica de paquetes se implementa sobre la estructura existente del servicio y del presupuesto, no creando una segunda fuente de verdad. La partida del presupuesto sigue siendo la unidad contractual y técnica. El paquete es una capa agregadora y operativa.

Base de datos y esquema
- `paquetes_trabajo` (nombre, nivel, modo de medición, partida guía, orden, `disciplina_id`, estado) y `paquete_trabajo_vinculos` (paquete × actividad × partida con metrado), migraciones `079` a `081` y `085`; catálogo `disciplinas` (`085`).
- `paquete_trabajo_partidas` y `paquete_trabajo_programacion` **quedan sin uso y se conservan** (nada se borra sin autorización de Victor).
- No duplicar la estructura contractual del DP: los vínculos apuntan a `dp_partidas` y a `cronograma_actividades`.
- Si el esquema lo permite, reservar `control_account_id` como campo opcional para una futura extensión EVM, nunca obligatorio.

API (verificada contra la rama integrada)
- `GET /api/paquetes-trabajo?proyectoId=`: `paquetes` (con `vinculos`, `disciplinaId` y `disciplinaNombre`), `actividades` (estructura), `partidasDp` y `restantePorPartida`; los 13 roles leen.
- `POST` crea (exige nombre, nivel y disciplina; no acepta fechas ni programación); `PATCH` con `EDITAR`, `MOVER` y `ARCHIVAR`.
- `PUT /api/paquetes-trabajo/vinculos`: el conjunto recibido es el estado final de los vínculos del servicio; valida partida y actividad del servicio, metrado > 0, hito sin metrado; llama `recalcular_pr_fechas_base`.
- `GET /api/disciplinas`: catálogo (solo lectura).
- Validación siempre en servidor, con los permisos de gestión y el alcance por servicio.

Las rutas `/servicios/:id/paquetes/...` del diseño original eran sugeridas y no se usaron.

Reglas de negocio
Cada paquete pertenece a un servicio.

Las partidas deben pertenecer al presupuesto del servicio actual.

El paquete debe tener nombre, nivel y disciplina; y al menos un vínculo con metrado.

Una partida puede repartirse entre varios paquetes; la suma de sus porciones debe llegar al 100 % del metrado contractual para crear el Plan Maestro. No se excede el metrado disponible.

El presupuesto del paquete se calcula desde sus partidas.

Solo RDT validados alimentan el avance oficial.

Un paquete con avance no se elimina físicamente.

Todos los cambios importantes se auditan.

Validaciones funcionales
- Servicio actual obligatorio.
- Nombre, nivel y disciplina obligatorios; disciplina del catálogo y activa.
- Metrado del vínculo > 0 (hito sin metrado).
- Un vínculo en un solo paquete vigente.
- Partidas y actividades pertenecen al servicio actual.
- No eliminar físicamente paquetes con avance.
- Aplicar permisos y auditoría existentes.

Pruebas recomendadas
- creación válida y datos faltantes (nombre, disciplina),
- restante por actividad y partida, hitos fuera de la regla,
- partida repartida entre dos paquetes (Σ = contractual),
- vínculo ya tomado por otro paquete,
- modos de medición,
- permisos de los 13 roles,
- auditoría,
- protección contra eliminación destructiva.

Criterios de aceptación
Se declaran vínculos actividad × partida con metrado exacto, con hitos aparte.

Se crea un paquete con nombre, nivel y disciplina, agrupando ítems de la estructura.

Se reparte una partida entre varios paquetes y se ve su restante.

Se mantienen las unidades originales.

Se llega desde el paquete hasta la partida.

Queda preparada la integración con el Plan Maestro, el RDT, el PR y el Dashboard.
