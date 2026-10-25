# 2026-10-07 — Plan Maestro: rediseño a tres paneles (espacio para la semana)

> Tarea con flujo de Orquestador. Estándar: `docs/00-estandar-agentes/04-flujo-sdd-y-planes.md`.
> **Maqueta re-aprobada por Victor el 2026-10-07**: `docs/05-diseno-y-referencias/mockups/plan-maestro-tres-paneles.html` (aprobada primero como F0-V en el plan de niveles) y `plan-maestro-rediseño.png` (raíz de `pg_control_proyectos`).
> Base de reglas ya acordadas: Spec `2026-09-30-paquetes-y-plan-maestro-grilla.md` (P6–P16) y correcciones del Plan Maestro del `Lote 3` del 2026-10-02 (O7, O8, O9), que quedaron explícitamente fuera de su alcance (línea 127). Este plan los implementa.

## Identificación y estado

- Tema: Cronograma → Plan Maestro (lienzo de programación semanal/diaria) — interfaz.
- Fecha: 2026-10-07.
- Estado: **Desplegado a producción (2026-10-14)**, pendiente de revisión de Victor en producción. Lo del 7-8 oct nunca se había commiteado (por eso no llegó al despliegue): se rescató en la rama `plan-maestro-tres-paneles` de la app y se pasaron a `main` solo los commits del Plan Maestro (`c0f38be`, `ae61e53`). Ajuste del 2026-10-14 por pedido de Victor («más área de trabajo»): encabezado y barra en una línea cada uno, tarjeta de mensajes solo con mensaje, «Editar por bloques» y leyenda como paneles flotantes, el lienzo usa todo el alto (`data-area-completa`: el marco no reserva el espacio del asistente en esta pantalla), columnas fijas y días más angostos, Disciplina como columna solo mientras falte, selector de OT visible en todos los estados. Panel derecho = Accesos rápidos, como la maqueta (se descartó el panel de detalle por celda del alcance de abajo). Verificado: tsc 0 errores, 1142 pruebas, capturas a 1366 y 1920. Quedan en la rama, sin desplegar ni revisar: cambios de Dashboard, RDT (consolidado con CNC y purgado) y scripts Marcobre del 7-8 oct.
- Estado anterior (2026-10-07): **Ejecutando** — alineación con la maqueta aprobada (2026-10-07, corrección de Victor: "debe quedar como la maqueta"): se revirtieron los defaults de semanas plegadas y paneles ocultos (la maqueta abre semanas expandidas y paneles visibles); la barra quedó con los controles de la maqueta (Personalizar campos, «Acumuladas: sí/no», «Real: sí/no», Plegar/Expandir semanas, línea de ayuda) reemplazando los tres botones por medida; columnas fijas con rótulos de una línea y anchos ajustados. Verificado: 129 pruebas + tsc 0 errores. Pendiente: revisión visual de Victor.
- Reemplaza en lo que contradice: la Fase "Lienzo" del plan `2026-09-30-paquetes-y-plan-maestro-grilla.md` (que quedó en `Planificando` y nunca se implementó; este plan toma su spec de reglas y le da la forma de la maqueta aprobada).

## Problema y contexto

El Plan Maestro actual es un lienzo único (`LienzoPlanMaestro.tsx`) con una columna por día; con las partidas del servicio y las semanas del proyecto el espacio para revisar o programar la semana es mínimo (queja de Victor, 2026-10-07: "el espacio para revisar o crear el plan semanal prácticamente no existe"). La maqueta de tres paneles ya está aprobada y las reglas de negocio ya fueron decididas con Victor (P6–P16); nunca se implementó porque el plan que debía hacerlo no pasó de `Planificando`.

## Objetivo

Reemplazar el lienzo único por la interfaz de la maqueta aprobada: **tres paneles** que den espacio real a la programación semanal, con las columnas fijas a la izquierda, la semana (sábado a viernes) con sus 6 columnas (avance físico, avance económico y HH —semanal y acumulado—) y lo real junto a lo programado, sin cambiar ninguna regla de negocio del PM.

## Alcance funcional

### Estructura de la pantalla (maqueta `plan-maestro-tres-paneles.html`)

1. **Panel izquierdo — columnas fijas** (scroll horizontal no las arrastra): WBS, descripción, Und., metrado contractual, costo unitario y HH por unidad de partida (`dp_partidas.hh_und_partida`). Filas por paquete y por partida suelta (la fila de paquete agrupa sus partidas; editable el metrado del paquete en modo "por avance del paquete", P10).
2. **Panel central — el lienzo**: una columna por día, semanas sábado→viernes, **6 columnas por semana**. En `BORRADOR` el usuario coloca metrados por día; en `APROBADO` es solo lectura. Semanas **colapsables y expandibles** (P7); al colapsar se ve la semana con sus totales.
3. **Panel derecho — detalle de la selección**: al hacer clic en una celda/fila, muestra la descomposición (metrado por día de esa partida/paquete, precio unitario, HH resultantes, y lo real del RDT validado de esa partida). El panel derecho también lleva el **selector de OT compacto** (≤ 200px, corrección O7 del Lote 3) y el interruptor de columnas acumuladas.

