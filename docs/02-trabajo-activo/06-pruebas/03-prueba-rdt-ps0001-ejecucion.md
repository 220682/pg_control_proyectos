# 03 - Ejecucion de la prueba funcional del RDT en PS-0001 (TECNET)

> Plan: `02-prueba-rdt-ps0001-plan.md`. App: https://py-control-proyectos-web.vercel.app (produccion). Servicio PS-0001 id `70c696ae-a810-4e83-b44c-c8dec352c631`. Evidencia: `docs/02-trabajo-activo/03-evidencia/2026-10-19-prueba-rdt-ps0001/`.
> Fechas de los 5 RDT: 19, 20, 21, 22 y 23.10.2026. Entrada con supervisor operativo (Lopez Caceres); validacion con Victor (administrador). Sin fotos por ahora.

## Tanda 1 - RDT del 19.10 (D1)

### 0. Precondicion que hubo que crear (HALLAZGO / accion con efecto)

- Con la cuenta de Lopez Caceres (supervisor operativo, miembro solo de PS-0000) el formulario mostro «No tienes acceso a esta OT / Al guardar, el sistema rechazara esta accion» al elegir PS-0001. Esto confirma el bloqueo por OT (prueba negativa de permisos OK).
- Para poder entrar el RDT, con la cuenta de Victor se edito el servicio (Editar servicio > «Supervisor operativo a cargo»): estaba asignado **Braulio** y se cambio a **Lopez Caceres Loayza**. **Victor: al terminar, restituir a Braulio si corresponde** (id usuario Braulio `1f040668-128c-4d1b-bd9b-80d6b2429a7a`). Se guardo el formulario con sus fechas sin cambio (2026-10-15 / 2026-10-16 / 2026-11-07).
- Observacion de producto: el campo es de un solo supervisor a cargo; no hay forma de que dos supervisores escriban en el mismo servicio.

### 1. Lo que se ingresa (antes de enviar) y desviaciones respecto al plan

| Campo | Plan D1 | Ingresado | Nota |
|---|---|---|---|
| N° OT / cliente | PS-0001 / TECNET | PS-0001 / TECNET | OK |
| Fecha / turno | 19.10 / Dia | 2026-10-19 / Dia | |
| Especialidad / ubicacion / semana | civil / Lingo 1 y vestuarios / 1 | Civil / Lingo 1 y vestuarios / 1 | texto libre |
| T1 D PT-01 guia 2.3 ML | prog 8.9, ejec 6.0, CNC | prog 8.9, ejec 6.0, CNC «Mano de obra insuficiente.» | Met. prog. NO se autocompleto desde el Plan Maestro; se escribio a mano |
| T2 D directa 3.1 UND | prog 1, ejec 1 | prog 1, ejec 1 | |
| T3 C vinculada 2.3 PT-01 | «PRUEBA FUNCIONAL charla de seguridad y reunion de inicio» | igual | |
| Personal | 1 CAPATAZ, 2 OPERARIO CIVIL, 2 OFICIAL CIVIL, 1 OPERADOR LINEA AMARILLA, 1 ING. SSOMA | ver abajo | el catalogo de personal NO tiene CAPATAZ, OFICIAL CIVIL ni INGENIERO SSOMA |
| Equipos | Retro JD 310G 8 HM en PT-01:2.2; Grupo electrogeno 11KW 8 HM en 3.1 | Retro 8 HM en **PT-01:2.3**; Grupo 8 HM en 3.1 | la app no deja elegir como WBS una partida derivada (2.2): solo la guia 2.3 (el plan lo preveia) |
| Observaciones | «PRUEBA FUNCIONAL D1: avance parcial por inicio de frente.» | igual | |
| Restriccion / inasistencia / materiales | ninguna (D1) | ninguna | se probaran en D2/D3 segun el plan |

Personal (personas reales del catalogo; no se invento ninguna):

| Cargo en el plan | Persona usada (cargo en catalogo) | T1 | T2 | T3 | Total |
|---|---|---|---|---|---|
| CAPATAZ (x1) | TAPIA TARRILLO WALTER ALEJANDRO (OPERARIO) - sustituto, no hay capataz en el catalogo | 7 | 0 | 1 | 8 |
| OPERARIO CIVIL (x2) | CABRERA CUBA JUAN DE DIOS (OPERARIO CIVIL) | 7 | 0 | 1 | 8 |
| | PANDURO GONZALES GABRIEL JACKSON (OPERARIO CIVIL) | 7 | 0 | 1 | 8 |
| OFICIAL CIVIL (x2) | SANDRO LUIS BARDALES TRUJILLO (OFICIAL, esp. CIVIL) | 3 | 4 | 1 | 8 |
| | ACHULLA POLANCO ELMER ADONIS (OFICIAL) | 3 | 4 | 1 | 8 |
| OPERADOR LINEA AMARILLA (x1) | ARROYO ABANTO ESTEBAN JEREMIAS (OPERADOR DE LINEA AMARILLA) | 7 | 0 | 1 | 8 |
| ING. SSOMA (MOI) | ZOILA JEAN PACAYA (INGENIERO DE SEGURIDAD, esp. SSOMA) | 1 | 0 | 1 | 2 |

Consecuencia: las tarifas del plan (CAPATAZ 15.38, OFICIAL CIVIL 13.37) pueden no aplicar; los cargos OPERARIO y OFICIAL se resolveran por equivalencia o quedaran SIN_RESOLVER. El AC de personal real puede diferir de 681.60 y no es un fallo de la app: hay que ver `recursos_sin_tarifa` en el PR y comparar contra las tarifas que resuelva la app.

### 2. Valores esperados tras VALIDAR D1 (del plan, D.7)

EV total 1,284.44; % fisico 3.22 %; PV 1,693.93 (4.24 %); SV -409.48; SPI 0.758; AC personal 681.60 (ver nota de cargos), equipos 379.44 (retro en 2.3 no cambia el total), transversales 311.07, materiales 170.71 (A) / 114.84 (B), AC total 1,542.82 / 1,486.95; HH reales MOD 48, MOI 2; HH ganadas 33.34; IP 0.694; PT-01 Real acum. 6.0 ml (2.1 = 0.5618, 2.2 = 2.520, 2.4 = 6.0, 2.5 = 0.0225, 2.6 = 6.0, 2.7 = 1.800); 3.1 = 1/1; PPC 87.50 % (8 actividades, 1 con CNC); Pareto CNC 1 evento.

### 3. RDT creado

- RDT PS-0001 / 19-10-2026 / Dia / Civil, cargado por Lopez Caceres Loayza. Estado inicial **REGISTRADO** (9 actividades = T1 + 6 derivadas + T2 + T3; 7 personas; 50 HH; 16 HM). Luego **VALIDADO** por Victor (administrador). La pantalla Status no muestra un numero de RDT (solo la fila por OT + fecha + turno).
- Flujo seguido: borrador > guardar > recargar > «Continuar» > editar > enviar > (aviso) > validar.

### 4. Esperado vs mostrado tras validar D1

Fuentes: PR `/proyectos/{id}/pr`, Curva S `/proyectos/{id}/curva-s`, Dashboard, Plan Maestro `/plan-maestro?proyectoId={id}` (la ruta `/proyectos/{id}/plan-maestro` del plan da 404; la real es `/plan-maestro?proyectoId=`).

| Pantalla / dato | Esperado (plan) | Mostrado | Veredicto |
|---|---|---|---|
| PR EV total | 1,284.44 | 1,284.44 | OK |
| PR % fisico | 3.22 % | 3.2 % (Plan Maestro: 3,22 %) | OK |
| PR PV al corte / SV / SPI | 1,693.93 / -409.48 / 0.758 | 1,693.93 / -409.48 / 0.76 | OK |
| PR HH ganadas | 33.34 | 33.34 | OK |
| PR EV por partida 2.1 / 2.3 / 3.1 | 0.5618 DIA (204.07) / 6.0 ml (32.94) / 1 und (311.43) | 0.56 (204.07) / 6.00 (32.94) / 1.00 (311.43) | OK |
| PR metrado derivado 2.2 / 2.5 / 2.7 | 2.520 / 0.0225 / 1.800 | 2.52 / 0.02 / 1.80 | OK (2 decimales) |
| PR AC equipos | 379.44 | 379.44 | OK |
| PR AC transversales | 311.07 | 311.07 (rotulado «Sin resolver» en el cuadro de AC) | valor OK, rotulo confuso |
| PR AC personal | 681.60 | 344.64 | DIFERENCIA explicada: ver 5.1 |
| PR AC materiales | 170.71 (A) / 114.84 (B) | 173.36 | DIFERENCIA: hipotesis C, ver 5.2 |
| PR AC total | 1,542.82 / 1,486.95 | 1,208.51 | explicado por 5.1 y 5.2 (1,542.82 - 336.96 + 2.65 = 1,208.51) |
| PR CV / CPI | -258.37 / 0.833 | +75.94 / 1.06 | consecuencia de AC |
| PR HH reales | 48 (MOD) | 51.35 (42 en 2.3 + 8 en 3.1 + 1.35 de 1.1) | DIFERENCIA: ver 5.3 |
| PR / Dashboard IP | 0.694 | 0.65 | consecuencia de 5.3 |
| PR PPC / actividades con CNC | 87.50 % (8 / 1) | 87.5 % (8 act., 1 con CNC en 2.3) | OK |
| Curva S diaria 19.10 (PV / EV) | 1,693.93 / 1,284.44 | 1,693.93 / 1,284.44 (AC 1,208.51) | OK |
| Curva S semanal | S1 cierra 23.10 | S1 (23-10) dice «posterior a la fecha de corte» en EV/AC, pero la «Lectura al 23-10» da EV 1,284.44, PV 8,513.45, SV -7,229.00, SPI 0.15 | HALLAZGO 5.4 |
| Dashboard avance / prog. | 3.22 % / 4.24 % | 3 % / 4 % (tabla por nivel: 3.2 % / 4.2 %) | OK |
| Dashboard HH | - | reales 51, acumuladas 51 (5 %), restan 941 | consistente con PR |
| Dashboard Pareto CNC | 1 evento | 1: «Mano de obra insuficiente.» 100 % | OK |
| Dashboard PPC | 87.5 % | 87.5 % | OK |
| Dashboard recursos sin tarifa | TOPOGRAFO solo en D4 | 3 de mano de obra (sin nombres) | consistente con 5.1 |
| Plan Maestro Prog. total S1 / Real total | 21.32 % / 3.22 % | 21,32 % ($8,513) / 3,22 % ($1,284); Real en el dia 19/10; semanas siguientes 0,00 % con acum. 3,22 % | OK |
| Plan Maestro PT-01 guia | Real acum. 6.0 de 30 | 6 de 30, rest. 24, 20,00 % | OK |
| Plan Maestro PT-01 2.1 | Real 0.5618; prog 8.9/30 de 2.81 | Met. 2,81 / acum. 0,56 / rest. 2,25; prog 0,83 x3 + 0,31 | OK |
| Status de RDTs | REGISTRADO > VALIDADO | REGISTRADO > VALIDADO (columna Validacion «Validado») | OK |
| Restricciones / inasistencias (Informes) | ninguna en D1 | no verificado | no probado |

