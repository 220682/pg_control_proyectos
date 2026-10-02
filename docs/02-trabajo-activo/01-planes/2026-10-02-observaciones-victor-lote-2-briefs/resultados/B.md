# Tanda B (O6) — Importación de cronograma de punta a punta · Resultados

**ESTADO DE LA TANDA: DETENIDA — pregunta devuelta al Orquestador. Este archivo NO es un cierre.**
Fecha: 2026-10-02 · Worker 2 · rama `local-worker-2` · worktree `.worktrees/local-worker-2` · commit `c502122` (push a `origin/local-worker-2` hecho) · dev server puerto 3112 (detenido al abandonar).

## Pregunta devuelta (bloqueante)

**PS-0006 tiene Plan Maestro APROBADO y la recarga del cronograma queda bloqueada (409) ANTES de llegar al parser.** El bloqueo es de la propia app (`decidirRecarga`, contrato C1) y no se puede confirmar ni saltar: `bloqueadoPorPlanAprobado: true` ignora `confirmarPerdida`.

Evidencia (POST real con `soloAnalizar=true`, sin escribir nada):

```
POST /api/cronograma -> 409
{
  "error": "No se puede volver a cargar el cronograma: el servicio tiene un Plan Maestro aprobado.",
  "bloqueadoPorPlanAprobado": true,
  "perderia": { "vinculos": 48, "paquetes": 4, "planMaestroBorrador": true }
}
LO QUE VERÍA VICTOR EN PANTALLA: "No se puede volver a cargar el cronograma: el servicio tiene un Plan Maestro aprobado."
BLOQUEO: el servicio tiene Plan Maestro APROBADO.
```

Sondeo de alternativas (solo lectura, `soloAnalizar=true` en todos los servicios no archivados): **solo existen 2 servicios vigentes y los dos están bloqueados por igual**:

```
servicios vigentes: 2
PS-0004 | Movimiento de tierra, e instalacion de bancoductos | cronograma previo: SÍ (cronograma_PS-0004_consecutivo_06-ago_a_26-sep-2026XX.xlsx, 65 act.) | BLOQUEADO por Plan Maestro APROBADO
PS-0006 | PRUEBA-F5B Servicio de verificacion | cronograma previo: SÍ (PRUEBA-cronograma.xlsx, 65 act.) | BLOQUEADO por Plan Maestro APROBADO
total no archivados: 2   (los archivados no sirven: la API responde «OT no vigente»)
```

**Opciones:**

1. **(Recomendada)** Victor retira/deshace la aprobación del Plan Maestro de **PS-0006** por la vía que él elija (no toco la BD; en el código no vi endpoint de des-aprobación: `PUT /api/plan-maestro` solo aprueba y archiva versiones) → ejecuto la tanda completa sobre PS-0006 como prevé el brief. Aviso: PS-0006 ya tiene cronograma previo (65 actividades, 48 vínculos, 4 paquetes, borrador de PM), así que la recarga pedirá `confirmarPerdida=true` y **eso destruiría esos vínculos/paquetes/borrador**; lo haría solo con tu confirmación explícita.
2. Victor crea/deja libre **otro servicio de prueba sin PM aprobado** e indica el N° OT → corro los dos smokes ahí y anoto qué se importó.
3. Victor autoriza de forma explícita un **reset del estado del PM de PS-0006** por la vía que indique (BD por protocolo de migraciones, que es de la tanda A).
4. Aplazar B1/B6 (los dos smokes) y que la tanda arranque por B2–B5, que son independientes del proyecto (parsers y mensajes, sin BD).

Con 1, 2 o 3 puedo continuar sin cambiar nada del brief; con 4 solo se cierran los ítems de código.

## Estados de los ítems

