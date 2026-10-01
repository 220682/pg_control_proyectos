# Resultados F3-C · Plan Maestro: lienzo y ocultar paneles

Carril 2 · rama `local-worker-2` · commit `82cc863` (sobre `35bcf07`). Sin push ni merge. Sin migraciones (no se aplicó ninguna).

## Skills revisados

`pg_control_proyectos/.claude/skills/`: `cerrar-tanda`, `seguir-flujo-de-planes`, `verificar-permisos-por-rol`. Repositorio de la app: no tiene carpeta de Skills (comprobado). Se aplicó `cerrar-tanda` (estados y traspaso van en este archivo). `verificar-permisos-por-rol` no aplica: no cambia quién puede qué (ningún chip, ruta ni permiso nuevo).

## Maqueta usada

La vigente y aprobada (2026-09-30): `mockups/plan-maestro-tres-paneles.html` (no `plan-maestro-lienzo.html` ni `paneles-ocultables.html`, que ahora solo redirigen). El marco de tres paneles no se reimplementó (es el `WorkspaceShell` real); solo se hizo el centro y el icono de ocultar de cada panel.

## Estado de los ítems

| ID | Estado | Evidencia |
|---|---|---|
| F3C-1 | Conforme (lógica y build); **Observado — pendiente de F5** (vista) | `src/lib/ui/paneles-ocultables.ts` + prueba (5 casos: alternar por lado, recordado por usuario, corrupto o sin almacenamiento = visibles, rótulos). `WorkspaceShell.tsx`: un icono por panel en la esquina interior (izq. a la derecha, der. a la izquierda), `aria-expanded`/`aria-controls`/`aria-label`/`title`, solo `lg`; oculto = tira de 24 px (`w-6`) con el icono; el contenido queda montado (no pierde estado). Móvil: cajón sin cambios, el control no aparece. |
| F3C-2 | Conforme (lógica y build); **Observado — pendiente de F5** (vista) | `src/lib/plan-maestro/lienzo-vista.ts` + `lienzo-vista.test.ts` (27 pruebas con las de paneles). `src/components/plan-maestro/LienzoPlanMaestro.tsx`: columnas fijas (WBS, descripción, Und., Met., costo unitario, HH por unidad, falta repartir) con `sticky left` por celda acumulado según las visibles (en móvil solo WBS y descripción), línea divisoria de 3 px en amarillo (`amber-400`), una columna por día, entrada de metrado por día (se confirma al salir de la casilla o con Enter), 4 filas de encabezado `sticky` con `top` por alturas reales, fila de total del servicio «Prog.» y «Real». |
| F3C-3 | Conforme (lógica); **Observado — pendiente de F5** (vista) | Semanas plegables por icono con `aria-expanded` (plegada = solo sus columnas de totales), «Plegar/Expandir semanas», plegar por paquete; «Editar por bloques» (partida, semana o rango de días, total → reparto uniforme, el último día absorbe el redondeo; reemplaza solo esos días de esa partida); «+ 7 días antes/después» amplía el rango; fechas de la actividad sombreadas como guía (no limitan: se puede escribir fuera, probado). |
| F3C-4 | Conforme (lógica) | Prueba con el anexo: servicio 22,56 / 48,78 / 76,22 / 100 %, $ 8 200, 172 HH; semanal 22,56 / 26,22 / 27,44 / 23,78 y HH 47/52/39/34; paquete 1 y directas; real por clave sin mezclar con lo programado. Seis columnas rotuladas «nombre (unidad)»; «Acumuladas: sí/no» deja las tres semanales. **Color del avance real**: solo «Físico acum. (%)» de filas «Real» (partida, grupo y total): 0 % sin clase, en curso `text-amber-400`, 100 % `text-emerald-400` con ✓, comparación al redondeo mostrado, leyenda visible; lo programado nunca lleva color. **Alineación** (design 1.9.0): texto a la izquierda; numéricos con encabezado a la derecha; anchos fijos justos por columna. **Barras de desplazamiento azuladas** (§8) aplicadas en la caja del lienzo con clases propias (ver hallazgo 2). |
| F3C-5 | Conforme (lógica) | «Falta repartir» por línea (completa, falta, excede), por grupo («n partidas por ajustar») y global (`<progress>` + texto). «Crear Plan Maestro» con `aria-disabled` hasta el 100 % (por línea y por partida contra el contractual); al pulsarlo deshabilitado sale un `role="alert"` que dice qué partidas faltan. `BORRADOR` se guarda parcial. Al crear, guarda y luego aprueba (el `PATCH APROBAR` valida lo guardado en servidor). |
| F3C-6 | Conforme | «Generar propuesta»/«Nueva propuesta» y «Editar distribución diaria» retirados de la pantalla. Se conserva un único «Crear borrador del Plan Maestro» (POST) cuando aún no hay plan: sin él no hay forma de iniciar el lienzo; **no copia** nada. Con APROBADO y rol administrador o jefe de proyectos: «Crear versión nueva» con motivo (`puedeCrearVersionPlanMaestro`, ya existente). `npx tsc --noEmit` limpio; `vitest run`: 75 archivos, 753 pruebas verdes tras ajustar la prueba del API; `eslint src`: 27 problemas, igual que `main` (9 errores, 18 avisos; sin nuevos); `npx next build --webpack` correcto. |