### 5. Diferencias y causa probable

5.1 **AC de personal 344.64 en vez de 681.60** (dif. 336.96). Causa: sustitucion de personas por falta de cargos en el catalogo (no es fallo de la app). TAPIA (cargo OPERARIO, por CAPATAZ), SANDRO BARDALES y ACHULLA (cargo OFICIAL, por OFICIAL CIVIL) quedaron sin tarifa (cuestan 0): 344.64 = 2 x 8 x 13.94 + 8 x 15.20 (los 2 OPERARIO CIVIL y el OPERADOR DE LINEA AMARILLA). Los 3 «recursos sin tarifa de mano de obra» del Dashboard serian OPERARIO, OFICIAL e INGENIERO DE SEGURIDAD (inferido; la vista no da nombres). Hallazgo de datos: el catalogo `recursos_personal` no tiene CAPATAZ, OFICIAL CIVIL ni INGENIERO SSOMA, y los cargos genericos OPERARIO y OFICIAL no resuelven tarifa. Zoila (INGENIERO DE SEGURIDAD) no es MOI: el PR dice «HH de MOI acumuladas 0.00 h» y sus 2 h entran como HH reales.
5.2 **Materiales 173.36**: coincide con una hipotesis C no prevista en el plan (M = 5,389.32 x 3.2167 %), es decir, la suma de materiales de los APU incluyendo transversales; no con 5,307.00 ni 3,570.22. Verificar contra el DP cual es el monto contractual correcto de materiales (el listado de insumos dice 5,307.00).
5.3 **HH reales 51.35 e IP 0.65**: la app incluye en HH reales (a) las horas de cargos no-MOI sin tarifa y las de Zoila (2 h) y (b) las HH de la transversal 1.1 (1.35 = 42 x p). El plan esperaba 48 (solo MOD) e IP 0.694. Respuesta a la pregunta E8: HH reales del PR = HH de RDT (incluso sin tarifa) + HH APU x p de transversales. A confirmar con Victor si el IP debe excluir las HH de la transversal.
5.4 **Curva S, lectura semanal**: con granularidad semanal el punto S1 (23-10) lee PV al 23-10 (8,513.45) pero EV al corte 19-10 (1,284.44): SV = -7,229.00 y SPI = 0.15, no comparables (el EV real al 23.10 aun no existe). La tabla de la misma pantalla dice «posterior a la fecha de corte». La lectura diaria si es correcta. Causa probable: la lectura semanal toma el ultimo EV/AC conocido sin recortar el PV al corte; mirar `src/app/api/curva-s/route.ts` y el componente de lectura de la Curva S (no confirmado en codigo).
5.5 **Programado no se autocompleta**: en el formulario `Met. prog.` queda vacio al elegir la actividad (el plan decia que lo trae del Plan Maestro por dia). Se escribio a mano (8.9 y 1).
5.6 **«Met.» / «Met. rest.» de la guia 2.3** muestran el metrado contractual de la partida completa (267 / 267), no el del paquete (30); el Plan Maestro, en cambio, muestra 30 / 6 / 24. Causa probable: el formulario toma `metrado` de la partida, no de la linea del paquete.
5.7 Plan: la ruta del Plan Maestro `/proyectos/{id}/plan-maestro` da 404; la real es `/plan-maestro?proyectoId={id}`.

### 6. Funciones probadas

| Funcion | Resultado |
|---|---|
| Bloqueo por OT sin asignacion (supervisor sin acceso a PS-0001) | OK: «No tienes acceso a esta OT» |
| Actividad de paquete (declarar por guia 2.3) con filas derivadas calculadas | OK (0.56 / 2.52 / 6 / 0.02 / 6 / 1.8) |
| Directa 3.1; actividad C vinculada a partida | OK |
| CNC (lista del catalogo) | OK (1 evento en el Pareto) |
| Tareo con personas del catalogo; totales HH | OK (50 HH) |
| Equipos: elegir WBS | PARCIAL: solo guias/directas (2.3, 3.1); no deja las derivadas (2.2) |
| Guardar borrador, recargar, «Continuar», datos intactos, editar | OK |
| Aviso de jornada (persona con 2 h de 8) | OK: confirm «No es obligatorio que coincida» |
| Enviar RDT | OK > REGISTRADO |
| Supervisor operativo sin botones Validar/Rechazar | OK (UI) |
| Validar con administrador (confirm) | OK > VALIDADO; PR recalculado |
| Trabajador no listado, materiales, restriccion, inasistencia, stand-by, HH extra, PDF borrador, plantilla, descargar | NO PROBADO en D1 |

### 7. No se pudo probar / queda abierto

- Restricciones, inasistencias, materiales, HH extra, stand-by, rechazo y correccion, duplicado (409), tope de la guia, validar el propio RDT por API: corresponden a D2 a D5 y a D.8.
- Avisos/notificaciones a validadores y al autor (no se revisaron las bandejas).
- Lista exacta de «recursos sin tarifa» (el PR no la muestra; el Dashboard solo da el conteo).
- Capturas en `docs/02-trabajo-activo/03-evidencia/2026-10-19-prueba-rdt-ps0001/`: `d1-formulario-antes-de-enviar.png`, `d1-pr-validado.png`, `d1-curva-s.png`, `d1-dashboard.png`, `d1-plan-maestro.png`.

## Tanda 2 - RDT del 20.10 (D2): rechazo, correccion e inasistencia

> Ejecutada el 19.10.2026 (hora Lima, noche). Entrada con Lopez Caceres (supervisor operativo, ya a cargo de PS-0001; no se toco); rechazo y validacion con Victor (administrador). Sin fotos. Capturas con prefijo `d2-` en la carpeta de evidencia.

### 1. Lo que se ingreso y desviaciones respecto al plan (D.3)

| Campo | Plan D.3 | Ingresado | Nota |
|---|---|---|---|
| OT / cliente / fecha / turno | PS-0001 / TECNET / 20.10 / Dia | igual (2026-10-20, Dia) | la fecha futura (20.10 > hoy 19.10) NO se bloqueo: ni el formulario ni el servidor la rechazan (D2-1) |
| Especialidad / ubicacion / semana | civil / Lingo 1 y vestuarios / 1 | Civil / Lingo 1 y vestuarios / 1 | |
| T1 PT-01 guia 2.3 ML | v1 prog 8.9, ejec 9.5; final ejec 8.9 | v1 prog 8.9, ejec 9.5; correccion ejec 8.9 | |
| T2 directa 3.1 | prog 1, ejec 1 | igual | |
| Personal | 7 personas | las mismas 7 de D1: TAPIA TARRILLO [OPERARIO, sustituye a CAPATAZ], CABRERA CUBA y PANDURO GONZALES [OPERARIO CIVIL], BARDALES TRUJILLO y ACHULLA POLANCO [OFICIAL], ARROYO ABANTO [OPERADOR DE LINEA AMARILLA], ZOILA JEAN PACAYA [INGENIERO DE SEGURIDAD] | horas T1/T2: TAPIA 8/0; CABRERA y PANDURO 5/3; BARDALES, ACHULLA, ARROYO 8/0; ZOILA 2/0. Total 50 HH (T1 44, T2 6). Sin T3 (no hay C/NC en D2) |
| Inasistencia | 1 persona, Falta, nota «PRUEBA FUNCIONAL: inasistencia informativa» | CABRERA BARRANCA MIGUEL ANGEL (catalogo, no es de las 7), Falta, misma nota | |
| Equipos | Retro 6 HM + 2 stand-by en 2.2; Grupo 8 HM en 3.1 | Retro 6 HM + 2 stand-by en PT-01:2.3 (la 2.2 derivada no se puede elegir); Grupo 8 HM en 3.1; ambos Operativo | mismo workaround que D1 |
| Observaciones | v1 «PRUEBA FUNCIONAL D2 v1: metrado con error, rechazar»; final «PRUEBA FUNCIONAL D2: corregido tras rechazo.» | igual | |
| Motivo de rechazo | «PRUEBA FUNCIONAL: el metrado de la guia no coincide con el control de campo; corregir a 8.9 ml» | igual | |
| Motivo de correccion | «PRUEBA FUNCIONAL: metrado corregido a 8.9 ml» | igual (se pide en un prompt del navegador) | |