### Reglas de negocio (heredadas, no se renegocian)

- **P8.** Medidas por separado: físico = metrado programado acumulado ÷ metrado contractual por partida; económico = metrado × precio unitario (el acumulado es el **PV**); HH = Σ metrado programado × HH por unidad. En filas de paquete y totales el % físico se pondera por costo (opción A decidida 2026-09-30; `calcularAvanceFisico` de `dashboard.ts` aplicado al programado).
- **P6.** Fechas libres: el rango del cronograma se sombrea como guía; se puede programar antes o después.
- **P14–P16.** Dos subfilas por partida: **Prog.** (editable en BORRADOR) y **Real** (solo lectura desde RDT validado, misma estructura semanal). Lo real alimenta EV y avance del PR; lo programado alimenta PV. No se mezclan (flujo 20). Interruptor para ocultar las acumuladas. Las semanas se extienden si hay real fuera del rango programado.
- **Edición de fechas y metrados** en la celda, con guardado por celda (corrección del Lote 3: fechas editables).
- **Bloqueo de aprobación**: no se puede aprobar el PM con metrados sin repartir (regla existente, se conserva).
- **Roles** (no cambian): ver = `puedeVerPlanMaestro`; editar/aprobar = `puedeGestionarPlanMaestro`.

### Técnica

- Columnas fijas: técnica existente de pantallas largas del repo (`overflow-x-auto`, `sticky left`); en el panel central evaluar virtualización de filas × días (el lienzo puede ser grande).
- Componentes nuevos: `PlanMaestroTresPaneles.tsx` (o equivalente) reemplazando el uso de `LienzoPlanMaestro.tsx` en la página del PM; se conservan `lib/plan-maestro*` y las APIs tal como están (no cambia el modelo de datos).

## Fuera de alcance

- Conectar las **HH reales por semana** al PM (quedan en 0 como marcador según P16; el dato se construye en otra tarea).
- Edición de las actividades del cronograma desde el PM.
- Reglas de negocio del reparto de metrados (solo se tocan fechas/metrados de la celda).

## Criterios de no-regresión (prueba en el servicio de prueba)

1. PV y avance del PR de un servicio de prueba (PS-0009 / PS-0011) idénticos antes y después del rediseño (fórmulas y APIs sin cambio).
2. `APROBADO` → pantalla solo lectura; `BORRADOR` → edición por celda.
3. Curva S económica: con granualidad Semanal igual que antes del cambio (el filtro por días/semanas de otro plan no toca esto).
4. La maqueta se cumple en Chrome (ancho 1366 y 1920) y en el ancho mínimo soportado por la app.

## Secuencia de ejecución (propuesta)

1. **Gate Spec** con este documento (Victor aprueba → pasa al plan).
2. Plan con puertas y tandas de workers (rango medio), con verificación sobre la maqueta en el servicio de prueba y no-regresión de PV/EV.
3. Cierre: comparativa de pantalla (maqueta vs implementado) para revisión de Victor.

## Avance 2026-10-14 (después del despliegue)

- Commits `4becbca` y `0374187` en `main` de la app, **desplegados a producción el 2026-10-14** (push `ae61e53..0374187`, Vercel «Deployment has completed»): jerarquía completa del presupuesto en Plan Maestro, PR, DP, Dashboard, selector de Crear RDT y consulta de partidas del Requerimiento; y arreglo de las divisorias y la línea amarilla que se deslizaban por detrás al hacer scroll (`border-separate`). Verificado: tsc 0 errores, 1139 pruebas en verde, revisión en pantalla de PS-0011 (Plan Maestro, PR, DP, Dashboard y selector de RDT).

## Reglas de negocio acordadas en esta tarea

- **Jerarquía completa del presupuesto en toda interfaz (Victor, 2026-10-14):** «siempre debo ver todos los niveles, es decir no perder el orden jerárquico». Opción elegida: «Dentro de su nivel» — cada paquete es una fila dentro del nivel donde están sus partidas (en cada nivel con su parte si tiene partidas en dos), conserva su declaración de metrado y sus fechas; las partidas directas van sueltas en su nivel. Contradecía el flujo 20 («grupos por paquete y partidas directas»); integrada en flujos 09, 20 y 06.

## Observaciones sobre la política

- Ninguna nueva.

## Carpetas/archivos huérfanos

- `.playwright-mcp/` en la raíz de `pg_control_proyectos` acumula registros de consola y capturas de las verificaciones (sin seguimiento en git). Reportado a Victor; no se borra nada.

## Pendiente de consulta

- ¿El panel derecho muestra la descomposición al hacer clic en cualquier celda (propuesta) o solo en filas de partida? (En la maqueta se ve para filas de paquete.)