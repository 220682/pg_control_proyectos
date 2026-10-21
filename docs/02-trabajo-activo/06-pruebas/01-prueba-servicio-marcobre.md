# 01 — Servicio de prueba MARCOBRE (PS-0011)

> Fecha: 2026-10-07. Estado: ejecutada y verificada; cambios de código en la
> app quedaron **locales, sin commit** (working tree de `main`).
> Scripts en `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\scripts\`.

## 1. Objetivo

Probar el circuito completo de la app en un servicio sintético: presupuesto →
cronograma → creación del servicio → paquetes de trabajo → Plan Maestro →
ejecución con RDT → datos coherentes en el dashboard (costo real desagregado,
curva S, PPC/CNC, productividad).

## 2. Qué se generó

- **Excel de presupuesto y cronograma** (`scripts/generar-excel-servicio-marcobre.mjs`, siguiendo la estructura de "prueba N°01"):
  `PPTO-servicio-marcobre 01.xlsx` y `Cron-servicio-marcobre 01.xlsx` en
  `pg_control_proyectos/docs/06-material-de-apoyo/Informacion para pruebas/`.
  - 3 subpresupuestos × 3 paquetes de partidas × 5 partidas = 45 partidas.
  - 1 paquete de trabajo por paquete de partidas, con sus 3 primeras partidas;
    las 2 restantes quedan sueltas (corrección de Victor del término).
  - Cronograma de 3 meses con EDT espejo del WBS.
- **Servicio** en el portafolio "Servicios Marcobre" (`scripts/flujo-servicio-marcobre.mjs`):
  PS-0011 (`0a20df2f-c5e9-4296-9c08-f89af499182d`), Plan Maestro APROBADO,
  estado EJECUCION, `tipo_dashboard=COMPLETO`.
- **30 RDT validados (66 % de las partidas)** con datos coherentes:
  - Tareo ≈ planeado: 7 060.35 HH declaradas = HH planeadas (0 % de diferencia).
  - Equipos: 120 HM (CAMIONETA PICK UP, US$ 18/HM) con tarifa congelada.
  - CNC: 10 de 30 actividades con causa del catálogo (`cnc_causa_id` resuelto).

## 3. Resultados verificados (corte 2026-10-07)

- Avance físico ~63 %; costo real AC = US$ 93 944.55 (MO US$ 91 784.55 +
  equipos US$ 2 160.00); `recursos_sin_tarifa` vacío; CPI ~1 (real ≈ plan).
- PPC 66.7 % (20/30 cumplidas) y Pareto de CNC con las causas, visibles en el
  bloque "PPC / Pareto de CNC" del dashboard.
- Dashboard: bloque "Costo real de recursos" en 4 apartados (MO, equipos,
  materiales, subcontratos — estos dos últimos valorizados por % de avance
  físico, regla 5 del flujo 21); KPIs IP y Horas ganadas; desempeño con
  filtro por los 5 niveles y orden (presupuesto / asc / desc).
- Plan Maestro alineado a la maqueta de tres paneles (header compacto,
  "Acumuladas: sí/no", botón del agente flotante).

## 4. Contratiempos y aprendizajes (para futuras sesiones)

- **OP8 (aprobación del Plan Maestro)**: `APROBAR` no persiste asignaciones
  inline → PV en 0. Solución: `GUARDAR_ASIGNACIONES` primero y `APROBAR` sin
  asignaciones. Script de reparación: `scripts/reparar-pv-marcobre.mjs`.
- **Conciliación 409** al importar el DP: equipos/cargos fuera del catálogo.
  Solución: alinear nombres al catálogo y reenviar con `resoluciones` de
  `accion:'NUEVO'`.
- **Validación de equipos en el RDT**: exige `wbs` declarado en `dp_partidas`
  y la tarifa se congela por nombre en `dp_recursos` (tabla SIN wbs por
  partida; es agregado por proyecto).
- **CNC no figuraba**: el Pareto del dashboard agrupa por `cnc_causa_id` y la
  validación lo resuelve por texto EXACTO contra `catalogo_cnc`. Causas de
  prueba deben usar los textos del catálogo, no texto libre.
- **El consolidado (API) no pasaba el campo `cnc`** → se agregó (route + tipo
  `ActividadConsolidado`).
- **Infraestructura local**: los procesos en background de Hermes mueren con
  `stdin is not a tty`; el dev server de Next se cae solo; patrón que
  funciona: `PowerShell Start-Process` + logs en scratch. Nada de esto rompió
  código de la app.
- **Delegación a rango medio**: el worker de minimax-m3 completó el bloque de
  costo real pero se colgó 53 min después (servidor local caído); se retomó
  en la sesión principal y se validó con pruebas + tsc.

## 5. Mejoras pendientes / recomendaciones

- Probar el **borrado de un servicio en EJECUCION** con la purga completa de
  RDT (`src/lib/rdts/purgar.ts`, ya escrita y validada por tsc; falta la
  prueba en vivo con PS-0010).
- Conectar las **HH reales por semana** al Plan Maestro (P16; hoy marcador 0).
- Declarar equipos variados en el tareo (hoy un solo equipo para todas las
  partidas).
- El filtro de desempeño por nivel usa la profundidad del WBS; con WBS de 4
  segmentos (Área explícita) hay que pasar a la estructura de niveles real.
- Revisar que el EV del servicio (~BAC de las partidas avanzadas) se mantenga
  ~igual al AC cuando el tareo declara el 100 % de las HH planeadas (prueba
  con CPI ~1; en servicios reales el tareo no necesariamente coincide).