### 2. Esperados (plan D.7 ajustados con la tanda 1)

- Tras RECHAZAR v1: acumulados = solo D1 (EV 1,284.44; AC 1,208.51; HH 51.35; 6.0 ml).
- Tras VALIDAR la correccion: EV 2,978.37; fisico 7.46 %; PT-01 guia 14.9 ml (2.1 = 1.395; 2.2 = 6.258; 2.7 = 4.47); 3.1 = 2 und; PV plan 3,387.85 (1,693.93 si el corte es hoy 19.10).
- AC personal (solo cargos con tarifa resuelta) 2 x 344.64 = 689.28; equipos 2 x 379.44 = 758.88 (la stand-by cuenta); transversales 9,670.42 x 7.459 % = 721.30; materiales 5,389.32 x 7.459 % = 401.97; AC total 2,571.43; CV +406.94; CPI 1.158.
- HH reales 2 x 50 + 1.1 transversal (42 x 7.459 % = 3.13) = 103.13; HH ganadas 76.66; IP 0.743 (incluye la HH de 1.1: diferencia ya conocida que Victor decidio cambiar; solo se anota el valor mostrado). PPC 93.75 % (16 actividades, 1 con CNC). Pareto CNC: 1 evento.

### 3. RDT creado y recorrido de estados

- RDT PS-0001 / 20-10-2026 / Dia / Civil, cargado por Lopez Caceres. id interno `9dfb68cb-3df0-41f7-8a54-279c98f4d5e7`; la pantalla Status no muestra numero de RDT (una fila por OT + fecha + turno).
- v1 enviado > REGISTRADO (8 actividades, 7 personas, 50 HH, 14 HM) > RECHAZADO (Victor) > corregido por Lopez > REGISTRADO > validado por Victor > **VALIDADO** (8 act., 7 pers., 50 HH, 14 HM).
- Estado final: 2 RDT en PS-0001, ambos VALIDADOS (19.10 y 20.10). No se creo ningun duplicado ni borrador.

### 4. Esperado vs mostrado

**4.1 Tras RECHAZAR (Victor), antes de corregir**

| Pantalla / dato | Esperado | Mostrado | Veredicto |
|---|---|---|---|
| Status, vista de Victor | RECHAZADO | RECHAZADO | OK |
| Status, vista del autor (Lopez) | RECHAZADO, motivo, opcion de corregir | RECHAZADO; botones Descargar, Ver historial de correcciones, Revisar RDT, Corregir RDT. El motivo NO aparece en la fila ni en «Revisar RDT»; solo en el Historial (fecha, quien, accion «Rechazo», motivo, estado que tenia) y en el aviso | OK, ver D2-3 |
| Aviso al autor | notificacion con el motivo | «Tu RDT del 20-10-2026 (turno dia) del servicio PS-0001 fue rechazado: PRUEBA FUNCIONAL: el metrado de la guia no coincide...», de Victor, grupo Supervision operativa | OK |
| Aviso a validadores al registrar | si | Victor recibio «RDT registrado para validar» (D1 y 20-10) | OK |
| PR | = solo D1 | EV 1,284.44; AC 1,208.51 (personal 344.64); HH 51.35; 3.2 % | OK: el rechazado no cuenta |
| Dashboard | = solo D1 | avance 3 %; IP 0.65; HH 51; PPC 87.5 % | OK |
| Rechazar sin motivo | error | «Indique el motivo del rechazo» | OK |

**4.2 Tras CORREGIR (Lopez) y VALIDAR (Victor)**

| Pantalla / dato | Esperado | Mostrado | Veredicto |
|---|---|---|---|
| PR EV / % fisico | 2,978.37 / 7.46 % | 2,978.37 / 7.5 % | OK |
| PR metrado PT-01 2.3 / 2.1 / 2.2 / 2.7 | 14.9 / 1.395 / 6.258 / 4.47 | 14.90 / 1.40 / 6.26 / 4.47 | OK |
| PR 3.1 | 2 und | 2.00 (50 %) | OK |
| PR AC personal / equipos | 689.28 / 758.88 | 689.28 / 758.88 | OK |
| PR AC «Sin resolver» (transversales) / materiales | 721.30 / 401.97 | 721.30 / 401.98 | OK |
| PR AC total / CV / CPI | 2,571.43 / +406.94 / 1.158 | 2,571.45 / +406.92 / 1.16 | OK (centavos) |
| PR PV al corte / SV / SPI | plan 3,387.85 / -409.48 / 0.879 | 1,693.93 / +1,284.44 / 1.76 (corte 19-10-2026) | DIFERENCIA, D2-1 |
| PR HH reales / ganadas / IP | 103.13 / 76.66 / 0.743 | 103.13 / 76.66 / 0.74 | OK (IP con HH de 1.1: diferencia conocida) |
| PR HM en 2.3 | 16 (6 + 2 stand-by + ...) | 16 HM en 2.3 (stand-by contada) | OK |
| Dashboard avance / IP / HH | 7.46 % / 0.74 / 103 | 7 % (7.5 %) / 0.74 / 103 (10 %), restan 889 | OK |
| Dashboard programado | 8.48 % (plan) | 4 % (4.2 %) | misma causa D2-1 |
| Dashboard PPC / Pareto CNC | 93.75 % / 1 | 93.8 % / 1 evento | OK |
| Dashboard recursos sin tarifa | 3 de MO | 3 de mano de obra | OK (ver D) |
| Curva S diaria | 19.10 y 20.10 con EV/AC | 19.10 correcto (EV 1,284.44; AC 1,208.51); 20.10 con PV 3,387.85 pero «posterior a la fecha de corte - sin ejecucion registrada» | DIFERENCIA, D2-1 |
| Curva S semanal | S1 (23-10) | S1 «posterior a la fecha de corte»; «Lectura al 23-10»: PV 8,513.45, EV 2,978.37, AC 2,571.45, SV -5,535.08, SPI 0.35 | mismo hallazgo 5.4 de D1 |
| Plan Maestro Real total | 7.46 %, $2,978, HH 103.13 | 7,46 % / $2 978 / 103,13 | OK |
| Plan Maestro PT-01 | 14.9 ml; 2.1 real 0.56 (19.10) + 0.83 (20.10); 49.67 % | PT-01 49,67 %, acum. 14,9, rest. 15,1; 2.1 Real 0,56 (19/10) y 0,83 (20/10) | OK |
| Status | VALIDADO | VALIDADO, 8 act., 7 pers., 50 HH, 14 HM | OK (la columna HM no cuenta la stand-by, el PR si; D2-5) |
| Aviso de validacion al autor | si | no verificado | no probado |

### 5. Diferencias y hallazgos nuevos (D2-n para no chocar con la numeracion de la tanda 1)

- **D2-1 Fecha futura y fecha de corte.** La app deja registrar y validar un RDT del 20.10 estando el 19.10. PR y Dashboard muestran corte 19-10-2026 pero EV, AC y HH ya incluyen el RDT del 20.10, mientras el PV se corta al 19.10: SV +1,284.44 y SPI 1.76 no significan nada (EV de manana contra PV de hoy). La Curva S diaria muestra el 20.10 con PV pero «sin ejecucion registrada» aunque hay un RDT validado. Causa probable: sin regla de fecha futura en servidor; el corte se fija en hoy solo para el PV y la serie diaria. Pregunta para Victor: bloquear la fecha futura en el RDT, o que el corte avance a la ultima fecha validada.
- **D2-2 Duplicado: la UI pide reemplazar con motivo (no muestra un 409).** Al enviar otro RDT con la misma OT + fecha + turno aparece un prompt «Ya hay un RDT cargado para esta OT, esta fecha y este turno. Si continuas, el anterior se reemplaza por este (queda en el historial). No se puede deshacer. ¿Que se observo y como se corrigio? (obligatorio para continuar)». No se continuo: no se creo ni reemplazo nada (el Status siguio con 50 HH y 7 personas). La correccion de un rechazado usa el mismo prompt (es un reemplazo con motivo). El 409 PARTE_DUPLICADO del plan queda detras del prompt y no se probo aislado.
- **D2-3 Motivo del rechazo poco visible para el autor.** La fila RECHAZADO del Status y «Revisar RDT» no muestran el motivo; solo el Historial de correcciones y la notificacion. Ademas «Revisar RDT» del rechazado muestra Met. acum. 15.50 (6.0 + 9.5 de la propia v1 rechazada): cuenta su propio metrado aunque no este validado (solo vista; el PR no lo cuenta).
- **D2-4 «Avance del paquete 2 %» en todos los paquetes** del selector (PT-01 a PT-08, incluso sin ejecucion): es el avance de la partida contractual (6/267), no del paquete. Misma causa que 5.6 de D1. No se reviso de nuevo tras validar D2.
- **D2-5 Stand-by en la columna HM del Status.** Status muestra 14 HM (sin la stand-by); el PR cuenta 16 en 2.3 (6 + 2 stand-by + 8 del grupo en 3.1 por partida). Posible incoherencia de criterio entre pantallas; por confirmar.
- **D2-6 Acceso de Lopez.** Sin acceso a PR ni al Plan Maestro («Tu rol no tiene acceso a esta pantalla» / «Solo roles con datos economicos y Planner ven el Plan Maestro»); si ve Dashboard y Curva S. Coincide con el flujo 14 (no contrastado con la Matriz de permisos).
- Consola del navegador: 1 entrada de error durante la correccion; no se investigo.

