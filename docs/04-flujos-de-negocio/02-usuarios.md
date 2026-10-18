# 02 — Usuarios
> Lee si: la tarea crea, edita o borra usuarios, roles, cargos o área, toca `/admin/usuarios`, o decide qué datos de su perfil edita cada persona. No lo abras solo para asignar alguien a un proyecto: eso vive en el flujo 08.


`/admin/usuarios`: crear (contraseña + invite), roles, cargo, área, borrar. Solo admin o jefe de proyectos.

**Área (perfil):** cada usuario se asigna a un área (`perfiles.area_id` → `areas`). El área código `PR` ("Proyecto") se renombró a **`JF` ("Jefatura")**, como área para asignar a los jefes.

**Pendiente:** “Pasar responsabilidades a” como flujo claro (hoy reasignar está en la ficha al borrar).

**Qué edita cada persona de su propio perfil (Victor, 2026-10-17):** los 13 roles cambian su **celular, su correo y su contraseña** desde Mi entorno ([flujo 03](03-entorno.md), permisos en la tabla 2 y la nota 14 del [flujo 14](14-accesos-y-restricciones.md)). **Nombre, cargo, área y roles siguen siendo de quien gestiona usuarios** (administrador y jefe de proyectos, en esta pantalla). La contraseña con la que el administrador crea al usuario es provisional en la práctica: el correo de invitación no la trae y la persona puede cambiarla sola. **Asignar o quitar servicios** a un usuario desde aquí avisa solo cuando es un supervisor operativo ([flujo 08](08-programa-portafolio-proyecto.md)).

Regla transversal: solo administrador asigna el rol administrador.
