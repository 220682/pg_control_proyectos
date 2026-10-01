# 16 — Paneles, navegación y alcance del servicio

## Objetivo

Definir cómo se organizan los accesos del sistema mediante tres paneles, diferenciando navegación, información y acciones operativas. Todos los roles ven todos los accesos; los que el rol no puede usar se muestran deshabilitados, con un título que lo explica. Todas las acciones se mantienen asociadas al servicio seleccionado.

Este flujo es de interfaz y navegación. No reemplaza la jerarquía funcional del proyecto ni crea una nueva estructura de negocio. Quién puede hacer qué lo decide el flujo 14 (`14-accesos-y-restricciones.md`) y el artefacto «Matriz de permisos»; este flujo solo dice cómo se muestra.

## Principio central

```
Paneles = navegación y acceso
Modelo de negocio = servicio, presupuesto, partidas, paquetes y ejecución
```

El panel izquierdo no debe crear una jerarquía adicional como “servicio → panel → área → disciplina”. Solo presenta accesos del contexto actual.

## Tres paneles

### Panel izquierdo — contexto del servicio

Está siempre activo en el workspace y lo ven todos los roles. Tiene dos bloques.

**Recursos de empresa** (catálogos que no pertenecen a un proyecto): Personal, Cargos, Equipos y Causas CNC. «Materiales» no es un recurso de empresa. El bloque lleva un botón mostrar/ocultar: **sin servicio seleccionado está visible; con servicio seleccionado está oculto**, y el usuario lo despliega cuando quiere. Los recursos de empresa nunca se reemplazan por los del servicio ni se mezclan con ellos. Lo que el rol no puede usar se muestra deshabilitado (regla 2). No hay acciones que requieran `servicio_id` sin servicio.

**Accesos del servicio** (solo con servicio seleccionado): los del servicio actual, organizados como se describe en «Organización del panel izquierdo». Todas las acciones reciben automáticamente el identificador del servicio seleccionado (ver «Contexto del servicio» y la regla E1).

### Ocultar y mostrar los paneles laterales

En escritorio (pantalla `lg` o mayor), cada panel lateral lleva **un icono propio de ocultar/mostrar en la esquina superior interior de su encabezado** (el del panel izquierdo, a su derecha; el del derecho, a su izquierda). Al ocultar un panel queda una tira estrecha (24 px) con el mismo icono para volver a mostrarlo, y el panel central toma el ancho liberado. El contenido oculto sigue montado: no pierde su estado. El icono es un botón con nombre accesible y estado expandido/contraído.

- **Recuerdo por usuario:** el estado de cada panel se guarda por usuario en el navegador y se restaura al volver; si no puede guardarse o leerse, los dos paneles quedan visibles.
- **Móvil:** el cajón de navegación no cambia y el control no aparece.
- Es un control de interfaz, **no un acceso**: no entra en el registro de accesos ni en la matriz del flujo 14, y es independiente del botón mostrar/ocultar de Recursos de empresa.
- El asistente flotante no debe tapar las columnas de las pantallas anchas (por ejemplo, el lienzo del Plan Maestro, [flujo 20](20-plan-maestro.md)); hoy el contenido reserva espacio inferior para él.

### Panel central — Mi entorno

Ruta:

```
/mi-entorno
```

Muestra las herramientas disponibles para el usuario según sus roles y permisos, aunque no pertenezcan únicamente a un solo rol. Ver flujo 03.

El grupo se determina mediante la prioridad definida por `slugEntornoDesdeRoles`, sin reemplazar la evaluación individual de permisos.

### Panel derecho — herramientas y accesos rápidos

Agrupa los accesos del servicio y las acciones rápidas por grupo o rol:

* Proyecto.
* Planificación.
* Supervisión operativa.
* SSOMA.
* Logística.
* Administración.
* Costos.
* Otros grupos configurados.

Un chip cuya pantalla existe abre esa pantalla con el servicio ya elegido (`?proyectoId=`). Un chip cuya pantalla no existe queda inerte, sin enlace, y el título dice «Sin pantalla todavía».

Se implementa mediante los patrones existentes de `NAV_PROYECTO`, `GruposAccordion`, `PanelSecciones` y `WorkspaceShell`.

## Asistente: elemento del shell fuera de los tres paneles

El asistente no es un cuarto panel ni un chip. Es un elemento propio del shell (`WorkspaceShell`) que convive con los tres paneles sin alterar su estructura.