### 6. Funciones probadas (tanda 2)

| Funcion | Resultado |
|---|---|
| Crear RDT con fecha futura | Permitido sin aviso (D2-1) |
| Inasistencia (catalogo, Falta, nota) | Guardada y recargada al corregir; la vista en Informes > Inasistencias NO se reviso |
| Equipo con HM stand-by (6 + 2) | Guardado; AC equipos correcto |
| Aviso de jornada (Zoila 2 h) | OK |
| Rechazar sin motivo | OK, bloqueado |
| Rechazar con motivo | OK > RECHAZADO; PR y Dashboard no cambian |
| Aviso al autor con el motivo | OK |
| Historial de correcciones | OK (rechazo y correccion con fecha, autor, motivo) |
| Corregir RDT rechazado (autor) | OK: formulario precargado completo; pide aviso de jornada y motivo; vuelve a REGISTRADO |
| Validar la correccion | OK > VALIDADO; PR recalculado exacto |
| Duplicado mismo dia y turno | Prompt de reemplazo; cancelado sin efecto (D2-2) |
| PR / Dashboard / Curva S / Plan Maestro con 2 RDT | OK salvo D2-1 |

### 7. Respuesta a D (solo lectura): por que OPERARIO y OFICIAL no tienen tarifa

Cargos de mano de obra directa del DP de PS-0001 (tarifa implicita = costo contractual / HH):

| Cargo en el DP | Unidad | Cantidad | Costo contractual | Tarifa implicita |
|---|---|---|---|---|
| CAPATAZ. (con punto) | HH | 74.04 | 1,139.78 | 15.39 |
| CAPATAZ | MES | 0.10 | 148.48 | por mes |
| OPERARIO | MES | 0.50 | 636.36 | por mes (equiv. 6.12/h) |
| OPERARIO CIVIL | HH | 176.86 | 2,464.06 | 13.93 |
| OFICIAL CIVIL | HH | 104.96 | 1,403.38 | 13.37 |
| OPERARIO MECANICO | HH | 150.00 | 2,091.00 | 13.94 |
| OFICIAL MECANICO | HH | 75.00 | 1,002.75 | 13.37 |
| OPERADOR DE LINEA AMARILLA | HH | 37.38 | 568.55 | 15.21 |
| OPERADOR DE EQUIPO LIVIANO | HH | 20.00 | 269.20 | 13.46 |
| PEON. / PEON | HH | 296.56 / 0.08 | 3,518.72 / 1.60 | 11.87 / 20.00 |
| VIGIA | HH | 57.38 | 680.15 | 11.85 |
| SUPERVISOR SSOMA / SUPERVISOR OPERATIVO | MES | 1.09 c/u | 3,287.33 / 3,521.84 | por mes |

Total mano de obra 20,733.21; materiales 5,389.32 (confirma M). MOI: solo Jefe de Proyectos (104 HH, 2,096.85); ALMACEN, CONDUCTOR, Ing. de Calidad, Ing. Oficina Tecnica, Ing. Operativo e Ingeniero SSOMA estan en 0.

No existe «OFICIAL» en el DP (solo OFICIAL CIVIL y OFICIAL MECANICO) y el unico «OPERARIO» esta en unidad MES, no HH. El catalogo de cargos de la empresa (37 cargos del presupuesto) si tiene OPERARIO y OFICIAL genericos, y las personas estan cargadas con ellos.

Como se vincula (lectura de `py_control_proyectos_web/src/lib/dp/tarifas.ts`, solo lectura, consistente con lo observado): el cargo de la persona se normaliza (mayusculas, sin punto final); se busca primero en la lista MOI del DP; si no, en las filas de mano de obra del DP **solo de unidad HH**, por nombre normalizado exacto, o por una equivalencia guardada al importar el DP. No hay equivalencia por jerarquia (OFICIAL no cae en OFICIAL CIVIL). Si no resuelve queda SIN_RESOLVER: cuesta 0, las horas igual cuentan, no bloquea. Por eso OPERARIO (su fila es MES), OFICIAL (sin fila) e INGENIERO DE SEGURIDAD (el DP trae INGENIERO SSOMA en MOI con 0 h) no resuelven; son los «3 recursos sin tarifa de mano de obra» del Dashboard. Opciones (decision de Victor, no ejecutadas): equivalencias OPERARIO > OPERARIO CIVIL, OFICIAL > OFICIAL CIVIL, INGENIERO DE SEGURIDAD > INGENIERO SSOMA; o cargar al personal con los cargos exactos del DP; o definir como tratar las filas en MES.

### 8. No se pudo probar / queda abierto

- Aviso de validacion al autor; Informes > Inasistencias y Restricciones; HH extra, NC, restriccion, materiales, trabajador no listado, tope de la guia, validar el propio RDT por API, correccion por Jefe de oficina tecnica, borrador/plantilla/PDF/descarga.
- 409 PARTE_DUPLICADO aislado (la UI lo antepone con un prompt).
- No se cambio el supervisor a cargo (sigue Lopez Caceres) ni ningun dato del servicio.
- Capturas: `d2-formulario-v1-antes-de-enviar.png`, `d2-status-registrado-v1.png`, `d2-pr-tras-rechazo.png`, `d2-historial-rechazo-vista-autor.png`, `d2-historial-tras-correccion.png`, `d2-dashboard.png`, `d2-curva-s.png`, `d2-curva-s-diaria.png`, `d2-plan-maestro.png`. No hay captura del PR tras validar; los valores estan en 4.2.

## Tanda 3 - D3: RDT del 21.10 (metrado mayor al programado, HH extra, NC, restriccion)

> Ejecutada la noche del 19.10.2026 (hora Lima). Entrada con Lopez Caceres (supervisor operativo, a cargo de PS-0001; no se toco); validacion con Victor (administrador). Sin fotos. Capturas con prefijo `d3-`.

### 1. Lo que se ingreso y desviaciones respecto al plan (D.4)

| Campo | Plan D.4 | Ingresado | Nota |
|---|---|---|---|
| OT / cliente / fecha / turno | PS-0001 / TECNET / 21.10 / Dia | igual (2026-10-21, Dia, Civil) | fecha futura aceptada (D2-1) |
| T1 PT-01 guia 2.3 ML | prog 8.9, ejec 10.0 | prog 8.9, ejec 10.0, sin CNC; restriccion en la fila: «PRUEBA FUNCIONAL: falta liberacion del frente de lingo 1 para continuar perfilado» | las partidas derivadas se calculan solas |
| T2 directa 3.1 UND | 1 de 1 | 1 de 1 | |
| T3 NC | «PRUEBA FUNCIONAL espera por liberacion de frente», vinculada a 2.3 PT-01 | igual (No contributoria, partida 2.3) | |
| Personal | las 7 personas de D1/D2 | las mismas 7: TAPIA (cargo CAPATAZ del plan; en catalogo OPERARIO), CABRERA CUBA y PANDURO (OPERARIO CIVIL), BARDALES y ACHULLA (OFICIAL), ARROYO (OPERADOR DE LINEA AMARILLA), ZOILA (ING. SSOMA) | horas T1/T2/T3: TAPIA 9/0/1; CABRERA, PANDURO, BARDALES, ACHULLA 6/3/1; ARROYO 9/0/1; ZOILA 2/0/0. HH extra 2 h en las 6 primeras (12 en total). Total 62 HH |
| Equipos | Retro 8 HM, Rotomartillo 6 HM, Grupo 8 HM | Retro JD 310G 8 y ROTOMARTILLO 6 en PT-01:2.3; Grupo 11 KW 8 en 3.1; todos Operativo | la 2.2 derivada no se puede elegir en el formulario; 22 HM |
| Observaciones | «PRUEBA FUNCIONAL D3: sobreproduccion de 1.1 ml sobre lo programado.» | igual | |
| Materiales / trabajador no listado | el plan D.4 no los preve | no ingresados | no probados: no se invento cantidad de materiales ni se crea persona fuera del catalogo |

Estado: RDT 21-10-2026 REGISTRADO (9 actividades, 7 personas, 62 HH, 22 HM) > VALIDADO por Victor (confirm «Esta ejecucion pasara a ser real oficial»). El aviso de jornada (personas con menos de 8 h) se acepto al enviar.

### 2. Esperados tras validar D3 (regla de tarifa de la tanda 1; materiales M = 5,389.32 x p)

