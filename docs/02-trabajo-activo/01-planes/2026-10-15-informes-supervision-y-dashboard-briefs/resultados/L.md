# Resultado tanda L (Worker 3) — verificación en vivo

Rama `local-worker-3` en eeaacd1 (build propio, app en :3013). Sin cambios de código ni commits. Sesión de administrador iniciada por Victor; 13 roles con `ver-como`. Servicio de prueba: PS-0000 «SERVICIO PRUEBA MARCOBRE 2026-10-07-19-33» (proyecto 0a20df2f-c5e9-4296-9c08-f89af499182d, portafolio Practica). Lecturas de solo lectura previas en JAHUAY (12101b3d).
Capturas: `docs/02-trabajo-activo/03-evidencia/capturas/2026-10-15-informes-supervision-y-dashboard/L/`.

## 1. Estado de los ítems
| ID | Estado | Evidencia / causa |
|---|---|---|
| L1 | Observado (parcial, 13 roles conformes) | Tabla de abajo. No se pudo observar «borrador ajeno = 404»: `ver-como` (rol o usuario) conserva el id del administrador, así que el borrador siempre es «propio». Falta una segunda cuenta real (Victor). |
| L2 | Observado | Hecho: diario Técnico (UI), semanal Técnico con 6 fotos (UI), COSTOS y PERSONALIZADO (API), emitir, versión 2, 409. No hecho: recorrido visual con la segunda cuenta; Ejecutivo y Fotográfico como formato no se crearon; B y C verificadas solo por las rutas (listado, detalle, datos en vivo). |
| L3 | Conforme (390 px) | Listado, nuevo, editor, emitido, foto, Dashboard, PR: `scrollWidth` = 390 en todas; capturas `L3-*-390.png`. Tabla del listado con scroll propio. |
| L4 | Conforme con defectos (abajo) | 18 archivos abiertos (PDF con PyMuPDF y render, Word con python-docx, Excel con openpyxl). Sin dinero en ningún byte salvo en COSTOS. Peso: ver §5. |
| L5 | Conforme (con una duda en 102) | Se comprobó con la app: crear informe y código `PS-0000-ID-n` (098/099), emitir, versión 2, trigger de inmutabilidad (409), foto de campo, pestaña Inasistencias con dato (099 y la 100/101: columnas HH extra y HM stand-by en vista previa). Duda: el AC de la Curva S no cuadra (L7), que puede ser la función SQL de la 102 no aplicada o una diferencia de regla; `db/pruebas/102_comparacion_ac.sql` lo resuelve. |
| L6 | Lista para Victor (abajo) | |
| L7 | Observado | AC PR = AC Dashboard = AC Costos = US$ 93,944.55 al corte 15-10 y 17-10; AC Curva S = 97,215.06. Subcontrato manual y materiales: no probados (servicio sin subcontratos). |

## 2. Tabla esperado / observado (API sin efecto, 13 roles) — todo coincide con lo esperado
| Rol | Listar, ver detalle, descargar (no COSTOS), Inasistencias, GET fotos | Crear informe y foto | Crear / ver / descargar COSTOS | Nueva versión |
|---|---|---|---|---|
| administrador | 200 | sí (400 por periodo en la prueba) | sí / sí / sí | 201 |
| jefe_de_proyectos | 200 | sí | sí / sí / sí | llega al guardia (409 por borrador ya existente) |
| jefe_de_oficina_tecnica | 200 | sí | sí / sí / sí | 409 (guardia pasa) |
| supervisor_operativo | 200 | sí | 403 / 403 / 403 | 409 (guardia pasa) |
| supervisor_costos, jefe_de_costos | 200 | 403 (foto 403, informes no COSTOS 403) | crear COSTOS sí; ver y descargar sí | 403 |
| supervisor_oficina_tecnica, planner, supervisor_logistica, supervisor_administracion, supervisor_ssoma, asistente, rrhh | 200 | 403 | 403 / 403 / 403 (también por URL directa) | 403 |
Además: informe inexistente = 404; emitido editado = 409 (v1 y v2); v1 pasó a REEMPLAZADO; con `ver-como` de usuario sin alcance sobre PS-0000 todo da 403 (alcance, no rol). La lista oculta el COSTOS a los 8 roles sin economía.
Paginas listado, nuevo y foto: 200 en los 13 roles (por fetch; la vista que ve cada rol en pantalla queda sin revisar).

