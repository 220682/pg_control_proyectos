# RDT: validación opcional, editar validados, cargos del presupuesto y Tecnet sin paquetes

Fecha: 2026-11-06. Estado: `Implementando` (código en `main` y verificado en producción; db/138 aplicada por Victor; falta que Victor actualice la Matriz de permisos y revise).

Lote de trabajo tradicional por orden directa de Victor. No siguió el flujo con Orquestador ni tuvo Gates.

## Objetivo, alcance y no alcance

- **Resultado esperado:** (a) un cargo no sale dos veces con nombres parecidos en el RDT; (b) el informe y el Dashboard dan el mismo avance; (c) cada servicio elige si sus RDT necesitan validación; (d) un RDT validado se puede editar; (e) Tecnet (PS-167) deja de trabajar por paquetes y no tiene partidas transversales.
- **Alcance:** Crear RDT y Status de RDTs, bloque «Avance por nivel» de los informes, Plan Maestro (versión «Sin paquetes»), flujos 06, 14, 20 y 22.
- **No alcance:** los 14 RDT validados de Tecnet se quedan como están (Victor).

## Repositorios

| Repositorio | Commit | Estado |
|---|---|---|
| `py_control_proyectos_web` | `0739b8e`, `6760750`, `f25cf50`, `dacd550` | en `main` (Vercel) |
| `pg_control_proyectos` | `d513467`, `1ecfad5`, `ceb3d57` y este commit | flujos 06, 14, 20, 22, 26 y este plan |

## Avance

- [x] **Causa del cargo doble** (datos reales, solo lectura): las plantillas de RDT de PS-108 tenían el nombre antiguo del catálogo («SUPERVISOR DE CALIDAD»); el RDT del 05-11 salió de una plantilla y luego se volvió a agregar a la misma persona desde la lista, que propone el nombre del presupuesto («INGENIERO DE CALIDAD»). El servidor solo exigía que hubiera tarifa: no renombraba ni impedía repetir a la persona.
- [x] El servidor guarda cada cargo con el nombre del presupuesto; el formulario hace lo mismo al cargar plantillas y borradores; una persona repetida se rechaza en el formulario y en el servidor (`PERSONA_REPETIDA`).
- [x] **Causa del 8.69 % contra 8.76 %:** el chip «Avance medio» del informe era un promedio simple de las filas de «Avance por nivel»; el Dashboard pondera por presupuesto. Se quitó y se agregó la fila «Total del servicio» (EV/BAC = 8.76 % en PS-108).
- [x] «Avance por nivel» en cuatro opciones: metrado por subpresupuesto, metrado completo, HH por subpresupuesto, HH completo. Subpresupuesto y nivel con unidades mezcladas solo muestran avance; todo nivel en negrita.
- [x] Interruptor por servicio «el RDT necesita validación» (admin y JP; por defecto «Sí»; migración `db/138` sin aplicar).
- [x] Editar un RDT validado (admin y JP): motivo, historial, sigue validado, recalcula el Consolidado.
- [x] Plan Maestro: versión «Sin paquetes»; al aprobarla se archivan los paquetes sin uso; cada línea hereda la disciplina de su paquete.
- [x] Tecnet PS-167: versión 4 «Sin paquetes» creada y aprobada (desde la app local, contra la base real).
- [x] Flujos 06, 14, 20 y 22 actualizados.
- [x] Victor aplicó db/138 (todos los servicios en «Sí»). Verificado en producción: interruptor activo y lápiz en Status de RDTs; informe ID-2 con «Total del servicio» 8.76 % y una sola fila de INGENIERO DE CALIDAD.
- [x] Por orden de Victor: borrada la fila repetida de Aquino (RDT de PS-108 del 05-11, la del nombre antiguo, 10 h MOI), con su foto en el historial del RDT (acción CORRECCION y motivo).
- [x] Cargos antiguos pasados al nombre del presupuesto con la misma función del servidor: 174 filas de RDT (PS-108 y PS-131), las 3 plantillas de RDT que existen (de todos los usuarios) y 0 borradores. Consolidado recalculado en los dos servicios: solo cambió lo esperado (HH indirectas de PS-108 de 620 a 610; metrado, HH directas y costo iguales). Revisión final de todos los RDT: 0 personas repetidas y 0 cargos fuera del presupuesto en PS-108, PS-131 y PS-167. Respaldo previo en el equipo local (carpeta temporal de la sesión; no se sube al repositorio porque lleva nombres y DNI).
- [x] **Tanda 3 (Victor, 2026-11-06):** «Avance por nivel» completo cortado por subpresupuesto (cada trozo con su encabezado, entero en la hoja; tope de 32 filas cortando en un nivel), en vista previa y PDF; botón «Elegir de la galería o de WhatsApp» en el selector de la caja (Victor aclaró que basta elegir la foto desde la carpeta de WhatsApp del celular, sin traer los grupos al sistema); filas y alto de las cajas de fotos editables en el celular; emojis fuera del PDF. Flujo 22 actualizado. Sin cambio de permisos (la Matriz no cambia por esta tanda).
- [x] **Tecnet sin transversales (Victor, 2026-11-07: «todas las partidas normales, no quiero nada de eso»):** la v4 había dejado 1.1 Movilización, 1.2 Seguridad y señalización y 4.1 Supervisión como transversales. Desde la app local contra la base real: marcas quitadas; cada una ligada a su actividad del cronograma (2, 3 y 17) con su metrado contractual; versión 5 «Sin paquetes» creada y aprobada con las 12 partidas normales; su programación repartida por igual en los días de trabajo (lunes a sábado) de su actividad (1.1: 2 viajes el 19 y 2 el 20/10; 1.2 y 4.1 en los 30 días del servicio); disciplina Preliminares (1.1, 1.2) y Civil (4.1).
- [x] **Tanda 4 (Victor, 2026-11-06):** «Elegir de un chat de WhatsApp» en el selector de la caja: grupos y contactos con fotos del último mes, fotos por día, la elegida entra al banco y a la caja. Visor local `scripts/whatsapp/visor_fotos.py` (solo 127.0.0.1 y solo responde a la app) e instalador `instalar-visor.ps1`. Flujos 22 y 26 actualizados. Sin cambio de permisos (usa el de subir foto).
- [x] **Cambio de proveedor a Google Cloud Run (Victor, 2026-11-07: Vercel gratis pausó la app por consumo; «no voy a pagar»):** imagen Docker de la app y script `scripts/despliegue/publicar-cloud-run.ps1` (proyecto `control-proyectos-promcoser`, us-east1, 0 a 3 instancias, alerta de gasto de 4 soles). Dirección nueva: https://control-proyectos-917220987246.us-east1.run.app. Claves nuevas de Cloudflare (solo el almacén `controldeproyectos`) y de Gmail (segundo secreto del cliente «Estado del servicio» y su dirección de retorno); Site URL y direcciones permitidas de Supabase Auth; lectura de correos (GitHub) y visor de fotos apuntan a la dirección nueva. Flujo 07 actualizado.