EV 4,827.61; % fisico 12.09 %; PT-01 24.9 ml; 3.1 = 3 und. AC: personal 1,141.62 (solo OPERARIO CIVIL 13.94 y OPERADOR 15.20 resuelven tarifa, con recargo por HH extra); equipos 1,159.32; transversales 1,169.16; materiales 651.57 (p = 12.09 %); AC total 4,121.67; CV +705.94; CPI 1.171. HH reales 167.08; HH ganadas 123.78; IP 0.741 (incluye la HH de 1.1, diferencia conocida). PPC 95.83 % (24 actividades, 1 CNC). PV: la fecha de corte del PR es 19.10 (D2-1), por eso PV/SV/SPI no son comparables.

### 3. Esperado vs mostrado tras validar D3

| Pantalla / dato | Esperado | Mostrado | Veredicto |
|---|---|---|---|
| Status | REGISTRADO > VALIDADO, 9 act., 7 pers., 62 HH | igual; 22 HM | OK |
| PR EV / % fisico | 4,827.61 / 12.09 % | 4,827.62 / 12.1 % | OK (centavos) |
| PR 2.3 acum. / 3.1 | 24.9 / 3 | 24.90 / 3.00 (75 %) | OK |
| PR AC personal / equipos | 1,141.62 / 1,159.32 | 1,141.62 / 1,159.32 | OK |
| PR AC «Sin resolver» (transversales) / materiales | 1,169.16 / 651.57 | 1,169.16 / 651.57 | OK |
| PR AC total / CV / CPI | 4,121.67 / +705.94 / 1.171 | 4,121.67 / +705.95 / 1.17 | OK |
| PR HH reales / HH ganadas / IP | 167.08 / 123.78 / 0.741 | 167.08 / 123.79 / 0.74 | OK (IP con HH de 1.1: diferencia conocida) |
| PR PV al corte / SV / SPI | corte 19.10 | 1,693.93 / +3,133.69 / 2.85 | D2-1, solo se anota |
| Dashboard avance / IP / HH | 12.09 % / 0.74 / 167 | 12 % / 0.74 / 167 | OK |
| Dashboard PPC / Pareto CNC | 95.83 % / 1 | 95.8 % / 1 evento | OK |
| Dashboard recursos sin tarifa | 3 de mano de obra | 3; OPERARIO CIVIL 52 HH, OPERADOR 26 HH | OK |
| Curva S diaria | 21.10 con EV/AC de D3 | solo 19.10 con ejecucion; 20 y 21.10 «posterior a la fecha de corte - sin ejecucion registrada» pese a RDT validados | D2-1 |
| Curva S semanal | EV y AC de D3 | lectura al 23-10: PV 8,513.45, EV 4,827.62, AC 4,121.67, SPI 0.57 | EV y AC OK; PV a fecha futura (hallazgo 5.4, ya conocido) |
| Plan Maestro Real total | 12.09 %, HH 167.08 | 12,09 % / $4 828 / 167,08 | OK |
| Plan Maestro PT-01 | 24.9 ml | PT-01 83,00 %, acum. 24,9, restante 5,1; 2.1 acum. 2,33; 2.2 acum. 10,46 | OK |
| Aviso al autor al validar | si | bandeja de Lopez: «Tu RDT del 21-10-2026 (turno dia) del servicio PS-0001 fue validado» (De: Victor, Pendiente) | OK |
| Aviso a validadores al registrar | si | Victor recibe «RDT registrado para validar» | OK |
| Restriccion de D3 (registro PS-0001-RE-n visible en Informes) | creada | no hay aviso ni registro de restriccion de PS-0001; el texto queda solo en el RDT; `/proyectos/{id}/restricciones` da 404; Informes solo tiene pestanas «Informes» e «Inasistencias» | D3-1 |
| Inasistencia de D2 en Informes > Inasistencias | aparece (20.10) | no verificable: el selector de fecha tiene max = hoy (19.10) y dice «Elige fechas validas: hasta hoy» | D3-2 |

### 4. Diferencias y hallazgos nuevos

- **D3-1 La restriccion de la actividad no genera registro visible.** El texto queda en el RDT, pero no hay aviso «Restriccion PS-0001-RE-n» (en la bandeja de Victor solo existe el viejo PS-0000-RE-1) y la pantalla Restricciones da 404 en produccion. Causa probable: la regla de restricciones por actividad (flujo 06, 2026-10-19) y la pantalla estan en trabajo de la app aun sin desplegar. No se corrigio; repetir tras el despliegue.
- **D3-2 Informes > Inasistencias no deja consultar fechas futuras** (consecuencia de D2-1): no se pudo comprobar la inasistencia del 20.10.
- **D3-3 Plan Maestro: mensaje transitorio «Este servicio aun no tiene un Plan Maestro»** (con boton de crear borrador) en la primera carga por URL; al recargar aparece el Plan Maestro con datos. No se pulso el boton. Riesgo: crear un borrador por error si se pulsa antes de que cargue.
- **D3-4 Curva S y PV con fechas futuras:** conocido (D2-1 y 5.4), solo se registran los valores mostrados; no es hallazgo nuevo.
- Verificado y OK: recargo por HH extra en el AC de personal; la NC suma HH y AC; sobreproduccion (10.0 > 8.9) sin pedir CNC.

### 5. Pruebas negativas (D.8) con Lopez, fecha 21.10, sin guardar nada

| Caso | Esperado | Mostrado | Veredicto |
|---|---|---|---|
| Tope de la guia: ejecutado 31 (> 30 del paquete) | rechaza | HTTP 400 en `POST /api/rdts/partes`: «Actividad 1: La cantidad declarada supera el metrado de la partida guia del paquete» | OK |
| HH extra (5) mayor que el total de la persona (2) | rechaza | mensaje en el formulario, sin llamada: «ZOILA JEAN PACAYA: Las horas extra (5) no pueden superar el total de la persona (2).» | OK |
| Duplicado misma OT + fecha + turno | 409 | `POST /api/rdts/partes` responde 409 y la UI abre el prompt de reemplazo («Ya hay un RDT cargado para esta OT, esta fecha y este turno... obligatorio»); se descarto sin reemplazar; D3 siguio con 62 HH | OK (aclara D2-2: el prompt es la reaccion al 409) |
| Supervisor operativo sin Validar/Rechazar | sin botones | en Status Lopez ve solo Descargar, Historial, Revisar RDT; Victor ve ademas Validar RDT y Rechazar RDT | OK (solo UI) |
| Validar el propio RDT por API; motivo vacio del reemplazo; rechazar un RDT ya VALIDADO; jefe de oficina tecnica corrigiendo | ver D.8 | no probado (payload desconocido o dejaria datos sobrantes) | no probado |

Consola: solo los dos errores esperados `Failed to load resource: the server responded with a status of 400 ()` (tope) y el 409. El error de consola de la correccion de D2 no se pudo reproducir porque en esta tanda no se corrigio ningun RDT.

### 6. Funciones probadas (D3)

Metrado mayor al programado sin CNC; HH extra con recargo; NC con partida; texto de restriccion (se guarda, sin registro: D3-1); equipos en dos WBS; enviar; validar; aviso al autor al validar; PR, Dashboard, Curva S, Plan Maestro; tope de la guia; HH extra mayor que el total; duplicado 409. Capturas: `d3-formulario-antes-de-enviar.png`, `d3-pr-validado.png`, `d3-dashboard.png`, `d3-curva-s-diaria.png`, `d3-plan-maestro.png`.

## Tanda 3 - D4: RDT del 22.10 (completa PT-01 y 3.1; PT-02 parcial con CNC; recurso sin tarifa)

> Misma noche. Entrada con Lopez, validacion con Victor. Capturas con prefijo `d4-`.

### 1. Lo que se ingreso y desviaciones respecto al plan (D.5)

| Campo | Plan D.5 | Ingresado | Nota |
|---|---|---|---|
| OT / fecha / turno | PS-0001 / 22.10 / Dia | igual (Civil) | |
| T1 PT-01 guia 2.3 | prog 3.3, ejec 5.1 | igual, sin CNC | PT-01 llega a 30 de 30 (100 %) |
| T2 PT-02 guia 2.3 | prog 5.6, ejec 4.0, CNC | igual, CNC «Falta de suministro oportuno de materiales.» | |
| T3 directa 3.1 | 1 de 1 | igual | 3.1 llega a 4 de 4 |
| Personal | CAPATAZ, 2 OPERARIO CIVIL, 2 OFICIAL, OPERADOR, TOPOGRAFO, ING. SSOMA | TAPIA 3/4/1; CABRERA y PANDURO 3/3/2; BARDALES y ACHULLA 2/3/3; ARROYO 4/4/0; RONALD MARTIN ALVARADO AGREDA 2/2/0 (cargo AYUDANTE TOPOGRAFO, sustituye a TOPOGRAFO); ZOILA 1/1/0 | 8 personas, 54 HH, sin HH extra |
| Equipos | Retro y Camion baranda y Grupo | Retro 5 HM (PT-01:2.3), Retro 3 HM (PT-02:2.3), Camion baranda 4 HM (3.1), Grupo 8 HM (3.1); todos Operativo | 20 HM |
| Observaciones | «PRUEBA FUNCIONAL D4: cierre de PT-01 y de 3.1.» | igual | |

Estado: RDT 22-10-2026 REGISTRADO (15 actividades, 8 personas, 54 HH, 20 HM) > VALIDADO por Victor (confirm «Validar el RDT del 22-10-2026? Esta ejecucion pasara a ser real oficial.»).

