================================================================================
PERMISOS DE VISIBILIDAD DE DATOS - BORRADOR VIVO
================================================================================

Estado: borrador inicial (2026-08-16), a afinar sub-proyecto a sub-proyecto de
py_control_proyectos_web. NO implementado todavia en la web -- hoy el unico
control de acceso real es src/lib/permisos/permisos.ts (quien puede subir
cada documento del checklist, quien confirma transiciones de estado, quien
gestiona usuarios). Este documento es el punto de partida para una capa mas
fina, que se construira mas adelante.

--------------------------------------------------------------------------------
0. LA DISTINCION (dicha por Victor, 2026-08-16)
--------------------------------------------------------------------------------

Dos ejes de permiso, independientes entre si:

  1. VISIBILIDAD DE DATOS ECONOMICOS -- quien puede ver montos/precios
     (presupuesto, costos, precios unitarios) y quien no, sin importar su
     rol de sistema. Ejemplo confirmado: el Administrador gestiona usuarios
     y el sistema, pero eso NO implica que pueda ver el presupuesto -- son
     permisos distintos (administracion del sistema != visibilidad de datos
     confidenciales).

  2. ALCANCE DE CAMPOS/ARCHIVOS -- dentro de lo que un rol SI puede ver,
     cuales campos o documentos especificos le corresponden (no todo-o-nada
     por formato). Ejemplo confirmado: Logistica ve la lista de materiales
     (la necesita para su trabajo, ver control_de_proyectos.txt 2.3 -- recibe
     "Listado de materiales CON costo"), pero no el presupuesto del proyecto
     completo.

  3. Ademas, dentro de cada rol: algunos pueden INGRESAR datos, otros son
     SOLO LECTURA, y en general cada uno deberia ver "solo lo que le
     compete" (no el proyecto completo sin filtrar).

--------------------------------------------------------------------------------
1. TABLA POR ROL (a llenar/afinar -- la mayoria sigue PENDIENTE)
--------------------------------------------------------------------------------

  Rol                          | Ve datos economicos | Que ve (alcance)         | Ingresa datos / solo lectura
  ------------------------------|----------------------|--------------------------|------------------------------
  Administrador                 | NO (confirmado)      | Todo lo NO economico;    | Gestion de sistema/usuarios,
                                 |                       | gestion de usuarios/     | no necesariamente datos de
                                 |                       | sistema                  | proyecto
  Jefe de Proyectos              | PENDIENTE            | PENDIENTE                | PENDIENTE
  Jefe de Oficina Tecnica        | PENDIENTE            | PENDIENTE                | PENDIENTE
  Supervisor Oficina Tecnica     | PENDIENTE            | PENDIENTE (dueno de DP:  | PENDIENTE
                                 |                       | ¿ve costos por ser quien |
                                 |                       | importa Partidas/WP?)    |
  Planner                        | PENDIENTE            | PENDIENTE                | PENDIENTE
  Supervisor de Costos           | PENDIENTE (se asume  | PENDIENTE                | PENDIENTE
                                 | SI, a confirmar)      |                          |
  Supervisor Operativo           | PENDIENTE            | PENDIENTE                | PENDIENTE
  Supervisor de Logistica        | PARCIAL (confirmado) | Listado de materiales    | PENDIENTE
                                 |                       | CON costo; NO el         |
                                 |                       | presupuesto del proyecto |
  Supervisor de Administracion   | PENDIENTE            | PENDIENTE                | PENDIENTE
  RRHH                           | PENDIENTE            | PENDIENTE                | PENDIENTE

--------------------------------------------------------------------------------
2. PREGUNTAS ABIERTAS (no inventar la respuesta -- confirmar con Victor cuando
   se retome este tema)
--------------------------------------------------------------------------------

  1. Logistica ve "Listado de materiales CON costo" segun control_de_proyectos.txt
     2.3 -- ¿eso cuenta como "dato economico" (tiene precio unitario por
     material) o el corte es mas fino (ve precio de materiales, pero no
     costo total/presupuesto del proyecto)? Falta precisar donde esta la
     linea.
  2. Supervisor de Oficina Tecnica es quien importa DP (Partidas de control +
     Work Package, ver spec de sub-proyecto 2) -- el precio unitario de cada
     partida en DP YA es un dato economico. ¿Puede verlo porque lo importa,
     o el importador deberia ocultarle el precio unitario a el tambien?
  3. Falta el resto de la tabla: Jefe de Proyectos, Jefe de Oficina Tecnica,
     Planner, Supervisor Operativo, Supervisor de Administracion, RRHH,
     Supervisor de Costos (se asume que SI ve datos economicos por ser su
     funcion, pero no esta confirmado explicitamente).

--------------------------------------------------------------------------------
3. COMO SE USARA ESTO
--------------------------------------------------------------------------------

Cuando se retome (probablemente al construir el modulo de reportes/dashboard
o al endurecer permisos de sub-proyecto 2), esta tabla es el insumo para
disenar la capa de permisos a nivel de campo, no solo a nivel de accion
(la que ya existe en permisos.ts). Se referencia desde
py_control_proyectos_web/docs/superpowers/specs/ cuando se disene esa capa,
sin duplicar contenido -- este archivo sigue siendo la fuente.

================================================================================
FIN DEL BORRADOR -- se afina sub-proyecto a sub-proyecto
================================================================================
