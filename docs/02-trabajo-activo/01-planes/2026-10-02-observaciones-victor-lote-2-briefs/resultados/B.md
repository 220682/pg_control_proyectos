# Tanda B (O6) — Importación de cronograma de punta a punta · Resultados

**ESTADO DE LA TANDA: CERRADA — B1–B7 «Conforme» (Worker 2 · tanda B).**
Fecha: 2026-10-02 · rama `local-worker-2` · worktree `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\local-worker-2` · commits `c502122` (smoke) y `a53ce5b` (esta tanda), ambos pusheados a `origin/local-worker-2` · dev server 3112 **detenido** al cerrar.

## Resolución de la pregunta anterior (servicio de prueba)

PS-0006 sigue **intacto y sin ninguna escritura** (igual que PS-0004). Por decisión del Orquestador (2026-10-02) creé un servicio de prueba nuevo por el flujo normal de la app, con la cuenta A (administrador), solo con lo mínimo que el flujo exige:

- `GET /api/proyectos/siguiente-ot` → `PS-0007`; `POST /api/proyectos` → **`PS-0007 · «PRUEBA-CRONO Importacion de cronograma»`**, uuid `479e9671-e2cb-438c-9658-4d3cdfbb7548`.
- Portafolio «Portafolio Practica» (vacío, de práctica), cliente `PRUEBA`, área `PRUEBA`, N° OC/OS `PRUEBA-NO-REAL`, adjudicación 2026-10-02, checklist solo con el documento «Cronograma» (id 16). Sin Plan Maestro, sin cronograma previo, sin datos reales de clientes u obras.

**Qué se importó (única escritura de la tanda):** el cronograma de **PS-0007**. Se cargaron y reemplazaron tres veces por los smokes (XLSX → PDF → XLSX → PDF); el estado final es `CRON-PROMCOSER-AESA-001.pdf` (78 actividades, 0 incompletas, `extraccionCompleta: true`), con su archivo en el bucket `documentos-proyecto/cronograma/<uuid>/`, la cabecera `proyecto_cronograma`, las filas de `cronograma_actividades`, `servicio_niveles`/`servicio_encabezados` (origen `CRONOGRAMA`) y el recálculo de `recalcular_pr_fechas_base`. Cero vínculos al DP (el servicio no tiene partidas), cero paquetes. Nada más se tocó: PS-0004 y PS-0006 no se escribieron.

## Estados de los ítems