## 3. Defectos y hallazgos (devueltos, ninguno corregido)
1. **AC de la Curva S distinto** (W2, SQL/102): serie al 15-10 = 97,215.06 contra 93,944.55 del PR, Dashboard y Costos (diferencia 3,270.51; también la serie diaria al 07-08: 3,336.65 contra 3,235.68 de la partida 1.1.1). El PR, el Dashboard y Costos coinciden entre sí.
2. **Marca BORRADOR en el PDF** (W1, G): el texto de la diagonal se parte en «BORRAD / OR». Cosmético.
3. **Alcance «fotos» del PDF**: la primera página queda casi vacía (solo Datos del servicio) y las fotos apaisadas ocupan celdas altas con mucho blanco. Cosmético (W1, G).
4. **Vista previa y emitido** (W3, F, no corregido por tiempo): las tablas usan el orden de claves del JSON («Wbs, Orden, Turno, Unidad, Etiqueta, Validado…») y etiquetas tipo «Hh Reales»; el PDF las ordena bien. Mejora: ordenar columnas.
5. **Efecto no buscado**: la sonda «nueva versión» como administrador creó el borrador v3 de PS-0000-ID-1 (ver §4).
6. **Foto de campo con GPS marcado**: en escritorio sin permiso de ubicación el envío tarda ~10 s («Enviando…»). Para L6.
7. Texto del PR: «materiales y subcontratos se miden por % de avance económico, no por costo capturado (regla 5)» contradice el otro texto «el monto ingresado suma al AC». Para el Documentador.
8. Los diarios sin partida muestran Personal con HH 0 y Costos con «Personal valorizado» vacío: dato de prueba, no defecto.

## 4. Datos de prueba creados (todos en PS-0000; desactivar después)
- Fotos de campo (6), «PRUEBA foto de campo 1..6», 17-10-2026 00:08-00:09 Lima; JPEG sintéticos de ruido (4000x3000, peor caso), no fotos reales de campo; ya reducidas a 1600 px (~270-290 KB c/u), sin GPS (la 1 con intento de GPS).
- PS-0000-ID-1: v1 Técnico diario 15-10 (REEMPLAZADO), v2 EMITIDO, v3 BORRADOR (por efecto no buscado). Título del bloque 1 «PRUEBA Datos del servicio». id v1 999368da, v2 864f437e.
- PS-0000-IS-1: semanal Técnico 12-17 oct, BORRADOR, 6 fotos asignadas (id e7ff1dad).
- PS-0000-ID-2: COSTOS diario 15-10, EMITIDO (inmutable, no se puede borrar) (id eb20948b).
- PS-0000-ID-3: PERSONALIZADO diario 15-10, BORRADOR (id 4d770885).
- Sin subcontratos, sin formatos de usuario, sin datos en otro servicio.

## 5. L4: archivos y pesos (informe semanal con 6 fotos, 1000 px q70 al exportar)
PDF 357 KB, Word 359 KB, Excel 362 KB (completo); fotos 351/356/354 KB; resumen 4-12 KB; diarios sin fotos 8-15 KB. Muy por debajo de ~4 MB; extrapolado ~55 KB por foto, 20 fotos ≈ 1.1 MB. Riesgo de límite de Vercel: bajo con estas cifras (con fotos reales de celular el peso por foto exportada debería ser similar porque se reducen con sharp). Tiempo de generación local 4-7 s por archivo (maxDuration 60).
Revisión: sin «$», «S/», «USD», «costo», «CPI» en PDF, Word y Excel de los formatos no COSTOS; COSTOS sí lleva EV, AC, CV, CPI, SPI y costo por partida; la marca BORRADOR está en los tres formatos; Excel con una hoja por bloque; Word con 6 imágenes en el semanal.

## 6. L6 — lista para que Victor pruebe en un celular real
1. Abrir `Foto de campo` desde el celular (PS-0000) y confirmar que se abre la cámara trasera (atributo `capture`; la cabecera `camera=()` no está verificada).
2. Aceptar o negar el permiso de ubicación; con GPS marcado, ver que no tarde más de unos segundos o que se pueda desmarcar.
3. Tomar 3 fotos seguidas: descripción obligatoria, mensaje «N fotos guardadas».
4. Sin señal (modo avión): comprobar el reintento y que no se pierda la foto.
5. En el editor del semanal, asignar las fotos al bloque y descargar PDF y Word en el celular.
6. Confirmar el tamaño final (≈300 KB por foto subida).

