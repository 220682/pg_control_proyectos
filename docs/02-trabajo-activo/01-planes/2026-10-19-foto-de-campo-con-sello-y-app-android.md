# Foto de campo con sello y app Android

## Identificación y estado

- Tema: que cada foto de campo salga con su fecha, hora y ubicación impresas sobre la imagen, y que la app se pueda instalar en los celulares Android del equipo como un archivo APK, sin tienda.
- Fecha de inicio: 2026-10-19.
- Estado: `Aprobado (Gate 1, 2026-10-19)`. En esta sesión se implementa solo el Paso 1 (foto con sello, tandas T1 a T3); el Paso 2 (APK) queda para otra sesión.

Puertas:

- Gate Spec: `aprobado` (Victor, 2026-10-19)
- Gate 1: `aprobado` (Victor, 2026-10-19: «aprobado»; ver Registro de decisiones)
- Gate 2: `pendiente`

## Spec

### Estado

`Aprobado` (2026-10-19).

### Problema y contexto

Victor quiere llevar la app al celular, solo Android por ahora (decidido el 2026-10-19: iPhone queda fuera). El uso principal en campo es la **Foto de campo** del flujo 22, y Victor pidió que la foto muestre sus datos de ubicación, como las fotos de obra con sello. Su ejemplo (una foto con cuatro líneas abajo a la derecha) trae: fecha, coordenadas, altitud y velocidad. Pidió **agregar la hora en la misma fila de la fecha**.

Lo que se verificó en el código (`py_control_proyectos_web`, `main` en `0b9961a`, 2026-10-19; releído por el Orquestador relevo con `main` en `1919fba`: `FotoCampo.tsx` y `foto-utils.ts` no cambiaron y los hallazgos H1 y H2 siguen vigentes):

| # | Hallazgo | Evidencia |
|---|---|---|
| H1 | **El GPS se lee al apretar «Guardar foto», no al tomar la foto.** Si el supervisor guarda después o ya se movió, la ubicación no es la de la foto. La hora sí se toma al elegir la foto. | `FotoCampo.tsx`: `leerGps()` se llama dentro de `enviar()`; `tomadaEn` se fija en `alElegir()` |
| H2 | **La foto pierde su ubicación interna.** El navegador la redibuja en un lienzo a 1600 px y eso borra los datos que la cámara guarde dentro del archivo. El GPS vive solo en la base de datos. | `FotoCampo.tsx`: `reducirFoto()` |
| H3 | **La ubicación se guarda pero no se muestra en ningún lado**: ni el banco de fotos, ni el editor, ni el PDF, Word o Excel del informe. | búsqueda de `lat`, `lng` y `gps` en `src/`: solo aparecen al capturar, validar y guardar |
| H4 | **La app no se puede empaquetar como archivos estáticos dentro del celular**: usa middleware con sesión por cookies de Supabase y 85 rutas de API. El APK tiene que abrir la app ya publicada. | `middleware.ts`, `src/app/api/` (85 `route.ts`) |
| H5 | La app **no es instalable hoy**: sin manifest, sin íconos y sin service worker. | `public/`, `src/app/layout.tsx` |
| H6 | Los PDF, Word y Excel salen de rutas de la API con descarga; dentro de un envoltorio Android las descargas **no se resuelven solas**. | `api/proyectos/[id]/informes/[informeId]/descargar`; por comprobar en el celular |
| H7 | En esta PC **no hay Android Studio, Java ni el SDK de Android**; Node 24.18.0 sí. | comprobado por el Orquestador con la consola |
| H8 | La dirección `https://py-control-proyectos-web.vercel.app` responde (HTTP 200 en `/login`, 2026-10-19). | consulta de cabeceras, solo lectura |

### Resultado esperado

1. Cada foto de campo guardada lleva, impreso abajo a la derecha, un **sello** con cuatro líneas como el ejemplo de Victor:

   ```
   22/9/2026 14:35
   15.1589S 75.0701W
   Altitud:815.4msnm
   Velocidad:2.5km/h
   ```

   Como el sello va dentro de la imagen, **sale solo** en el banco de fotos, en el editor y en el PDF, Word y Excel del informe, sin tocar los exportadores.
2. La ubicación de la foto es la del momento en que se **toma**, no la del momento en que se guarda.
3. Un **APK Android** instalable que abre la app publicada: con el logo de PROMCOSER, cámara, GPS y descargas funcionando, y un aviso simple de «Sin conexión» cuando no hay internet.
4. Una actualización de la web llega sola a los celulares con el APK instalado, sin reinstalar.

### Alcance

**Paso 1 — Foto con sello (web; sirve ya desde el navegador del celular).**

- Leer el GPS al tocar «Tomar foto» y refrescarlo al volver de la cámara; guardar en la base ese mismo valor, para que el sello y los datos coincidan.
- Imprimir el sello sobre la imagen ya reducida, en la esquina inferior derecha, texto blanco con contorno oscuro, de un tamaño relativo a la imagen que se lea en la descarga a 1000 px y en las cajas de fotos del editor.
- Formato del sello: línea 1 `d/M/aaaa HH:mm` en **hora de Lima** y 24 h (igual que el banco); línea 2 coordenadas con 4 decimales y letra de hemisferio (`15.1589S 75.0701W`); línea 3 `Altitud:815.4msnm` y línea 4 `Velocidad:2.5km/h` (velocidad en km/h, un decimal), **solo si el celular entrega ese dato**; si no lo entrega, esa línea no se imprime.
- La casilla «Guardar la ubicación (GPS)» se mantiene como hoy: si la desmarcan, el sello lleva solo la fecha y la hora, y no se guardan coordenadas. Lo mismo si el celular no logra ubicación (se avisa, como hoy).
- Una **imagen de muestra** del sello sobre una foto real, para que Victor la vea antes de construir todo el flujo.
- Actualizar el flujo 22.

**Paso 2 — APK Android.**

- Un envoltorio (Capacitor) que abre la app publicada, con el nombre «Control de Proyectos» y el logo de PROMCOSER (`public/logos/promcoser.png`).
- Permisos de cámara y ubicación; las descargas de PDF, Word y Excel funcionan y el archivo se puede abrir.
- Aviso simple de «Sin conexión» si no hay internet.
- APK firmado y su instructivo corto de instalación para el equipo; repartido por archivo (WhatsApp o Drive), sin tienda.
- Documentar cómo se compila un APK nuevo y dónde se guarda la llave de firma.

### No alcance

- iPhone y las tiendas (Play Store y App Store), por decisión de Victor del 2026-10-19.
- **Uso sin señal:** sin internet no se usa la app; no hay cola de fotos guardadas en el celular (decisión de Victor, 2026-10-19; coincide con el flujo 22: «fuera de esta versión: guardar fotos sin señal»).
- Notificaciones push (la app no las tiene, flujo 04).
- Editar fotos a mano (recorte o anotaciones); el sello es automático.
- Mostrar las coordenadas en pantalla fuera de la imagen, y guardar altitud o velocidad en la base: solo viven en el sello.
- Cambios de permisos por rol, pantallas nuevas o migraciones de base de datos.

### Usuarios / roles afectados

Subir una foto de campo sigue siendo solo de los 4 roles de campo; ver y usar el banco, de los 13 roles (flujo 22). El APK lo puede instalar cualquier miembro del equipo, y dentro de la app cada rol conserva exactamente lo que ya puede hacer. **No cambia ningún permiso, menú ni acceso**, así que la matriz de permisos y el flujo 14 no se tocan (el Planner lo confirma).

### Reglas de negocio y documentos afectados