## Evidencia

- Tecnet sin transversales: 0 marcadas y 0 en la foto de la v5; las 12 partidas programadas al 100 % de su metrado; las 9 de antes con la misma programación (215 combinaciones, 0 diferencias); el catálogo del RDT lista las 12. Curva S al 07-11, antes → después: PV 24,850.33 → 25,530.88, EV 7,582.46 → 5,400.70, AC 14,357.91 → 12,227.12 (sale lo que antes se estimaba para las tres con el % físico); PV total 39,930.56 sin cambio. Respaldo previo en la carpeta temporal de la sesión.
- Tanda 4: tipos y lint limpios, 2726 pruebas de la app y 15 del script de WhatsApp pasan. Con los datos reales: 70 chats con fotos del último mes (29 grupos); en la app local se abrió «Villa Fase 2», el día más reciente mostró sus 31 fotos con hora y autor, y al elegir una quedó en la caja 1 («Figura N°01») y en el banco. Esa foto de prueba se quitó de la caja y se borró (registro y archivo) con la misma app; el informe quedó como estaba.
- Tanda 3: tipos y lint limpios, 2722 pruebas pasan; vista previa (1366 px) y PDF de `PS-108-2026-ID-2` en «Metrado completo»: 5 hojas, cada subpresupuesto con su encabezado y ninguno partido a media hoja; el modo del bloque se devolvió a «Metrado por subpresupuesto». Selector a 390 px: el botón abre el explorador de archivos (no se subió foto de prueba para no dejar registros en la base real).
- Tipos limpios; 2716 pruebas pasan (una corrida tuvo 2 fallos intermitentes que no se repitieron); lint sin errores nuevos (los 8 que salen son de archivos no tocados).
- Pantalla (Playwright, 1366 px): Status de RDTs con el interruptor (deshabilitado hasta db/138) y el lápiz en filas validadas; informe `PS-108-2026-ID-2` con «Metrado por subpresupuesto» (1: 8.76 %, 2: 0.29 %, 3: 0.00 %, 4: 55.69 %, total 8.76 %; coincide con el Consolidado) y «Metrado completo» con niveles en negrita. El modo del bloque se devolvió a como estaba.
- Tecnet: v4 con 58 líneas, 0 de paquete, 9 partidas; PV por partida y fecha igual a v3 (215 combinaciones, 0 diferencias); Consolidado igual antes y después; 14 RDT reposicionados; 8 paquetes archivados; el catálogo del RDT lista las 9 partidas directas con el acumulado del Consolidado.
- Cloud Run (2026-11-08): la app responde, sin errores en los registros; Cloudflare probado (subir y borrar un archivo). Prueba completa en la app publicada, en Tecnet PS-167 con el 04-11: RDT creado desde el formulario (borrador → enviar, 8 personas, 80 HH, partida 2.3), validado en Status de RDTs, visto en el Dashboard (HH reales 850 → 930) y en un informe diario nuevo (2 actividades 0.34 y 3.50 ml, 8 personas, 80 HH). Después se borraron el informe, el RDT, su borrador y sus 3 avisos: el Dashboard volvió a HH 177 / 850, EV 5,400.70 y AC 12,227.12, igual a la Curva S tras la v5 (antes de la prueba el Dashboard aún mostraba 7,582.46 y 14,357.91: no se había recalculado al aprobar la v5; la validación lo recalculó).