## 7. Preguntas abiertas
- ¿Victor puede iniciar la segunda cuenta para observar el borrador ajeno (404) y el alcance real?
- ¿Se crea un subcontrato (partida) en PS-0000 para probar el subcontrato manual y los materiales de L7?
- Resolver el AC de la Curva S con `db/pruebas/102_comparacion_ac.sql` (Victor/Orquestador).

## 8. Decisiones del Orquestador y encargos posteriores
- L1 (borrador ajeno 404, recorrido con la segunda cuenta), subcontrato manual y materiales de L7: **Observados**, los prueba Victor con la lista de L6. L4: **Conforme**.
- Nota: durante el corte de sesión alguien más generó `PS-0000-ID-4` (PDF) y descargó el v3 de ID-1; no fue este Worker. Revisar para la lista de datos de prueba.

### Encargo 1 — Diagnóstico del AC de la Curva S (solo lectura, nada aplicado)
Veredicto: **no hay defecto en la SQL.** La diferencia es exactamente la suma de los materiales por % de avance físico que solo la Curva S ya incluye.
- Fórmula de `curva_s_proyecto` (102): `ac_acum(d) = Σ(HH×tarifa×recargo extra + HM×tarifa, hasta d) + materiales(d) + subcontratos(d)`, con `materiales(d) = Σ costo_contractual(material) × EV_acum(d) / BAC`.
- En PS-0000 (datos reales, GET): materiales contractuales US$ 5,197.49 (Dashboard), BAC 188,284.88.
  - 07-08: EV 3,657.63 -> avance 0.019426 -> 5,197.49 × 0.019426 = **100.97** = 3,336.65 − 3,235.68 (el día no tiene HH extra, stand-by ni gastos sin partida: 243.36 HH de OFICIAL, 4 HM, todo en 1.1.1).
  - Corte: EV 118,478.05 -> avance 0.62925 -> 5,197.49 × 0.62925 = **3,270.51** = 97,215.06 − 93,944.55.
- Subcontratos: 0 (el servicio no tiene). HH extra, stand-by y costo sin partida no intervienen en la diferencia.
- Causa: el PR guarda su AC (`proyecto_pr.costo_materiales_acum`, `costo_subcontratos_acum`) al recalcular; el PR de PS-0000 dice «Generado el 07-10-2026», anterior a la 102, y las columnas valen 0. PR, Dashboard y Costos leen ese guardado; la Curva S lo calcula en vivo con la función. Es un dato viejo, no una regla distinta.
- Lado correcto (R20: todo suma al costo real): la **Curva S**. Tras aplicar 102 hay que **recalcular el PR de los servicios existentes** (botón «Recalcular PR» por servicio, o una vez `select recalcular_pr_desde_rdt(proyecto_id) from proyecto_pr;` en base). Resultado esperado en PS-0000: AC PR = Dashboard = Costos (nuevo) = Curva S = US$ 97,215.06. El informe COSTOS emitido PS-0000-ID-2 quedó congelado con 93,944.55 (v2 posterior lo corregiría).
- Se recomienda que la aplicación de 102 incluya ese paso de recálculo (no hace falta 103 ni se escribió). Confirmación: Victor puede pulsar «Recalcular PR» en PS-0000 (escribe solo tablas derivadas del PR del servicio de prueba) o correr `db/pruebas/102_comparacion_ac.sql` con el id 0a20df2f-c5e9-4296-9c08-f89af499182d; no es necesario para el veredicto.
- Texto del PR obsoleto: «AC cubre solo HH y HM… materiales y subcontratos se miden por % de avance económico, no por costo capturado (regla 5)» contradice R20; pasar al Documentador.