| ID | Estado | Evidencia |
|---|---|---|
| B1 | Conforme | `node scripts/smoke-cronograma.mjs "<PDF>" "<XLSX>" --proyecto PS-0007` contra `npm run dev -- --webpack -p 3112`: **los dos archivos devuelven HTTP 200** con `propuesta` completa (PDF: 3 niveles, 74 filas de encabezado; XLSX: 2 niveles, 13 filas). Parámetro `soloAnalizar` verificado en `src/app/api/cronograma/route.ts:427`. La reproducción del fallo se hizo con las variantes inválidas (más abajo): todas imprimen `LO QUE VERÍA VICTOR EN PANTALLA` con `traducirErrorApi` real. Salidas en «Evidencia de smokes». |
| B2 | Conforme | Diagnóstico escrito de **formato, fase y mensaje** más abajo: los parsers **no** tienen defecto (local + API + tests verdes); el fallo estaba en la capa de mensaje (sesión caducada → HTML sin `error`, prefijo técnico en `traducir-error`) y en un único 500 real de la ruta (uuid). |
| B3 | Conforme | `src/app/api/cronograma/route.ts`: `esIdProyectoValido(proyectoId)` en el POST (`route.ts:275-284`) → **400 `El N° OT del servicio no es válido`** en lugar de `500 {"error":"invalid input syntax for type uuid: \"PS-0007\""}`; verificado con llamada real (caso A). Diff de la causa raíz de pantalla en B5. `npx tsc --noEmit` OK. |
| B4 | Conforme | Helper `logFalloImportacion` (`route.ts:151`) llamado en **17 caminos de fallo** del POST (permiso, servicio/uuid, alcance, archivo, tamaño, formato, lectura de servicio, OT no vigente, bloqueo de recarga, sin actividades, mapa de niveles, subida a storage, cabecera, actividades, niveles, encabezados, vínculos automáticos, recálculo PR) más el `catch` de lectura y el `catch` global, todos con **etapa + formato + nombre de archivo + mensaje**. Salida real del log en «Evidencia de smokes». |
| B5 | Conforme | `traducir-error.ts:26-27`: el prefijo técnico (`Error: …`, `identificador: …`) se **quita y conserva el motivo** (antes devolvía el fallback genérico). `FormularioCronograma.tsx:151` y `:186` pasan su **fallback real como 2.º argumento** (el `??` muerto ya no hace falta) y `:138-141` / `:180-181` detectan respuesta no JSON (sesión caducada) antes de traducir. Test nuevo `src/lib/errores/traducir-error.test.ts` (4 pruebas). `npx vitest run src/lib/errores` → 4/4. |
| B6 | Conforme | **Smokes reales** sobre PS-0007 (servicio desbloqueado creado para ello, ver arriba): éxito XLSX (14 act. / 10 tareas / 4 resúmenes / 0 incompletas) y éxito PDF (78 act. / 53 tareas / 23 resúmenes / 2 hitos / 0 incompletas), ambos con `extraccionCompleta: true` y persistencia verificada por `GET /api/cronograma`; fallos con motivo específico **y** log en servidor (corrupto.xlsx, nota.pdf, .txt, vacio.xlsx, mapa roto, N° OT no uuid). |
| B7 | Conforme | `npm test` → **100 archivos / 1030 tests en verde**; `npx tsc --noEmit` → OK; `npm run lint` → **0 problemas en mis archivos** (los 27 restantes —9 errors,18 warnings— son deuda preexistente de otros archivos, ninguno mío); `npx next build --webpack` → `EXIT=0`, `✓ Compiled successfully in 10.6s`. |

## Diagnóstico de causa raíz (B2): formato, fase y mensaje

**Formato — descartado.** Los dos archivos reales de `docs/06-material-de-apoyo/Informacion para pruebas/` pasan por los parsers sin error:

- `Cron-prueba N°01.xlsx` (28 626 bytes) → `exceljs` → hoja 1, cabecera en fila 6, **14 actividades, 0 incompletas**.
- `CRON-PROMCOSER-AESA-001.pdf` (723 256 bytes) → `PDFParse.getText()` → `parsearTextoPdfCronograma` → **78 actividades, 0 incompletas**; el texto extraído es idéntico al fixture `cron-promcoser-aesa-001.txt` salvo CRLF vs LF.
- Coincide con los tests ya verdes (`parser-excel.test.ts`, `niveles.test.ts`, `informe.test.ts`). Por eso **`lib/cronograma/*` no se tocó**.

**Fase — tres fases distintas, ninguna en el parser:**

1. **Antes de que corra la ruta (ésta es la pantalla genérica que veía Victor).** Con la sesión caducada, `src/middleware.ts:33-37` redirige a `/login` (HTML). La forma hace `resp.json().catch(() => ({}))` → `body.error` **undefined** → `traducirErrorApi(undefined)` → **`"Ocurrió un error"`**. Reproducido sin navegador (POST sin cookie): `HTTP 500`, `content-type: text/html`, `redirected: true`, `url final: …/login`, cuerpo JSON `{}`, pantalla `"Ocurrió un error"`.
2. **En el traductor.** `traducir-error.ts` devolvía el fallback genérico a cualquier mensaje con prefijo técnico (`^[A-Za-z_]+:` → `Error: …`, `identificador: …`), perdiendo el motivo. Hoy se quita el prefijo y se devuelve el resto (`route` y form conservan su fallback solo cuando no hay mensaje).
3. **Único 500 real de la ruta.** `POST /api/cronograma` no validaba el identificador: con `proyecto_id = PS-0007` la consulta revienta → `500 {"error":"invalid input syntax for type uuid: \"PS-0007\""}` (crudo de Postgres, en inglés). Hoy: `400 {"error":"El N° OT del servicio no es válido"}` (mismo texto que el GET, `route.ts:57-59`).

