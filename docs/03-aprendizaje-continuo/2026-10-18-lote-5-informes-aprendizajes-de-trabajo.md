# Aprendizajes de trabajo del Lote 5 de observaciones (2026-10-18)

## Origen

Plan [`2026-10-18-observaciones-victor-lote-5-editor-informes.md`](../02-trabajo-activo/01-planes/2026-10-18-observaciones-victor-lote-5-editor-informes.md), apartado «Mejoras (de trabajo)». Trabajo tradicional (sin Orquestador): editor de informes de supervisión. Solo método y herramientas; las reglas del sistema se integraron en los flujos 06 y 22.

## Observación

### 1. Si Victor dice «igual que el cuadro que te indiqué», se copia la estructura de ese cuadro; no se inventa una adaptada

Para «Avance por nivel» el agente armó sus propias columnas (Nivel, Nombre, Partidas, Avance, Restante) y las marcó como «supuesto por confirmar». Victor respondió que debía ser igual al cuadro de «Actividades ejecutadas». Cuando la referencia ya fue dada (captura o tabla nombrada), se reutiliza tal cual y solo se adapta lo que no tenga sentido para ese dato, diciendo exactamente qué se adaptó y por qué (aquí: un nivel mezcla unidades, así que se mide en % ponderado por presupuesto en vez de metrado).

### 2. Un conflicto entre un pedido nuevo y `design.md` se muestra con la cita exacta, no con un resumen

El agente dijo que `design.md` alineaba la cabecera igual que el dato; Victor contestó que `design.md` «no dice cómo van los valores». Sí lo dice (§ Alineación de columnas, regla del 2026-09-30), pero la forma de planteárselo no se entendió. Al consultar una contradicción con un documento normativo, se copia la frase y el número de sección y se propone la salida concreta (qué se cambia y dónde), en una sola pregunta.

### 3. Cerrar el lote incluye llenar los cuatro apartados del plan y, aun con el código listo, no se da por terminado hasta el push

Victor tuvo que pedir «cierra con las mejoras». Los apartados «Mejoras», «Reglas de negocio», «Observaciones sobre la política» y «Huérfanos» se llenan al ocurrir cada hallazgo; al terminar una tanda de construcción se revisa que no queden en «Sin entradas todavía» (reincide en `cierre-de-plan-completo`).

### 4. Generar un PDF de muestra desde una prueba temporal y mirarlo como imagen

Para revisar el diseño del PDF sin servidor ni sesión: una prueba de Vitest temporal arma el documento con `datos-prueba-test.ts` y lo escribe en el scratchpad; PyMuPDF (`fitz`) lo convierte a PNG (`get_pixmap(dpi=..., clip=...)` para acercar una zona). Se borra la prueba al terminar. Sirvió para ver que el color de acento sobre el azul no contrastaba en las barritas de progreso.

### 5. Parches de varios archivos: script de Python escrito con la herramienta Write

Los heredocs con barras invertidas y comillas rompieron los reemplazos (reincide, ver los aprendizajes de Informes y del Lote 4). Un script `patch_*.py` creado con Write, con una función `edit(ruta, [(viejo, nuevo)])` que falla si el texto aparece distinto de una vez, evita reemplazos silenciosos.

### 6. `cobertura-avisos.test.ts` agota los 5 s cuando la máquina está cargada

Falla de forma intermitente en la corrida completa y pasa sola. No es del lote; se corre aparte antes de culpar al cambio.

### 7. Cuando Victor nombra algo con su palabra de negocio, se confirma qué es en el sistema antes de construir

«Paquete de partidas» se leyó como el paquete de trabajo del flujo 19 y se propuso otra tabla; Victor aclaró que era el nivel 3.3 del presupuesto (rol `PAQUETE_PARTIDAS`) y que ahí solo quería el avance. Dos rondas de maqueta se perdieron. Lo que funcionó: mostrar la maqueta en una tabla con sus datos reales antes de escribir código, y corregirla con lo que él dijo.

### 8. Una aclaración corta de Victor puede corregir mi lectura de la anterior, no confirmarla

«Quiero saber el avance de un 3 Tuberías, no el de sus metrados» describía la columna Avance, no pedía quitar los metrados. Ante una frase que parece contradecir la anterior, se contrasta con lo ya dicho y se muestra el resultado antes de revertir.

## Clasificación y destino propuesto

| # | Tipo | Destino propuesto |
|---|---|---|
| 1 | Método de trabajo con Victor | Candidata a `00-estandar-agentes/01-principios-y-seguridad.md` |
| 2 | Método de consulta | Candidata a `00-estandar-agentes/01-principios-y-seguridad.md` |
| 3 | Reincidencia de cierre | Ya está en `04-flujo-sdd-y-planes.md`; queda como evidencia |
| 4 | Técnica de verificación | Candidata a `01-contexto-repositorio/04-pruebas-y-evidencia.md` |
| 5 | Entorno Windows | Reincidencia: candidata a Skill |
| 6 | Prueba inestable | Se queda como aprendizaje |
| 7 | Método de consulta | Candidata a `00-estandar-agentes/01-principios-y-seguridad.md` (junto con la 2) |
| 8 | Método de consulta | Se queda como aprendizaje |