## Pendientes

1. Victor actualiza la Matriz de permisos con las dos filas nuevas del flujo 14.
2. Título del bloque del informe `PS-108-2026-ID-2`: dice «Avance por nivelñ» (ya estaba así guardado; lo corrige Victor si quiere).
3. Victor revisa en producción.
4. Victor corre una vez `scripts/whatsapp/instalar-visor.ps1` (enciende el visor de fotos con el puente al entrar a Windows y cada hora si se cayó). El agente no pudo hacerlo: cambiar lo que arranca con Windows quedó bloqueado por seguridad.
5. En los RDT de Tecnet se reporta el avance de 1.1, 1.2 y 4.1 (ya no se calcula solo): hasta entonces su avance ganado es 0.
6. Victor vuelve a conectar Gmail en la app nueva (Gestión de interesados). El correo al equipo con la dirección nueva (redactado, 9 personas sin las cuentas de Victor ni las de prueba) queda en pausa por decisión de Victor (2026-11-08) hasta que diga «envíalo».
7. Aprobar una versión del Plan Maestro no recalcula el Dashboard de inmediato (Tecnet mostró los valores de antes de la v5 hasta que se validó un RDT): revisar si al aprobar se debe recalcular el Consolidado.
8. ~~Braulio Huamán Díaz no aparecía en la lista de personal del RDT~~ — estaba desactivado en Recursos › Personal (la app no guarda quién ni cuándo). Por orden de Victor (2026-11-08) se activaron Braulio (cargo SUPERVISOR OPERATIVO), Ciro Calachihua y Cayo Gutiérrez Juan Wilfredo; Abran Castro sigue desactivado (ya no trabaja). Verificado: los tres salen en la lista del formulario.

## Mejoras (de trabajo)

Trasladadas el 2026-11-08 a [`03-aprendizaje-continuo/2026-11-08-cambio-a-cloud-run-y-aprendizajes-del-plan-rdt.md`](../../03-aprendizaje-continuo/2026-11-08-cambio-a-cloud-run-y-aprendizajes-del-plan-rdt.md).

- Con mensajes dictados por voz que no se entienden del todo, mirar primero la captura que manda Victor (qué pantalla y qué equipo) antes de construir: la primera lectura («la galería del celular») no era lo que pedía (sus chats de WhatsApp en la PC).
- Lo que arranca con Windows (accesos de Inicio, scripts que corren al iniciar) no lo cambia el agente: se entrega un instalador en la app y Victor lo corre.

- Antes de aprobar un Plan Maestro desde la app, guardar el PV por partida y fecha y el Consolidado, y compararlos después: así se demuestra que la versión nueva no cambió nada que no debía.
- Vercel no entrega sus variables secretas (salen como «[SENSITIVE]»): al cambiar de proveedor, las claves se sacan nuevas en cada servicio (Cloudflare, Google) y se guardan solo en el equipo de Victor, fuera de los repositorios.
- Al publicar desde la carpeta de la app, excluir `.worktrees/`: con ella la subida pesaba 192 MB y 33 mil archivos y se trababa.

## Reglas de negocio acordadas en esta tarea

Integradas en los flujos: dónde vive la app y sus direcciones (07), validación opcional por servicio y edición de RDT validado (06, 14), cargo con nombre del presupuesto y persona no repetida (06), versión «Sin paquetes» del Plan Maestro (20, 14), «Avance por nivel» en cuatro opciones con total del servicio (22).

## Observaciones sobre la política

- Ninguna.

## Carpetas/archivos huérfanos

- Los mismos del plan [Informes: Avance por nivel completo](2026-11-06-informes-avance-completo-y-plantilla-promcoser.md); ninguno nuevo. Sin borrar.