**Mensaje en pantalla (antes → después):**

| Situación | Antes | Después |
|---|---|---|
| Sesión caducada (HTML sin `error`) | `Ocurrió un error` | `Tu sesión ha expirado. Inicia sesión de nuevo para continuar con el cronograma.` |
| `Error: …` / `identificador: …` | `Ocurrió un error` | el motivo, sin el prefijo |
| `proyecto_id` no uuid | `invalid input syntax for type uuid: "PS-0007"` (500) | `El N° OT del servicio no es válido` (400) |
| Archivo ilegible / sin actividades / mapa roto / formato no soportado | motivo (ya era específico) | idem, **y ahora además queda logueado en servidor** |

## Evidencia de smokes

**B1 — análisis (`soloAnalizar=true`), los dos archivos:**

```
POST /api/cronograma -> 200   (CRON-PROMCOSER-AESA-001.pdf, 723256 bytes)
propuesta: 3 nivel(es) detectado(s), 74 fila(s) de encabezado, servicio: PRUEBA-CRONO Importacion de cronograma
PANTALLA: sin mensaje de error (la forma solo pinta `error` cuando la llamada se rechaza)

POST /api/cronograma -> 200   (Cron-prueba N°01.xlsx, 28626 bytes)
propuesta: 2 nivel(es) detectado(s), 13 fila(s) de encabezado
PANTALLA: sin mensaje de error
```

**B6 — éxito de punta a punta (análisis + guardado + persistencia):**

```
--- EXITO 1: XLSX ---(--guardar) ---
POST /api/cronograma -> 200
INFORME: totalActividades=14 tareas=10 resumenes=4 hitos=0 enlazadasADp=0 incompletas=0
extraccionCompleta: true

--- EXITO 2: PDF ---(--guardar) ---
GET previo: cronograma previo: SÍ — Cron-prueba_N_01.xlsx (14 act.)
POST /api/cronograma -> 200
INFORME: totalActividades=78 tareas=53 resumenes=23 hitos=2 enlazadasADp=0 incompletas=0
extraccionCompleta: true
GET posterior: cronograma previo: SÍ — CRON-PROMCOSER-AESA-001.pdf (pdf), 78 actividad/actividades
```

**B6 — fallos con motivo específico en pantalla:**

```
corrupto.xlsx (30 bytes, no es zip)      -> 400
  cuerpo: {"error":"No se pudo leer el archivo: Can't find end of central directory : is this a zip file ? …"}
  PANTALLA: "No se pudo leer el archivo: Can't find end of central directory : is this a zip file ? …"

nota.pdf (PDF inválido)                  -> 400
  PANTALLA: "No se pudo leer el archivo: Invalid PDF structure."

nota.txt (formato no soportado)          -> 400
  PANTALLA: "Solo se acepta Excel (.xlsx, con la plantilla de columnas) o PDF exportado de MS Project"

vacio.xlsx (sin actividades)             -> 400
  PANTALLA: "No se encontró ninguna actividad reconocible en el archivo"

mapa de niveles roto (JSON inválido)     -> 400
  PANTALLA: "El formato del mapa de niveles no es válido"

proyecto_id = "PS-0007" (no uuid)        -> 400   (antes: 500 con error crudo de Postgres)
  PANTALLA: "El N° OT del servicio no es válido"

sin cookie de sesión                     -> HTML de /login, cuerpo {}
  PANTALLA (antes): "Ocurrió un error"   →  (ahora) "Tu sesión ha expirado…"
```

**B4 — log en servidor de esos mismos fallos (salida de `dev-3112.log`):**

