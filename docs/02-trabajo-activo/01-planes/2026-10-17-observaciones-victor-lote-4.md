# 2026-10-17 — Observaciones de Victor, Lote 4 (levantar, desplegar y que Victor revise)

> Lote de trabajo tradicional, sin flujo de Orquestador: Victor pasa las observaciones sobre la app real (`py_control_proyectos_web`); el agente las levanta, las verifica en la app con login real, las despliega a `main` y Victor revisa. Cada observación se registra aquí cuando se atiende.

## Identificación y estado

- Fecha: 2026-10-17
- Estado: **ABIERTO** (Victor sigue pasando observaciones)
- Despliegue: push a `main` de la app (Vercel despliega desde GitHub)

## Observaciones

| # | Observación (Victor) | Estado | Dónde |
|---|---|---|---|
| L4-1 | En Mano de obra directa del DP y en «Cargos (HH)» los cargos en MES no se convierten a HH: se suman los meses como si fueran horas. Mostrar las HH reales, como la MOI (Cantidad · Meses · HH · Costo), y el total de HH reales | Levantada y verificada en local; en despliegue | DP (C1), descargas Excel y PDF del DP, `/proyectos/{id}/recursos/cargos` |

### L4-1 — Detalle

- **Cálculo:** 1 MES = 208 HH, un solo lugar (`src/lib/dp/conversion-hh.ts`); el mismo factor de la MOI. La regla quedó en el [flujo 09](../../04-flujos-de-negocio/09-importar-dp.md) («Mano de obra directa en la vista del DP») y en el [flujo 16](../../04-flujos-de-negocio/16-paneles.md).
- **Verificado (PS-0003, local, login real):** C1 con columnas Cargo · Unid. · Cantidad · HH Contractual · Costo; total 3612,78 HH = 1699,18 HH del DP en HH + 9,20 MES × 208 (1913,60 HH); costo total sin cambio (36719,68). Excel y PDF con la misma tabla y los mismos totales. «Cargos (HH)» con la misma conversión y total, visto con la cuenta de Victor y con la de López Cáceres (sin acceso al DP; ve Cargos sin costos).
- **Efecto en la reconciliación de HH:** las partidas no cuentan los cargos en MES, así que se comparan contra las HH de mano de obra que el DP trae en HH. PS-0003 pasó de «REVISAR 0,54 %» (9,20 meses sumados como horas) a «OK 0,00 %», con los MES mostrados aparte.
- **Pruebas:** `npm test` (1631 pasan), `tsc --noEmit` sin errores. `eslint` marca un `prefer-const` que ya existía en `src/lib/dp/agregacion.ts:64`, fuera de esta tarea.

## Reglas de negocio acordadas en esta tarea

| Regla | Dónde quedó |
|---|---|
| Los cargos de mano de obra en MES se muestran convertidos a HH reales (1 MES = 208 HH) junto a la cantidad en su unidad, con total de HH reales, en el DP (pantalla, Excel y PDF) y en «Cargos (HH)» | Flujo 09, sección «Mano de obra directa en la vista del DP: HH reales»; flujo 16, «Recursos del servicio» |
| La reconciliación de HH compara partidas contra las HH de mano de obra en HH; los cargos en MES van aparte | Flujo 09 (misma sección) |

## Mejoras (de trabajo)

- Sin entradas todavía.

## Observaciones sobre la política

- Sin entradas todavía.

## Carpetas/archivos huérfanos

- `py_control_proyectos_web/db/095_cerrar_lectura_directa.sql`: archivo sin versionar que ya estaba en el árbol antes de este lote. No se tocó; lo decide Victor.
- `pg_control_proyectos/.playwright-mcp/`: carpeta sin versionar con capturas, logs y descargas de pruebas anteriores. No se borró nada.

## Pendientes de decisión de Victor

1. **Equipos (C2) con unidad MES** (camioneta pick up, minivan): siguen bajo «HM Contractual» con el valor en meses. Falta definir cuántas horas-máquina vale un mes antes de convertirlos.