| Qué dice hoy | Qué pasaría a decir | Documento |
|---|---|---|
| «guarda hora y, si el usuario lo permite, GPS… el navegador reduce la imagen a 1600 px antes de subirla» (sección «Foto de campo y banco de fotos») | Lee el GPS al tomar la foto, y antes de subirla imprime el sello (fecha y hora de Lima, coordenadas, altitud y velocidad cuando el celular las entrega) en la esquina inferior derecha; hora y coordenadas se siguen guardando | [22 Informes de supervisión](../../04-flujos-de-negocio/22-informes-de-supervision.md) |
| «Fuera de esta versión: guardar fotos sin señal y subirlas después, y editar fotos» | Sin cambio; se agrega que la app Android tampoco funciona sin señal | flujo 22 |
| «Configuración» menciona «adaptación móvil» y dice que su alcance real está sin definir | Se agrega una sección «App Android»: qué es, que abre la app publicada, que requiere internet, solo Android y reparto por archivo | [01 Configuración](../../04-flujos-de-negocio/01-configuracion.md) (extensión, no contradicción) |
| `AGENTS.md` dice que no hay comandos de compilación verificados | Cuando el APK exista, el procedimiento de compilación se documenta en `01-contexto-repositorio/`; si hace falta tocar `AGENTS.md`, va como observación sobre la política para el Auditor | `01-contexto-repositorio/` |

No afectados (revisados por el Orquestador contra los disparadores `Lee si:`): 14 (accesos), 16 (paneles), 04 (notificaciones).

### Datos, API, migraciones o dependencias

- **Paso 1:** sin migración, sin API nueva y sin dependencias nuevas. `lat` y `lng` ya existen en la tabla de fotos de campo.
- **Paso 2:** dependencias de desarrollo nuevas (Capacitor: núcleo, línea de comandos y plataforma Android) y una carpeta `android/`; el Planner decide si vive en el repositorio de la app y lo declara en el plan. Sin cambios en la base ni en la API.
- **Dirección que abre el APK:** `https://py-control-proyectos-web.vercel.app` (verificada). Queda escrita dentro del APK: cambiarla después exige un APK nuevo para todos.
- **Llave de firma del APK:** se genera con Victor, se guarda fuera del repositorio y ningún agente la lee ni la muestra.
- **Entorno de compilación:** Android Studio (incluye Java y el SDK) debe instalarse en esta PC; es gratis. Lo instala Victor, guiado.
- **Nombre, identificador de la app y versión mínima de Android:** los propone el Planner; el identificador no se puede cambiar después sin que sea otra app, por eso se aprueba en el Gate 1.
- **Cabeceras de seguridad:** sin cambios previstos (`camera=()` no afecta a la captura por archivo; `geolocation=(self)` ya permite la ubicación). Se comprueba en el celular.

### Diseño / UI aplicable

El sello no es una pantalla: es texto sobre la imagen. La referencia es la foto de ejemplo de Victor (2026-10-19). Las pantallas existentes no cambian de aspecto. El Planner revisa `design.md` por si conviene dejar anotado el estilo del sello.

### Riesgos y decisiones pendientes

**Decisión con Victor (resuelta el 2026-10-19):**

- **Dirección que abre el APK:** `https://py-control-proyectos-web.vercel.app` (la recomendada; Victor aprobó con «OK, DALE»). Si más adelante quiere una dirección propia, exige un APK nuevo para todos.

**Decididas por el Orquestador (operativas):** hora de Lima en 24 h; nombre «Control de Proyectos» (el título actual de la app); la casilla de GPS se mantiene; las coordenadas se guardan como hoy.

**Riesgos:**

1. **Descargas dentro del APK (H6):** si no funcionan solas, hay que resolverlas; es la función de negocio más expuesta.
2. **Ubicación al volver de la cámara:** al abrir la cámara de Android, la página queda en segundo plano y puede no recibir lecturas de GPS; la velocidad es la más difícil de obtener. Se mitiga leyendo al volver y omitiendo la línea que falte. Se prueba en celular real.
3. **El GPS del navegador exige HTTPS:** una prueba en celular contra un servidor de desarrollo en la red local no sirve. Se necesita una vista previa en HTTPS de la rama del Worker o el despliegue ya fusionado. Por confirmar si el alojamiento entrega esa vista previa.
4. **Legibilidad:** el sello debe leerse después de que el informe reduce la foto a 1000 px y en las cajas de fotos.
5. **El sello lo genera el celular:** sirve como registro operativo, no como prueba a prueba de manipulación.
6. **Actualizaciones:** la web se actualiza sola en el APK; un cambio del envoltorio (ícono, permisos) exige un APK nuevo y cada persona lo instala encima. Un APK repartido por archivo no se actualiza solo.
7. **Instalación fuera de tienda:** cada celular debe permitir «instalar apps desconocidas» y Android puede mostrar un aviso de seguridad.
8. **Trabajo en paralelo:** el plan del cronograma (rama `local-worker-6`) y el de Notificaciones siguen abiertos; no tocan `FotoCampo.tsx` ni `foto-utils.ts`. El Planner confirma por archivo antes de asignar.

### Criterios de aceptación

**Paso 1**

- Al tocar «Tomar foto» empieza la lectura de ubicación, y la foto guardada lleva las coordenadas de ese momento, no las del botón «Guardar».
- La imagen guardada trae el sello con las cuatro líneas en el formato indicado; sin altitud o sin velocidad, esa línea no aparece; sin GPS, solo la fecha y la hora.
- Con la casilla de GPS desmarcada no se imprimen ni se guardan coordenadas.
- El sello se lee en el PDF del informe y en la caja de fotos del editor.
- La foto sigue pesando 3 MB o menos y 1600 px de lado mayor; sin migración.
- Las pruebas del formato del sello (hemisferios, redondeo, líneas omitidas, hora de Lima) pasan, y `tsc`, el lint y las pruebas existentes quedan como estaban.
- Victor probó en su celular y vio las cuatro líneas correctas.

**Paso 2**

- El APK se instala en un celular Android, abre la app y se puede iniciar sesión; la sesión se comporta igual que en el navegador.
- «Tomar foto» abre la cámara y la ubicación funciona, pidiendo los permisos una sola vez.
- Los PDF, Word y Excel del informe se descargan al celular y se pueden abrir.
- Sin internet se ve el aviso «Sin conexión», no una página rota.
- Una publicación nueva de la web aparece en la app sin reinstalar (verificado con un cambio visible).
- La llave de firma no está en el repositorio, y el instructivo de instalación y de compilación existe.

### Estrategia de prueba / evidencia

- Pruebas unitarias del formato del sello (función pura) y de la lectura de ubicación simulada; `tsc`, lint y la suite existente.
- Verificación en el navegador con emulación de celular y ubicación simulada, subiendo una foto de muestra al campo de archivo (la cámara real no se automatiza); capturas del banco y del PDF con el sello.
- Verificación en celular real de Victor para cámara, GPS y descargas (Paso 1 sobre HTTPS; Paso 2 con el APK instalado), con un checklist visual preparado por el Planner.
- El APK se compila con Android Studio en esta PC y se instala por cable o por archivo.
- Evidencia en `03-evidencia/` y, al final, informe del Auditor en `04-auditoria/`.

### Aprobación (Gate Spec)

- [x] El Responsable humano aprueba este Spec (Victor, 2026-10-19: «OK, DALE», respondiendo a la aprobación y a la dirección del APK).

## Referencia al Spec aprobado

Este mismo archivo, sección «Spec», aprobado el 2026-10-19. Aún sin commit: el commit y el push los autoriza Victor.

## Objetivo, alcance y no alcance

Ver el Spec arriba (se copia aquí al aprobarse).

## Entorno, repositorios, ramas y worktrees

Verificado por el Orquestador el 2026-10-19:

- **Entorno:** `local`.
- **Documentación** (`pg_control_proyectos`): `main` directo, sincronizada con `origin/main` (0 0).
- **Código** (`py_control_proyectos_web`): `main` en `0b9961a`, sincronizada con `origin/main` (0 0) y sin cambios propios pendientes (solo un archivo ajeno sin seguimiento, `db/095_cerrar_lectura_directa.sql`).
- **Ramas libres para reutilizar:** `local-worker-1`, `local-worker-2` y `local-worker-3` ya están fusionadas en `main` y sus carpetas de trabajo están limpias, pero van 54, 56 y 25 commits detrás de `main`. `local-worker-4` y `local-worker-7` también están fusionadas pero no se proponen. **No libres:** `local-worker-5`, `local-worker-6` y `plan-maestro-tres-paneles` (sin fusionar).
- **Propuesta (se autoriza en el Gate 1; hasta entonces no se toca nada):** reutilizar `local-worker-1` para el Paso 1 y `local-worker-2` para el Paso 2, puestas al día con `main` por el Worker git.