### 2. Esperados tras validar D4

EV 6,549.78; % fisico 16.40 %; AC personal 1,486.26; equipos 1,838.76; transversales 1,586.23; materiales 884.00; AC total 5,795.26; CV +754.52; HH reales 222.89 (216 + 6.89 de transversal); HH ganadas 167.81; PPC 94.87 % (39 actividades, 2 CNC); Pareto 2 eventos; recursos sin tarifa 4 (entra AYUDANTE TOPOGRAFO).

### 3. Esperado vs mostrado tras validar D4

| Pantalla / dato | Esperado | Mostrado | Veredicto |
|---|---|---|---|
| Status | VALIDADO, 15 act., 8 pers., 54 HH, 20 HM | igual | OK |
| PR EV / % fisico | 6,549.78 / 16.40 % | 6,549.78 / 16.4 % | OK |
| PR 2.3 acum. / 3.1 | 34.0 / 4 (100 %) | 34.00 / 4 (100 %) | OK |
| PR AC personal / equipos | 1,486.26 / 1,838.76 | 1,486.26 / 1,838.76 | OK |
| PR AC «Sin resolver» / materiales | 1,586.23 / 884.00 | 1,586.23 / 884.01 | OK (centavo) |
| PR AC total / CV / CPI | 5,795.26 / +754.52 | 5,795.26 / +754.52 / 1.13 | OK |
| PR HH reales / ganadas / IP | 222.89 / 167.81 | 222.89 / 167.80 / 0.75 | OK (IP con HH de 1.1: diferencia conocida) |
| PR PV al corte / SV / SPI | corte 19.10 | 1,693.93 / +4,855.86 / 3.87 | D2-1, solo se anota |
| Dashboard avance / IP / HH | 16.4 % / 0.75 / 223 | 16 % / 0.75 / 223 (22 %) | OK |
| Dashboard PPC / Pareto | 94.87 % / 2 | 94.9 % / 2 causas (Mano de obra insuficiente 1; Falta de suministro oportuno de materiales 1) | OK |
| Dashboard recursos sin tarifa | 4 | 4 (era 3); OPERARIO CIVIL 68 HH, OPERADOR 34 HH | OK |
| Curva S diaria | 22.10 con EV/AC | 22.10 «sin ejecucion registrada» | D2-1 |
| Curva S semanal | EV 6,549.78, AC 5,795.26 | lectura al 23-10: PV 8,513.45, EV 6,549.78, AC 5,795.26, SV -1,963.66, SPI 0.77, CPI 1.13 | EV y AC OK; PV a fecha futura (5.4) |
| Plan Maestro Real total | 16.40 %, HH 222.89 | 16,40 % / $6 550 / 222,89 | OK |
| Plan Maestro PT-01 / PT-02 | 100 % (30/30) / 4 ml | PT-01 100 % (30 de 30); PT-02 3,96 % (4 de 101) | OK |
| Aviso por recurso sin tarifa a administrador / jefe de proyectos | si (D.7.6) | no aparece en la bandeja de Victor (lo mas reciente es «RDT registrado» del 22-10) | D4-1 |
| Aviso al autor al validar D4 | si | no verificado (cuenta de Lopez no abierta tras validar D4; la funcion ya estaba OK en D3) | no probado |

### 4. Diferencias y hallazgos nuevos

- **D4-1 Sin aviso por recurso sin tarifa.** Al validar D4 el Dashboard pasa de 3 a 4 recursos sin tarifa y la validacion no se bloquea (regla A5), pero la bandeja de Victor no recibe aviso (tampoco se vio en D1). El plan esperaba aviso a administrador y jefe de proyectos. Causa probable: el aviso no existe o se emite en otra condicion; no se reviso el codigo.
- **D4-2 «Met. acum.» de PT-02 en el formulario.** Muestra el acumulado de la partida (24.90) y no el del paquete; misma causa que 5.6 y D2-4; no es nuevo, pero se nota mas con dos paquetes en un mismo RDT.
- **D4-3 Equipos en dos paquetes.** Las dos filas de retroexcavadora muestran WBS «2.3» sin el paquete; no se pudo confirmar en pantalla a cual paquete queda cada una (el AC de equipos coincide en total).
- Verificado y OK: completar un paquete (PT-01 100 %) y una partida directa (3.1 de 4 en 4); segundo paquete parcial con CNC (PPC 94.9 %); recurso sin tarifa no bloquea la validacion y suma sus horas a HH reales; Pareto con dos causas.

### 5. Funciones probadas (D4)

Dos paquetes en un mismo RDT; CNC con segundo motivo; directa que completa la partida; cargo sin tarifa sin bloqueo; cuatro filas de equipo; validar; PR, Dashboard, Curva S, Plan Maestro. Capturas: `d4-formulario-antes-de-enviar.png`, `d4-pr-validado.png`, `d4-dashboard.png`, `d4-curva-s-diaria.png`, `d4-plan-maestro.png`.

### 6. No probado en la tanda 3

Materiales y trabajador no listado en el formulario; validar el propio RDT por API; rechazar un RDT ya VALIDADO y revalidar; reemplazar un VALIDADO; correccion por jefe de oficina tecnica; Informes > Restricciones (pantalla no desplegada); Informes > Inasistencias del 20.10 (fecha futura); aviso al autor de D4; PDF, borrador, plantilla y descarga.

## Tanda 4 - D5: RDT del 23.10 (igual al programado; cierre de 3.2; PEON)

> Ejecutada la noche del 19.10.2026 (hora Lima). Entrada con Lopez Caceres (supervisor operativo, a cargo de PS-0001; no se toco); validacion y lecturas con Victor (administrador). Sin fotos. Capturas con prefijo `d5-`.

### 1. Lo que se ingreso y desviaciones respecto al plan (D.6)

| Campo | Plan D.6 | Ingresado | Nota |
|---|---|---|---|
| OT / fecha / turno | PS-0001 / 23.10 / Dia | igual (2026-10-23, Dia, Civil); ubicacion «Vestidores y lingo oxidos», semana 1 | fecha futura aceptada (D2-1) |
| T1 PT-02 guia 2.3 ML | prog 8.9, ejec 8.9 | prog 8.9, ejec 8.9, sin CNC | Met. prog. escrito a mano (5.5); «Met. acum.» del formulario mostro 34 (30 + 4: acumulado de la partida, no del paquete: 5.6); las 6 derivadas se calcularon solas (2.1 0.83; 2.2 3.74; 2.4 8.9; 2.5 0.03; 2.6 8.9; 2.7 2.67) |
| T2 directa 3.2 UND | prog 4, ejec 4 | prog 4, ejec 4 | la 3.2 aparecio al 0 % en el selector |
| Descripcion de las actividades | no prevista | texto corto «... (PRUEBA FUNCIONAL D5)» en T1 y T2 | el campo «Que se hizo» no se autocompleta al elegir la partida |
| Personal | 1 CAPATAZ, 2 OPERARIO CIVIL, 2 OFICIAL CIVIL, 2 PEON, 1 OPERADOR, 1 ING. SSOMA | las 7 personas de D1 a D4 + 2 PEON del catalogo (9 personas) | sustituciones iguales a las anteriores; PEON: GOMEZ HUAMAN CHRISTOPHER IVAN y HERNANDEZ COLLQUE ANGEL EDMUNDO (cargo PEON en el catalogo, sin sustitucion) |
| Horas T1/T2 | CAPATAZ, OPERARIO, OFICIAL 6/2; PEON 8/0; OPERADOR 8/0; SSOMA 2/0 | TAPIA, CABRERA, PANDURO, BARDALES, ACHULLA 6/2; los 2 PEON 8/0; ARROYO 8/0; ZOILA 2/0 | 66 HH (56 en T1, 10 en T2), sin HH extra ni T3 |
| Equipos | Retro 8 HM PT-02:2.2; Rotomartillo 4 HM PT-02:2.3; Camion baranda 6 HM en 3.2 | Retro 8 HM y Rotomartillo 4 HM en el WBS 2.3 (guia de PT-02); Camion baranda 6 HM en 3.2; todos Operativo | la 2.2 derivada no se puede elegir (igual que D1 a D4); 18 HM |
| Observaciones | «PRUEBA FUNCIONAL D5: cierre de 3.2.» | igual | |

Aviso de jornada al enviar: «ZOILA JEAN PACAYA: 6h menos (cargo 2h de 8h)», aceptado. Estado: RDT 23-10-2026 REGISTRADO (8 actividades, 9 personas, 66 HH, 18 HM) > VALIDADO por Victor (confirm «¿Validar el RDT del 23-10-2026? Esta ejecucion pasara a ser real oficial.»).

### 2. Esperados tras validar D5

Con la regla de tarifa (solo cargos con tarifa resuelta) y materiales M = 5,389.32 x p. Acumulado real: PT-01 30 ml, PT-02 12.9 ml (4.0 + 8.9), 3.1 = 4, 3.2 = 4; EV_resto 5,902.89; p = 20.75 %.

