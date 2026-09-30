# F5-A · Integración: unir los cuatro carriles y pruebas cruzadas

Lee primero `00-reglas-de-contexto.md`. **Carril de integración** · rama `local-worker-1` (la del carril 1, ya con los merges de los carriles 3, 2 y 4 hechos **por el Orquestador**, en ese orden), puerto 3111.
Fase F5 · **Depende de:** todas las tandas de F1 a F4 cerradas y merges hechos. Contrato: `00-contratos-tecnicos.md` (todas las secciones: léelas por Grep según necesites).
**Eres el único que puede editar los archivos congelados** (`permisos.ts`, `registro-accesos.ts`, pruebas de `src/lib/config/`, `db/README.md`).
**Punto de commit:** al cerrar la tanda, en `local-worker-1`.

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| F5A-1 | La rama integrada compila sin conflictos sin resolver; los conflictos que aparecieron (se esperan ninguno por la matriz de propiedad) están resueltos con el criterio del dueño del archivo y anotados. `db/README.md` lista las migraciones 073 a 084 con su orden de aplicación | `git status`, diff de `db/README.md` |
| F5A-2 | `npm test`, `npx tsc --noEmit`, `npm run lint` (comparado con el total medido en `main` `45c9e0a`, que mides tú primero) y `npx next build --webpack` en verde; sin deuda de lint nueva en los archivos tocados | Salida de comandos |
| F5A-3 | **Prueba cruzada del anexo de 4 semanas** de punta a punta en un archivo nuevo de pruebas: paquetes con una partida repartida → líneas del Plan Maestro → totales semanales y acumulados → planificado del PR (suma por partida) → PV de la Curva S; los números del anexo salen exactos | Prueba verde |
| F5A-4 | **Prueba cruzada del RDT**: el real se atribuye al paquete × partida; el PR suma por partida aunque esté en dos paquetes; la clave sigue igual tras una versión nueva del Plan Maestro | Prueba verde |
| F5A-5 | Los datos simulados se reemplazan por los reales: las pantallas de Paquetes, lienzo y selector del RDT consumen `NodoEstructura[]` de `src/lib/niveles/`; `reales` del lienzo sale de `realPorClaveReporte`; sin adaptadores vacíos | Diff + pruebas |
| F5A-6 | Permisos y accesos: las pruebas existentes de `registro-accesos`, `matriz-accesos`, `panel-*` y `nav-proyecto` siguen verdes **sin chip nuevo**; `puedeCrearVersionPlanMaestro` (administrador y jefe de proyectos) probada con los 13 roles; la acción «Crear paquete» del panel abre Paquetes en modo crear | Pruebas verdes |

## Contrato técnico verificado (2026-09-30, `45c9e0a`)

- Orden de merges (Orquestador): carril 3 → carril 2 → carril 4 sobre `local-worker-1`. Migraciones: Victor las aplica **después** de esta tanda (checkpoint); tú solo verificas que los archivos existen, están en orden y no se pisan.
- Baseline de lint: hay que medirlo en `main` antes de comparar (el 2026-09-23 eran 9 errores y 18 avisos; hoy puede ser distinto). `npm run build` con Turbopack no corre en worktrees con `node_modules` enlazado: usa `--webpack`.
- Restricciones que ya rigen: el motor del PR, el Dashboard y la Curva S no se modifican; todo en USD y costo directo.
- Los totales y fórmulas salen de `00-contratos-tecnicos.md` § C3 y del Anexo del Spec.

## Qué NO hacer

- No apliques migraciones. No hagas push ni merge a `main` (lo hace el Orquestador tras el Gate 2). No crees chips ni accesos.
- No cambies contratos: si una prueba cruzada muestra que un contrato falla, detente y devuelve la pregunta.
- Ante contradicción con un flujo, acción destructiva o duda de negocio: detente y devuelve la pregunta.

## Cierre

`resultados/F5-A.md` (estado de F5A-1 a F5A-6, conflictos y cómo se resolvieron, handoff, llamadas). Commit en `local-worker-1`, `git add` explícito.
