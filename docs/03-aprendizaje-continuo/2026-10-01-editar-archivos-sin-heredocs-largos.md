# Escribir y editar archivos con la herramienta de escritura, no con heredocs largos

**Fecha:** 2026-10-01
**Origen:** Workers F0-R, F0-T, F0-U1, F0-U2, F1-B, F1-C, F2-B a F2-D, F3-A a F3-E, F4-A a F4-C y F5-A del plan niveles-paquetes-plan-maestro-rdt
**Tarea relacionada:** `docs/02-trabajo-activo/01-planes/2026-09-30-niveles-paquetes-plan-maestro-rdt.md`
**Categoría:** `herramientas/edición`

## Hallazgo

Casi todos los Workers del plan perdieron al menos una llamada con el mismo fallo: un heredoc largo de Bash (`<<'EOF'`) con tildes, comillas, apóstrofos o `$` dentro termina en «unexpected EOF», no ejecuta nada o corrompe el contenido. Pasó con código TypeScript, scripts de Python y archivos de texto.

## Qué funcionó

1. **Archivos nuevos o largos:** escribirlos con la herramienta de escritura (Write), no con `cat <<EOF`.
2. **Ajustes pequeños sobre varios sitios:** guardar un script de Python en un archivo (con Write) y ejecutarlo. Cada reemplazo con `assert texto.count(ancla) == 1` detecta anclas que no coinciden o que se repiten (un `.index()` sobre el texto equivocado duplicó un bloque).
3. **`sed` sobre código con barras invertidas y comillas** se corrompe: no usarlo para eso.
4. **Fin de línea:** comprobar antes si el archivo usa CRLF (maquetas y `design.md` lo usan) y normalizar antes de reemplazar; si no, las anclas multilínea no coinciden.
5. **`String.replace` de JavaScript:** el texto de reemplazo interpreta `$'` y `$&` como patrones; usar una función de reemplazo.
6. La herramienta de edición exige haber leído el archivo con la herramienta de lectura; un `cat` en Bash no cuenta.
7. **Nunca `git stash -u` para comparar** contra otra versión: se ejecutó por error una vez (se restauró con `stash pop`, sin pérdida). Comparar con `git archive` a una carpeta temporal o con `git show`.

## Destino propuesto

Promover a `docs/00-estandar-agentes/` (nota breve en el brief base de Workers) cuando Victor lo apruebe; mientras tanto, queda como aprendizaje.
