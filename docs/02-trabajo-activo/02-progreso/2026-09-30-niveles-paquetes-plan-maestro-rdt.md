# Progreso — Niveles, Paquetes, Plan Maestro (lienzo) y RDT desde el Plan Maestro

## Referencia al plan

- Plan: `docs/02-trabajo-activo/01-planes/2026-09-30-niveles-paquetes-plan-maestro-rdt.md` (19 tandas, 109 ítems, 4 carriles).
- Encargos: `docs/02-trabajo-activo/01-planes/2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/` (índice de tandas, reglas de contexto, contratos por carril, protocolo de migraciones, un brief por tanda, carpeta `resultados/`).
- Specs aprobados: `…/2026-09-30-niveles-presupuesto-y-cronograma.md`, `…/2026-09-30-paquetes-y-plan-maestro-grilla.md`, `…/2026-09-30-rdt-desde-plan-maestro.md`.
- Evidencia y auditoría: se crean cuando haya algo que registrar (`03-evidencia/` y `04-auditoria/`, mismo nombre de archivo).

## Estado general y fase actual

- Gate Spec: aprobado por Victor (2026-09-30), los tres Specs.
- Gate 1: aprobado por Victor (2026-09-30): plan, tabla de cambios a flujos en bloque, carpetas de trabajo, migraciones aplicadas por los Workers.
- Carpetas de trabajo creadas (2026-09-30, autorizadas por Victor).
- **Ola 1 lanzada (2026-09-30):** F0-A (maquetas), F1-A (carril 1, puerto 3101), F3-A (carril 2, puerto 3102) y F2-A (carril 3, puerto 3103, con las migraciones 079 a 081). Estado del plan: «Implementando». Skills revisados por el Orquestador: `seguir-flujo-de-planes`. Pendiente: medir cada sesión y consolidar sus resúmenes aquí al llegar.

## Tabla de roles / Workers y estado

| Rol | Estado |
|---|---|
| Orquestador | Activo. Este chat llegó a ~564k de contexto; se recomienda traspaso a un chat nuevo antes de lanzar la ola 1. |
| Planner | Terminó el plan (y sus dos ajustes). No tiene más trabajo pendiente. |
| Workers | Ola 1: F3-A **cerrada** (7 ítems conformes, commit `72aace7` en `local-worker-2`, `resultados/F3-A.md`). F0-A, F1-A y F2-A **cortadas a medias** por el límite de uso de la cuenta (error 429, se reinicia 4:50 pm Lima): trabajo parcial guardado, tandas NO cerradas ni medidas. |
| Auditor | No asignado (va después de F5). |

## Skills revisados

Skills de `.claude/skills/` de `pg_control_proyectos`: `cerrar-tanda`, `verificar-permisos-por-rol`, `seguir-flujo-de-planes`. El repositorio de la app no tiene carpeta de Skills (comprobado). El Orquestador usó `seguir-flujo-de-planes` al pasar el Gate 1.

## Avances terminados

- Specs, plan, Punch List, briefs y contratos por carril; subidos a `main` de `pg_control_proyectos`.
- Política nueva aplicada al estándar: carpeta `04-auditoria`, revisión de Skills, resumen de cierre por tanda, flujo SDD con enlace al artefacto visual y primera lectura obligatoria en `AGENTS.md`, Skill `seguir-flujo-de-planes`.
- Protocolo de migraciones y credenciales escrito (`00-protocolo-migraciones.md`).
- Carpetas de trabajo de la app `local-worker-2`, `-3` y `-4` creadas desde `main`; `local-worker-1` ya existía. Las cuatro en `45c9e0a`, limpias, con `node_modules` enlazado al del repositorio principal y `.env.local` copiado (autorización permanente).

## Trabajo actual

Retomar la ola 1: relanzar F0-A, F1-A y F2-A con Workers nuevos que continúen desde el trabajo parcial (ver Handoff del 2026-09-30, segundo).

## Pendientes

1. **Lanzar la ola 1** (hasta 4 Workers a la vez): F0-A (maquetas de Niveles y Paquetes, trabaja en `pg_control_proyectos`, sin carpeta de la app), F1-A (carril 1, `local-worker-1`), F3-A (carril 2, `local-worker-2`), F2-A (carril 3, `local-worker-3`; escribe **y aplica** las migraciones 079–081: es la primera en el orden). Usar la «Plantilla del prompt de lanzamiento» del índice de tandas. Cada Worker usa `cerrar-tanda` y deja `resultados/<tanda>.md`.
2. **Reglas de permiso:** el sistema de permisos denegó al Planner tocar lo relacionado con credenciales; puede bloquear también a los Workers al aplicar migraciones. Victor pidió «ir viendo lo de las reglas». **Estado (2026-09-30):** el sistema impide que un agente modifique sus propias reglas de permiso (lo denegó al intentarlo); las reglas las agrega Victor, y el Orquestador ya le entregó la lista exacta (scripts `migrar_<tanda>.py` permitidos y lectura de la carpeta de credenciales prohibida). Comprobar con Victor, **antes de la ola 2** (F1-B y F4-A aplican migraciones), que las agregó. Si el sistema pide aprobación para un script, Victor lo aprueba en el momento o lo corre él con el prefijo `!` (ver el protocolo).
3. Victor revisa las maquetas de F0-A antes de las tandas de interfaz de Niveles y Paquetes, y las de F0-B antes del lienzo y del selector del RDT.
4. Medir cada sesión de Worker con el script de `…-paneles-servicio-persistente-briefs/medicion.md` (meta: ≤ 80 llamadas, ≤ 200k de contexto).

