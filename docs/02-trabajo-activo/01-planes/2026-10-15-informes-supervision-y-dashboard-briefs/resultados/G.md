# Resumen de cierre — Tanda G: Informes, descargas Word, PDF y Excel

## Tanda, rol y modelo

Worker 1 · G, Sonnet, esfuerzo medio. Ola 3, carril W1, tras D (0369ab8 verificado con `git log`).

## Estado de los ítems

| ID | Estado | Evidencia | Causa y quién lo resuelve |
|---|---|---|---|
| G1 | Conforme | `docx@^9.12.0` en `package.json`/`package-lock.json`; `exportar/word.ts`; prueba abre el `.docx` como zip (JSZip), halla `word/media/*` y 3 `<w:drawing>` para 3 fotos | — |
| G2 | Conforme | `exportar/pdf.ts` sobre `src/lib/pdf/hoja.ts` (sin editarlo): cabecera de tres cajas, tablas con cabecera repetida, marca de agua «BORRADOR» en cada página, fotos 2/4/6 por página (prueba de conteo de páginas); lectura con `pdf-parse` | — |
| G3 | Conforme | `exportar/excel.ts`: hoja «Informe», una hoja por tabla, hoja «Fotos» con imagen, descripción, partida, hora y bloque; releído con `exceljs` (3 imágenes, filas iguales al modelo) | La «miniatura» es la foto original reducida solo en pantalla (ver G-H2) |
| G4 | Conforme | `descargar/route.ts`: `?formato=pdf\|docx\|xlsx&alcance=completo\|resumen\|fotos`, `maxDuration = 60`; 400 por valores inválidos, 404 borrador ajeno, 403 COSTOS sin economía, 409 emitido sin foto fija; emitido solo desde `fotoFija` (prueba: `componerDatosPorTipo` no se llama) | — |
| G5 | Conforme (medido) | Tabla de abajo | Riesgo de tamaño: ver G-H1 |
| G6 | Conforme | `exportar.test.ts` (17 pruebas): PDF, Word y Excel muestran las mismas celdas del modelo que alimenta a la vista previa | La vista previa (tandas E/F) aún no existe: «mismos datos» se verificó contra el modelo `DocInforme`, que ella debe consumir (G-H3) |
| G7 | Conforme (por ruta) / Observado (por pantalla) | `descargar-rutas.test.ts` (23 pruebas): 13 roles x 3 formatos x 3 alcances; COSTOS sin economía = 403 por URL directa, 200 con economía; cualquier rol conocido descarga los otros formatos. Skill `verificar-permisos-por-rol` aplicado en su parte de pruebas de ruta | Lo visual por rol queda «Observado» para la tanda L (P36: sin cuentas de prueba) |

Todo «no probado en base»: las migraciones 098 a 102 pueden no estar aplicadas (P33); el camino del borrador depende de `componer-datos.ts` (mockeado en las pruebas) y de la tabla `fotos_campo` y el bucket `documentos-proyecto` (simulados).

## Medición G5 (corregida por G-H1: 20 fotos, reducidas con sharp a 1000 px y calidad 70)

Fotos: 20 JPEG reales de 4000x3000 generados con sharp (ruido suavizado, el peor caso de compresión), 3,47 MB cada una (69,4 MB en total). Reducir las 20 en paralelo: 1267 ms, quedan 308 KB cada una (6,0 MB en total). No incluye la descarga desde Storage. Máquina de desarrollo Windows. Comando: `MEDIR_INFORMES=1 MEDIR_SALIDA=<archivo> npx vitest run medicion`.

| Formato | Vuelta 1 | Vuelta 2 | Archivo | Memoria (RSS) |
|---|---|---|---|---|
| PDF | 86 ms | 35 ms | 6,02 MB | +19 / +13 MB |
| Word | 911 ms | 720 ms | 6,03 MB | +31 / +44 MB |
| Excel | 549 ms | 488 ms | 6,03 MB | +63 / +0 MB |

Antes de reducir: 50 MB por archivo, Word 6 a 16 s, Excel 4,5 a 5 s. Meta de ~4 MB por archivo: NO se logró con estas fotos (6,0 MB), porque el ruido casi no se comprime (308 KB por foto a 1000 px); una foto real de obra suele quedar mucho más chica, pero no está medido con fotos reales. Si hiciera falta, bajar el lado mayor a ~800 px o la calidad. El límite de ~4,5 MB de Vercel queda «por confirmar» contra el plan.

## Rama, commits y archivos tocados