* **Icono en toda pantalla del workspace**, con y sin servicio, en escritorio y móvil: un icono flotante (48 px) abajo a la derecha, dentro del panel central (`main`). Un clic despliega el panel del asistente y otro clic (o Escape, o el botón de cerrar) lo repliega.
* **Panel desplegable no modal**: no bloquea el resto de la pantalla y queda por debajo de los cajones y los modales.
* **Una sola instancia** en toda pantalla del workspace. Quedan fuera las pantallas sin shell: login y activar (no hay sesión) y el dashboard del portafolio (`app/programas/…`), que se reporta como excepción a Victor.
* **No es un chip**: no figura en el registro de accesos ni en la matriz del flujo 14, y no depende de ningún permiso. Está disponible para todos los roles (no confundir con el rol de usuario «asistente»).
* **Vista previa sin datos**: hoy solo muestra un aviso y un campo de texto sin efecto; no llama a ninguna API. Ver flujo 17 (no habilitado): el asistente del shell no es el agente allí descrito.
* **Estado al navegar**: el shell vive en el layout del workspace, así que al navegar entre pantallas del workspace el asistente conserva su estado (abierto o replegado) y no se duplica.

Posición, capas y patrón visual: `design.md` §3.

## Clasificación de chips

Todos los chips deben clasificarse como uno de estos dos tipos.

### Chips informativos

Permiten consultar, visualizar o descargar información. No crean ni modifican datos.

Ejemplos:

* Alcance.
* Presupuesto.
* Cronograma.
* Cargos.
* Equipos.
* Planos.
* PETS.
* Paquetes de trabajo.
* Consolidado RDTs.
* RQ.

### Chips de acción

Ejecutan una operación sobre el servicio actual.

Ejemplos:

* Generar RQ.
* Crear RDT.
* Subir RDT.
* Crear paquete de trabajo.
* Importar presupuesto.
* Importar cronograma.
* Registrar avance.

La separación debe ser visual y funcional. Un chip informativo no debe activar mutaciones y un chip de acción debe indicar claramente que ejecutará una operación.

## Organización del panel izquierdo

Con servicio seleccionado, el panel izquierdo tiene siete grupos:

```
Servicio seleccionado
├── Alcance y presupuesto
│   ├── OT
│   ├── Alcance
│   ├── Presupuesto
│   ├── DP (Datos del proyecto)
│   └── Paquetes de trabajo
├── Planificación
│   ├── Cronograma
│   └── Plan Maestro
├── Recursos del servicio
│   ├── Cargos (HH)
│   ├── Equipos (HM)
│   ├── Materiales (c/c)
│   └── Personal nuevo
├── Documentación
│   ├── Planos
│   └── PETS
├── Reportes
│   ├── Consolidado RDTs
│   ├── Requerimiento (RQ)
│   ├── PR
│   ├── Dashboard
│   ├── Curva S
│   ├── Registro de costos
│   └── Consolidado del servicio
├── Acciones
│   ├── Generar RQ
│   ├── Crear RDT
│   ├── Subir RDT
│   └── Crear paquete de trabajo
└── Servicio
    ├── Ficha del servicio
    ├── Editar servicio
    └── Editar checklist
```

La ubicación de un chip puede ajustarse a la arquitectura visual, pero no debe duplicarse sin una razón clara. La estructura vigente está en `src/lib/config/panel-izquierdo.ts`, derivada del registro de accesos.

## Paquetes de trabajo en el panel

“Paquetes de trabajo” debe ser un chip informativo de consulta y gestión del contexto del servicio. Al abrirlo, el usuario verá los paquetes del servicio seleccionado.

Dentro de esa pantalla se mostrarán las acciones permitidas:

* Crear paquete.
* Editar paquete.
* Asignar partidas.
* Registrar o consultar avance.
* Cerrar o archivar.

No es necesario crear un chip separado para cada operación si la pantalla ya contiene acciones internas. Sin embargo, “Crear paquete” aparece como acceso rápido (acción del panel): **abre `/paquetes-trabajo` con el servicio elegido y el formulario de paquete nuevo abierto (modo crear, `?accion=crear`)**, no guarda nada al abrirse, y lo pueden usar administrador, jefe de proyectos y planner (flujo 14, «Gestionar paquetes de trabajo»); al resto se le muestra deshabilitado. No es un chip nuevo ni un permiso nuevo. «Asignar partidas» incluye declarar los vínculos con metrado y los hitos; el avance real ya no se registra en el paquete sino en el RDT (flujos 06 y 18), y el paquete solo lo consulta.

## Contexto del servicio

Todas las rutas y acciones específicas de servicio deben cumplir:

```
servicio seleccionado → autorización → operación → retorno al mismo servicio
```

El contexto debe conservarse mediante:

* Parámetro de URL `?proyectoId=` (o ruta `/proyectos/[id]`).
* Identificador seguro en sesión o contexto de servidor.
* Validación de pertenencia del recurso al servicio.