```
[cronograma] No se pudo leer/parsear el archivo {
  formato: 'excel', archivo: 'corrupto.xlsx',
  proyectoId: '479e9671-e2cb-438c-9658-4d3cdfbb7548',
  error: "Can't find end of central directory : is this a zip file ? …"
}
[cronograma] No se pudo leer/parsear el archivo {
  formato: 'pdf', archivo: 'nota.pdf',
  proyectoId: '479e9671-e2cb-438c-9658-4d3cdfbb7548', error: 'Invalid PDF structure.'
}
[cronograma] Importación rechazada · etapa=sin_actividades {
  formato: 'excel', archivo: 'vacio.xlsx',
  proyectoId: '479e9671-e2cb-438c-9658-4d3cdfbb7548',
  mensaje: 'No se encontró ninguna actividad reconocible en el archivo'
}
[cronograma] Importación rechazada · etapa=mapa_de_niveles {
  formato: 'excel', archivo: 'Cron-prueba N°01.xlsx',
  proyectoId: '479e9671-e2cb-438c-9658-4d3cdfbb7548',
  mensaje: 'El formato del mapa de niveles no es válido'
}
[cronograma] Importación rechazada · etapa=servicio {
  formato: null, archivo: 'Cron-prueba N°01.xlsx', proyectoId: 'PS-0007',
  mensaje: 'El N° OT del servicio no es válido'
}
[cronograma] Importación rechazada · etapa=formato {
  formato: null, archivo: 'nota.txt',
  proyectoId: '479e9671-e2cb-438c-9658-4d3cdfbb7548',
  mensaje: 'Formato no soportado (ni Excel ni PDF)'
}
```

**B7 — validación:**

```
npm test               → Test Files 100 passed (100) · Tests 1030 passed (1030)
npx tsc --noEmit       → OK (sin salida)
npm run lint           → 27 problems (9 errors, 18 warnings) — ninguno en mis archivos;
                         verificados: route.ts, traducir-error.ts(+test), FormularioCronograma.tsx,
                         smoke-cronograma.mjs → 0 problemas
npx next build --webpack → EXIT=0 · ✓ Compiled successfully in 10.6s
```

## Archivos tocados (solo los de mi fila)

- `src/app/api/cronograma/route.ts` — `esIdProyectoValido` en POST; helper `logFalloImportacion` + 17 llamadas; `proyectoId` añadido al log de lectura.
- `src/lib/errores/traducir-error.ts` — el prefijo técnico se quita y se conserva el motivo.
- `src/lib/errores/traducir-error.test.ts` — nuevo (4 pruebas).
- `src/components/ui/FormularioCronograma.tsx` — fallback real en `:151` y `:186`; detección de respuesta no JSON en `:138-141` y `:180-181`.
- `scripts/smoke-cronograma.mjs` — la cadena de pantalla solo se imprime cuando la llamada se rechaza (antes imprimía `Ocurrió un error` también en éxito).

No se tocó: `db/` ni migraciones, carril 1 (`page.tsx`, checklist, editor, catálogo), `permisos.ts`, `registro-accesos.ts`, `lib/cronograma/*`, flujos, estándar, plan, progreso ni evidencia.

## Handoff (≤15 líneas)

1. Tanda cerrada B1–B7 «Conforme»; commit `a53ce5b` pusheado a `origin/local-worker-2` (además `c502122` del smoke).
2. Dev server 3112 **detenido**; relanzar con `npm run dev -- --webpack -p 3112` desde el worktree.
3. Servicio de prueba creado: **PS-0007 «PRUEBA-CRONO Importacion de cronograma»** (`479e9671-e2cb-438c-9658-4d3cdfbb7548`), portafolio «Portafolio Practica»; queda con el cronograma PDF (78 act.).
4. PS-0006 y PS-0004 **no se escribieron** en toda la tanda (solo GET/`soloAnalizar` rechazado por el 409).
5. Uso: `node scripts/smoke-cronograma.mjs <archivo> [--guardar] [--confirmar] [--proyecto PS-0007] [--fallback TEXTO]`.
6. El script resuelve N° OT → uuid, hace login password-grant, monta la cookie y traduce con `traducirErrorApi` real; en éxito ya no imprime cadena de error.
7. `route.ts` pasó de 474 a ~610 líneas por los logs; el orden de las guardas del POST no cambió.
8. Para regenerar los fallos: `corrupto.xlsx`/`nota.pdf`/`nota.txt`/`vacio.xlsx` eran temporales ya borrados (se recrean en 2 líneas).
9. Verificación final antes de cerrar: `npm test`, `tsc`, `lint`, `next build` (todos arriba).
10. No tocar `db/`, migraciones, carril 1, permisos, flujos, plan, evidencia ni progreso.
11. Credenciales solo con `Read` en `cuentas-prueba.md`; nunca imprimirlas (no aparecen en ningún archivo de esta tanda).
12. Pendiente de decisión de Victor: ver «Observación sobre la política» 5 (middleware) y «Conflicto» 1 (otros formularios con el mismo `??` muerto).
13. El estado final de PS-0007 es el PDF; si se quiere volver al XLSX, basta reejecutar el smoke `--guardar` (pidió confirmación solo si hay vínculos/paquetes).