### Encargo 2 — Orden de columnas en pantalla
Commit `1b7ad79` en `local-worker-3` (pusheado, solo esa rama): `ordenarClaves` y `rotuloClave` en `src/components/informes/editor-utils.ts`; `BloqueVista.tsx` los usa en tablas y campos de la vista previa y del emitido, con el orden y los rótulos del PDF (actividades diario y semanal, personal, equipos, indicadores, encabezado; `etiqueta` al final). Prueba en `editor-utils.test.ts` (4 casos). `npm test` 1564 verdes (149 archivos), `tsc` limpio, lint 9 errores y 22 avisos (los preexistentes), build webpack correcto. No verificado en el navegador tras el cambio.

## 9. CIERRE FINAL (reemplaza el estado de la §1)
### Tabla final por ítem
| ID | Estado | Nota |
|---|---|---|
| L1 | Observado | 13 roles conformes en API y COSTOS 403; falta «borrador ajeno = 404» y alcance real: lo prueba Victor con su segunda cuenta (decisión del Orquestador). |
| L2 | Observado | Recorrido hecho con la cuenta de administrador (diario, semanal con fotos, COSTOS, PERSONALIZADO, emitir, v2, 409); segunda cuenta pendiente (Victor). |
| L3 | Conforme | 390 px sin scroll horizontal. |
| L4 | Conforme | Archivos revisados; pesos ~360 KB con 6 fotos. |
| L5 | Conforme | Migraciones comprobadas por la app; la «duda de 102» se resolvió (dato viejo del PR, ver abajo). |
| L6 | Lista | Para Victor (abajo). |
| L7 | Conforme en el cuadre del AC en los lugares que la rama permite; Observado en subcontrato manual y materiales por avance | Ver cuatro valores. |

### Cuadre del AC en PS-0000 tras «Recalcular PR» (POST /pr/recalcular, 200 ok), corte 2026-10-15 / 17
| Lugar | AC |
|---|---|
| Curva S (`/api/curva-s`, 15-10 y 17-10) | **97,215.06** |
| Formato Costos (borrador nuevo PS-0000-ID-5) | **97,215.06** |
| PR (pantalla `/pr`) | 93,944.55 (sin cambio) |
| Dashboard (pantalla) | 93,944.55 (sin cambio) |
Curva S = Costos = 97,215.06 (diferencia con el anterior = materiales 3,270.51). **PR y Dashboard siguen en 93,944.55 porque el cargador de pantalla de esta rama no lee `costo_materiales_acum` / `costo_subcontratos_acum`**; solo `evm.ts` y los cargadores de informes los usan. Esa lectura es de la tanda S (desgloseAc), que no está incorporada en `local-worker-3`. Tras incorporar S, PR y Dashboard deben dar 97,215.06; **L7 queda pendiente de esa verificación para estos dos lugares** (el diagnóstico indica que el dato guardado ya es correcto). El COSTOS emitido PS-0000-ID-2 sigue congelado en 93,944.55.

### Datos de prueba (PS-0000; no borrar)
- 6 fotos de campo «PRUEBA foto de campo 1..6» (17-10).
- PS-0000-ID-1: v1 REEMPLAZADO, v2 EMITIDO, v3 BORRADOR (por sonda de L1; descargado después, origen de la descarga desconocido).
- PS-0000-IS-1 semanal BORRADOR con 6 fotos; PS-0000-ID-2 COSTOS EMITIDO (inmutable); PS-0000-ID-3 PERSONALIZADO BORRADOR; **PS-0000-ID-5 COSTOS BORRADOR** (id 616e1cea, cuadre del AC).
- **PS-0000-ID-4**: origen desconocido (posible prueba de Victor u otra sesión); no creado por este Worker; no borrado.
- Efecto del «Recalcular PR»: se actualizaron las columnas derivadas del PR de PS-0000 (materiales y subcontratos acumulados).

### Defectos devueltos y estado
| Defecto | Estado |
|---|---|
| Marca BORRADOR partida en el PDF y alcance «fotos» con primera página vacía | Corregidos por W1 en aa843f5 (no incorporado aún en local-worker-3; no re-verificado aquí) |
| Orden de columnas en vista previa y emitido | Corregido: 1b7ad79 y 5e0c4b3 (`local-worker-3`); verificado en el navegador el orden del emitido (N.º, Turno, Descripción, WBS…; Nombre, Cargo, HH…; Equipo, Partida, HM…); captura `L2-emitido-orden-columnas-1440.png`. El último ajuste (rótulos Descripción y Nivel) solo con pruebas, sin recarga en navegador |
| Texto del PR sobre AC y regla 5 | Corregido por W2 en 850ff41 (no incorporado aún aquí) |
| AC Curva S contra PR | Dato viejo del PR; resuelto con recálculo; falta lectura en pantalla (tanda S) |
| GPS ~10 s al guardar foto en escritorio con GPS marcado | **Pendiente, para Victor** (probar en celular real) |
| Datos de prueba de origen desconocido (ID-4, descarga de v3) | Anotados |