| ID | Estado | Evidencia / motivo |
|---|---|---|
| B1 | Observado | `scripts/smoke-cronograma.mjs` creado, lint OK y ejecutado contra `npm run dev -- --webpack -p 3112` con `soloAnalizar=true` en los dos archivos; **la reproducción del fallo no llegó al parser**: ambas llamadas devuelven 409 por Plan Maestro aprobado (salida completa arriba). Parametro `soloAnalizar` verificado en `src/app/api/cronograma/route.ts:348`. |
| B2 | Pendiente | No diagnosticado: exige llegar al parser (exceljs/PDFParse), que el 409 corta antes. Es local (sin BD), se puede hacer en cuanto se desbloquee o se autorice la opción 4. |
| B3 | Pendiente | Sin cambio de código todavía (no hay causa raíz diagnosticada). |
| B4 | Pendiente | El `console.error` de la ruta de lectura sigue en `route.ts:314` (único log hoy). |
| B5 | Pendiente | `traducir-error.ts:23` sigue devolviendo el fallback para mensajes con prefijo técnico; `FormularioCronograma.tsx:133` y `:164` siguen con `??` muerto; no existe `traducir-error.test.ts`. |
| B6 | Observado | Smoke de éxito **imposible** sobre PS-0006 mientras tenga PM aprobado (ver pregunta). Smoke de fallo pendiente por la misma causa. |
| B7 | Pendiente | Corrida de `npm test` / `tsc` / `lint` / `build` completa al reanudar (solo `npx eslint scripts/smoke-cronograma.mjs` → OK). |

## Evidencia disponible

**Sesión sin navegador (patrón verificado, sin navegador):**

```
--- 1. Sesión (password grant, sin navegador) ---
login HTTP 200 · cuenta administradora autenticada
cookie: sb-ppdaawrtuqkfzpozmtyc-auth-token (2672 chars, 1 trozo/s, formato base64- de @supabase/ssr)
--- 2. Resolución del servicio PS-0006 ---
GET /api/proyectos/vigentes -> 200; PS-0006 = uuid 51f5905b-6198-46b3-a3d3-abd4793c0e7c · PRUEBA-F5B Servicio de verificacion
--- 3. Estado previo del servicio PS-0006 (uuid 51f5905b-6198-46b3-a3d3-abd4793c0e7c) ---
GET /api/cronograma -> 200
cronograma previo: SÍ — PRUEBA-cronograma.xlsx (excel, cargado 2026-10-01T16:24:46.215+00:00), 65 actividad/actividades, enlazadas al DP: 57
```

Formato del cookie verificado contra `node_modules/@supabase/ssr/dist/main/cookies.js`: valor `base64-` + base64url del JSON de sesión, troceado a 3180 (`createChunks`), nombre `sb-<hostname[0]>-auth-token` (SupabaseClient.ts: `sb-${hostname.split('.')[0]}-auth-token`). Credenciales leídas solo con `Read` en `cuentas-prueba.md`; nunca impresas ni escritas.

**Salida del smoke de éxito:** no existe todavía (bloqueado).
**Salida del smoke de fallo:** no existe todavía (bloqueado).

## Qué se importó en PS-0006

**Nada.** Cero escrituras: todas las llamadas de análisis/sondeo fueron rechazadas por el 409 o fueron GET/`soloAnalizar`. PS-0006 queda exactamente como estaba (cronograma previo `PRUEBA-cronograma.xlsx`, 65 actividades, 57 enlazadas al DP).

## Diagnóstico de causa raíz

No alcanzado (B2). Lo único diagnosticado hasta ahora es el bloqueo de recarga (arriba) y el hallazgo técnico 5 de abajo.

## Handoff (≤15 líneas)

