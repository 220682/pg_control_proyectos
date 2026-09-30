# F1-C · Niveles: pantallas de confirmación, aviso de recarga y consumidores propios

Lee primero `00-reglas-de-contexto.md`. Carril **1 · Niveles** · rama `local-worker-1`, puerto 3111.
Fase F1 · **Depende de:** F1-B cerrada **y de la maqueta aprobada por Victor**: `mockups/importar-dp-niveles.html` y `mockups/cronograma-niveles.html` (F0-A). Sin maqueta aprobada, no empieces.
**Punto de commit:** al cerrar la tanda, en `local-worker-1`.

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| F1C-1 | Importar DP muestra el **paso de confirmación de niveles** según la maqueta: cuenta de niveles, lista en orden, fila de muestra por grupo con desplegable de rol, propuesta por defecto, filas «para revisar», aprobar | Lógica en módulo puro con prueba; `tsc` y build |
| F1C-2 | El cronograma tiene el mismo paso con sus roles. **Se retira de su pantalla** el bloque de vínculos con metrado, la lista «partidas incompletas» y la columna Hito (pasan a Paquetes, F2); la carga y la vista quedan | Prueba de la lógica + build |
| F1C-3 | **Aviso de recarga** en DP y cronograma: con Plan Maestro aprobado, bloqueo con mensaje; sin él, lista de lo que se perdería y confirmación explícita (`confirmarPerdida`) | Prueba de la lógica de mensajes |
| F1C-4 | Las pantallas **DP y PR agrupan según el mapa** (archivos propios: `proyectos/[id]/dp/**` y `proyectos/[id]/pr/page.tsx`), con el mismo aspecto para servicios de 3 niveles típicos | Prueba de equivalencia + build |
| F1C-5 | Estados **vacío, carga y error**, móvil (390 px) y accesibilidad del paso de niveles; `npx tsc --noEmit`, suite, lint comparado con `main` y `next build --webpack` | Salida de comandos |

## Contrato técnico verificado (2026-09-30, `45c9e0a`)

- Pantalla de importar DP: `src/app/(workspace)/proyectos/[id]/dp/importar-dp.tsx` (lista los `errores` de la API) y `dp/page.tsx` (usa `agruparPorSubpresupuesto`). PR: `proyectos/[id]/pr/page.tsx` (~236 agrupa con la misma función).
- Cronograma: `src/components/ui/FormularioCronograma.tsx` (bloque de vínculos con `guardarVinculos`, columna «Hito» con checkbox y `/api/cronograma/hitos`). Su página: `src/app/(workspace)/cronograma/page.tsx`.
- Los consumidores de **otros carriles** (`rdts/catalogos`, `FormularioCrearRdt.tsx`, `rdts/consolidado`, `api/paquetes-trabajo`, `api/plan-maestro`) **no los editas**: usarán el mapa por el contrato `NodoEstructura` en su momento; tú solo dejas `src/lib/niveles/` listo.
- Tablas largas con scroll horizontal y cabecera fija (`design.md` §8); sin `max-w-*` en el contenedor de página; `scope` en los `<th>`. Política de interfaz nueva (flujo 16): **no hay pantalla ni chip nuevo** (es un paso dentro de la importación); incluye en tu evidencia móvil y estados.
- Permisos: sin cambios (importar DP: administrador y jefe de proyectos; subir cronograma: administrador, jefe de proyectos y planner).
- No hay navegador en esta tanda (F5 verifica en vivo): el resto queda `Observado — pendiente de F5` con la lista de comprobación.

## Qué NO hacer

- No cambies el aspecto de las pantallas para servicios con 3 niveles típicos. No crees chips ni rutas. No toques `permisos.ts`, `registro-accesos.ts` ni sus pruebas.
- No edites `rdts/**`, `paquetes-trabajo/**`, `plan-maestro/**`. No apliques migraciones. Sin push.
- Ante contradicción con un flujo escrito o con la maqueta aprobada: detente y devuelve la pregunta.

## Cierre

`resultados/F1-C.md` (estado de F1C-1 a F1C-5, handoff, comprobaciones de navegador pendientes para F5, llamadas). Commit en `local-worker-1`, `git add` explícito.