## Skills aplicables

- `cerrar-tanda`: al cerrar cada tanda.
- `trasladar-hallazgos`: en la tanda final del Documentador.
- `seguir-flujo-de-planes`: el Orquestador, antes de declarar el cierre.
- `verificar-permisos-por-rol`: **no aplica**, porque el plan no cambia permisos, menús ni accesos.
- El repositorio de la app no tiene carpeta de Skills.

## Fases y dependencias

Planner, 2026-10-19. Base verificada: app `main` en `1919fba` (`FotoCampo.tsx` 238 líneas, `foto-utils.ts` 34, `reducir.ts` 22, `vitest` con `environment: 'node'` e `include: src/**/*.test.ts`, así que **no hay pruebas de componentes**: la lógica del sello y del GPS se aísla en funciones puras y se prueba ahí). Dos carriles independientes: el Paso 1 toca solo `src/components/informes/` (archivos nuevos y `FotoCampo.tsx`); el Paso 2 toca solo la raíz de la app (`package.json`, `package-lock.json`, `capacitor.config.ts`, `android/`, `.gitignore`, `eslint.config.mjs`). No comparten archivos.

### Carriles, tandas y olas

| Tanda | Carril / Worker | Ítems | Qué entrega | Depende de |
|---|---|---|---|---|
| T1 | Paso 1 · Worker 1 | S-01 a S-05 | Funciones puras del sello y **muestra sobre foto real** (parada de Victor tras S-01) | Autorización de Gate 1 y rama al día |
| T2 | Paso 1 · Worker 1 | S-06 a S-10 | Lectura de GPS al tocar «Tomar foto», refresco al volver y sello integrado en `FotoCampo.tsx` | T1 y visto bueno de Victor a la muestra |
| T3 | Paso 1 · Worker 1 | S-12 a S-17 | Verificación en navegador emulado, editor, PDF, Word y Excel; checklist para el celular de Victor | T2 |
| T4 | Paso 2 · Worker 2 | A-01 a A-06 | Capacitor armado, carpeta `android/`, ícono, permisos y APK de depuración que abre `/login` | Victor instala Android Studio |
| T5 | Paso 2 · Worker 2 | A-07 a A-12 | Sesión, cámara y GPS, descargas, «Sin conexión», enlaces y actualización automática | T4 |
| T6 | Paso 2 · Worker 2 | A-13 a A-17 | Llave de firma, APK firmado, instalación en celulares del equipo, borrador del procedimiento | T5; para A-16, el Paso 1 ya desplegado |
| T7 | Documentador | D-01 a D-06 | Flujos 22 y 01, documento de compilación, instructivo, traslado de hallazgos | T3 y T6 |

**Olas:** Ola 1 = T1 (y T4 en paralelo si Victor ya instaló Android Studio; si no, T4 espera y el Paso 1 avanza solo). Ola 2 = T2. Ola 3 = T3 ‖ T5. Ola 4 = prueba de Victor del Paso 1 en su celular sobre la vista previa de la rama ‖ T6; la fusión a `main` solo ocurre después del Gate 2, sin fusión anticipada (Victor, 2026-10-19). **En esta sesión solo corren las olas 1 a 3 del Paso 1 (T1 a T3); T4 a T6 quedan para otra sesión.** Ola 5 = T7. Ola 6 = Auditor y Gate 2. **7 tandas, 2 Workers de código, 6 olas.** Cada tanda cabe en 80 llamadas de Worker (estimación del Planner: T1 50 a 60, T2 55 a 65, T3 50 a 60 con las capturas, T4 45 a 60, T5 55 a 70, T6 35 a 50).

**Parada de Victor dentro de T1:** el Worker 1 entrega S-01 (imagen de muestra) y termina su sesión con un resumen parcial; el Orquestador muestra la imagen a Victor; con su visto bueno (y su elección del tamaño, ver S-01) se relanza el Worker 1 para S-02 a S-05 con el mismo brief. Sin visto bueno no se empieza T2.

### Reglas fijadas por el Planner para construir el sello

1. **El sello depende de la casilla de GPS, que hoy aparece después de elegir la foto.** Por eso el sello **no** se imprime al reducir (como pide el Spec, «sobre la imagen ya reducida»), sino sobre una **copia** del lienzo ya reducido: `FotoCampo.tsx` conserva el lienzo reducido sin sello, y el blob final se genera con el sello según la casilla y la lectura vigentes. La vista previa muestra el blob con sello y se regenera al marcar o desmarcar la casilla. Así no se comprime dos veces un JPEG y la casilla funciona como hoy.
2. **Lectura de ubicación:** una lectura al tocar «Tomar foto» o «Cambiar foto» (guardada en una referencia) y otra al volver de la cámara (`maximumAge: 0`, en paralelo con la reducción de la imagen). Regla de elección: si la lectura al volver llega a tiempo, gana; si no, vale la del toque; si ninguna sirve, no hay coordenadas, se muestra el aviso de hoy y el sello lleva solo fecha y hora. Las coordenadas que se envían al servidor son **las mismas** que se imprimieron.
3. **Tamaño del sello (valor inicial, lo confirma la muestra):** letra del 3 % del lado mayor de la imagen guardada (1600 px da 48 px; a 1000 px da 30 px), mínimo 14 px, interlineado 1,25, blanco con contorno oscuro de 12 % de la letra, margen del 2 % del lado mayor, alineado a la derecha y abajo, tipografía sans-serif del sistema. Tope: el bloque no pasa del 40 % del ancho de la imagen (en foto vertical también); si lo pasa, la letra baja hasta cumplirlo. La muestra enseña **dos variantes (3 % y 4 %)** y Victor elige; la elegida queda como constante.
4. **Cómo se mide la legibilidad:** (a) por cálculo, en una prueba: letra en px sobre la imagen de 1000 px del informe (`reducir.ts`: lado mayor 1000, JPEG 70) y su equivalente en puntos sobre la caja; (b) por inspección, con capturas al 100 % del PDF y de la caja del editor. Referencia: a 3 %, la letra mide 30 px sobre 1000 px, que en una caja de 2 columnas de la hoja A4 (unos 90 mm de ancho) equivale a unos 7,7 pt. **Límite conocido:** con 3 y 4 columnas el sello se vuelve pequeño (4 columnas: unos 3,7 pt); se anota en el flujo 22 como límite, no se corrige en este plan. La caja por defecto del editor (2 columnas, 45 mm de alto, foto sin recortar) se mide aparte y su resultado se registra.
5. **Hora del sello:** la de `tomadaEn` (momento en que se elige la foto), en hora de Lima 24 h con formato `d/M/aaaa HH:mm`; a medianoche sale `00:05`, nunca `24:05` (se usa `hourCycle: 'h23'`).
6. **Hemisferio del cero:** latitud o longitud 0 se imprime como N o E (por el signo del valor original). Redondeo a 4 decimales sobre el valor absoluto; las pruebas usan valores sin ambigüedad de coma flotante.
7. **Nombres y lugar de los archivos nuevos** (propuesta, el Worker confirma que no chocan): `src/components/informes/sello-foto.ts` (funciones puras `formatearSello`, `tamanoSello`, conversión de la lectura y elección de lectura), `sello-foto.test.ts`, y `dibujar-sello.ts` (dibujo sobre el lienzo). Los tipos de `ResultadoGps` se amplían en `foto-utils.ts` (altitud y velocidad en m/s, ambas pueden ser nulas). La ruta de API y `fotos-campo.ts` **no cambian**: solo reciben archivo, descripción, `tomadaEn`, `wbs`, `lat` y `lng`.

### Entorno de trabajo del Paso 2 (por confirmar en T4)