## Cambios fuera de la lista (todos en archivos del carril 2)

- `src/app/api/plan-maestro/route.ts` (`GET`): campo **aditivo** `actividades: [{ id, fechaInicio, fechaFin }]` y el rango de semanas incluye esas fechas (sin él un borrador nuevo, sin metrado repartido, no tendría semanas ni guía). Es una adición al contrato C3 (no quita ni cambia lo existente); la prueba `plan-maestro-api.test.ts` se ajustó (claves de la respuesta). **El Orquestador debe reflejarlo en `contrato-c3-plan-maestro.md`.**
- `src/app/(workspace)/plan-maestro/page.tsx`: pasa `puedeCrearVersion` y usa el patrón `flex-1 min-h-0` (§8).

## Handoff

- Falta, para F5: **verificar en navegador** (F5-B/F5-C): ocultar/mostrar cada panel (icono en la esquina, recuerdo al recargar, el centro toma el ancho), el lienzo (sticky de columnas fijas y de las 4 filas del encabezado, barras azuladas, sombreado de guía, semanas plegables, colores del real, alineación), el estado `APROBADO` en solo lectura y la versión nueva con motivo. Las posiciones `top-5` del icono y el `lg:pl-5` de «Accesos rápidos» se calcularon por la maqueta, sin verlas.
- Comandos: `cd D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\local-worker-2` · `npx vitest run src/lib/plan-maestro src/lib/ui` · `npx tsc --noEmit` · `npm run dev -- --webpack -p 3112`.

## Hallazgos y preguntas para el Orquestador

1. **Columnas opcionales (contradicción en el brief).** El brief lista área, disciplina, frente, costo total, HH totales y método de medición; a la vez dice «no agregues Área/Disciplina/Frente»; `design.md` y la maqueta aprobada dicen «BAC y Disciplina». Los datos de disciplina, área, frente y método **no existen** en C3. Se ofrecen solo las que se calculan de datos reales: **Costo total ($)** (BAC de la línea) y **HH totales**, por «Personalizar campos» (`PersonalizarCampos.tsx` reutilizado). Disciplina (y las demás) quedan pendientes de que Victor defina su origen.
2. **Barras azuladas y `globals.css` (congelado/ajeno).** `globals.css` define las barras en gris (`#334155`) para toda la app; el cambio de §8 a azulado (`#3d5a8a` sobre `#0b1222`, ver `marco-tres-paneles.css`) es global y no es de este carril. Se aplicó solo a la caja del lienzo; **F5-A debe decidir** si se unifica en `globals.css` (las pantallas existentes quedan fuera de este plan).
3. **Recordado «por usuario».** `UsuarioShell` no trae el id del usuario; `layout.tsx` (ajeno) no lo pasa. El shell acepta `usuario.id` opcional y, sin él, usa el nombre como clave (guardado en `localStorage` del navegador). **F5-A:** pasar `id: usuarioActual?.id` en `layout.tsx` para que sea exacto.
4. **Asistente y relleno inferior.** `design.md` §3 dice que el asistente «no reserva espacio», pero el shell actual deja `pb-[4.5rem]` en el contenedor del contenido (reservado para él). No se tocó (afecta a todas las pantallas); el icono no tapa columnas hoy. Si Victor quiere que el lienzo use todo el alto, es un cambio del shell para decidir.
5. **Niveles de la estructura.** El contrato de líneas (C3) no trae nivel (`NodoEstructura`); el lienzo agrupa por paquete y partidas directas. Las filas de «Nivel» de la maqueta quedan para cuando el carril 1 entregue los niveles (F5-A). «Por avance del paquete» (maqueta, paquete 2) tampoco está en C3: no se implementó.
6. Las HH reales (`hhReales`) dependen del carril 4; mientras `reales` venga vacío, todas las filas «Real» muestran 0 % en blanco.

## Mejoras de trabajo

- En `bash`, un `heredoc` con tildes y comillas dentro de una orden larga falló («unexpected EOF»): para archivos de código usar la herramienta Write, no `cat <<EOF` en la shell.
- Si se anota «Observado — pendiente de F5» con las medidas calculadas a ojo (`top-5`, `pl-5`), dejar escrita la medida de la maqueta junto a la comprobación.

## Reglas de negocio detectadas

- Ninguna nueva. Se aplicaron las ya escritas: «Crear Plan Maestro» solo con 100 % (por línea y por partida), borrador parcial, fechas de la actividad como guía sin límite, color del avance real solo en filas «Real».

## Huérfanos

- `generarPropuestaDiaria` (`src/lib/plan-maestro/plan-maestro.ts`) y sus pruebas quedaron sin uso en la pantalla (la «copia» retirada); no se borraron. Reportar a Victor.

## Llamadas

Aprox. 45 llamadas de herramienta.
