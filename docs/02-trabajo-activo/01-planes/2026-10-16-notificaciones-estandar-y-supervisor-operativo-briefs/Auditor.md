# Brief del Auditor — Plan Notificaciones

## Rol, modelo y tanda

Auditor · Sonnet · esfuerzo medio. Se lanza como «Auditor · Notificaciones». Solo lee y verifica: **no implementa, no hace merge, no edita flujos ni código, no aprueba por Victor y no borra nada**. Su único archivo de salida es el informe.

## Qué entrega

Un informe propio en `D:\VICTOR\CLAUDE CODE\pg_control_proyectos\docs\02-trabajo-activo\04-auditoria\2026-10-16-notificaciones-estandar-y-supervisor-operativo.md` (mismo nombre base que el plan), con la plantilla `docs/00-estandar-agentes/06-plantillas/06-informe-auditoria.md` y las secciones que exige `docs/00-estandar-agentes/02-roles-y-delegacion.md` § Auditor: `APLICAR AHORA`, `PROPONER A RESPONSABLE`, `NO PROMOVER`, `PROPONER SKILL`, pendientes técnicos y documentales, y **recomendación de estado** (listo / bloqueado / requiere corrección). Sin la clasificación de hallazgos el informe no vale.

## Qué verificar (en este orden; con comandos, no de memoria)

1. **Primer chequeo:** que toda la implementación está en la rama `local-worker-7` del repo de la app (`D:\VICTOR\CLAUDE CODE\py_control_proyectos_web`, worktree `.worktrees/local-worker-7`; usa `git log --oneline main..local-worker-7`, `git branch --contains <commit>` para `cc44f47`, `814efb4`, `c067583`, `69ce6aa`, `817e9d8`, `bcba4da`, `853bf57`, `e3c4dfa`, `04739ec`, `041e9e4`, `b6017c2`, `9529853`, `83bd0f9`, `21a0e59`, `1d036ec`, `85626fd`, `9611338`), que **no** está en `main` y que cada tanda la hizo un Worker separado (los resúmenes de cierre lo dicen). Si falla, detente y repórtalo.
2. **Segundo chequeo:** en el plan (`...\01-planes\2026-10-16-notificaciones-estandar-y-supervisor-operativo.md`), ninguna fila del libro de hallazgos queda en `Registrada` (solo se admiten «Trasladada» y las abiertas que esperan decisión de Victor, listadas); los apartados de mejoras, reglas, observaciones sobre la política y huérfanos están llenos y trasladados; las mejoras de trabajo están en `docs/03-aprendizaje-continuo/` y las reglas de negocio integradas en los flujos.
3. **Trazabilidad con el plan:** cada ítem de la Punch List (T1-xx a T9-xx) tiene estado y evidencia: contrasta con los resúmenes `resultados/*.md` y las capturas de `...\03-evidencia\2026-10-16-notificaciones-estandar-y-supervisor-operativo\t7\`. Lista los ítems sin verificar, los Observados y los que cambiaron de alcance.
4. **Política de coherencia (AGENTS.md):** cada regla nueva o cambiada del plan aparece en el flujo afectado (04, 05, 06, 12, 14, 16, 02, 03, 07, 08) y la tabla `coherencia-flujos-codigo.md` coincide con el código real (revisa por muestreo 6 eventos del catálogo `src/lib/notificaciones/catalogo.ts` contra el flujo 04). Comprueba que el flujo 14 y la «Matriz de permisos» van juntos: el artefacto no pudo abrirse con la cuenta del Orquestador (`resultados/T8B.md` trae las filas exactas) → repórtalo como pendiente de Victor, no como cumplido.
5. **Calidad y seguridad de código (por muestreo, solo lectura):** (a) validación en servidor y permisos en `api/perfil/*`, la acción `devolver`/`reenviar`/`corregir` del RQ y `revisar`; (b) ninguna contraseña se registra ni se devuelve; (c) las migraciones `db/108_notificaciones_evento_entorno.sql` y `db/109_rq_devuelto.sql` son aditivas e idempotentes y ya están **aplicadas por Victor** (lo confirmó el 2026-10-18); (d) no hay secretos en los dos repos (`git grep` de patrones obvios, sin imprimir valores) ni claves de las cuentas de prueba en archivos del repo documental (busca los correos de prueba con clave cercana; las claves viven solo en la memoria local, que **no debes leer**); (e) `cobertura-avisos.test.ts` (`SITIOS`) al día.
6. **Verificación independiente de pruebas:** en el worktree, `npm test`, `npm run lint` (9 errores previos ajenos al plan: confirma que son los mismos con `git stash`-free: compara con `git diff main..local-worker-7 --stat` que ninguno de los archivos con error fue tocado) y `npx tsc --noEmit`.
7. **Git de ambos repos:** estado de `main` de la app (debe seguir en `69ebf94` o el que corresponda; reporta cuántos commits lleva `local-worker-7` por delante, y qué ramas de otros planes (Cronograma `local-worker-6`, permisos `local-worker-5`) podrían chocar con los archivos tocados: lista los archivos en común con `git diff --name-only`); en el repo documental, `git status` y `git rev-list --left-right --count origin/main...main`; separa lo que es de este plan de los cambios ajenos sin commitear (flujos 09, 14 parcial, 16 parcial, 18, 19, 20, 22, `design.md`, mockups: **no son de este plan; no los incluyas ni los toques**).
8. **Riesgos para el merge:** lista lo que Victor debe saber antes de aprobar subir el código: migraciones ya aplicadas (108, 109) que el código viejo en producción tolera o no (el código de `main` actual ¿rompe con `proyecto_id` nulo o con `DEVUELTO`? lee dónde `main` consume `notificaciones` y `proyecto_requerimientos.estado`), avisos viejos sin referencia, datos de prueba que quedan en producción (servicio PS-0005, RQ -002 y -003 de `PS-0000`, RDT de prueba y mensajes) y lo que falta limpiar.

## Qué leer, y qué no

Lee el plan (completo), `resultados/*.md` (T1A, T1B, T1C, T2, T3, T4, T5, T6, T6b, T7A, T7B, T7C, T7fix, T8A, T8B), el progreso, el libro de hallazgos y los flujos tocados. **No leas** `.env.local`, ni la memoria local de cuentas, ni `.playwright-mcp/`. No uses el navegador.

## Límites

80 llamadas como meta. Si encuentras algo bloqueante, dilo primero en el informe. No resuelvas dudas de negocio: lístalas en `PROPONER A RESPONSABLE`. Commitea solo tu informe con `git add` explícito (rama `main`, mensaje en español terminado en `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`), sin push.

## Criterios de salida

Informe emitido como archivo propio con la clasificación completa y una recomendación de estado clara; commit solo del informe.