- EV 8,287.52 (plan D.7); % fisico 20.75 %; PV al corte 23.10 8,513.44; SV -225.92; SPI 0.973 (solo si el corte fuera 23.10; hoy el corte es 19.10, D2-1).
- AC personal: 1,486.26 + OPERARIO CIVIL 2 x 8 x 13.94 (223.04) + OPERADOR 8 x 15.20 (121.60) + PEON 16 x 11.86 (189.76) = 2,020.66. Equipos 1,838.76 + 305.84 + 14.00 + 450.00 = 2,608.60. Transversales 9,670.42 x p = 2,007.08. Materiales 5,389.32 x p = 1,118.55. AC total 7,754.89; CV +532.63; CPI 1.069.
- HH reales 282 de RDT + 42 x p (8.72) = 290.72; HH ganadas 219.98; IP 0.757 (incluye las HH de 1.1: diferencia conocida). PPC 95.74 % (47 actividades, 2 con CNC); Pareto 2 eventos; recursos sin tarifa 4 (PEON si tiene tarifa).

### 3. Esperado vs mostrado tras validar D5

| Pantalla / dato | Esperado | Mostrado | Veredicto |
|---|---|---|---|
| Status | VALIDADO, 8 act., 9 pers., 66 HH, 18 HM | igual (columna Paquete: solo «ZANJA Vestidores y lingo oxidos», sin mencion de la directa 3.2) | OK |
| PR EV / % fisico | 8,287.52 / 20.75 % | 8,287.53 / 20.8 % (Plan Maestro 20,75 %) | OK (centavo) |
| PR metrado acum. 2.3 / 3.1 / 3.2 | 42.9 / 4 / 4 | 42.90 (16.1 %) / 4.00 (100 %) / 4.00 (100 %) | OK |
| PR derivados 2.1 / 2.2 / 2.5 / 2.7 | 4.0169 / 18.018 / 0.1607 / 12.87 | 4.02 / 18.02 / 0.16 / 12.87 | OK |
| PR AC personal / equipos | 2,020.66 / 2,608.60 | 2,020.66 / 2,608.60 | OK |
| PR AC «Sin resolver» (transversales) / materiales | 2,007.08 / 1,118.55 | 2,007.08 / 1,118.55 | OK (rotulo confuso conocido) |
| PR AC total / CV / CPI | 7,754.89 / +532.63 / 1.069 | 7,754.89 / +532.64 / 1.07 | OK |
| PR HH reales / ganadas / IP | 290.72 / 219.98 / 0.757 | 290.72 / 219.98 / 0.76 | OK (IP con HH de 1.1: diferencia conocida) |
| PR HH por partida | 2.3 = 225 (plan, solo D); 3.1 = 37; 3.2 = 10 | 2.3 = 235 (222 D + 7 C + 6 NC; incluye las 10 h de ZOILA); 3.1 = 37; 3.2 = 10 | consecuencia de 5.1 (cargos no MOI y C/NC cuentan); el plan D.7.3 no los incluia |
| PR costo atribuido 3.1 / 3.2 | plan 1,108.41 / 590.00 | 821.62 / 505.76 | consecuencia de 5.1 (personas sin tarifa cuestan 0) |
| PR PV al corte / SV / SPI | corte 19.10 | 1,693.93 / +6,593.60 / 4.89 | D2-1, solo se anota |
| PR PPC / activ. con CNC | 95.74 % (47 / 2) | 95.7 % (47 act., 2 con CNC en 2.3) | OK |
| Dashboard avance / IP / HH | 20.75 % / 0.76 / 291 | 21 % (prog. 4 %) / 0.76 / reales 291, ganadas 220; acum. 291 (29 %), restan 702 | OK (prog. 4 %: D2-1) |
| Dashboard por nivel (real) | N1 20.8 / N2 16.1 / N3 100 / N4 20.8 | 20.8 / 16.1 / 100 / 20.8 | OK |
| Dashboard PPC / Pareto CNC | 95.74 % / 2 | 95.7 % / 2 causas (Mano de obra insuficiente 1; Falta de suministro oportuno de materiales 1) | OK |
| Dashboard recursos sin tarifa | 4 | 4 («4 de mano de obra, 0 de equipos»); sin nombres | OK; ver D5-2 |
| Dashboard recursos HH (contractual vs acum.) | - | PEON. 16/296.6; OPERARIO CIVIL 84/176.9; OPERADOR DE LINEA AMARILLA 42/37.4 (marcado en rojo: exceso sobre lo contractual) | consistente con lo ingresado |
| Dashboard «Completo»: costo real por recurso (MO) | PEON 189.76 | PEON. 189.76; PEON 0.00; OPERARIO CIVIL 1,184.90; OPERADOR DE LINEA AMARILLA 646.00; resto 0 | OK; PEON usa la tarifa de «PEON.» (11.86), no la de 20.20 |
| Curva S diaria | 19 a 23.10 con EV/AC | solo 19.10 con EV 1,284.44 / AC 1,208.51; 20 a 23.10 «posterior a la fecha de corte - sin ejecucion registrada» (con PV) | D2-1 |
| Curva S semanal | S1 (23-10): EV 8,287.52, AC 7,754.89, SV -225.92, SPI 0.973 | «Lectura al 23-10»: PV 8,513.45, EV 8,287.53, AC 7,754.89, SV -225.92, CV +532.64, SPI 0.97, CPI 1.07; la fila S1 de la tabla sigue diciendo «posterior a la fecha de corte - sin ejecucion registrada» | lectura OK (coincide con el plan); fila de tabla: hallazgo 5.4 |
| Plan Maestro Real total | 20.75 %, $8,288, HH 290.72 | 20,75 % / $8 288 / 290,72 | OK |
| Plan Maestro Prog. total S1 | 21.32 % ($8,513) | 21,32 % / $8 513 / 225,49 h | OK |
| Plan Maestro PT-01 / PT-02 | 100 % / 12.9 de 101 | PT-01 100 % (30 de 30); PT-02 12,77 % (12,9 de 101, rest. 88,1) | OK |
| Plan Maestro PT-02 2.3 Real | 22.10 = 4.0; 23.10 = 8.9 | 4 (22/10) y 8,9 (23/10); Prog 5,6 y 8,9 | OK |
| Plan Maestro 3.2 | 4 de 4 el 23.10 | Real 4 el 23/10, 100 % completada, restante 0 | OK |
| Aviso a validadores al registrar | si | Victor: «RDT registrado para validar ... 23-10-2026» (11:15 p. m.); quedo ATENDIDO al validar | OK |
| Aviso al autor al validar (D5 y D4) | si | bandeja de Lopez: «Tu RDT del 23-10-2026 / 22-10-2026 / 21-10-2026 / 20-10-2026 / 19-10-2026 fue validado» (De: Victor) y el de rechazo del 20-10 con su motivo | OK (cierra el no probado de D4) |
| Aviso por recurso sin tarifa | no aplica en D5 (no entro uno nuevo) | no hay aviso de ningun tipo de recurso sin tarifa en la bandeja | D4-1 sin cambios |

### 4. Diferencias y hallazgos nuevos (D5-n)

- **D5-1 Columna «Paquete» del Status ignora las directas.** El RDT del 23.10 incluye la directa 3.2 pero la columna solo dice «ZANJA Vestidores y lingo oxidos»; el D4 con 3.1 tampoco la listaba. Menor y de presentacion; sin impacto en calculos.
- **D5-2 «Recursos sin tarifa» sin lista de nombres.** El Dashboard da solo el conteo (4) y su enlace «Asignar tarifa en Recursos» abre `/recursos/personal` (el catalogo general), no la lista de cargos sin tarifa; el PR no la muestra y la ficha «Completo» solo lista costos por recurso del DP. La lista (OPERARIO, OFICIAL, INGENIERO DE SEGURIDAD, AYUDANTE TOPOGRAFO) sigue siendo inferida (tanda 2, seccion 7), no vista en pantalla.
- Respuesta a la duda E4 del plan: con PEON la app congela la tarifa de «PEON.» (11.86); el APU con PEON a 20 no se uso (PEON = 0.00 en el costo por recurso).
- Respuesta a la duda del plan sobre PPC (E8): se cuentan las filas derivadas como actividades; la CNC cae solo en la fila guia (2.3: 6 actividades, 2 con CNC); PPC 95.7 % coincide con el plan.
- Sin diferencias de calculo en D5: todo lo de EV, AC, HH, PPC y Plan Maestro coincide con el esperado (hasta el centavo), salvo lo ya conocido (D2-1, 5.4, 5.3 por la HH de 1.1).

### 5. Funciones probadas (D5)

Completar una directa (3.2 de 4 en 4); segundo paquete avanzando (PT-02 12.9 de 101) con metrado igual al programado sin CNC; cargo PEON del catalogo (resuelve tarifa de «PEON.»); 9 personas y 66 HH; tres filas de equipo (dos en la guia de PT-02 y una en la directa); aviso de jornada; enviar; validar; aviso al validar y al autor; PR, Dashboard (Parcial y Completo), Curva S (semanal y diaria), Plan Maestro, Status; descarga de PDF de los cinco RDT validados (ver Cierre). Capturas: `d5-formulario-antes-de-enviar.png`, `d5-pr-validado.png`, `d5-dashboard.png`, `d5-curva-s-semanal.png`, `d5-curva-s-diaria.png`, `d5-plan-maestro.png`, `d5-status-cinco-validados.png`.

### 6. No probado en la tanda 4

Materiales y trabajador no listado en el formulario; fotos; restricciones de la actividad y la pantalla Restricciones (D3-1: no desplegada); Informes > Inasistencias (fecha futura); validar el propio RDT por API; rechazar un RDT ya VALIDADO y revalidar; reemplazar un VALIDADO; correccion por jefe de oficina tecnica; borrador, plantilla y PDF de borrador; contenido del PDF descargado (solo se comprobo que el servidor lo entrega).

