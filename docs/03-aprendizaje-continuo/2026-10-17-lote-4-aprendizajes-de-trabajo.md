# Aprendizajes de trabajo del Lote 4 de observaciones (2026-10-17)

## Origen

Plan [`2026-10-17-observaciones-victor-lote-4.md`](../02-trabajo-activo/01-planes/2026-10-17-observaciones-victor-lote-4.md), apartado «Mejoras (de trabajo)», cerrado el 2026-10-17. Trabajo tradicional (sin Orquestador): HH reales de los cargos en MES, cuadre de HH de PS-108 con el listado de insumos, pantallas Alcance y Presupuesto y ojo de contraseña. Solo método y herramientas; ninguna regla del sistema (esas se integraron en los flujos 09, 12, 14 y 16).

## Observación

### 1. Si Victor dice que las cifras no cuadran, primero comprobar que el archivo se aplicó (reincide «verificar antes de afirmar»)

Victor sumó la mano de obra directa más la indirecta y «no llegaba» a las HH del listado. La causa no estaba en el archivo generado: la pantalla DP de producción seguía con la importación vieja (la línea «Importado el … desde …» mostraba el 15/10 y otro nombre de archivo). Antes de revisar el cálculo, se abre el DP del servicio y se compara la fecha y el nombre del archivo importado con el que se espera. Después de la carga correcta, se contrastaron los totales de la pantalla (5.054,12 HH directas, 1.248 HH de MOI, BAC 322.877,39) con el cálculo hecho con el lector real de la app.

### 2. Comitear solo los cambios propios en un archivo con cambios ajenos: parche filtrado por hunk

Los flujos 12, 14 y 16 tenían cambios sin comitear de sesiones anteriores mezclados con los de la tarea. Funcionó: `git diff -U0 archivo` → quedarse con los hunks propios (cuando un hunk mezcla una línea ajena con una propia, se reescribe para dejar solo la inserción propia) → guardar el parche en el scratchpad → `git apply --cached --unidiff-zero --ignore-whitespace parche`. Se revisa con `git diff --cached -U0` antes de comitear. Es más corto que reconstruir el blob con `git update-index --cacheinfo`. Los archivos ajenos quedan modificados en el árbol, sin tocar.

### 3. `toLocaleString` en un componente cliente con render en servidor rompe la hidratación (React #418)

La fecha de subida del archivo se dibujaba distinta en el servidor (UTC) y en el navegador de Victor, y la consola de producción mostró «Minified React error #418». Se corrigió envolviendo el texto con la fecha en un `<span suppressHydrationWarning>`. En local no se pudo ver porque no se pudo iniciar sesión; salió en la primera verificación en producción. Revisar la consola (`read_console_messages` / `browser_console_messages`) en cada pantalla nueva con fechas.

### 4. El modo automático bloquea el inicio de sesión y los clics de escritura en producción desde Playwright

Se denegaron dos acciones: cargar el DP de PS-0003 desde el navegador (acción sobre producción) y rellenar el formulario de login local con las cuentas de prueba (uso de credenciales). No se buscó un rodeo. Lo que sí se pudo: aprovechar la sesión ya iniciada en el dominio de producción para **leer** pantallas y verificar el despliegue, y dejar a Victor lo que escribe datos o necesita iniciar sesión. Conviene planear la verificación de pantallas autenticadas contra el dominio desplegado, y la de escritura con permiso explícito de Victor.

### 5. Las claves de prueba quedan visibles al leer el archivo de memoria

Abrir `cuentas-prueba.md` con Read muestra las claves en la salida de la herramienta (pasó otra vez en esta sesión, además del `sed` de la sesión anterior). Se evita releer el archivo cuando la sesión del navegador ya está iniciada, y las claves nunca se repiten en el chat ni se copian a archivos del repositorio.

### 6. Heredocs de Bash con comillas siguen fallando (reincide, candidata a Skill)

Un bloque de varios heredocs con apóstrofes y plantillas TSX falló con «unexpected EOF» y no creó ningún archivo. Con la herramienta Write cada archivo se creó sin problema (reincidencia de los aprendizajes del plan de Informes, punto 1).

### 7. Skills creadas para repetir el cuadre de HH (en `01_pg_planeamiento`)

`comparar-insumos-presupuesto` y `cuadrar-hh-con-insumos` (en `01_pg_planeamiento/.claude/skills/`) comparan el listado de insumos con el presupuesto y abren las líneas de «Sub Partidas:» con sus HH sin cambiar el costo unitario de ninguna partida. Su lector es un espejo de `py_control_proyectos_web/src/lib/dp/`: si la app cambia su lectura, hay que revisar `scripts/lib-presupuesto.cjs`. Probadas con PS-108, PS-131, PS-140 y PS-167.

## Clasificación y destino propuesto

| # | Tipo | Destino propuesto |
|---|---|---|
| 1 | Reincidencia de un principio | Ya está en `00-estandar-agentes/01-principios-y-seguridad.md`; queda como evidencia |
| 2 | Técnica de Git | Candidata a `01-contexto-repositorio/03-entorno-git-y-worktrees.md` |
| 3 | Técnica de verificación | Candidata a `01-contexto-repositorio/04-pruebas-y-evidencia.md` |
| 4 | Límite de la herramienta | Candidata a `01-contexto-repositorio/04-pruebas-y-evidencia.md` |
| 5 | Seguridad de credenciales | Candidata a `00-estandar-agentes/01-principios-y-seguridad.md` |
| 6 | Entorno Windows | Reincidencia: candidata a Skill (ver el aprendizaje del plan de Informes) |
| 7 | Referencia | Se queda como aprendizaje |