- Capacitor y su plataforma Android se instalan **como dependencias de desarrollo** en la app; versión exacta y requisitos de Node: **por confirmar** (Node 24.18.0 está instalado; el requisito de la versión vigente de Capacitor no se verificó).
- La carpeta `android/` vive **en el repositorio de la app**, en la raíz (lugar por defecto de Capacitor, que exige `package.json` al lado). Se mantiene fuera de Vercel por no ser parte de `next build`; el Worker comprueba que `eslint`, `tsc` y `next build` quedan como estaban (se añade `android/` a los ignorados de ESLint y se verifica que `capacitor.config.ts` no rompe `tsc`).
- `node_modules` de `local-worker-1` y `local-worker-2` son carpetas reales (verificado), no accesos directos; tras ponerlas al día, el Worker git corre la instalación limpia si cambió `package-lock.json` (**por confirmar** si cambió). En worktrees se usa `--webpack` para `dev` y `build` (documento 03 de entorno).
- Puertos de desarrollo: el que fije el Orquestador por Worker; el Paso 2 no necesita servidor local.

## Equipo del plan

Política de modelos de `09-orquestacion-y-modelos.md` (Claude Code): Sonnet para razonar y construir, Haiku solo para lo mecánico, **sin Opus**, esfuerzo medio por defecto.

| Rol | Modelo | Esfuerzo | Sesión o tanda | Rama | Worktree | Estado |
|---|---|---|---|---|---|---|
| Orquestador | Sonnet | Medio (Victor lo subió a alto en su sesión, ver Registro) | todo el plan | `main` | N/A | activo |
| Planner | Sonnet | Medio | pasos 5 y 6 | `main` | N/A | entrega este plan |
| Worker 1 (Paso 1) | Sonnet (parte visual y lógica; no Haiku) | Medio | T1, T2, T3 | `local-worker-1` | `.worktrees/local-worker-1` (autoriza Gate 1) | pendiente |
| Worker 2 (Paso 2) | Sonnet | Medio | T4, T5, T6 | `local-worker-2` | `.worktrees/local-worker-2` (autoriza Gate 1) | pendiente |
| Documentador | Sonnet en T7: integra reglas en flujos existentes (22 y 01), así que no va en Haiku; el Orquestador lo anota aquí | Medio | T7 | `main` (repo de documentos) | N/A | pendiente |
| Worker git | Haiku | Medio | a pedido: poner `local-worker-1` y `-2` al día con `main` antes de T1 y T4 (avance rápido, ambas están 0 commits adelante y 56 y 58 atrás, comprobado); instalación limpia si cambió `package-lock.json`; commits, push y fusión solo con autorización de Victor | opera sobre las demás | | pendiente |
| Auditor | Sonnet | Medio | tras T7 | `main` | N/A | pendiente |

**Ramas y worktrees:** `local-worker-1` y `-2` están limpias y totalmente fusionadas en `main`; `local-worker-3` queda de reserva. **No se tocan** `local-worker-5`, `-6` ni `plan-maestro-tres-paneles` (no libres). `local-worker-1`, `-2` y `-3` existen también en `origin`. `.env.local` se copia del checkout principal al worktree sin leerlo (autorización permanente de Victor, 2026-09-27; el Worker git lo verifica con `cmp` y con `git status`).

**Choque con el otro Orquestador (informes), revisado por archivo en `git log -6 --stat`:** sus últimos commits tocan `BloqueVista.tsx`, `EditorInforme.tsx`, `EditoresBloque.tsx`, `Miniatura.tsx`, `PartesVista.tsx`, `VistaEmitido.tsx`, `cajas-fotos.ts`, `componer-datos.ts` y `exportar/` (`comun.ts`, `pdf.ts`, `word.ts`, `excel.ts`). **Este plan no edita ninguno**: el Paso 1 solo edita `FotoCampo.tsx` y `foto-utils.ts`, y crea archivos nuevos; no toca los exportadores (el sello viaja dentro de la imagen). Riesgo residual bajo: si ese Orquestador cambia `reducir.ts`, `cajas-fotos.ts` o `Miniatura.tsx`, cambia cómo se ve el sello en el informe; el Orquestador de este plan relee `git log` de esos tres archivos antes de T3. El Paso 2 modifica `package.json`, `package-lock.json` y `eslint.config.mjs`, que ese Orquestador toca rara vez; al fusionar se revisa el conflicto.

### Asignación de modelos y esfuerzos por fase (Gate 1)

| Fase | Worker asignado | Modelo | Esfuerzo | Justificación | Aprobación Victor |
|---|---|---|---|---|---|
| T1 a T3 (Paso 1) | Worker 1 | Sonnet | Medio | Lógica de formato y parte visual; ninguna fase pide esfuerzo alto | por aprobar |
| T4 a T6 (Paso 2) | Worker 2 | Sonnet | Medio | Configuración nativa nueva; la prueba de descargas (A-09) es la única con riesgo y se resuelve con un ensayo, no con más esfuerzo | por aprobar |
| T7 | Documentador | Sonnet | Medio | Integra reglas en flujos existentes | por aprobar |
| Auditor | Auditor | Sonnet | Medio | Verifica trazabilidad y evidencia | por aprobar |

El Planner **no propone esfuerzo alto en ninguna fase**; si A-09 (descargas) falla en dos intentos, el Orquestador pide esfuerzo alto puntual a Victor antes de subir.

### Brief de cada Worker

Los briefs (8 KB como máximo, plantilla `13-brief-de-tanda.md`) viven en `2026-10-19-foto-de-campo-con-sello-y-app-android-briefs/`, con un `00-indice-de-tandas.md`. **El Planner no los escribió en este paso**: los escribe el Orquestador o un Planner de briefs por grupo de tandas. Grupos pendientes: (1) briefs de T1, T2 y T3; (2) briefs de T4, T5 y T6; (3) brief de T7. Lo ya verificado para cada brief (contrato técnico) está en esta sección y en «Archivos / componentes afectados».

### Prompt del Auditor

Alcance: Punch List completa de este plan; trazabilidad de las filas RN-1 a RN-4 y de las nuevas contra los flujos 22 y 01 y el documento de compilación; que no se editó ningún permiso, menú ni acceso; que la llave de firma no está en ninguno de los dos repositorios (`git ls-files` y búsqueda de `.jks`, `.keystore` y de contraseñas en el árbol y en el historial de las ramas del plan); que `fotos-campo.ts` y la ruta de API no cambiaron; que los hallazgos del libro se trasladaron. Criterios: sección 6 del estándar. Informe en `04-auditoria/` con el formato `06-informe-auditoria.md`.

## Archivos / componentes afectados

**App `py_control_proyectos_web` (código):**

| Archivo | Cambio | Paso |
|---|---|---|
| `src/components/informes/FotoCampo.tsx` | Lectura de GPS al tocar y al volver; conservar el lienzo reducido; estampar según la casilla; vista previa con sello; enviar lo impreso | 1 |
| `src/components/informes/foto-utils.ts` y `foto-utils.test.ts` | Ampliar `ResultadoGps` (altitud, velocidad); sin romper las pruebas existentes | 1 |
| `src/components/informes/sello-foto.ts` y `sello-foto.test.ts` (nuevos) | Funciones puras del sello y de la lectura | 1 |
| `src/components/informes/dibujar-sello.ts` (nuevo) | Dibujo del sello sobre el lienzo | 1 |
| `package.json`, `package-lock.json`, `capacitor.config.ts` (nuevo), `eslint.config.mjs`, `.gitignore` | Capacitor como dependencia de desarrollo, ignorados de `android/` | 2 |
| `android/` (nueva carpeta) | Proyecto Android generado; permisos, ícono, firma sin secretos y manejo de descargas | 2 |

**No se tocan:** `src/lib/informes/fotos-campo.ts`, la ruta `api/proyectos/[id]/fotos-campo/`, `reducir.ts`, los exportadores, `cajas-fotos.ts`, `Miniatura.tsx`, `middleware.ts` y `next.config.ts` (cabeceras: `camera=()` no afecta a la captura por archivo y `geolocation=(self)` ya permite la ubicación; se comprueba en el celular).

