---
name: verificar-permisos-por-rol
description: Verifica que cada rol de una aplicación ve y puede hacer exactamente lo que dice su tabla de permisos, comparando lo esperado contra lo observado con un mecanismo de suplantación de rol y llamadas sin efecto. Úsalo al cambiar permisos, menús o accesos por rol.
---

# Verificar permisos por rol

Sirve para cualquier aplicación con roles y una fuente escrita de permisos. No depende de un proyecto concreto.

## Entradas (pídelas si no las tienes)

1. **Tabla de permisos**: la fuente de verdad (rol × pantalla o acción → permitido / no permitido).
2. **Lista de roles** que existen.
3. **Mecanismo de suplantación**: cómo ver la app como otro rol sin iniciar sesión de nuevo (p. ej. una función de «ver como»). Si no existe, una cuenta por rol.
4. **Datos de prueba autorizados** y el entorno donde se puede probar.

## Pasos

1. Inicia sesión una sola vez con la cuenta que puede suplantar; prueba todos los roles con el mecanismo de suplantación.
2. Por cada rol, recorre cada pantalla y acción de la tabla. Usa llamadas de solo lectura o sin efecto; nunca borres ni modifiques datos reales. Si una acción de escritura es imprescindible, usa registros de prueba marcados y desactívalos después.
3. Anota lo **observado** (visible / oculto / bloqueado / mensaje devuelto).
4. Distingue el motivo del bloqueo: **rol** sin permiso frente a **alcance** (el rol sí puede, pero no sobre ese elemento). La suplantación suele cambiar el rol pero no el alcance del usuario real.
5. Si compruebas redirecciones con llamadas HTTP, recuerda que algunos servidores responden 200 con el aviso de redirección en el cuerpo; confirma con el navegador.
6. Compara con la tabla y entrega una tabla rol × acción con *esperado / observado / resultado*.

## Salida

- Tabla de resultados y lista de diferencias, cada una con la fila de la tabla de permisos que incumple.
- Las diferencias se corrigen en el código **o** en la tabla, según decida el responsable del negocio; nunca se cambia la tabla para que coincida sin consulta.

## Reglas

- No leer ni mostrar credenciales; no copiarlas a archivos.
- Borra las capturas o snapshots temporales del navegador al terminar.
- Si algo no se pudo verificar, dilo; no lo declares conforme.