Rama `local-worker-1` (worktree `.worktrees/local-worker-1`), pusheada. Commits: `59111bc` (G1-G3), `e7ac566` (G4-G7) y el de la corrección G-H1 (ver `git log`); `git branch --contains` de ambos: `local-worker-1`. No se tocó `local-worker-3` ni `main`. Árbol limpio.

Creados: `src/lib/informes/exportar/{comun,word,pdf,excel,fuente}.ts`, `datos-prueba-test.ts`, `exportar.test.ts`, `medicion.test.ts`; `src/app/api/proyectos/[id]/informes/[informeId]/descargar/{route.ts,descargar-rutas.test.ts}`. Editados: `package.json`, `package-lock.json` (`docx` y `sharp`). Corrección G-H1: `exportar/reducir.ts` y `reducir.test.ts`. `fuente.ts` y `datos-prueba-test.ts` no estaban en la lista del brief (el brief permitía un `comun.ts`; el cargador va aparte para que `comun.ts` quede puro y sin base).

Verificación: `npm test` 138 archivos pasan y 1 omitido (medición), 1433 pruebas (tras G-H1); `npx tsc --noEmit` sin errores; `npm run lint` 9 errores y 22 avisos (tras G-H1), todos preexistentes (mis archivos: 0; el brief decía 22 avisos, el aviso de más es `_tituloGrupo` en `src/lib/notificaciones/grupo-proceso.ts`, no tocado); `npx next build --webpack` en verde.

## Hallazgos

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| G-H1 | RESUELTO por el Orquestador (parcial) | Con 20 fotos de 3 MB, los tres archivos pesan ~50 MB. Una función de Vercel no devuelve más de 4,5 MB en un cuerpo no transmitido por streaming (por confirmar contra el plan de Vercel), y Word tarda 6 a 16 s. Además `maxDuration = 60` sigue por confirmar | Implementado: `sharp` declarado en `package.json`; `exportar/reducir.ts` (1000 px, calidad 70, orientación corregida) aplicado en `cargarBytesFotos`. Quedan 6 MB por archivo con fotos de ruido; límite de Vercel por confirmar. Antes: elegir reducir las fotos al incrustarlas (requiere declarar `sharp` en `package.json`, hoy solo está como dependencia transitiva de Next, o recortar en la subida) y/o responder por streaming. No lo decidí: no estaba en el brief |
| G-H2 | RESUELTO | La «miniatura» del Excel es ahora la foto reducida (G-H1) | — |
| G-H3 | mejora de trabajo | Word, PDF y Excel salen de un único modelo (`armarDocumento` en `comun.ts`); la vista previa de E/F debería consumir el mismo modelo para que «mismos datos» sea cierto por construcción | Tandas E y F |
| G-H4 | PENDIENTE de la tanda E (aceptado por el Orquestador) | El brief no define la forma de `config` de los bloques sin fuente automática (INCIDENCIAS, SEMAFORO, LOGROS_ALERTAS, RESTRICCIONES, PROXIMAS_ACTIVIDADES, TEXTO, TABLA, CLIMA_TURNO, FIRMAS). Los imprimo de forma genérica (`texto`; `columnas`+`filas`; arreglos; pares clave-valor) | Tanda E (editor) debe confirmar las claves reales; si difieren, se ajusta `partesDeConfig` en `comun.ts` |
| G-H5 | regla de negocio (decisión de implementación, por confirmar) | `alcance`: *resumen* = Datos del servicio, Semáforo, Indicadores, Logros y alertas, Avance por nivel, Costos-indicadores y Firmas; *fotos* = Datos del servicio y bloques de fotos. Los importes no llevan símbolo de moneda (no está definido en los datos). Word no tiene marca de agua diagonal: «BORRADOR» va grande en el encabezado de cada página | Victor, al validar el flujo de informes |
| G-H6 | conflicto con un flujo/brief | El plan cita `rdts/exportar` como patrón; no existe. Usé `rdts/exportador-*.ts` y `dp/exportador-excel.ts` | Corregir el plan |
| G-H7 | archivo huérfano | `.env.local` del worktree se sobrescribió con el principal (autorizado) | Ninguno |

## Traspaso

- Hecho: G1 a G7 en `local-worker-1`, probado sin base. Lo de pantalla por rol queda a la tanda L.
- Falta: decisión de Victor sobre G-H1/G-H2 (tamaño de archivo y límite de respuesta); enlace de la pantalla (E/F) a la ruta `descargar` con los botones y los 3 alcances; prueba contra base real cuando 098 a 102 estén aplicadas, con una descarga de borrador y otra de emitido.
- Verificación: `npm test`, `npx tsc --noEmit`, `npm run lint`, `npx next build --webpack` (resultados arriba).

## Llamadas y contexto