**Documentación (repositorio `pg_control_proyectos`), en T7:** flujo 22 (sección «Foto de campo y banco de fotos» y «Fuera de esta versión»), flujo 01 (nueva sección «App Android»), `01-contexto-repositorio/10-app-android.md` (nuevo: compilación y custodia de la llave; `00-indice.md` de esa carpeta lo enlaza), instructivo de instalación para el equipo.

**Tabla «dice hoy / pasaría a decir» del Spec: confirmada y ampliada.**

| Qué dice hoy | Qué pasaría a decir | Documento |
|---|---|---|
| Las cuatro filas del Spec (foto de campo, fuera de esta versión, «Configuración», `AGENTS.md`) | Sin cambio de fondo; se confirman | flujos 22 y 01, `01-contexto-repositorio/` |
| Flujo 22, «Foto de campo»: «guarda hora y, si el usuario lo permite, GPS» | Se agrega el límite de legibilidad: el sello se lee en 1 y 2 columnas de la hoja; en 3 y 4 columnas es pequeño | flujo 22 (adición) |
| Flujo 22, «Foto de campo»: no dice de dónde viene la foto | Se agrega que la hora y la ubicación del sello son las del teléfono en el momento de elegir la foto, y que sirven como registro operativo, no como prueba contra manipulación | flujo 22 (adición) |
| Flujo 22, «Descarga» | Sin cambio: las fotos incrustadas ya llevan el sello | flujo 22 |
| `design.md` | **No se toca.** El sello no es un componente de pantalla, su estilo queda en el flujo 22 y `design.md` tiene cambios sin commitear de otra sesión | decisión del Planner |

**Aviso, compatibilidad con el flujo 22 (punto a confirmar con Victor en el Gate 1):** el flujo 22 dice en la línea 48 «solo fotos con hora» y en la 60 que la hora ya no sale por defecto en el pie de la foto (Victor, 2026-10-19; es del otro Orquestador y **no se edita aquí**). El sello imprime fecha y hora **dentro de la imagen**: el Planner lo trata como compatible (el pie de la caja no cambia; la hora sale solo en el sello). Queda como una frase de confirmación en la consulta del Gate 1.

**Permisos y conflictos de negocio revisados:** el índice de `04-flujos-de-negocio/README.md` confirma que 14 (accesos), 16 (paneles) y 04 (notificaciones) no se afectan: no cambia ningún permiso, menú, acceso ni pantalla. La matriz de permisos no se toca. `verificar-permisos-por-rol`: **no aplica** (confirmado). Único conflicto de redacción hallado: el de la hora (arriba). Un hueco del Spec resuelto por el Planner: la casilla de GPS aparece después de elegir la foto, así que el sello se genera sobre una copia (regla 1); se registra en el Registro de decisiones.

## Punch List embebida

Gate 1: aprobado el 2026-10-19. Estados: `Sin verificar` / `Conforme` / `Observado` / `No aplica`. La evidencia va a `03-evidencia/` homónima (una captura por ítem como máximo).

### Ítems funcionales

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| S-01 | T1 | Imagen de muestra: el sello (dos variantes, 3 % y 4 %) sobre una foto real, generada con las mismas funciones que usará la app; **PARADA: Victor la ve y elige** | Imagen en la evidencia y visto bueno de Victor registrado en el Registro de decisiones | Conforme |
| S-06 | T2 | Al tocar «Tomar foto» y «Cambiar foto» se inicia una lectura de ubicación; al volver de la cámara se hace otra, con `maximumAge: 0`, en paralelo con la reducción | Prueba con geolocalización falsa inyectada: 1 llamada al tocar y 1 al volver; 0 llamadas al tocar «Guardar foto» | Conforme |
| S-07 | T2 | Regla de elección: gana la lectura al volver; si falla o no llega, vale la del toque; si ninguna sirve, sin coordenadas y con el aviso de hoy | Prueba de la función de elección con los 4 casos | Conforme |
| S-08 | T2 | `FotoCampo.tsx` conserva el lienzo reducido sin sello; el blob final lleva el sello; la vista previa lo muestra y se regenera al cambiar la casilla | Revisión del diff y captura de la vista previa con y sin la casilla | Conforme |
| S-09 | T2 | Lo que se guarda coincide con lo impreso: el `lat` y `lng` enviados son los de la lectura usada en el sello; con la casilla desmarcada no se envían `lat` ni `lng` y el sello no lleva coordenadas | Prueba de la función que arma los datos del sello y del formulario; captura de la solicitud en el navegador emulado | Conforme |
| S-12 | T3 | En el navegador con emulación de celular y ubicación simulada, subir una foto de muestra al campo de archivo: el banco de fotos del servicio de prueba muestra el sello | Captura del banco con las cuatro líneas | Conforme |
| S-17 | T3 | Victor prueba en su celular con cámara real sobre HTTPS y confirma las cuatro líneas correctas (checklist visual preparado por el Worker 1) | Checklist firmado por Victor en el Registro de decisiones | Sin verificar |
| A-02 | T4 | Capacitor configurado: nombre «Control de Proyectos», identificador de paquete aprobado, dirección `https://py-control-proyectos-web.vercel.app` | `capacitor.config.ts` revisado en el diff | Sin verificar |
| A-06 | T4 | APK de depuración compila, se instala en un celular Android y abre `/login` | Captura del celular o del emulador con el login | Sin verificar |
| A-07 | T5 | Se inicia sesión en la app y la sesión se comporta como en el navegador (sigue al cerrar y volver a abrir; cerrar sesión funciona) | Capturas del ingreso y de la reapertura | Sin verificar |
| A-08 | T5 | «Tomar foto» abre la cámara y la ubicación funciona; los permisos se piden una sola vez | Prueba en celular real de Victor (o del equipo), anotada | Sin verificar |
| A-09 | T5 | Los PDF, Word y Excel del informe se descargan al celular y se pueden abrir (riesgo H6: ensayo con dos opciones, ver Riesgos) | Los tres archivos abiertos en el celular, capturas | Sin verificar |
| A-10 | T5 | Sin internet se ve el aviso «Sin conexión», no una página rota; al volver la señal se puede reintentar | Captura en modo avión | Sin verificar |
| A-11 | T5 | El botón Atrás del celular navega dentro de la app y no la cierra de golpe; un enlace a otro sitio no deja al usuario atrapado (**por confirmar** el comportamiento real) | Prueba anotada | Sin verificar |
| A-12 | T5 | Una publicación nueva de la web aparece en la app sin reinstalar (cambio visible hecho a propósito, con permiso de Victor, y revertido) | Dos capturas antes y después | Sin verificar |
| A-16 | T6 | El APK firmado se instala en al menos dos celulares distintos del equipo y muestra la foto con sello (Paso 1 ya desplegado) | Lista de celulares, versión de Android y capturas | Sin verificar |

### Datos y cálculos

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| S-02 | T1 | `formatearSello` cumple el formato: hemisferios N/S/E/O (cuatro combinaciones y el cero); redondeo a 4 decimales; línea de altitud omitida si falta, línea de velocidad omitida si falta (cada una por separado); velocidad 0 sí se imprime (`0.0km/h`); hora de Lima en 24 h con `d/M/aaaa HH:mm`, incluida medianoche (`00:05`) y cambio de día entre UTC y Lima; sin coordenadas, solo la primera línea | `npm test`: casos con valores fijos como `-15.1589`/`-75.0701` da `15.1589S 75.0701W`, y `22/9/2026 14:35` desde `2026-09-22T19:35:00Z` | Conforme |
| S-03 | T1 | `tamanoSello(ancho, alto)` da letra del 3 % del lado mayor (o la elegida en S-01), mínimo 14 px, margen del 2 %, y el bloque no pasa del 40 % del ancho (probado con 1600×1200, 1200×1600 y 1600×900) | `npm test` y el cálculo de la letra equivalente sobre 1000 px | Conforme |
| S-04 | T1 | `dibujarSello` pinta las líneas de abajo hacia arriba, alineadas a la derecha, con contorno y relleno; con la lista vacía no pinta nada | `npm test` con contexto de dibujo simulado (cuenta de llamadas y posición) | Conforme |
| S-05 | T1 | La lectura del teléfono se convierte a datos del sello: velocidad de m/s a km/h con un decimal; `null`, `NaN` o negativos de altitud o velocidad dan línea omitida; altitud negativa válida se imprime | `npm test` | Conforme |

