# Scripts

Herramientas locales del repositorio de documentación. Ninguna usa el contenido de los planes de forma destructiva: solo leen, miden o consultan.

| Script | Para qué | Quién lo usa | Documento |
|---|---|---|---|
| `medir.py` | Mide sesiones de agentes: llamadas, tokens por tipo, modelo y contexto máximo, agrupados por tanda, Worker, rol y total | El Orquestador, por evento | `docs/00-estandar-agentes/08-medicion-y-relevo.md`, `docs/01-contexto-repositorio/09-medicion-y-modelos.md` |
| `arranque.py` | Mide el contexto con el que **arranca** cada sesión (el de su primera llamada: `AGENTS.md`, bloque de Skills y brief) y cuánto crece por su cuenta; con `--bloques` muestra de qué herramienta vino ese contexto | El Orquestador y el Analista del flujo, al revisar el arranque de un plan | `docs/00-estandar-agentes/08-medicion-y-relevo.md`, `docs/01-contexto-repositorio/09-medicion-y-modelos.md` |
| `niveles-modelos.py` | Mide el consumo de tokens y costo por modelo desde la base de opencode y los reparte en los **cinco niveles**; `--niveles N`, `--modelo <subcadena>`, `--dir <ruta>`, `--json` | El Orquestador, al elegir modelo para una tanda | `docs/00-estandar-agentes/10-niveles-de-modelos.md` |
| `esperados_rdt_ps0001.py` | Calcula los valores **esperados** de la prueba del RDT en PS-0001 (EV, PV, AC, HH, IP por día) desde el presupuesto y el cronograma, sin usar la app, y con `--comparar` los contrasta con lo observado | El Orquestador y quien corra la prueba v2 | `docs/02-trabajo-activo/06-pruebas/04-prueba-rdt-ps0001-v2-guion.md` |
| `prueba_rdt_ps0001/limpiar.py` (+ `comun.py`) | Playwright en Python, sin agentes: inicia sesión con las variables `PG_CORREO` y `PG_CLAVE`, lista y borra (`--borrar`) los RDT de PS-0001 por la API de la app; guarda respaldo JSON en `salida/` (ignorada por git) | Victor, antes de repetir la prueba v2 | `docs/02-trabajo-activo/06-pruebas/04-prueba-rdt-ps0001-v2-guion.md` |
| `verificar-referencias.py` | Comprueba que ningún documento quede sin enlazar y que ningún enlace esté roto | El Documentador antes de cerrar; el Auditor lo comprueba | `docs/00-estandar-agentes/02-roles-y-delegacion.md` |
| `verificar.ps1` | Consulta al verificador (Jev) antes de una acción irreversible; reúne los hechos con git y con el plan | El hook o el Orquestador | `docs/00-estandar-agentes/07-verificador-de-acciones.md`, `docs/01-contexto-repositorio/07-jev-verificador.md` |
| `hook-verificar.ps1` | Adaptador del hook `PreToolUse`: decide qué órdenes pasan por el verificador. **No está registrado en ninguna configuración** | El hook | `docs/01-contexto-repositorio/07-jev-verificador.md` |
