# 16 — Paneles, navegación y alcance del servicio

## Objetivo

Definir cómo se organizan los accesos del sistema mediante tres paneles, diferenciando navegación, información y acciones operativas. El flujo debe mostrar únicamente las funciones permitidas al usuario y mantener todas las acciones asociadas al servicio seleccionado.

Este flujo es de interfaz y navegación. No reemplaza la jerarquía funcional del proyecto ni crea una nueva estructura de negocio.

## Principio central

```
Paneles = navegación y acceso
Modelo de negocio = servicio, presupuesto, partidas, paquetes y ejecución
```

El panel izquierdo no debe crear una jerarquía adicional como “servicio → panel → área → disciplina”. Solo presenta accesos del contexto actual.

## Tres paneles

## Panel izquierdo — contexto del servicio

Su contenido depende de si existe un servicio seleccionado.

## Sin servicio seleccionado

Muestra recursos generales de la empresa que no pertenecen a un proyecto específico:

* Cargos de personal.
* Maquinaria.
* Herramientas.
* Otros catálogos corporativos autorizados.

No debe mostrar acciones que requieran `servicio_id`.

## Con servicio seleccionado

Muestra los accesos propios del servicio actual. Todas las acciones deben recibir automáticamente el identificador del servicio seleccionado.

El usuario no debe poder cambiar de servicio durante una acción iniciada desde este panel.

## Panel central — Mi entorno

Ruta:

```
/mi-entorno
```

Muestra las herramientas disponibles para el usuario según sus roles y permisos, aunque no pertenezcan únicamente a un solo rol.

El grupo se determina mediante la prioridad definida por `slugEntornoDesdeRoles`, sin reemplazar la evaluación individual de permisos.

## Panel derecho — herramientas y accesos rápidos

Agrupa los accesos del servicio y las acciones rápidas por grupo o rol:

* Proyecto.
* Planificación.
* Supervisión operativa.
* SSOMA.
* Logística.
* Administración.
* Costos.
* Otros grupos configurados.

Se implementa mediante los patrones existentes de `NAV_PROYECTO`, `GruposAccordion`, `PanelSecciones` y `WorkspaceShell`.

## Clasificación de chips

Todos los chips deben clasificarse como uno de estos dos tipos.

## Chips informativos

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

## Chips de acción

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

Con servicio seleccionado, se recomienda organizarlo así:

```
Servicio seleccionado
├── Alcance y presupuesto
│   ├── Alcance
│   ├── Presupuesto
│   └── Paquetes de trabajo
├── Planificación
│   └── Cronograma
├── Recursos
│   ├── Cargos (HH)
│   └── Equipos (HM)
├── Documentación
│   ├── Planos
│   └── PETS
├── Reportes
│   ├── Consolidado RDTs
│   └── RQ
└── Acciones
    ├── Generar RQ
    ├── Crear RDT
    └── Crear paquete de trabajo
```

La ubicación de un chip puede ajustarse a la arquitectura visual, pero no debe duplicarse sin una razón clara.

## Paquetes de trabajo en el panel

“Paquetes de trabajo” debe ser un chip informativo de consulta y gestión del contexto del servicio. Al abrirlo, el usuario verá los paquetes del servicio seleccionado.

Dentro de esa pantalla se mostrarán las acciones permitidas:

* Crear paquete.
* Editar paquete.
* Asignar partidas.
* Registrar o consultar avance.
* Cerrar o archivar.

No es necesario crear un chip separado para cada operación si la pantalla ya contiene acciones internas. Sin embargo, “Crear paquete” puede aparecer como acceso rápido para roles autorizados.

## Contexto del servicio

Todas las rutas y acciones específicas de servicio deben cumplir:

```
servicio seleccionado → autorización → operación → retorno al mismo servicio
```

El contexto debe conservarse mediante:

* Parámetro de ruta.
* Identificador seguro en sesión o contexto de servidor.
* Validación de pertenencia del recurso al servicio.

Nunca se debe confiar únicamente en un `servicio_id` enviado desde el navegador.

## Reglas de navegación