### Permisos

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| P-01 | T3 y T6 | No cambia ningún permiso, menú ni acceso: el diff no toca `src/app/api/`, `middleware.ts` ni la lógica de roles; subir foto sigue siendo de los 4 roles de campo y el banco de los 13 | `git diff --stat` contra `main` de cada rama, sin esas rutas | Conforme (rama local-worker-1; falta repetir en la rama del Paso 2) |

`verificar-permisos-por-rol` no aplica.

### UI / responsive / accesibilidad

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| S-13 | T3 | En el editor, la caja de fotos por defecto (2 columnas, 45 mm de alto, foto sin recortar) y la de 1 columna: el sello se lee; se anota la letra medida en px de pantalla | Captura de la caja al 100 % y la medida | Observado (sello pequeno en la hoja; ver resultados/T3.md) |
| S-14 | T3 | En el PDF del informe (foto reducida a 1000 px, JPEG 70) el sello se lee en 1 y 2 columnas; se anota el equivalente en puntos (referencia: unos 7,7 pt a 3 % con 2 columnas) y el límite en 3 y 4 columnas | Captura de la página del PDF al 100 % | Observado (sello pequeno en la hoja; ver resultados/T3.md) |
| S-15 | T3 | Word y Excel: la foto incrustada trae el sello (solo se comprueba; no se tocan los exportadores) | Una captura de cada uno | Conforme |

### Estados vacío / carga / error

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| S-16 | T3 | Casos límite en el navegador emulado: permiso de ubicación denegado (aviso de hoy, sello con fecha y hora), casilla desmarcada, ubicación sin altitud o sin velocidad, ubicación que tarda más del plazo | Una captura por caso en una sola hoja de evidencia | Conforme |
| S-10 | T2 | La foto con sello sigue pesando 3 MB o menos y 1600 px de lado mayor (la escalera de calidades sigue funcionando); sin migración | Prueba de tamaño con una foto de 12 MP y medida del archivo resultante | Conforme |

### Validación en servidor / API

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| V-01 | T2 y T6 | La ruta de fotos de campo y `fotos-campo.ts` no cambian; las pruebas existentes que validan GPS fuera de rango, tope de 3 MB y descripción obligatoria siguen pasando | `git diff` vacío en esos archivos; `npm test` | Conforme |

### Android (Paso 2)

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| A-01 | T4 | Entorno de compilación comprobado tras instalar Android Studio: Java, SDK y herramientas disponibles; versiones anotadas (**por confirmar**) | Salida de los comandos de versión, sin rutas privadas | Sin verificar |
| A-03 | T4 | Plataforma Android creada en `android/`; `tsc`, lint y `next build` (en el checkout principal) quedan como estaban; `android/` no mete archivos de compilación en git | Salidas de los tres y `git status` | Sin verificar |
| A-04 | T4 | Ícono de la app con el logo de PROMCOSER (`public/logos/promcoser.png`) | Captura del cajón de aplicaciones | Sin verificar |
| A-05 | T4 | Permisos del manifiesto: internet, cámara y ubicación (fina y aproximada) y nada más (**nombres exactos por confirmar** contra la versión instalada) | Diff del manifiesto | Sin verificar |
| A-13 | T6 | Llave de firma generada **con Victor** (él ejecuta el comando guiado; ningún agente ve la clave ni las contraseñas), guardada fuera de los dos repositorios, con una copia de respaldo que Victor define | Victor confirma carpeta y respaldo (sin la ruta en el repositorio) | Sin verificar |
| A-14 | T6 | La configuración de firma lee los datos desde un archivo externo al repositorio; `git ls-files` y la búsqueda de `.jks`, `.keystore` y de contraseñas en el árbol dan cero resultados | Salida de las búsquedas | Sin verificar |
| A-15 | T6 | APK firmado compilado (lo ejecuta Victor guiado, con la llave) y su versión visible en Ajustes de Android | Captura de la información de la app | Sin verificar |
| A-17 | T6 | Borrador técnico en el resumen de cierre: pasos de compilación, versiones usadas, dónde se guarda la llave (sin revelarla), cómo subir de versión | Resumen de cierre de la tanda | Sin verificar |

### Documentación (T7)

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| D-01 | T7 | Flujo 22: lectura de GPS al tomar, sello y su formato, límite de legibilidad, origen de la hora y la ubicación; «fuera de esta versión» con la app Android | Diff del flujo | Sin verificar |
| D-02 | T7 | Flujo 01: sección «App Android» (qué es, abre la app publicada, requiere internet, solo Android, reparto por archivo) | Diff del flujo | Sin verificar |
| D-03 | T7 | `01-contexto-repositorio/10-app-android.md`: compilación, versiones, custodia de la llave, cómo publicar un APK nuevo; enlazado desde `00-indice.md`; si hace falta tocar `AGENTS.md`, va como observación sobre la política | Archivo y diff del índice | Sin verificar |
| D-04 | T7 | Instructivo de instalación para el equipo, en una hoja y en lenguaje simple («instalar apps desconocidas», aviso de seguridad, actualización) | Archivo | Sin verificar |
| D-05 | T7 | Hallazgos trasladados a su destino con el Skill `trasladar-hallazgos` (reglas de negocio ya integradas en los flujos; mejoras; huérfanos reportados) | Libro de hallazgos sin filas en `Registrada` | Sin verificar |
| D-06 | T7 | Coherencia: referencias entre documentos válidas (herramienta de verificación de referencias de `scripts/`, nombre exacto por confirmar en `scripts/README.md`) | Salida de la herramienta | Sin verificar |

### Regresión

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| R-01 | T2, T3 y T6 | `npm test` (vitest) pasa con el mismo número de pruebas previas más las nuevas | Salida con la cuenta de pruebas | Conforme |
| R-02 | T2, T3 y T6 | `tsc` sin errores (**comando exacto por confirmar**: el `package.json` no trae un script de tipos; el Worker usa el que documente el `AGENTS.md` de la app o `npx tsc --noEmit`, lo anota) | Salida | Conforme |
| R-03 | T2, T3 y T6 | `npm run lint` queda igual que en `main` (mismos avisos o ninguno) | Salida comparada con la de `main` | Conforme |
| R-04 | T3 y T6 | `next build` compila: con `--webpack` en el worktree o con el modo normal en el checkout principal | Salida | Conforme |
| R-05 | T3 | Una foto de campo guardada antes de este plan (sin sello) se sigue viendo en el banco y en el informe sin errores | Captura | Conforme |

## Riesgos y bloqueos

Los del Spec (1 a 8) siguen vigentes. Lo que agrega el Planner:

