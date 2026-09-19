19 — Paquetes de trabajo y jerarquía de control
Objetivo
Permitir que el usuario agrupe partidas del presupuesto en paquetes de trabajo controlables, sin modificar la base contractual. La partida continúa siendo la unidad de trazabilidad y reportabilidad; el paquete es una capa operativa de agrupación.

Jerarquía recomendada
La jerarquía funcional visible es:

text
Servicio
└── Área o ubicación
    └── Disciplina
        └── Frente de trabajo
            └── Paquete de trabajo
                └── Partidas
                    └── Actividades del cronograma
                        └── Registros RDT
Desde el punto de vista de datos, área, disciplina y frente deben manejarse preferentemente como atributos clasificadores del paquete, no como niveles rígidos obligatorios. Esto evita forzar relaciones cuando una partida se ejecuta en varias ubicaciones o frentes.

La estructura contractual se conserva así:

text
Servicio
└── Presupuesto / DP / WBS
    └── Partidas
Y los paquetes se relacionan con esas partidas:

text
Servicio
├── Presupuesto / DP / WBS
│   └── Partidas
└── Paquetes de trabajo
    └── Partidas asignadas
Frente y paquete
El frente de trabajo es una agrupación operativa amplia, por ejemplo “Cimentaciones” o “Montaje mecánico”. El paquete es una unidad concreta que puede planificarse, ejecutarse y medirse, por ejemplo “Cimentación de tanque T-101”.

text
Frente: Obras civiles del área norte
├── Paquete: Excavación de cimentaciones
├── Paquete: Acero y encofrado
└── Paquete: Concreto estructural
Datos del paquete
Servicio.

Código único.

Nombre.

Área o ubicación, escrita por el usuario o seleccionada entre valores existentes.

Disciplina desde catálogo fijo.

Frente de trabajo, existente o nuevo.

Unidad de control.

Meta.

Responsable.

Estado.

Partidas asignadas.

Fechas planificadas opcionales.

Presupuesto calculado.

Avance calculado.

Unidades diferentes
El paquete puede tener una unidad conceptual distinta a las unidades de sus partidas.

text
Paquete: Cimentación de tanque T-101
Unidad del paquete: cimentación terminada
Meta: 1 unidad

Partidas:
- Excavación: 120 m³
- Concreto pobre: 15 m³
- Acero: 8 500 kg
- Encofrado: 280 m²
- Concreto estructural: 75 m³
- Pernos: 24 unidades
No se suman físicamente m³, kg, m² y unidades. Cada partida conserva su unidad original y recibe un peso dentro del paquete.

Avance ponderado
text
Avance del paquete = Σ(peso de la partida × avance validado de la partida)
Ejemplo de pesos y avance:

Partida	Peso	Avance	Aporte
Excavación	10 %	100 %	10 %
Concreto pobre	5 %	100 %	5 %
Acero	25 %	60 %	15 %
Encofrado	20 %	50 %	10 %
Concreto estructural	30 %	20 %	6 %
Pernos	10 %	0 %	0 %
Total	100 %		46 %
El paquete se reporta al 46 %, pero el usuario puede abrir el detalle por partida.

Reportabilidad
La cadena de trazabilidad será:

text
Servicio → Paquete → Partida → Actividad → RDT validado → PR → Dashboard
La partida sigue siendo la unidad base para presupuesto, valorización, avance validado, costo y auditoría. El paquete no se convierte en una nueva partida.

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
Presupuesto / DP
→ Selector de control
→ Paquetes opcionales
→ Partidas
→ Cronograma
→ Plan Maestro
→ Plan semanal / 3WLA
→ RDT validado
→ PR
→ Dashboard
El cronograma debe continuar vinculándose contra DP/WBS y no contra PR. Si una partida tiene varias actividades, la relación debe conservarse a nivel de partida.

Implementación recomendada para la app real
La lógica de paquetes debe implementarse sobre la estructura existente del servicio y del presupuesto, no creando una segunda fuente de verdad. La base debe seguir usando la partida del presupuesto como unidad contractual y técnica. El paquete es una capa agregadora y operativa.

Base de datos y esquema
- Mantener la partida de presupuesto como unidad base de trazabilidad, costo y avance.
- Crear o reutilizar tablas / modelos del servicio para:
  - áreas por servicio,
  - frentes por servicio,
  - catálogos de disciplina,
  - paquetes por servicio,
  - relación paquete-partida con peso y asignación,
  - configuración de modo de control por servicio o presupuesto.
- No duplicar la estructura contractual del DP. Los campos de partida y su metrado deben quedar vinculados a `dp_partidas` o la entidad equivalente ya existente.
- Si el esquema lo permite, reservar `control_account_id` como campo opcional para una futura extensión EVM, pero nunca hacerlo obligatorio en esta fase.

Modo de control
El servicio o el presupuesto debe permitir elegir:
- `DIRECTO_PARTIDAS`
- `POR_PAQUETES`
- `MIXTO`

En control directo, no se obliga a crear paquetes. En control por paquetes, cada paquete debe tener al menos una partida y un peso total válido. En control mixto, algunas partidas tienen control directo y otras se agrupan.