Nunca se debe confiar únicamente en un `servicio_id` enviado desde el navegador.

**Acciones desde el panel (E1).** Las acciones (Generar RQ, Crear RDT, Subir RDT, Crear paquete) abren con el servicio seleccionado ya elegido en su selector de OT y no guardan nada al abrirse. El selector sigue siendo editable, pero **si se cambia el servicio dentro de la acción, la URL y los paneles lo siguen**: nunca hay dos servicios distintos a la vez.

## Reglas de navegación

1. Sin servicio no se muestran acciones específicas del servicio.
2. Con servicio se muestran **todos** los accesos a todos los roles; los que el rol no puede usar se muestran **deshabilitados** (`aria-disabled`, atenuados, cursor no permitido y sin enlace), con un título que explica por qué. Ver no es acceder.
3. Un chip deshabilitado no es accesible escribiendo la URL: el servidor valida igual que antes y rechaza la ruta directa. La barrera del servidor no cambia con lo que la interfaz muestre.
4. Toda ruta debe validar autenticación, rol y pertenencia al servicio.
5. Las acciones iniciadas desde el panel mantienen el servicio actual.
6. Al volver a “Mi entorno”, se conserva el grupo y el contexto permitido.
7. Las pantallas a pantalla completa ofrecen el chip «Salir a Mi entorno» y, con servicio seleccionado, este lleva a `/mi-entorno?proyectoId=…` (conserva el servicio); sin servicio lleva a `/mi-entorno`. El pie del panel izquierdo también tiene un acceso a Mi entorno siempre visible.
8. Las notificaciones deben dirigir a `/notificaciones`, no duplicarse en otros paneles.
9. Los estados y colores deben reutilizar las fuentes únicas existentes.
10. Todo acceso nuevo se declara una sola vez en el registro único de accesos (ver «Tabla de accesos») y, además, en el artefacto «Matriz de permisos» (https://claude.ai/artifact/4no1PCEfDb5pYmgmnrP5MT), base del flujo 14 (política de coherencia y trazabilidad, `docs/01-contexto-repositorio/02-arquitectura-y-fuentes-de-verdad.md`). Toda pantalla nueva sigue la «Política de interfaz nueva».

### Entrar a una pantalla sin ver su contenido

Poder entrar a una pantalla no equivale a ver todo su contenido: un rol puede usar una acción de una pantalla sin ver sus datos (por ejemplo, logística sube el registro de costos sin verlo). Hay además dos excepciones acotadas de la tabla 1 del flujo 14: el planner ve y gestiona Plan Maestro, y el supervisor de oficina técnica ve el DP (no lo importa). El detalle por rol vive solo en el flujo 14; aquí solo se fija que la interfaz debe mostrar el acceso deshabilitado o habilitado según esa tabla, sin inferir permisos de escritura a partir de poder ver.

## Política de interfaz nueva

Aprobada por Victor el 2026-09-30. **Toda pantalla nueva del workspace nace con esta política, sin que Victor tenga que pedirla chip por chip:**

1. **Vive dentro del shell** (`WorkspaceShell`, los tres paneles); no crea layout paralelo.
2. **Se declara una sola vez** en el registro único de accesos, con id, nombre, grupo, tipo (informativo o acción), ruta o acción, si requiere servicio (sí, opcional o no), permiso requerido y en qué paneles es visible. De ese registro salen automáticamente el panel izquierdo, el derecho, Mi entorno, el envío de `?proyectoId=`, el estado habilitado o deshabilitado y la matriz derivada del flujo 14. Si la pantalla no debe tener chip, se declara como excepción con motivo. Una prueba automática falla si hay una pantalla del workspace sin entrada ni excepción.
3. **Conserva el servicio.** Recibe `?proyectoId=` (o vive bajo `/proyectos/[id]`), no lo pierde al navegar ni al redirigir (usa el helper de servicio) y lo preselecciona en su selector de OT o en su filtro N° OT. Cambiar el servicio dentro de la pantalla actualiza la URL.
4. **Tiene tipo.** Un chip informativo consulta, visualiza o descarga y no muta datos; un chip de acción ejecuta una operación sobre el servicio actual y lo indica.
5. **Permisos.** Define su función de permiso en `permisos.ts`, con ver, crear, editar, eliminar o archivar, subir, registrar avance y descargar evaluados por separado. La interfaz muestra deshabilitado, con título explicativo, lo que el rol no puede usar; el servidor valida autenticación, rol y pertenencia del recurso al servicio, nunca solo el `servicio_id` del navegador. Ver no implica poder.
6. **Sale en la matriz del flujo 14**, derivada del registro; la tabla no se edita a mano.
7. **Diseño.** Respeta `design.md`: componentes existentes, tablas con scroll horizontal y encabezado fijo, sin `max-w-*` en el contenedor de página, navegación móvil, `scope` en los `<th>`.
8. **Estados y colores** de las fuentes únicas existentes (por ejemplo `claseBadgeEstado`); estados de carga, vacío y error contemplados.
9. **Las notificaciones** van a `/notificaciones`, no se duplican en otros paneles.
10. **Su Punch List incluye estos puntos por defecto**, con la prueba de cada permiso por los dos lados (cuenta con permisos altos y cuenta sin permisos de administración) y la prueba de humo del registro. La plantilla de ítems está en `docs/01-contexto-repositorio/05-diseno-y-ui.md`.

## Tabla de accesos

La fuente de los paneles es el **registro único de accesos** (`src/lib/config/registro-accesos.ts`). El flujo 14 y el artefacto «Matriz de permisos» son la base de quién puede qué: el registro se ajusta a ellos, y la matriz que se deriva del registro solo se compara con el flujo 14 para detectar diferencias; no se edita a mano ni lo reemplaza.

Cada acceso tiene metadatos comunes:

* `id` o slug.
* Nombre.
* Grupo.
* Tipo: informativo o acción.
* Ruta o acción.
* Requiere servicio: `sí`, `opcional` o `no`. «Opcional» aplica a las pantallas que abren sin servicio y lo preseleccionan si se abren con él (Plan Maestro, Status de Requerimiento, Consolidado RQ, Status de RDTs).
* Permiso requerido.
* Visible en panel izquierdo.
* Visible en panel central.
* Visible en panel derecho.

Esto permite generar la matriz de roles y accesos de manera consistente.

## Permisos mínimos

Para cada chip debe existir una evaluación independiente de:

* Puede ver.
* Puede crear.
* Puede editar.
* Puede eliminar o archivar.
* Puede subir archivos.
* Puede registrar avance.
* Puede descargar.

No se debe inferir automáticamente que quien puede ver también puede modificar.

## Estado de implementación

Implementado:

* `WorkspaceShell` con los tres paneles y el asistente como icono flotante.
* `/mi-entorno` (`EntornoTrabajoGrupo`, `herramientasPorGrupo`).
* Paneles laterales ocultables con un icono por panel y recuerdo por usuario (plan niveles-paquetes-plan-maestro-rdt, F3-C; lógica y compilación verificadas, observación visual por rol pendiente de F5).
* Panel izquierdo completo: Recursos de empresa con botón mostrar/ocultar y siete grupos con servicio (27 chips: 17 con pantalla y 10 inertes sin enlace).
* Panel derecho con chips que abren la pantalla con el servicio elegido.
* Registro único de accesos (`registro-accesos.ts`, `panel-izquierdo.ts`, `panel-derecho.ts`) y prueba de cobertura de pantallas.
* Chips deshabilitados con título por permiso.

Pendiente: los 10 chips sin pantalla (sin enlace hasta que exista la pantalla).

## Criterios de aceptación

* El panel izquierdo muestra Recursos de empresa (con mostrar/ocultar) con y sin servicio, y los accesos del servicio cuando hay uno seleccionado.
* Los recursos de empresa no se mezclan con recursos del servicio.
* Los chips informativos y de acción aparecen separados.
* Las acciones quedan fijadas al servicio actual y, si se cambia, la URL y los paneles lo siguen.
* Paquetes de trabajo aparece dentro del alcance del servicio.
* «Crear paquete» abre Paquetes en modo crear, con el servicio elegido.
* Cada panel lateral se oculta y se muestra con su icono en la esquina interior, y el estado se recuerda por usuario.
* Todos los roles ven todos los chips; los no autorizados aparecen deshabilitados con título.
* El servidor rechaza las rutas directas sin permiso, igual que antes.
* El panel central muestra herramientas según permisos reales.
* El panel derecho conserva los grupos existentes.
* Cada nuevo acceso se declara en el registro y sale en la matriz derivada.
* El asistente aparece como icono en toda pantalla del workspace, una sola vez.
* Se conserva la navegación móvil y las tablas con scroll.

Historia: pedido de Victor el 2026-09-16 (tres paneles que organizan los chips de acceso); ampliado el 2026-09-27 con el servicio persistente entre pantallas (plan `2026-09-27-paneles-servicio-persistente`) y el 2026-09-30 con ocultar paneles y «Crear paquete» en modo crear (plan `2026-09-30-niveles-paquetes-plan-maestro-rdt`).

Flujo relacionado: 14 (Accesos y restricciones).