## Cierre de la ejecucion

### Estado final de los cinco RDT de PS-0001 (turno Dia, Civil, cargados por Lopez Caceres)

| Fecha | Estado final | Actividades | Personas | HH | HM | Recorrido |
|---|---|---|---|---|---|---|
| 19.10.2026 | VALIDADO | 9 | 7 | 50 | 16 | registrado > validado |
| 20.10.2026 | VALIDADO | 8 | 7 | 50 | 14 | registrado > rechazado > corregido > validado |
| 21.10.2026 | VALIDADO | 9 | 7 | 62 | 22 | registrado > validado |
| 22.10.2026 | VALIDADO | 15 | 8 | 54 | 20 | registrado > validado |
| 23.10.2026 | VALIDADO | 8 | 9 | 66 | 18 | registrado > validado |

Sin borradores ni duplicados. Descarga: el boton «Descargar en formato PROM-GP-002» de cada fila entrega `/api/rdts/partes/{id}/pdf` con HTTP 200, `application/pdf`, firma `%PDF-`, nombre `RDT_PS-0001_2026-10-DD.pdf` y 6.5 a 8.3 KB en los cinco; no se guardo ningun archivo y no se inspecciono el contenido. Los cinco aparecen VALIDADOS en Status (columna Validacion «Validado») y en los avisos al autor; el historial de correcciones del 20.10 no se volvio a abrir en la tanda 4 (su contenido se verifico en la tanda 2); la vista previa del PDF no se abrio, solo la descarga por el enlace.

### Acumulados finales por pantalla (corte mostrado 19-10-2026)

| Pantalla | Valores |
|---|---|
| PR | EV 8,287.53; avance fisico 20.8 %; AC 7,754.89 (personal 2,020.66; equipos 2,608.60; transversales «Sin resolver» 2,007.08; materiales 1,118.55; subcontratos 0); CV +532.64; CPI 1.07; HH reales 290.72; HH ganadas 219.98; IP 0.76; PPC 95.7 % (47 act., 2 con CNC); PV al corte 1,693.93; SV +6,593.60; SPI 4.89 (D2-1) |
| Dashboard | avance 21 % (prog. 4 %); IP 0.76; HH 291 de 992 (29 %), restan 702; PPC 95.7 %; Pareto 2 causas (50 % / 50 %); recursos sin tarifa 4; partidas sin actividad 3 (1.2, 2.5, 4.1); sobre-ejecutadas 0 |
| Curva S semanal | lectura al 23-10: PV 8,513.45; EV 8,287.53; AC 7,754.89; SV -225.92; CV +532.64; SPI 0.97; CPI 1.07 |
| Curva S diaria | solo el 19.10 con EV/AC; 20 a 23.10 «sin ejecucion registrada» (D2-1) |
| Plan Maestro | Real total 20,75 % / $8 288 / 290,72 h; Prog. total S1 21,32 % / $8 513; PT-01 100 %; PT-02 12,77 % (12,9 de 101); 3.1 y 3.2 completas (4 de 4) |
| Status | 5 RDT VALIDADOS |

El esperado del plan (20.75 % real, SPI 0.973, EV 8,287.52) coincide con lo mostrado en el % real, el EV y la lectura semanal de la Curva S; el SPI del PR no coincide por la fecha de corte (D2-1).

### Lista consolidada de diferencias y hallazgos (D1 a D5, sin repetir)

Acciones con efecto: (a) para poder entrar RDT en PS-0001 se cambio el supervisor operativo a cargo de Braulio a Lopez Caceres Loayza (D1); restituir a Braulio (`1f040668-128c-4d1b-bd9b-80d6b2429a7a`) si Victor lo quiere; (b) los 5 RDT de prueba (observaciones con «PRUEBA FUNCIONAL») quedan validados y contaminan avance, AC, HH y Curva S de PS-0001 hasta que Victor los rechace o borre. Ninguna otra accion con efecto en datos reales.

Diferencias de datos o de regla (no son fallos de la app):
1. El catalogo de personal no tiene CAPATAZ, OFICIAL CIVIL ni INGENIERO SSOMA; los cargos OPERARIO, OFICIAL e INGENIERO DE SEGURIDAD (y AYUDANTE TOPOGRAFO) no resuelven tarifa (cuestan 0, sus horas cuentan); equivalencias propuestas en la tanda 2, seccion 7 (decision de Victor). PEON si resuelve («PEON.», 11.86). Consecuencia: AC de personal menor que el del plan y costo atribuido a 3.1/3.2 menor; HH de 2.3 incluyen las de ZOILA y C/NC.
2. Materiales: la app usa 5,389.32 x p (suma de materiales de los APU, confirmado contra el DP), no 5,307.00 ni 3,570.22 del plan.
3. HH reales incluyen las HH de la transversal 1.1 (42 x p) y las horas de cargos no MOI sin tarifa: IP 0.76 contra 0.809 del plan. Cambio de regla ya decidido por Victor; se corregira.

Hallazgos de la app o del producto (por orden de importancia):
4. **D2-1** Fecha futura aceptada sin aviso (formulario y servidor) y fecha de corte fija en hoy: PV al 19.10 contra EV/AC con RDT de hasta el 23.10 da SV +6,593.60 y SPI 4.89; la Curva S diaria dice «sin ejecucion registrada» para dias con RDT validado; el Dashboard muestra programado 4 %. Afecta tambien a Informes > Inasistencias, que no consulta fechas futuras (D3-2).
5. **D3-1** La restriccion escrita en la actividad no genera registro PS-0001-RE-n ni aviso; la pantalla Restricciones da 404 en produccion (pendiente de despliegue; repetir la prueba).
6. **D4-1** Sin aviso al administrador y al jefe de proyectos por recurso sin tarifa (A5 del plan).
7. **5.4** Curva S semanal: la tabla muestra la fila de la semana como «posterior a la fecha de corte» aunque la «Lectura al 23-10» da valores; en D1 a D3 la lectura mezclaba PV a la fecha futura con EV al corte (SPI no comparable); en D5 coincide con el plan porque EV y PV llegan al mismo dia.
8. **5.5** La «Met. prog.» no se autocompleta desde el Plan Maestro (se escribe a mano); tampoco la descripcion de la actividad.
9. **5.6 / D2-4 / D4-2** «Met.», «Met. acum.», «Met. rest.» y «Avance del paquete» muestran el valor de la partida contractual (267, 34, 13 %), no el del paquete (30 / 101); lo correcto aparece en el Plan Maestro.
10. **D1 (equipos)** El formulario solo deja elegir como WBS de un equipo las guias y las directas (2.3, 3.1, 3.2), no las derivadas (2.2); y no muestra a que paquete queda cada fila (**D4-3**).
11. **D2-3** El motivo del rechazo no aparece en la fila del Status ni en «Revisar RDT» del autor (solo en el historial y en el aviso); «Revisar RDT» del rechazado cuenta su propio metrado.
12. **D2-5** La columna HM del Status no cuenta la stand-by; el PR si.
13. **D3-3** Plan Maestro: mensaje transitorio «Este servicio aun no tiene un Plan Maestro» con boton de crear borrador mientras carga; riesgo de pulsarlo.
14. **D5-2** «Recursos sin tarifa»: solo conteo; el enlace no lleva a una lista de cargos sin tarifa.
15. **D5-1** La columna «Paquete» del Status no menciona las directas.
16. Menores: rotulo «Sin resolver» para las transversales en el cuadro de AC del PR; la ruta `/proyectos/{id}/plan-maestro` del plan da 404 (la real es `/plan-maestro?proyectoId=`); el campo es de un solo supervisor a cargo por servicio (D1); D2-6 Lopez no ve PR ni Plan Maestro (coincide con el flujo 14, no contrastado con la Matriz).
17. **D2-2** (aclarado en D3): el duplicado mismo OT + fecha + turno devuelve 409 y la UI abre el prompt de reemplazo con motivo obligatorio; correcto.

Pruebas negativas OK (D3): tope de la guia (HTTP 400), HH extra mayor que el total, duplicado 409, rechazar sin motivo, supervisor sin botones Validar/Rechazar, bloqueo por OT sin asignacion.

Preguntas abiertas para Victor: D2-1 (bloquear fecha futura o mover el corte); desplegar y repetir D3-1; D4-1; equivalencias de cargo; D2-3, D2-5, D5-1 y D5-2; IP sin la HH de 1.1 (ya decidido); si restituir a Braulio; quien rechaza o borra los 5 RDT de prueba.

Metodo (para quien repita): la sesion se cierra con el boton «Cerrar sesion» del panel izquierdo (la pantalla de login autocompleta con Victor: reescribir correo y clave); en el formulario el tareo es `locator('table').nth(1)` (inputs: T1..Tn y HH extra) y el selector de persona admite `selectOption({label})`; los equipos viven en la tabla con `th` «HM stand-by» y su WBS en el modal `div.fixed.inset-0` (el boton «Elegir» n.º 1 es la guia de PT-02, el ultimo es 3.2); el Plan Maestro virtualiza las filas: hay que hacer scroll al fondo de sus contenedores para leer las directas; el selector de granularidad de la Curva S es un `select` (valor `diaria`).
