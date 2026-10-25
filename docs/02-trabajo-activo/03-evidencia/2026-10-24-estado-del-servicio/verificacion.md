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