## Commits, ramas y worktrees usados

- `pg_control_proyectos`: `main`, último commit de este trabajo `f90090d`, sincronizado con GitHub.
- `py_control_proyectos_web`: `main` = `45c9e0a`, igual a `origin/main`. Ramas y carpetas: `local-worker-1` a `local-worker-4` en `.worktrees/`, todas en `45c9e0a`. Turbopack no corre con el `node_modules` enlazado: usar `--webpack` (por eso el navegador va solo en F5).

## Hallazgos registrados en el momento

- PS-0006 ya no existe (eliminado en la limpieza del plan de paneles). Quedan PS-0004 y PS-0005; todos los servicios existentes son de prueba; F5-B crea un servicio de prueba dedicado.
- Credenciales: están en `C:\Users\BRANDY\Downloads\DIARIO\entorno_variable.txt` (nombres `PR_DB_URL` y `SUPABASE_ACCESS_TOKEN`). **No abrir ni mostrar ese archivo.** El `.env.local` de la app no las trae.
- El servidor de base de datos de Claude (`postgresql`) no conecta porque su ruta en la configuración de Victor no existe; el real está en `D:\VICTOR\CLAUDE CODE\mcp_postgresql`. No hace falta para este plan. Victor decide si se corrige.
- El artefacto «Flujo SDD a Cierre» está desactualizado (no incluye `04-auditoria` ni la revisión de Skills). Victor decide si se actualiza.
- Otra sesión dejó sin subir un cambio en `04-flujos-de-negocio/14-accesos-y-restricciones.md` (sincronización del artefacto de la matriz). No es de este plan: no tocarlo ni incluirlo en commits.
- `Trazabilidad.xlsx` (Victor lo edita) aparece modificado: no incluirlo en ningún commit.

## Bloqueos, riesgos y decisiones requeridas

- Riesgo: permisos para migraciones (ver pendiente 2).
- Abierto sin bloquear: nombre del rol extra cuando un archivo trae más de 5 niveles.
- La nota sobre el plan semanal (3WLA) en `planes-futuros.md` no se agregó; solo si Victor lo pide.

## Próximo paso verificable

Con contexto limpio: leer este archivo y el índice de tandas, lanzar la ola 1 y comprobar que cada Worker crea su `resultados/<tanda>.md`.

## Medición de Workers (script de `medicion.md` del plan de paneles; metas: ≤ 80 llamadas, ≤ 200k de contexto, ≤ 12M de caché)

| Tanda | Sesión | Llamadas | Herramientas | Contexto máx. | Caché | ¿Cumple? | Nota |
|---|---|---|---|---|---|---|---|
| F3-A | `agent-aecdc3c15a32996b` | 14 | 15 | 99k | 1,1M | Sí | Cerrada (el resumen decía ~19 llamadas; manda la medición) |
| F0-A (1.ª sesión) | `agent-a8d82746485b2169` | 17 | 32 | 140k | 1,5M | Sí | Cortada por límite de uso |
| F1-A (1.ª sesión) | `agent-a46c4b15b573649e` | 12 | 22 | 114k | 0,9M | Sí | Cortada por límite de uso |
| F2-A (1.ª sesión) | `agent-a02847794eaaf438` | 23 | 25 | 117k | 2,0M | Sí | Cortada por límite de uso |

## Ola 1, relanzamiento (2026-09-30, tarde)

Verificado con comandos antes de relanzar: `local-worker-1` en `61cdc02` (WIP F1-A, 9 archivos), `local-worker-2` en `72aace7` (F3-A), `local-worker-3` en `3dd2c00` (WIP F2-A, 8 archivos), `local-worker-4` intacta en `45c9e0a`; `main` de la app = `origin/main`; `pg_control_proyectos` sincronizado, solo `Trazabilidad.xlsx` modificado (no se incluye). Relanzados tres Workers (F0-A, F1-A, F2-A) con la instrucción de revisar el WIP y no rehacerlo; F2-A comprueba primero si las migraciones 079 a 081 ya existen en la base.

### Resultados consolidados de la ola 1