### L6 para Victor (celular real y segunda cuenta)
1. Foto de campo desde el celular: ¿abre la cámara trasera? (`capture`; cabecera `camera=()` no verificada).
2. Permiso de ubicación: ¿cuánto tarda con GPS marcado? (en escritorio ~10 s) ¿se puede desmarcar?
3. Tres fotos seguidas; mensaje «N fotos guardadas»; sin señal: reintento sin perder la foto.
4. Asignar fotos al bloque, descargar PDF y Word en el celular.
5. Con la segunda cuenta: borrador del administrador = 404; COSTOS = 403 si no tiene economía; alcance sobre PS-0000.
6. Tras incorporar la tanda S: PR y Dashboard de PS-0000 deben mostrar AC 97,215.06.

## 10. L-bis (rama `local-worker-3` en `f1e7a7b`, integra W1 aa843f5 y W2 H, I, J, K, S, 850ff41)

Comandos: `npm test` 159 archivos verdes (1 omitido), 1620 pruebas verdes; `tsc` limpio; lint 31 problemas (9 errores y 22 avisos, los preexistentes); `next build --webpack` compilado. El `.snap` de curva-s apareció modificado por fin de línea y se restauró con `git checkout`. App reiniciada en :3013. Sin commits nuevos en L-bis (no hubo corrección menor propia).

### Los cuatro valores del AC tras «Recalcular PR» (PS-0000)
| Lugar | AC (US$) |
|---|---|
| PR (fila Total proyecto) | 97.215,06 |
| Dashboard (tarjeta AC; xlsx 97215.0647; PDF) | 97.215,06 |
| Curva S (API) | 97.215,06 |
| Costos (borrador PS-0000-ID-5) | 97.215,06 |

Franja de desglose del PR (S3, S4): Personal 91.784,55 + Equipos 2.160,00 + Materiales 3.270,51 + Subcontratos 0,00 = 97.215,06. Materiales 3.270,51 = 5.197,49 × EV/BAC. Fila «Materiales y subcontratos (sin partida)» 3.270,51; pie actualizado (R20, db/102). CV 21.262,98, CPI 1,22.

### Tabla por ítem
| Ítem | Resultado |
|---|---|
| S3/S4 AC en cuatro lugares y franja de desglose | Conforme (capturas `Lbis-pr-1440/390.png`, `Lbis-dashboard-*`, `Lbis-curva-s-*`) |
| H1 supervisor operativo a cargo | Conforme: «Supervisor operativo a cargo: Lopez Caceres Loayza» |
| H2 barra de avance físico | Conforme: «Ejecutado 63% · prog. 97% · Restante 37%» |
| H3 tarjetas IP y HH contractuales | Conforme |
| I4/I6 recursos y partidas donde se usó | Conforme (`Lbis-I4-recursos-1440.png`, `Lbis-I6-recurso-partidas-1440.png`); la lista tarda unos segundos |
| I5 teclado/táctil | Teclado, hover y Escape sin error; táctil real **Observado** (celular de Victor) |
| J1 detalle del AC al tocar la tarjeta | Conforme (`aria-expanded` true→false; `Lbis-J1-detalle-AC-1440.png`) |
| J2/J3/J6 franja «En revisión» y similares | **Observado**: sin datos en revisión en PS-0000 para provocarlos |
| K pestañas HH/HM/Subcontratos | Conforme (`aria-selected` cambia) |
| K7/M9 descargas del Dashboard | COMPLETO xlsx 11 hojas y pdf 5 págs con dinero; PARCIAL xlsx 8 hojas y pdf 4 págs sin dinero. **Defecto M9 abajo** |
| Sin scroll horizontal a 1440 y 390 px (PR, Dashboard, Curva S) | Conforme (`scrollWidth` = `innerWidth`) |
| A4 faltantesParaEjecucion / confirmar transición | **Observado**: el servicio ya está en EJECUCION; no se puede provocar sin tocar el estado |
| N4 sección Subcontratos del PR | Visible «Este servicio no tiene subcontratos» |
| Subcontrato manual | **Observado**: el servicio no tiene subcontratos y `PUT /pr/subcontratos` responde 400 «Ese subcontrato no pertenece a este servicio»; crearlo exige editar el DP, fuera del alcance. Materiales por avance sí verificados |
| D RDT con HH extra y HM stand-by | **Observado**: ninguno de los 32 partes de PS-0000 trae horasExtra ni horasStandby > 0 (se revisó el parte 6f30cb19: extra 0, stand-by 0, estado vacío). Crear y validar un parte «PRUEBA» cambiaría el AC real del servicio y no se pudo deshacer; lo prueba Victor o se autoriza expresamente |