## Hallazgos de los cinco grupos (en el momento)

1. **Mejora de trabajo:** patrón de sesión sin navegador reutilizable (password grant → cookie `sb-<ref>-auth-token` `base64-` troceado a 3180 → llamada a la API), ya verificado y usado en los tres smokes. Candidato a `docs/03-aprendizaje-continuo/` al cierre del plan.
2. **Mejora de trabajo:** en Windows PowerShell 5.1, `Get-Content -Raw`/`Set-Content` sobre un `.mjs` UTF-8 con acentos lo corrompe (doble codificación) y `node -e "…"` rompe con las comillas de PowerShell: usar las herramientas de lectura/escritura de archivos y `.mjs` temporales.
3. **Regla de negocio acordada:** ninguna nueva. Se aplicó tal cual la RB4 de Gate 1 (motivo específico en pantalla + log en servidor con formato, nombre y mensaje).
4. **Observación sobre la política:** el brief fijaba PS-0006 sin comprobar antes si tenía Plan Maestro aprobado; el chequeo previo (misma llamada de análisis, sin escribir) debería ser un paso del brief o del Gate 1. No edito el brief: lo clasifica el Auditor y decide Victor en el Gate 2.
5. **Observación sobre la política / pregunta para el responsable humano:** la pantalla genérica «Ocurrió un error» se reproduce con la sesión caducada porque **`src/middleware.ts:33-37` redirige a `/login` también para rutas `/api/*`** (HTML, sin `error` que traducir). La mitigación quedó en la forma (mensaje de sesión expirada); corregirlo en el origen exigiría tocar `middleware.ts`, **fuera de mi carril** → lo dejo como pregunta: ¿se hace esa excepción para rutas de API o se mantiene la redirección?
6. **Conflicto/pregunta para el responsable humano:** el mismo `??` muerto (`traducirErrorApi(x) ?? '…'`, que nunca se aplica porque la función siempre devuelve string) está en `FormularioSubirRdt.tsx:55` y `FormularioPlanMaestro.tsx:244/269`. No los toqué (no son archivos de mi fila) → se propone corregirlos en su carril.
7. **Archivo o carpeta huérfano:** ninguno detectado.

## Skills revisados

Lista `.claude/skills/` de `pg_control_proyectos`: `cerrar-tanda`, `seguir-flujo-de-planes`, `trasladar-hallazgos`, `verificar-permisos-por-rol`. La app (`py_control_proyectos_web`) no tiene carpeta de Skills (comprobado en la raíz y en el worktree). `verificar-permisos-por-rol` **no aplica**: ningún cambio de permisos. `cerrar-tanda` aplicado en este cierre: estados fila por fila, evidencia con comando y resultado, traspaso ≤15 líneas, hallazgos de los cinco grupos, limpieza de temporales, `git add` uno por uno, commit en la rama del trabajador y push.

## Fuentes de verdad revisadas

Actualizadas: ninguna fuente central (esta tanda solo escribe en `resultados/B.md` y en su carril de código). Pendientes de decisión de Victor/Auditor: la observación 5 (middleware y rutas `/api/*`) y la 6 (`??` muerto en dos formularios de otro carril); la RB4 ya estaba aprobada y no se modificó.

## Número de llamadas

95 llamadas de herramienta al cerrar la tanda (incluidas lecturas, ediciones, smokes, validación, commit/push y limpieza).