| # | Riesgo o bloqueo | Qué se hace |
|---|---|---|
| R9 | **Descargas en el APK (H6).** Un envoltorio Android no resuelve solo las descargas con cabecera de archivo adjunto. Abrirlas en el navegador del teléfono **no sirve**: no comparte la sesión de la app y daría "sin sesión". | A-09 ensaya dos opciones y registra cuál funcionó (**ambas por comprobar, ninguna verificada**): (A) bajar el archivo desde la propia app con la sesión y guardarlo/abrirlo con complementos de Capacitor; (B) un escuchador de descargas en la parte nativa que usa las cookies de la app. La opción A toca código web de los botones de descarga de informes (archivos que hoy edita el otro Orquestador): si se elige A, se consulta antes al Orquestador y se coordina. |
| R10 | **Sello con una foto que no es del momento.** Si el teléfono deja elegir una foto de la galería, el sello llevaría la hora y el lugar de ahora, no los de la foto. `capture="environment"` lo evita en la mayoría de los Android, pero no se verificó. | Se prueba en celular real (S-17, A-08). Si ocurre, se anota como hallazgo y se decide con Victor; no se resuelve dentro de este plan. |
| R11 | **Vista previa en HTTPS para probar el GPS.** Verificado solo en parte: el historial de despliegues de GitHub muestra despliegues `Preview` ya hechos para commits de ramas de trabajo (por ejemplo el de `local-worker-2`, `7067a79`, del 2026-10-17), así que el alojamiento sí genera vistas previas al subir una rama. **Por confirmar:** si esa vista previa deja iniciar sesión (protección de despliegues de Vercel, usuario y base compartidos con producción). Una vista previa **usa la misma base y el mismo almacenamiento que producción**: las pruebas deben ir contra un servicio de prueba sin alcance real. | Se pide a Victor autorización para subir la rama (consulta del Gate 1). Plan B: si la vista previa no deja iniciar sesión, la prueba en el celular espera a la fusión posterior al Gate 2; no hay fusión anticipada (Victor, 2026-10-19). |
| R12 | **Instalación de Android Studio.** Sin Java ni SDK en esta PC, T4 no arranca. | El Paso 1 no depende de eso; T4 queda en espera. |
| R13 | **Llave de firma.** Si se pierde, los celulares con el APK instalado no se pueden actualizar encima (hay que desinstalar y reinstalar). Si se filtra, otro podría firmar un APK falso. | Se genera con Victor, se guarda fuera de los repositorios, con copia de respaldo; ningún agente la lee. El Auditor revisa que no esté en el historial. |
| R14 | **Datos en el APK.** La dirección, el identificador del paquete y el nombre quedan escritos dentro del APK; cambiarlos exige un APK nuevo para todos. | Se aprueban en el Gate 1 (consulta). |
| R15 | **Inicio de sesión por correo de invitación.** Los enlaces de activación de cuenta (`/auth/activar`) se abren en el navegador del teléfono, no dentro del APK. | Se anota en el instructivo: activar la cuenta en el navegador y luego iniciar sesión en la app. |
| R16 | **Dependencias nuevas en una app que Vercel construye.** Capacitor entra solo como dependencia de desarrollo; si la compilación de Vercel se afecta, se descubre en la vista previa. | R-04 y la vista previa de la rama del Paso 2 antes de fusionar. |

## Consulta única para el Gate 1

El Orquestador la presenta a Victor en lenguaje simple y sin códigos de ítem. Son seis puntos.

1. **Ramas de trabajo:** ¿autoriza reutilizar las carpetas de trabajo `local-worker-1` (para la foto con sello) y `local-worker-2` (para el APK), ya fusionadas y sin cambios, poniéndolas al día con `main`? Con ello también autoriza la copia de `.env.local`, que ya tenía autorizada.
2. **Datos del APK (no se pueden cambiar después sin otro APK):** nombre «Control de Proyectos»; identificador de paquete propuesto `pe.promcoser.controlproyectos` (**propuesta del Planner; el dominio de PROMCOSER no se verificó**, Victor decide); versión mínima de Android: la que fije la plantilla de Capacitor vigente, **por confirmar al instalar** (se espera Android 6 o 7, que cubre los celulares de campo comunes; el Worker informa la cifra exacta y Victor la aprueba antes de compilar).
3. **Datos de prueba y herramientas:** que se use un **servicio de prueba sin alcance real** para subir fotos de muestra, y que se autorice iniciar sesión con las cuentas de prueba (las dos que ya existen) con herramientas de navegador. Las fotos de prueba quedan en la misma base que producción, así que se borran o se dejan identificadas (**Victor decide**; el Worker no borra nada por su cuenta).
4. **Vista previa en HTTPS para probar el GPS en su celular:** ¿autoriza subir la rama de trabajo al repositorio en la nube para que el alojamiento cree una vista previa (hay antecedentes de que lo hace, falta ver si deja iniciar sesión), o prefiere esperar a fusionar con `main` y probar en la dirección real? Subir una rama y fusionarla son acciones que solo hace el Worker git con su autorización.
5. **Esfuerzo:** todo en medio; el Planner no pide esfuerzo alto en ninguna fase. Se vuelve a consultar solo si las descargas del APK fallan dos veces.
6. **Android Studio:** ¿confirma que lo instalará (gratis, guiado) **antes** de la parte del APK? Sin él, solo avanza la foto con sello. Y una frase: ¿confirma que el sello con fecha y hora impresas dentro de la imagen es compatible con la regla de que la hora ya no salga en el pie de la foto en el informe?

Además, Victor debe tener a mano una **foto real de campo** para la imagen de muestra (su foto de ejemplo con el sello de cuatro líneas sirve de referencia visual; si no la aporta, el Worker usa una foto del repositorio de apoyo, **por confirmar** cuál sirve; en `06-material-de-apoyo` solo hay imágenes de interfaz).


## Registro de decisiones

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-10-19 | iPhone queda fuera por ahora; todo es Android | Victor |
| 2026-10-19 | Sin tienda: el APK se reparte por archivo al equipo | Victor |
| 2026-10-19 | Sin internet no se usa la app: no hay cola de fotos sin señal | Victor |
| 2026-10-19 | El sello es como su foto de ejemplo, con la hora en la misma fila de la fecha | Victor |
| 2026-10-19 | Orden de trabajo: primero la foto con sello, después el APK | Victor (aprobó el orden al pedir el Spec) |
| 2026-10-19 | Hora de Lima en 24 h, nombre «Control de Proyectos», casilla de GPS se mantiene, coordenadas se guardan como hoy | Orquestador |
| 2026-10-19 | Gate Spec aprobado; el APK abre `https://py-control-proyectos-web.vercel.app` | Victor («OK, DALE») |
| 2026-10-19 | Esfuerzo de la sesión del Orquestador en «alto» (`/effort`), aunque la política dice «medio»; los subagentes siguen en medio salvo orden distinta | Victor |
| 2026-10-19 | El sello no se imprime al reducir sino sobre una copia del lienzo reducido, porque la casilla de GPS aparece después de elegir la foto (hueco del Spec resuelto sin cambiar su intención) | Planner |
| 2026-10-19 | La lectura de ubicación se hace al tocar «Tomar foto» y al volver de la cámara; gana la de al volver, y lo guardado coincide con lo impreso | Planner (aplica RN-2) |
| 2026-10-19 | Tamaño inicial del sello 3 % del lado mayor, con muestra de 3 % y 4 % para que Victor elija; `design.md` no se toca | Planner |
| 2026-10-19 | El sello (fecha y hora dentro de la imagen) se trata como compatible con la regla de la hora fuera del pie del flujo 22; se confirma con Victor en el Gate 1 | Planner (por confirmar) |
| 2026-10-19 | `android/` vive en la raíz del repositorio de la app; Capacitor como dependencia de desarrollo; llave de firma fuera de los repositorios | Planner (se aprueba en Gate 1) |
| 2026-10-19 | **Gate 1 aprobado** con las recomendaciones de la consulta única: reutilizar `local-worker-1` y `local-worker-2` (y la copia de `.env.local`); servicio de prueba sin alcance real y las dos cuentas de prueba; vista previa de la rama para probar el GPS; todo en esfuerzo medio; el sello es compatible con la hora fuera del pie | Victor («aprobado») |
| 2026-10-19 | Esta sesión avanza solo hasta el Paso 1 (T1 a T3). Quedan pendientes para el Paso 2: identificador del paquete, versión mínima de Android e instalación de Android Studio | Victor («en esta sesión avanzamos solo hasta el paso 1») |
| 2026-10-19 | **Sin fusión a `main` antes del Gate 2.** Se corrigieron la ola 4 y el plan B de la vista previa; la actualización automática del APK (A-12 y A-16) se verifica después de la fusión | Orquestador (la regla del flujo lo exige; Victor lo aprueba al aprobar el plan) |
| 2026-10-19 | Sello: tamano 3 %, y IDENTICO a su foto de referencia (Roboto peso normal, sombra suave sin contorno, interlineado apretado, pegado a la esquina); Roboto se carga en la app con next/font para que salga igual en todos los celulares | Victor («de 3 % ... tal cual la imagen», «esta bien continua») |
| 2026-10-19 | **Sello definitivo = `muestra-sello-v2-3pct.jpg`** (3 %, estilo de su referencia). Victor la vio y confirmó: «es la que queda». Cierra S-01 y la parada de T1. El sello pequeño en la hoja del PDF (≈ 5 pt, S-13 y S-14) queda como límite conocido, sin cambiar el tamaño | Victor |
| 2026-10-19 | **Prueba en celular real: el GPS no funcionó** (vista previa de la rama `local-worker-1`, commit `0d53c5b`, probada por Victor). Queda **pendiente**: no se diagnosticó (falta saber qué vio: sin permiso, aviso de ubicación, sello sin coordenadas u otra cosa). S-17 sigue `Sin verificar`; Victor pausa este plan para atender otra observación de la app. La rama está subida a `origin/local-worker-1` y no se fusiona antes del Gate 2 | Victor |
| 2026-10-19 | Autoriza usar su cuenta de prueba para el navegador; el servicio de prueba esta en el «Portafolio Practica» (PS-0000, programa Promcoser), no en el portafolio por defecto | Victor |
| 2026-10-19 | La foto de ejemplo de Victor (sello abajo a la derecha: `22/9/2026`, coordenadas, `Altitud:` y `Velocidad:`) es la referencia visual. Victor pidió solo agregar la hora después de la fecha, en la misma fila | Victor |