- **F0-A (maquetas de Niveles y Paquetes): cerrada, 7 de 7 ítems conformes** (`resultados/F0-A.md`). El Worker revisó el WIP `d0b700e` contra el brief y no hizo falta corregir nada. Verificación solo estructural (sin navegador, según el brief); el Orquestador comprobó además que en el ejemplo de 5 niveles el nivel 2 propone «Área». **Nadie ha abierto las maquetas a simple vista: Victor las revisa.** Seis preguntas de diseño para Victor en el resultado. Al aprobar: quitar «pendiente de aprobación» en `design.md` y `mockups/README.md`. Sin hallazgos nuevos. Sesión de cierre: 8 llamadas (medición del script pendiente de anotar).

## Última actualización y responsable

2026-09-30, Orquestador.

## Handoffs

### Handoff del 2026-09-30 (Orquestador → Orquestador con contexto limpio)

- **Objetivo y estado:** ver «Estado general». Gate 1 cumplido; carpetas listas; ola 1 sin lanzar.
- **Qué leer, en este orden:** la sección «Flujo con Orquestador» de `AGENTS.md` (con su primera lectura obligatoria) y el Skill `seguir-flujo-de-planes`; este archivo; `…-briefs/00-indice-de-tandas.md`, `00-reglas-de-contexto.md` y `00-protocolo-migraciones.md`. **No** releer los 21 flujos ni los tres Specs completos: los Workers leen solo lo que su brief nombra.
- **Terminado y no terminado:** ver «Avances terminados» y «Pendientes».
- **Pruebas ejecutadas:** ninguna de código todavía (no hay Workers lanzados). Se verificó: sincronización de ambos repositorios, carpetas de trabajo limpias, tamaños de briefs ≤ 8 KB.
- **Cómo habla Victor y cómo hay que hablarle:** lenguaje simple, sin códigos internos de ítems ni siglas, una decisión por pregunta con recomendación; verificar antes de afirmar; no declarar cerrado nada sin la lista de verificación del Skill.
- **Límites:** el Orquestador no implementa, no hace merge ni push de la app sin autorización en el Gate 2, no edita `AGENTS.md` ni los flujos por su cuenta.
- **Próximo paso concreto:** lanzar F0-A, F1-A, F2-A y F3-A con la plantilla del índice.

### Handoff del 2026-09-30 (segundo: Orquestador → Orquestador con contexto limpio)

- **Estado de la ola 1:** F3-A cerrada y verificada (commit `72aace7`, árbol limpio, 696 pruebas, `tsc` en 0; el lint lo tomó igual a `main` sin compararlo). Las otras tres se cortaron por límite de uso de la cuenta; ninguna escribió su `resultados/<tanda>.md`.
- **Trabajo parcial guardado (sin verificar, hay que revisarlo antes de seguir):**
  - F0-A: sin commit en `pg_control_proyectos` (se subió como «WIP F0-A» junto con este traspaso): maquetas `cronograma-niveles.html`, `importar-dp-niveles.html`, `paquetes-agrupar.html`, `paquetes-declarar.html`, más cambios a `design.md`, `mockups/README.md` e `index.html`. Falta comprobar contra el brief `f0-tanda-a.md` qué ítems están completos.
  - F1-A: commit `61cdc02` «WIP» en `local-worker-1` con `src/lib/niveles/**` (9 archivos, con pruebas). Sin verificar `npm test`/`tsc`.
  - F2-A: commit `3dd2c00` «WIP» en `local-worker-3` con `db/079`–`081` y `src/lib/paquetes-trabajo/` (5 archivos). **No se sabe si las migraciones 079–081 se aplicaron** (no hay resultado ni candado en `resultados/`); el Worker nuevo debe comprobarlo con `select 1` y consultas de existencia antes de aplicar, sin asumir.
- **Cómo retomar:** lanzar Workers nuevos con la plantilla del índice, añadiendo al prompt: «Hay trabajo parcial ya commiteado como WIP: revísalo contra tu brief, completa lo que falte y no lo rehagas». Puertos de prueba usados: 3101 a 3103 (el índice no los fija; el brief de F3-A dice 3112, sin efecto).
- **Límite de uso:** el reinicio fue 4:50 pm (Lima). Con 4 Workers a la vez se agotó la cuenta; considerar lanzar 2 o 3 a la vez.
- **Medición:** pendiente con `medicion.md` del plan de paneles; mide F3-A y las tres cortadas (anotar «cortada por límite»).
- **Commits:** nada de la app subido (sin push, sin merge). Ramas `local-worker-1` y `-3` con un commit WIP cada una; `local-worker-2` con F3-A; `-4` intacta.
- **Pendientes de Victor sin cambios:** reglas de permiso antes de la ola 2; maquetas de F0-A a su revisión; rol extra con más de 5 niveles; ruta del servidor de base de datos; nota 3WLA solo si la pide. Hallazgo nuevo (de F3-A): usar `git stash -u` en un árbol compartido es riesgoso (mejora de trabajo, consolidar al cierre).