1. Sin servicio no se muestran acciones específicas del servicio.
2. Con servicio se muestran solo accesos autorizados para ese servicio y usuario.
3. Un chip oculto por permisos no debe ser accesible solo escribiendo la URL.
4. Toda ruta debe validar autenticación, rol y pertenencia al servicio.
5. Las acciones iniciadas desde el panel mantienen el servicio actual.
6. Al volver a “Mi entorno”, se conserva el grupo y el contexto permitido.
7. Las pantallas a pantalla completa deben ofrecer “Salir a Mi entorno” cuando corresponda.
8. Las notificaciones deben dirigir a `/notificaciones`, no duplicarse en otros paneles.
9. Los estados y colores deben reutilizar las fuentes únicas existentes.
10. Cada chip nuevo debe registrarse también en el flujo 14 de accesos y restricciones.

## Tabla de accesos

El flujo 14 debe derivarse de los mismos identificadores usados por los paneles y permisos. No se deben mantener listas independientes que puedan quedar desactualizadas.

Cada acceso debería tener metadatos comunes:

* `id` o slug.
* Nombre.
* Grupo.
* Tipo: informativo o acción.
* Ruta o acción.
* Requiere servicio: sí/no.
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

## Existente o parcial

* `WorkspaceShell`.
* `/mi-entorno`.
* `EntornoTrabajoGrupo`.
* `herramientasPorGrupo`.
* `NAV_PROYECTO`.
* `GruposAccordion`.
* Panel derecho parcial.
* Panel central existente.

## Pendiente

* Panel izquierdo completo.
* Separación visual definitiva entre informativos y acciones.
* Catálogos corporativos sin servicio.
* Accesos propios del servicio seleccionado.
* Inclusión de Paquetes de trabajo.
* Matriz visual de permisos del flujo 14.
* Registro centralizado de chips para evitar deuda de actualización.

## Criterios de aceptación

* El panel izquierdo cambia correctamente según exista o no un servicio seleccionado.
* Los recursos corporativos no se mezclan con recursos del servicio.
* Los chips informativos y de acción aparecen separados.
* Las acciones quedan fijadas al servicio actual.
* Paquetes de trabajo aparece dentro del alcance del servicio.
* Se respetan permisos en la interfaz y en el servidor.
* Las rutas directas no permiten evadir permisos.
* El panel central muestra herramientas según permisos reales.
* El panel derecho conserva los grupos existentes.
* Cada nuevo chip puede incorporarse a la matriz de accesos.
* Se conserva la navegación móvil y las tablas con scrol

**No implementado como visión completa** (partes ya existen por separado, pero no bajo este diseño de conjunto). Pedido por Victor el 2026-09-16: 3 paneles que organizan los chips de acceso a la interfaz.

1. **Panel derecho** — divide las acciones en apartados por grupo/rol (Proyecto, Planificación, Supervisión operativa, SSOMA, etc.), cada uno con sus chips. Acceso rápido a la interfaz. Ya existe parcialmente: `NAV_PROYECTO` (`nav-proyecto.ts`) + `GruposAccordion` (`PanelSecciones.tsx`), renderizado en `WorkspaceShell.tsx`.
2. **Panel central** — el "entorno del usuario" (`/mi-entorno`): muestra los apartados/chips a los que el usuario tiene acceso, no solo los de su propio rol. Ya existe: `EntornoTrabajoGrupo.tsx` + `herramientasPorGrupo` (`grupo-proceso.ts`). También abarca otras funciones además de chips (ej. crear usuario, según permiso).
3. **Panel izquierdo — NO EXISTE TODAVÍA.**
   - Sin servicio seleccionado: recursos de la empresa (catálogo, no por proyecto) — por ahora 3 campos: cargos de personal, maquinaria, herramientas.
   - Con un servicio seleccionado: cambia a mostrar los chips PROPIOS de ese servicio (no un desplegable de OT — ya se entiende que es "su alcance"): Alcance, Presupuesto, Cronograma, Cargos (HH), Equipos (HM), Planos, PETS, Consolidado RDTs, RQ.
   - Dos tipos de chip, separados visualmente: **informativos** (solo ver + descargar, sin modificar) y **acciones** (van debajo, disparan una acción sobre ESE servicio sin opción de cambiar de servicio — ej. Generar RQ, Crear RDTs ya fijados al servicio actual).

Flujo relacionado: 14 (Accesos y restricciones) — la tabla de roles×accesos se deriva de estos mismos paneles.
