# Foto de campo con sello y app Android

## Identificación y estado

- Tema: que cada foto de campo salga con su fecha, hora y ubicación impresas sobre la imagen, y que la app se pueda instalar en los celulares Android del equipo como un archivo APK, sin tienda.
- Fecha de inicio: 2026-10-19.
- Estado: `Propuesta` (Spec redactado por el Orquestador el 2026-10-19; falta el Gate Spec).

Puertas:

- Gate Spec: `pendiente`
- Gate 1: `pendiente`
- Gate 2: `pendiente`

## Spec

### Estado

`Propuesto`.

### Problema y contexto

Victor quiere llevar la app al celular, solo Android por ahora (decidido el 2026-10-19: iPhone queda fuera). El uso principal en campo es la **Foto de campo** del flujo 22, y Victor pidió que la foto muestre sus datos de ubicación, como las fotos de obra con sello. Su ejemplo (una foto con cuatro líneas abajo a la derecha) trae: fecha, coordenadas, altitud y velocidad. Pidió **agregar la hora en la misma fila de la fecha**.

Lo que se verificó en el código (`py_control_proyectos_web`, `main` en `0b9961a`, 2026-10-19):

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

**Decisión pendiente con Victor (una):**

- **¿Qué dirección debe abrir el APK?** Recomendación: la actual (`py-control-proyectos-web.vercel.app`). Si Victor piensa tener una dirección propia, debe decirlo antes de repartir el APK.

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

- [ ] El Responsable humano aprueba este Spec.

## Referencia al Spec aprobado

Pendiente del Gate Spec.

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

Las define el Planner. Propuesta del Orquestador: dos carriles independientes (el Paso 1 toca `FotoCampo.tsx` y `foto-utils.ts`; el Paso 2 agrega el envoltorio y no toca esos archivos). El Paso 2 empieza cuando Victor instale Android Studio.

## Equipo del plan

A cargo del Planner, según la política de modelos del repositorio (sin Opus). Equipo por defecto: Orquestador, Planner, hasta dos Workers de código, Documentador, Worker git y Auditor.

## Archivos / componentes afectados

Los lista el Planner. Previstos: `src/components/informes/FotoCampo.tsx`, `src/components/informes/foto-utils.ts` y sus pruebas (Paso 1); configuración y carpeta del envoltorio Android (Paso 2); flujos 22 y 01.

## Punch List embebida

Pendiente del Planner.

## Riesgos y bloqueos

Ver «Riesgos y decisiones pendientes» del Spec.

## Registro de decisiones

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-10-19 | iPhone queda fuera por ahora; todo es Android | Victor |
| 2026-10-19 | Sin tienda: el APK se reparte por archivo al equipo | Victor |
| 2026-10-19 | Sin internet no se usa la app: no hay cola de fotos sin señal | Victor |
| 2026-10-19 | El sello es como su foto de ejemplo, con la hora en la misma fila de la fecha | Victor |
| 2026-10-19 | Orden de trabajo: primero la foto con sello, después el APK | Victor (aprobó el orden al pedir el Spec) |
| 2026-10-19 | Hora de Lima en 24 h, nombre «Control de Proyectos», casilla de GPS se mantiene, coordenadas se guardan como hoy | Orquestador |

## Enlaces a progreso y evidencia homónimos

Se crean al pasar el Gate 1.

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