Rutas / endpoints sugeridos
- GET /servicios/:id/paquetes
- POST /servicios/:id/paquetes
- GET /servicios/:id/paquetes/:paqueteId
- PATCH /servicios/:id/paquetes/:paqueteId
- POST /servicios/:id/paquetes/:paqueteId/partidas
- PATCH /servicios/:id/paquetes/:paqueteId/partidas/:partidaId
- POST /servicios/:id/paquetes/:paqueteId/validar
- POST /servicios/:id/paquetes/:paqueteId/archivar
- GET /servicios/:id/paquetes/:paqueteId/avance

En la app real, estas rutas deben reutilizar los permisos del servicio actual y la validación del usuario autenticado.

Componentes / pantallas sugeridas
- Listado de paquetes con búsqueda, filtros por servicio, área, disciplina, frente, estado y responsable.
- Crear paquete.
- Detalle de paquete.
- Edición básica.
- Gestión de partidas asignadas.
- Cálculo de presupuesto y avance ponderado.
- Acciones internas: asignar partidas, calcular pesos, validar paquete, archivar.

Formulario recomendado
- Nombre obligatorio.
- Descripción opcional.
- Área: editable o seleccionable según configuración.
- Disciplina: seleccionada desde catálogo fijo o opcional si el paquete es flexible.
- Frente: crear o elegir según el servicio.
- Unidad de control obligatoria para el paquete.
- Meta obligatoria cuando la unidad es cuantificable.
- Responsable opcional.
- Estado de paquete.
- Fechas opcionales.
- Selección múltiple de partidas del presupuesto del servicio.

Reglas de negocio
Cada paquete pertenece a un servicio.

Las partidas deben pertenecer al presupuesto del servicio actual.

Área, disciplina y frente de trabajo son clasificadores configurables del paquete. Cada uno será obligatorio únicamente cuando el paquete requiera control o reportabilidad por ese eje. El sistema podrá definir paquetes estándar, con los tres clasificadores obligatorios, y paquetes flexibles, donde dichos campos sean opcionales.

Para paquetes del tipo estándar, el sistema podrá exigir área, disciplina y frente como campos obligatorios. Para paquetes flexibles o especiales, estos campos podrán ser opcionales según la configuración del servicio.

Regla funcional definitiva
Campo | Regla recomendada
Área | Obligatoria si el paquete se controla o reporta por ubicación.
Disciplina | Obligatoria si el paquete pertenece a una especialidad definida.
Frente | Obligatorio si el paquete forma parte de un frente operativo.
Nombre | Siempre obligatorio.
Unidad de control | Obligatoria para medir el paquete.
Meta | Obligatoria cuando el paquete use una unidad cuantificable.
Partidas | Al menos una para activar el paquete.
Pesos | 100 % para activar el paquete medible.

Tipos de paquete
Paquete estándar
Usado en la mayoría de los trabajos de obra.

Área: obligatoria.
Disciplina: obligatoria.
Frente: obligatorio.

Ejemplo:
Área: Planta de procesos.
Disciplina: Civil.
Frente: Cimentaciones.
Paquete: Cimentación de tanque T-101.

Paquete flexible
Usado cuando el control no necesita los tres clasificadores.

Área: opcional.
Disciplina: opcional.
Frente: opcional.

Ejemplo:
Paquete: Pruebas generales del servicio.
Unidad: sistema liberado.
Meta: 1 sistema.

En este caso, puede no existir una única ubicación, disciplina o frente aplicable.

La disciplina proviene de un catálogo controlado cuando exista disciplina definida.

El paquete debe tener nombre, unidad y meta.

Debe tener al menos una partida.

La suma de pesos debe ser 100 % para activar el paquete.

No se duplican partidas activas, salvo distribución parcial autorizada.

El presupuesto se calcula desde las partidas asignadas.

Solo RDT validados alimentan el avance oficial.

Un paquete con avance no se elimina físicamente.

Todos los cambios importantes se auditan.

Validaciones funcionales
- Servicio actual obligatorio.
- Área, disciplina y frente obligatorios solo si corresponden al tipo de paquete.
- Nombre, unidad y meta obligatorios.
- Al menos una partida.
- Pesos entre 0 y 100.
- Suma de pesos igual a 100 % para paquetes medibles.
- Partidas pertenecen al servicio actual.
- No duplicar partidas activas, salvo distribución parcial soportada.
- No exceder la cantidad o monto disponible.
- No eliminar físicamente paquetes con avance.
- Aplicar permisos y auditoría existentes.

Cálculo de avance
avance_paquete = Σ(peso_partida × avance_validado_partida)

No se suman unidades incompatibles. Una partida puede estar en m³, kg, m² o unidades, mientras el paquete puede tener una unidad conceptual distinta.

Pruebas recomendadas
- creación válida,
- datos faltantes,
- pesos incorrectos,
- partidas de otro servicio,
- duplicidades,
- cálculo presupuestal,
- avance ponderado,
- unidades diferentes,
- modos de control,
- permisos,
- auditoría,
- protección contra eliminación destructiva.

Criterios de aceptación
Se puede elegir control directo, por paquetes o mixto.

Se puede crear un área dentro del servicio.

Se selecciona disciplina desde catálogo.

Se crea o selecciona un frente.

Se crea paquete con unidad y meta.

Se asignan partidas múltiples.

Se validan pesos y duplicidades.

Se calcula el presupuesto.

Se calcula el avance ponderado.

Se mantienen las unidades originales.

Se consulta por área, disciplina y frente.

Se llega desde el paquete hasta la partida.

Queda preparada la integración con cronograma, Plan Maestro, 3WLA, RDT, PR y Dashboard.