### Defectos devueltos
| Defecto | Archivo | Carril dueño |
|---|---|---|
| **M9**: con `tipo_dashboard` = PARCIAL y rol con economía, la **página** sigue mostrando todo el dinero (BAC, PV, EV, AC, SV, CV, composición en US$, CV por partida; 183 apariciones de «US$», igual que Completo), mientras que el **archivo descargado** PARCIAL no lleva dinero y el flujo 11 dice que el Parcial no tiene ningún dato económico. La página usa `puedeEditarTipo` para el bloque de dinero (líneas ~124, 296, 358, 508) y `datos-descarga.ts` ~119 usa `tipo_dashboard === 'COMPLETO' && conEconomia` | `src/app/(workspace)/proyectos/[id]/dashboard/page.tsx` | W2 |

### Datos de prueba nuevos en L-bis
Ninguno nuevo. Se llamó «Recalcular PR» (tablas derivadas de PS-0000) y se alternó `tipo_dashboard` con `PATCH /api/proyectos/{id}/tipo-dashboard`; **quedó en COMPLETO** (se asumió que era el valor original; no se conocía con certeza, Victor debe confirmarlo).

## 11. Re-verificación Dashboard Parcial (merge d5233c9, 2026-10-17)

Servidor del puerto 3013 reconstruido con `npx next build --webpack` y relevantado sobre `local-worker-3` (d5233c9); el build anterior era previo al merge.
- Valor encontrado de `tipo_dashboard` en PS-0000: **COMPLETO** (183 «US$» en la página). Se puso PARCIAL con `PATCH /api/proyectos/{id}/tipo-dashboard` (cuerpo `{tipoDashboard}`) y se dejó de nuevo en **COMPLETO** al terminar.
- **PARCIAL, sesión de Victor (rol con economía): Conforme.** La página tiene 0 «US$», sin AC 97.215 ni BAC/PV/EV/CV; solo aparece «SPI» en la nota del PPC («no se mezcla con SPI»). Sin scroll horizontal a 1440. Descargas: xlsx 19.321 bytes y PDF 12.113 bytes (4 págs), tamaño y número de hojas/páginas iguales al Parcial ya revisado (xlsx 8 hojas, PDF 4 págs, sin dinero); no se re-abrió el contenido celda por celda. Página y archivos coinciden (sin dinero). Captura `L-bis-dashboard-parcial-1440.png`.
- **COMPLETO: Conforme.** Página con dinero (398 «US$» en el HTML) y AC 97.215,06; descargas xlsx 25.844 bytes y PDF 17.592 bytes. Captura `L-bis-dashboard-parcial-completo-1440.png`.
- Defecto M9: **cerrado**.

## 12. Pruebas finales (H-1)

Servidor 3013 con la sesión de Victor vigente (rama 9633de4 solo agrega `.gitattributes`; no se reconstruyó). `tipo_dashboard` de PS-0000 no se tocó (COMPLETO).