Unas 45 llamadas.

## Skills revisados

`cerrar-tanda` (secuencia aplicada, sin commit de documentación: lo hace el Orquestador) y `verificar-permisos-por-rol` (pruebas de ruta por rol; lo visual queda para L). Los demás: ninguno aplica.

## Fuentes de verdad revisadas

No se editó ninguna. Pendientes para el Documentador/Orquestador: flujo 14 (acceso a descargas: quien ve el informe lo descarga; COSTOS exige economía) y la matriz de permisos, si aún no registran la ruta `descargar` y los tres alcances (G-H5).

Cierre del Documentador (2026-10-16): «Fuentes de verdad revisadas: ninguna fuente central editada en este cierre. Pendientes de decisión o de la tanda M: flujo 14 y matriz de permisos (ruta `descargar`, alcances y economía de COSTOS; G7 observado), flujo 22 de informes (M1) y la validación de G-H5 por Victor.»

## Corrección D-H / G-H (decisión del Orquestador a las preguntas de F)

Commit en `local-worker-1` (ver `git log`, mensaje «Correccion D-H / G-H»). Todo «no probado en base».

| Punto | Qué se hizo | Evidencia |
|---|---|---|
| F-H1 | `GET informes/[informeId]` devuelve, **aditivo** (no cambia `tipos.ts`): `datos` por id de bloque, `fotos` por id de bloque y `errorDatos` si falla el cálculo en vivo (el editor abre igual con `datos: {}`). Borrador: `cargarFuente` (mismo compositor que la descarga); emitido: de `fotoFija`. `fuente.ts` descarta los bloques económicos si el formato no es COSTOS (R5); COSTOS sin economía sigue 403 por `cargarInformeVisible` | `correccion-dh.test.ts`: 13 roles (COSTOS 200 solo con economía, 403 sin filtrar datos), 404 borrador ajeno/inexistente, 401, sin dinero, fallo de la fuente |
| F-H4 | Nuevo `src/lib/informes/fotos-huerfanas.ts`. El PATCH que cambia bloques suelta (`informe_id` y `bloque_id` nulos) las fotos de bloques que ya no existen; `emitir` hace lo mismo antes de armar la foto fija. No hay transacción: se guarda primero el informe y luego se sueltan las fotos; si eso falla responde 500 y repetir el PATCH (o emitir) es idempotente | pruebas de PATCH sin el bloque, PATCH que lo conserva y emisión sin fotos huérfanas |
| F-H5 | `GET fotos-campo?informeId=` lista las fotos desde el primer hasta el último día del periodo (fecha Lima), con las reglas del informe (borrador ajeno y uuid malo = 404, COSTOS sin economía = 403, 401 sin sesión); `?fecha=` sigue igual; si vienen las dos manda `informeId` | pruebas de bordes de día Lima, 13 roles, 400/401/403/404 |
| F-H2 | `partesDeConfig` alineado con las claves de F: `items[]` (INCIDENCIAS/RESTRICCIONES/PROXIMAS_ACTIVIDADES), `firmantes[{nombre,cargo}]` (tabla Nombre, Cargo, Firma), `texto`, `columnas`+`filas`, CLIMA_TURNO, `logros`/`alertas`, SEMAFORO `{estado,texto}`; los datos de prueba usan esas claves | `config-f.test.ts`: PDF, Word y Excel imprimen todas |

Comandos: `npm test` 140 archivos pasan y 1 omitido, 1470 pruebas; `tsc` sin errores; lint 9 errores y 22 avisos (ninguno nuevo); build webpack en verde. G-H4 queda cerrado por F-H2. Pendiente: la tanda F/E debe usar los campos nuevos `datos`/`fotos` del GET y `?informeId=`; documentar en los flujos 14/16 (Documentador).

- Corrección (defectos de la tanda L, commit «Descargas PDF: la marca BORRADOR sale entera…» en `local-worker-1`): la marca de agua se partía en «BORRAD / OR» porque a 110 pt la palabra no cabía en la caja de 520 pt y pdfkit la envolvía; ahora el tamaño se calcula para que quepa y se dibuja sin caja. Con alcance «fotos» la primera página quedaba casi vacía porque el bloque de fotos forzaba página nueva; ahora sigue en la página actual si caben el título y una tanda (150 pt por fila). Pruebas con `pdf-parse` en `pdf-marca-y-fotos.test.ts`. Word (encabezado «BORRADOR» en una línea) y Excel (A1) ya estaban cubiertos por `exportar.test.ts`. `npm test` 1475 pasan, `tsc` limpio, lint 9 errores y 22 avisos (sin nuevos), build webpack en verde.
