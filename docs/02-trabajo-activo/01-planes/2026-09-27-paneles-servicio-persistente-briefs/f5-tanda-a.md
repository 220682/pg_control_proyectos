# F5-A · Pruebas automáticas: cobertura de pantallas, integridad, humo, matriz derivada y redirects

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F5 · **Depende de:** F4B-C cerrada (F1 a F4B completas).
**Punto de commit:** Al cerrar la fase F5 (fin de esta tanda).
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-53 | Prueba de humo automática: una función pura recibe un registro con **una** entrada de prueba nueva y esa entrada aparece en panel izquierdo, panel derecho, Mi entorno, con `?proyectoId=`, con estado por permiso y como fila de la matriz | `npm test` |
| PL-55 | Prueba de cobertura: falla si existe una pantalla del workspace sin entrada en el registro ni excepción declarada. Se demuestra en rojo (página temporal, sin commitearla) y en verde | Salida de `npm test` en rojo y en verde |
| PL-56 | Función de matriz derivada del registro: produce roles × accesos; se **compara** con la matriz base del flujo 14 y las diferencias quedan listadas en la evidencia (la matriz base es la fuente: el registro se ajusta a ella, no al revés) | Lista de diferencias |
| PL-57 | Prueba de fuente: ningún `redirect('/mi-entorno')` ni enlace literal a una pantalla de servicio en el workspace pierde el servicio (o está en una lista de excepciones con motivo) | `npm test` |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- vitest: entorno `node`, `include: src/**/*.test.ts`; no hay jsdom ni pruebas de componentes. Todo es prueba pura sobre el registro y sobre el sistema de archivos de Node.
- **PL-55:** `src/lib/config/cobertura-pantallas.test.ts` recorre `src/app/**/page.tsx` con `fs` (45 pantallas verificadas en 1942b01, incluidas `src/app/page.tsx`, `(inicio)/login`, `(inicio)/auth/activar` y `src/app/programas/[id]/portafolios/[portafolioId]/dashboard`, esta última fuera de `(workspace)`) y **falla** si una pantalla no está en el registro ni en la lista de excepciones con motivo (`/login`, `/auth/activar`, `/admin/usuarios`, `/configuraciones`, `/mi-perfil`, `/programas/**`, raíz…). Demuéstralo en rojo con una pantalla temporal (p. ej. `src/app/(workspace)/_prueba-cobertura/page.tsx`, sin commitear; bórrala tú, que la creaste) y en verde.
- **PL-53:** prueba de humo: función pura recibe un registro con **una** entrada nueva; aparece en panel izquierdo, derecho, Mi entorno, con `?proyectoId=`, con estado por permiso y como fila de la matriz.
- **PL-56:** función de matriz roles × accesos derivada del registro; se **compara** con las tablas 1 y 2 de `D:\VICTOR\CLAUDE CODE\pg_control_proyectos\docs\04-flujos-de-negocio\14-accesos-y-restricciones.md` (leídas del archivo) y las diferencias se listan en la evidencia (la matriz base manda; el registro se ajusta a ella).
- **PL-57:** prueba de fuente: ningún `redirect('/mi-entorno')` ni enlace literal a pantalla de servicio en el workspace pierde el servicio, salvo excepciones con motivo.
- Contadores: actualiza los que fijen números (aprendizaje 2026-09-23, R12).

## Qué NO hacer

- No cambies permisos. Las pantallas temporales no se commitean.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
