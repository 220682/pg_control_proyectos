# Evidencia — Estado del servicio (2026-10-24)

Verificaciones corridas en `py_control_proyectos_web` (sin commit todavía):

| Verificación | Resultado |
|---|---|
| `npx tsc --noEmit` | Sin errores |
| `npx vitest run` (completo) | 208 archivos pasan, 1 omitido; 2306 pruebas pasan, 1 omitida |
| `npx vitest run src/lib/estado-servicio` | 37 pruebas de piezas puras (huella, horarios, reglas, lectura del mensaje, cifrado, validación de la respuesta de IA) pasan |
| `npx eslint` sobre los archivos nuevos (`src/lib/estado-servicio`, `src/components/estado-servicio`, rutas API y las tres páginas) | Sin errores ni avisos |
| `npm run lint` (todo el repositorio) | Ya trae miles de errores previos ajenos a esta tarea; no se usó como criterio |

**No verificado (honestidad):**

* La pantalla no se abrió en un navegador: la migración `db/119_estado_servicio.sql` no está aplicada en Supabase, así que las consultas fallarían.
* La lectura real de Gmail, el flujo de permiso de Google, la clasificación con IA y la descarga de adjuntos reales **no se probaron**: faltan las claves de Victor.
* La Matriz de permisos (artefacto) no se pudo actualizar: esta cuenta no puede abrirla.

## Prueba real con Gmail (2026-10-24 / 25)

Buzón conectado: `oficinatecnica@promcoser.com.pe` (cuenta de empresa, agregada como usuario de prueba en Google Cloud; el aviso «Verify it's you» de la cuenta pidió un celular que Victor no tenía a mano y se resolvió entrando desde otro navegador). Sin el segundo buzón todavía.

| Prueba | Resultado |
|---|---|
| Conectar el buzón (OAuth, token cifrado) | Funciona: el buzón aparece como «Leyendo» |
| «Sincronizar ahora» (1.ª corrida) | **Falló con 504**: en 60 s alcanzó a guardar 29 correos y 95 adjuntos, pero no a clasificar ni a cerrar el registro. Corregido en la app (`4022ee7`): la lectura corta a los 35 s y la clasificación a los 52 s, y el botón repite pasadas hasta terminar (tope 12) |
| «Sincronizar ahora» (con el arreglo) | Terminó sin errores: **200 correos** leídos (11 al 25 de octubre; la primera lectura mira 14 días atrás), **158 con adjuntos** guardados, 0 duplicados (un solo buzón), cada pasada ≈ 35 s y ≈ 20 correos |
| Clasificación | **0 ubicados, 200 en «Por revisar»**. Esperado con el diseño actual: no hay clave de IA y no existe ningún tema, y las reglas solo ubican si el servicio o un tema existente se nombra. 14 correos traen un código `PS-####` pero aun así quedan en «Por revisar» porque no hay tema al que mandarlos |

**Hallazgo de diseño (para decidir con Victor):** sin IA, el sistema no puede crear temas por sí mismo; hay que crear los temas a mano (ej. PETS) o configurar `ANTHROPIC_API_KEY`. No probados todavía: la IA, la pantalla de temas/«Por revisar» con datos reales, el correo completo y la descarga de adjuntos desde la pantalla, el segundo buzón y el disparador horario.

## Lectura desde el 7 de septiembre y clasificación manual en tandas (2026-10-25)

Orden de Victor: empezar con trabajo manual (lo hace el agente) y ver luego cómo automatizar; revisar los dos buzones desde el 7 de septiembre.

| Paso | Resultado |
|---|---|
| Segundo buzón conectado | `proyectos@promcoser.com.pe`, agregado como usuario de prueba en Google Cloud; ambos buzones aparecen «Leyendo» |
| Adjuntos | Dejaron de copiarse a Supabase (`e3e3925`, `GUARDAR_ARCHIVOS_ADJUNTOS = false`): los ~200 MB ya guardados bajo `estado-servicio/` (519 archivos) pesaban demasiado; solo se guarda nombre, tipo y tamaño. Destino acordado para los archivos: Cloudflare R2 |
| Lectura | `ultima_lectura` de ambos buzones puesta en 2026-09-07; el botón «Sincronizar ahora» en tandas (`2568fe1`: 3000 ids por buzón, consulta de ya-guardados por bloques de 150). Resultado: **1 341 correos** (641 oficinatecnica, 700 proyectos) |
| Duplicados entre buzones | **300 copias** (293 de proyectos con original en oficinatecnica, 5 y 2 dentro del mismo buzón). 6 originales estaban en proyectos y se intercambiaron para que el original sea el de oficinatecnica (regla de Victor: por defecto oficina técnica). Todos quedaron coherentes |
| Estado | 1 041 en «Por revisar», 300 duplicados, 0 ubicados |
| Ronda 1 (Sonnet, 4 lotes de 60 al azar = 240) | Solo **27 %** es de los 4 servicios (PS-0001: 5, PS-0002: 7, PS-0003: 26, PS-0004: 27); 120 son de otros trabajos de Promcoser, 36 administrativos de campamento y personal, 19 ruido. Dejó el aprendizaje en [`2026-10-25-clasificar-correos-en-tandas.md`](../../../03-aprendizaje-continuo/2026-10-25-clasificar-correos-en-tandas.md) |
| Ronda 2 (Haiku, 9 lotes de ~90 = 801) | Los 9 lotes escribieron su salida (JSON en el scratchpad, fuera del repo). **Validada con script** al cierre (`validar.mjs`): 801 salidas, ids y orden iguales a la entrada en los 9 lotes, 0 resúmenes de más de 180 caracteres, 0 destinos inválidos (varios subagentes solo habían comprobado por conteo porque el verificador de seguridad de comandos falló). Resultado: PS-0001 27, PS-0002 27, PS-0003 109, PS-0004 83, ajenos 555 |
| Base de datos | **No se escribió ningún tema, nota ni asignación**. Nada de la clasificación está aplicado todavía |

Los correos exportados y las salidas de los clasificadores viven solo en el scratchpad de la sesión; no entran al repositorio por ser privados de la empresa. Hallazgo de seguridad: dos correos de Tecnovias traen usuario y contraseña en el texto y ya están guardados en la base; Victor decidió no tocarlos.