### Prueba A — parte con HH extra y HM stand-by: Conforme
Parte «PRUEBA» `0699db4b-8374-4f04-8af5-6369dd97e7f7`, PS-0000, 2026-10-16 turno Día, actividad 3.2.4 con metrado ejecutado 0 (para no mover el EV). Persona: JOSHUA FARIAS (OFICIAL), 10 HH totales, 2 extra. Equipo: CAMIONETA PICK UP, 6 HM operativas + 2 stand-by, estado Stand-by. Validado con la sesión de Victor y «Recalcular PR».
Tarifas reales (acumulado/horas del PR): OFICIAL 91.784,55 / 7.060,35 h = 13,00 US$/HH; CAMIONETA PICK UP 2.160,00 / 120 HM = 18,00 US$/HM.
| | Antes | Después | Cálculo a mano |
|---|---|---|---|
| Personal | 91.784,55 | 91.921,05 (+136,50) | (8 + 1,25 × 2) × 13 = 136,50 |
| Equipos | 2.160,00 | 2.304,00 (+144,00) | (6 + 2) × 18 = 144,00 |
| AC total | 97.215,06 | 97.495,56 (+280,50) | 280,50 |
Sin cambio: BAC 188.284,88, PV 182.115,04, EV 118.478,05, materiales 3.270,51, subcontratos 0, IP 1,00. HH reales de OFICIAL 7.060,35 → 7.070,35 (+10 = total del parte; la extra va dentro del total y no suma aparte). CV, CPI y EAC cambian solo por el AC.
Cuadre al mismo corte: PR 97.495,56; Dashboard 97.495,56; Curva S 97.495,56 (EV y PV iguales); Costos (borrador PS-0000-ID-5, leído sin emitir) 97.495,56. Capturas `L-ter-A-pr-1440.png`, `L-ter-A-dashboard-1440.png`.

### Prueba B — subcontrato manual: Observado (no se hizo)
No existe vía para agregar un subcontrato a PS-0000 sin tocar el DP: los subcontratos salen de `dp_recursos` (tipo `subcontrato`, `src/lib/pr/subcontratos.ts`) y no hay API que agregue recursos; `PUT /pr/subcontratos` solo mide subcontratos que ya existen (400 «Ese subcontrato no pertenece a este servicio»). La única vía es reemplazar o reimportar el DP; no se hizo.

### Datos de prueba creados
RDT PRUEBA `0699db4b-8374-4f04-8af5-6369dd97e7f7` (VALIDADO; suma +280,50 al AC de PS-0000). Aparece un borrador PS-0000-ID-6 que no creé en esta sesión (origen desconocido, no se borró).

## 13. Lectura de los servicios reales y recálculo del PR (2026-10-17)

Victor autorizó en el chat recalcular el PR de los servicios reales. **No se hizo ni hace falta.** El Worker leyó (solo lectura) los cuatro servicios reales del portafolio «Servicios Marcobre»; no hay otros reales y «Practica» solo tiene PS-0000.

| Servicio | Lectura (2026-10-17) |
|---|---|
| PS-0001 INSTALACIÓN DE BATERÍA DE ALCANTARILLAS Y ENROCADOS – JAHUAY | AC 0,00 (personal, equipos, materiales y subcontratos en 0,00); avance físico 0 %; BAC US$ 263.778,08; último punto de la Curva S con PV, EV y AC en 0 |
| PS-0002 FACILIDADES DE VILLA DE EJECUCIÓN FASE 2 | AC 0,00; avance 0 %; Curva S en 0; HH contractuales 1.699,18 |
| PS-0003 MANTENIMIENTO EXTERIOR DEL CCI | AC 0,00; avance 0 %; Curva S en 0; HH contractuales 869,52 |
| PS-0004 OBRAS CIVILES PARA SISTEMA DETECCIÓN CONTRAINCENDIOS | AC 0,00; avance 0 %; Curva S en 0; HH contractuales 943,46 |

- Con AC 0 y avance 0 % no hay nada que el recálculo corrija.
- El único intento de escritura (`POST pr/recalcular` de PS-0001) fue denegado por el sistema de permisos («Modify Shared Resources»: es la base de producción); el Worker no buscó otra vía. **No se escribió nada en ningún servicio real.**
- Captura: `docs/02-trabajo-activo/03-evidencia/capturas/2026-10-15-informes-supervision-y-dashboard/L/L-real-PS-0001-antes.png`.
- Conclusión (H-6 / R43): no aplica hoy, porque los servicios reales no tienen avance ni costo. El recálculo solo se necesitaría para un servicio con RDT validados antes de la 102 (solo PS-0000, ya recalculado). Desde la 102 cada validación de RDT recalcula con materiales y subcontratos. La regla R43 sigue vigente.