1. Tanda DETENIDA en la pregunta de arriba; no se cerró ningún ítem como Conforme.
2. Dev server 3112 detenido; relanzar con `npm run dev -- --webpack -p 3112` desde el worktree.
3. `scripts/smoke-cronograma.mjs` está commiteado (`c502122`) y pusheado; uso: `node scripts/smoke-cronograma.mjs <archivo> [--guardar] [--confirmar] [--proyecto PS-0006] [--fallback TEXTO]`.
4. El script resuelve solo el N° OT → uuid (`/api/proyectos/vigentes`), hace login password-grant, monta el cookie y traduce el cuerpo con `traducirErrorApi` real (importado del TS).
5. Para reproducir el fallo (B1) basta `node scripts/smoke-cronograma.mjs "<PDF>" "<XLSX>"` con el servicio desbloqueado.
6. B2 no necesita BD: exceljs → `parsearExcelCronograma(hoja)` y `PDFParse.getText()` → `parsearTextoPdfCronograma(texto)` con los archivos reales de `docs/06-material-de-apoyo/Informacion para pruebas/`.
7. El bloqueo es previo al parser (`route.ts:284-292`), así que ninguna opción de confirmación lo abre.
8. Ambos servicios vigentes (PS-0004, PS-0006) están bloqueados; los archivados no sirven («OT no vigente»).
9. No tocar `db/`, migraciones, carril 1, permisos, flujos, plan, evidencia ni progreso.
10. Recuerda: credenciales solo con `Read` en `cuentas-prueba.md`; nunca imprimirlas.
11. Si se reanuda, actualizar esta tabla de estados y completar smokes de éxito y fallo antes de cerrar.

## Hallazgos de los cinco grupos (en el momento)

1. **Mejora de trabajo:** patrón de sesión sin navegador ya verificado y reutilizable (password grant → cookie `sb-<ref>-auth-token` `base64-` troceado a 3180 → llamada a la API). Queda anotado para trasladar a `docs/03-aprendizaje-continuo/` al cierre.
2. **Mejora de trabajo:** en Windows PowerShell 5.1, `Get-Content -Raw` + `Set-Content` sobre un `.mjs` UTF-8 con acentos lo corrompe (doble codificación `Ã³`); usar la herramienta de edición de archivos, no cmdlets de texto.
3. **Regla de negocio acordada:** ninguna nueva. La RB4 (motivo específico en pantalla + log en servidor con formato, nombre y mensaje) ya venía aprobada en Gate 1.
4. **Observación sobre la política:** el brief fija PS-0006 para el smoke sin comprobar antes si el servicio está bloqueado por Plan Maestro aprobado; el chequeo previo (misma llamada de análisis, sin escribir) debería ser un paso del brief o del Gate 1 para no gastar la tanda. No edito el brief: lo clasifica el Auditor y decide Victor en el Gate 2.
5. **Conflicto/pregunta para el responsable humano:** la pregunta de arriba (bloqueo de PS-0006). **Técnico, en mi carril:** `POST /api/cronograma` no valida `esIdProyectoValido(proyectoId)` (sí lo hace el GET en `route.ts:57-59`), así que un N° OT en lugar de uuid devuelve `500 {"error":"invalid input syntax for type uuid: \"PS-0006\""}` con el error crudo de Postgres en lugar de un 400 limpio; candidato a corregir dentro de B3/B4 si el Orquestador lo autoriza.
6. **Archivo o carpeta huérfano:** ninguno detectado.

## Skills revisados

Lista `.claude/skills/` de `pg_control_proyectos`: `cerrar-tanda`, `seguir-flujo-de-planes`, `trasladar-hallazgos`, `verificar-permisos-por-rol`. La app (`py_control_proyectos_web`) no tiene carpeta de Skills (comprobado en la raíz y en el worktree). `verificar-permisos-por-rol` **no aplica**: ningún cambio de permisos. `cerrar-tanda` leído: sus pasos 1, 3 y 4 se aplican aquí solo en la medida de lo posible porque **la tanda no se cerró** (pasos de estados, evidencia y traspaso); los pasos de commit/push quedan hechos para el script (`c502122`).

## Número de llamadas

71 llamadas de herramienta al detener la tanda (incluidas las de limpieza y verificación del commit).
