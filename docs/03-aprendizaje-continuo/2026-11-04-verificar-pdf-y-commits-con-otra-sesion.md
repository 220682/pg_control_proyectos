# 2026-11-04 — Verificar un PDF generado en la app y comitear cuando otra sesión trabaja en el mismo árbol

## Origen

Trabajo diario (sin plan) sobre «Status de servicios» ([flujo 27](../04-flujos-de-negocio/27-status-de-servicios.md)): PDF oscuro igual al dashboard, encabezado de los PDF configurable y 5 métricas nuevas (app `913d57c`, `21aac8d`; docs `0df1240`, `2a1cfa9`).

## Método que funcionó

- **Ver el PDF antes de entregar, no solo la pantalla.** La ruta real del PDF pide sesión, así que con `curl` responde 307 al inicio de sesión. Lo que funcionó fue un banco temporal: una página `src/app/(workspace)/zz-banco-status` con datos de ejemplo y una ruta `src/app/api/zz-banco-pdf` que genera el PDF con la misma función de la app y **lo escribe en el scratchpad**. Se llama desde Playwright con `page.request.get(...)`, que lleva la sesión; `require` no existe dentro de `run_code`, por eso el archivo lo escribe la ruta y no el script. Después se abre con la herramienta Read, que muestra cada hoja como imagen. Al terminar se borra el banco antes de comitear.
- **Probar ambas orientaciones y el caso con más texto** (nombres largos, montos de 7 cifras, periodo «Nov 2025–Feb 2026»): los cortes y desbordes salieron ahí, no con los datos cortos.
- **Comitear solo lo propio con pathspec.** Otra sesión tenía cambios sin comitear en el mismo árbol de la app. `git add` solo de los archivos nuevos propios y `git commit -F - -- <rutas>` con la lista exacta; después `git status --short` confirma que lo ajeno sigue sin tocar.

## Trampas encontradas

- **Helvetica de pdfkit (WinAnsi) no tiene el signo menos «−» (U+2212):** se imprime como `"`. Usar el guion ASCII `-`; la raya «–» sí existe.
- **`characterSpacing` rompe el cálculo de ancho** de `widthOfString`, y los títulos que debían entrar en una línea se partían. Se quitó.
- **Recortar texto al ancho exacto todavía lo parte en dos líneas** por redondeo: dejar 1 pt de holgura.
- **`doc.openImage` existe en tiempo de ejecución pero no en los tipos** de pdfkit: requiere un cast.
- **La prueba `cobertura-avisos.test.ts` falla por tiempo (14 s) en la corrida completa** cuando la máquina está cargada; sola pasa. No confundirla con una regresión: volver a correrla aislada antes de concluir.
- **Los heredocs complejos en Bash de Windows fallan** («unexpected EOF»); para reemplazos múltiples, escribir un script Python con la herramienta Write en el scratchpad y ejecutarlo (ya anotado en `2026-10-17-informes-supervision-y-dashboard-aprendizajes-de-trabajo.md`; se repitió).

## Destino propuesto

Se queda como aprendizaje. Candidata a procedimiento reusable: «verificar un PDF de la app con banco + Read».
