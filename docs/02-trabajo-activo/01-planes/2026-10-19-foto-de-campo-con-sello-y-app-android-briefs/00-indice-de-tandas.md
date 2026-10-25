# Índice de tandas — Foto de campo con sello (Paso 1)

Plan: `../2026-10-19-foto-de-campo-con-sello-y-app-android.md`. Planner de briefs, 2026-10-19. Un Worker (Worker 1, Sonnet, esfuerzo medio), rama `local-worker-1`, worktree `py_control_proyectos_web/.worktrees/local-worker-1`, base `1919fba`.

| Tanda | Brief | Ítems | Depende de |
|---|---|---|---|
| T1 | [T1.md](T1.md) | S-01 a S-05 | Gate 1 (aprobado) y rama al día |
| T2 | [T2.md](T2.md) | S-06 a S-10, V-01, R-01 a R-03 | T1 y visto bueno de Victor a la muestra |
| T3 | [T3.md](T3.md) | S-12 a S-16, S-17 (checklist), P-01, R-01 a R-05 | T2 |

## Parada de Victor dentro de T1
T1 se lanza dos veces con el mismo brief. **Lanzamiento A:** solo S-01 (dos imágenes de muestra, 3 % y 4 %); el Worker termina con un resumen parcial. El Orquestador enseña las imágenes a Victor y él elige. **Lanzamiento B:** S-02 a S-05 con el tamaño elegido (el Orquestador lo escribe en el prompt). Sin visto bueno no se lanza T2. La foto base de la muestra debe ser SIN sello: si el repositorio no trae una real, el Worker genera una neutra y el Orquestador ofrece la de Victor.

## Lo que el Orquestador debe poner en cada prompt de lanzamiento
Qué lanzamiento es; puerto de desarrollo; dirección, servicio de prueba sin alcance real y cuenta de prueba (los briefs no traen credenciales); en T3, si autoriza el push de la rama (por defecto no) y la dirección de la vista previa si existe. Antes de T3, releer `git log` de `reducir.ts`, `cajas-fotos.ts` y `Miniatura.tsx` (riesgo con el otro Orquestador de informes).

## Por confirmar
- S-11 aparece en el plan como parte de T2 pero no existe en su Punch List; T2 lo advierte y no lo trabaja.
- `tsc`: sin script en `package.json` y sin mención en el `AGENTS.md` de la app; el Worker prueba `npx tsc --noEmit` y lo registra como por confirmar.
- `--webpack` en `dev` y `build` de worktrees (viene del documento de entorno citado por el plan, no releído aquí).
- Cómo ver el PDF, Word y Excel para las capturas, y cómo dibujar la muestra del sello sin canvas en Node (T1 y T3 lo resuelven y lo anotan).
- Vista previa de la rama en el alojamiento: solo con autorización del Orquestador; si no deja iniciar sesión, la prueba de Victor espera a la fusión posterior al Gate 2.

T4 a T6 y T7: otro Planner de briefs, en otra sesión.
