# Brief Tanda N — servicio de prueba con Plan Maestro en BORRADOR + verificación en vivo del PATCH

**Plan:** `2026-10-02-observaciones-victor-lote-3-plan.md` · **Carril:** `local-worker-4`, worktree `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\local-worker-4`. **Autorizado por Victor el 2026-10-03** (mismo camino que R7 del Lote 3). **NO** crees ramas, **NO** trabajes en `main`, **NO** hagas merge, **NO** hagas push.

## Por qué

La Tanda E quedó con el `PATCH /api/plan-maestro` **sin verificar en vivo**: el guardado exige un Plan Maestro en estado `BORRADOR` y **no existe ningún servicio de prueba en ese estado**. Es un bloqueo de datos, no de código (OP9). Con tu servicio de prueba se cierra.

## Qué hacer

### 1. Crear el servicio de prueba

- Nombre obligatorio: **`PRUEBA-…`** (marcado como prueba, sin datos reales). suggested: `PRUEBA-PM Repo-01`.
- Créalo **por el flujo normal de la app** con la cuenta A, leyendo los endpoints en `src/app/api/` — no insertes a mano en la base ni por SQL.
- **No toques** ningún servicio existente: `PS-0004`, `PS-0006`, `PS-0007` (`PRUEBA-CRONO`) y `PS-0009` (`PRUEBA-DASH`) quedan intactos.
- Déjalo con un **Plan Maestro en estado `BORRADOR`**. Descubre cómo se crea un borrador leyendo el código (`src/app/api/plan-maestro/route.ts` y el flujo 20) y, si hace falta un DP o cronograma mínimo para que exista, créalo también en ese servicio de prueba.
- Registra su código y su UUID en tu resultado.

### 2. Verificar en vivo el PATCH del Plan Maestro (lo pendiente de la Tanda E)

Con el servicio del punto 1:
- `GET /api/plan-maestro?proyectoId=<uuid>` → que las líneas traen `esDeclaracionPaquete`, `metradoPaquete`, `fechaInicio`, `fechaFin`.
- `PATCH` con `declaraciones` de **una fila que sea de paquete** y valores neutrales → **debe persistir**. Lee después y confirma que el valor quedó guardado.
- `PATCH` **restaurador** con esos campos en `null` → deja el dato como estaba. **Lectura de confirmación**.
- `PATCH` con `metradoPaquete` en una fila que **no** sea de paquete → debe **rechazar con 400** y el mensaje «Solo las filas de declaración de paquete declaran metrado».
- **401/403/409:** si una llamada devuelve HTML en vez de JSON, es **fallo de sesión**, no del endpoint: anótalo y no lo cuentes.

### 3. Verificar en vivo lo de la Tanda F que quedó pendiente

- `GET /api/cronograma/actividades/[id]/impacto` sobre una actividad con partes **VALIDADO** y **REGISTRADO** → debe contar **solo los VALIDADO** (regla V-R1).
- `GET /api/rdts/catalogos` → las **8** disciplinas con sus nombres correctos.

## Cómo hacer la sesión (patrón que funcionó en la Tanda E)

- **Login**: usa `createServerClient` de `@supabase/ssr` con un `cookieStore` tipo `Map` (con `getAll`/`setAll`) y `signInWithPassword`; reutiliza las cookies que devuelva. **No construyas la cookie a mano.** Detalle exacto en `resultados/E.md` de este plan.
- **Credenciales**: `C:\Users\BRANDY\.claude\projects\d--VICTOR-CLAUDE-CODE-pg-control-proyectos\memory\cuentas-prueba.md`, **solo con la herramienta `Read`**. Prohibido `grep`/`sed`/`cat`, imprimir valores o copiarlos a archivos, commits, resultados o chat.
- **Servidor**: `npm run dev -- --webpack -p 3114` desde el worktree (sin `--webpack` no levanta). **Arranca el tuyo y detén al terminar**; no uses el puerto de otra sesión.
- Scripts de apoyo **fuera del repositorio** y borrados al final. Ningún secreto en la salida.

## Cierre

- `resultados/N.md`: servicio creado (código y UUID), las cuatro comprobaciones del PATCH con sus salidas reales, las dos del impacto y catálogos, y el **estado final del Plan Maestro** del servicio (déjalo en `BORRADOR`).
- Si no puedes crear el servicio sin navegador, **detente y devuelve la pregunta con 2 o 3 opciones concretas**; no improvises writes.
- Hallazgos en las **4 categorías**. No edites el archivo del plan.
- Una línea de respuesta: servicio creado (código), PATCH verificado sí/no, impacto V-R1 verificado sí/no.