## Enlaces a progreso y evidencia homónimos

Se crean al pasar el Gate 1, con los nombres homónimos de este plan:

- Progreso: `02-trabajo-activo/02-progreso/2026-10-19-foto-de-campo-con-sello-y-app-android.md`
- Evidencia: `02-trabajo-activo/03-evidencia/2026-10-19-foto-de-campo-con-sello-y-app-android/`
- Briefs: `02-trabajo-activo/01-planes/2026-10-19-foto-de-campo-con-sello-y-app-android-briefs/` (por escribir)
- Auditoría: `02-trabajo-activo/04-auditoria/2026-10-19-foto-de-campo-con-sello-y-app-android.md`

## Libro de hallazgos

Un hallazgo se anota en el momento en que ocurre, no al cerrar.

| ID | Fecha | Quién (rol, tanda) | Qué | Destino propuesto | Estado | Enlace al destino |
|---|---|---|---|---|---|---|

### Mejoras (de trabajo)

Ninguna.

### Reglas de negocio acordadas en esta tarea

| ID | Fecha | Quién (rol, tanda) | Qué | Destino propuesto | Estado | Enlace al destino |
|---|---|---|---|---|---|---|
| RN-1 | 2026-10-19 | Orquestador, con Victor | La foto de campo lleva impreso un sello con fecha y hora de Lima, coordenadas, altitud y velocidad (las dos últimas solo si el celular las entrega) | Flujo 22, «Foto de campo y banco de fotos» | Registrada | |
| RN-2 | 2026-10-19 | Orquestador, con Victor | La ubicación se lee al tomar la foto, no al guardarla | Flujo 22 | Registrada | |
| RN-3 | 2026-10-19 | Orquestador, con Victor | La app Android abre la app publicada y requiere internet; sin señal no se usa | Flujo 01 (sección «App Android») y flujo 22 | Registrada | |
| RN-4 | 2026-10-19 | Orquestador, con Victor | Solo Android y reparto por archivo; iPhone y tiendas quedan fuera por ahora | Flujo 01 | Registrada | |

### Observaciones sobre la política

Ninguna.

### Carpetas/archivos huérfanos

Ninguna.

## Informe de Auditoría

Pendiente. Se enlaza aquí cuando exista en `02-trabajo-activo/04-auditoria/`.

## Mensaje de cierre

Pendiente.

## Elementos postergados propuestos para planes futuros

- App para iPhone (necesita la cuenta de Apple Developer y compilación en un Mac o en la nube).
- Publicación en Play Store con prueba interna, para que el envoltorio también se actualice solo.
- Fotos sin señal con subida posterior, si Victor cambia de opinión.
- Sello legible en 3 y 4 columnas de la hoja del informe (hoy es un límite conocido); sello con hora y lugar del archivo cuando la foto venga de la galería (riesgo R10).

## Handoff — 2026-10-19 (relevo del Orquestador)

Aún no hay archivo de progreso: el plan sigue en el Spec, sin subagentes lanzados. El handoff va aquí por eso.

### Fecha

2026-10-19.

### Objetivo y estado

Foto de campo con sello (Paso 1) y APK Android (Paso 2). **Spec propuesto; Gate Spec pendiente de Victor.** Única decisión abierta que él debe contestar: qué dirección abre el APK (recomendada: `https://py-control-proyectos-web.vercel.app`, responde 200 en `/login`).

### Plan / progreso / evidencia relacionados

Este plan. Informe de consumo y política recalibrada: `../05-eficiencia/2026-10-19-consumo-de-tokens-del-flujo.md`.

### Rama, worktree y último commit

- Repo de documentos: `main`, sincronizado con `origin/main` (0 0) tras el commit `ee2a6b1` (política de modelos); el commit de este handoff va encima. Hay 22 archivos sin commitear de sesiones anteriores que **no son de este plan** (no tocarlos).
- Repo de la app: `main` en `1919fba`, sincronizado (0 0). **El Spec dice `0b9961a`: avanzó con dos commits del Lote 5 de informes** (`017806f` y `1919fba`, este último con la hora fuera del pie de fotos). Hay que releer `FotoCampo.tsx` y la generación del informe antes de que el Planner fije el alcance. `db/095_cerrar_lectura_directa.sql` sin seguimiento no es de este plan.
- Sin worktrees creados ni autorizados.

### Terminado

Spec escrito y subido. Informe de consumo de tokens. Política recalibrada y subida: relevo del Orquestador a 200k, Planner con metas de Worker, tope de salida de herramientas para el Orquestador, declarar modelo al activar el flujo. Decisiones de Victor del 2026-10-19: Documentador en Haiku por defecto; documentos de modelos pasados a Claude Code (opencode queda como referencia); compactación a 250k aplicada por él; diez skills de redes sociales apagados en este proyecto (`.claude/settings.local.json`).

### No terminado

Gate Spec. Después: Planner (pasos 5 y 6) → plan y Punch List → Gate 1 → Workers → Documentador → Auditor → Gate 2 → cierre.

### Pruebas ejecutadas

Ninguna de código. Verificado con comandos: ramas y sincronía de ambos repositorios, `/login` en 200, `skillOverrides` presente en el ejecutable de Claude Code.

### Bloqueos y riesgos

- Gate 1 debe pedir: reutilizar los worktrees `local-worker-1` (Paso 1) y `local-worker-2` (Paso 2), nombre, identificador y versión mínima de Android del APK, y los datos de prueba.
- Victor debe instalar Android Studio antes del Paso 2 (no hay Java ni SDK en su PC).
- Corre otro Orquestador en paralelo (sesión `2470d4f3`, Lote de informes): no editar sus archivos ni los del repo de la app sin verificar.
- Los skills de redes sociales están en `off`, pero la documentación consultada dice que escribir el comando a mano aún podría ejecutarlos; comprobar en la sesión nueva que ya no aparecen en el listado.
- Observación para Victor (no es de este plan): su configuración de usuario tiene el esfuerzo en `xhigh` para Sonnet 5.5 (y `high` general), mientras la política dice esfuerzo medio. No se tocó.
- Orquestador saliente: sesión `ab0aaa6e`, 62 llamadas, 10,25 M de caché leída, contexto máximo 297k (pasó la red de seguridad de 250k).

### Qué debe leer el siguiente agente

`AGENTS.md`; `docs/00-estandar-agentes/04-flujo-sdd-y-planes.md`; `08-medicion-y-relevo.md`; el Skill `seguir-flujo-de-planes`; este plan (el Spec); del índice de flujos, solo el 01 y el 22; `09-orquestacion-y-modelos.md` (tabla de Claude Code). Confirmar el estado con `git status` y `git rev-list --left-right --count origin/<rama>...<rama>` en ambos repositorios antes de actuar.

### Próximo paso concreto

Declarar modelo y esfuerzo de la sesión, decir en qué paso está el flujo y pedir a Victor el Gate Spec (aprobar el Spec y contestar la dirección del APK). Si aprueba, lanzar el Planner en Sonnet con las metas de 08 (80 llamadas, 200k).
