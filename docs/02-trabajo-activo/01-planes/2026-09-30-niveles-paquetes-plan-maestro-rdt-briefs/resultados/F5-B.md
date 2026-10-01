# Resultados F5-B (servicio de prueba y verificación en vivo)

Carril de integración · rama `local-worker-1` (0250dab) · puerto 3111 · cuenta A (administrador). Sin cambios de código en la app (no hay commit nuevo); sin push, merge ni migraciones; no se borró nada.

## Skills revisados
`pg_control_proyectos/.claude/skills/`: `cerrar-tanda`, `seguir-flujo-de-planes`, `trasladar-hallazgos`, `verificar-permisos-por-rol`. App: sin carpeta `.claude/skills/`. Se usó `cerrar-tanda` (estados, evidencia y traspaso en este archivo). `verificar-permisos-por-rol` no aplica (F5-B no cambia permisos).

## Servicio de prueba
- Portafolio «Servicios Marcobre» (programa Promcoser), donde están PS-0004 y PS-0005.
- Nuevo: **PS-0006 «PRUEBA-F5B Servicio de verificacion»** (cliente/área PRUEBA, OC «PRUEBA-OC»), id `51f5905b-6198-46b3-a3d3-abd4793c0e7c`, URL `/proyectos/51f5905b-6198-46b3-a3d3-abd4793c0e7c`. El N° OT es correlativo y de solo lectura (PS-0006), no admite el prefijo PRUEBA; el nombre sí lo lleva. PS-0004 y PS-0005 no se tocaron (solo lecturas GET).
- Archivos sintéticos (generados fuera del repositorio, en el scratchpad, a partir de `PS-065-2026 - BANCODUCTOS - APU CORREGIDO.xlsx`): DP con un nivel extra «PRUEBA AREA SINTETICA» (4 niveles de archivo = 5 con el Servicio implícito) y un cronograma sintético con los mismos códigos EDT (65 filas). No existe DP real de 5 niveles.

## Estado de ítems

| ID | Estado | Evidencia |
|---|---|---|
| F5B-1 | Conforme | Ficha creada y DP importado (HH contractual 5312,08 = la de PS-0004). `capturas/niveles-paquetes-plan-maestro-rdt/F5B-1.jpg` |
| F5B-2 | Conforme | DP: «Se encontraron 4 niveles en el presupuesto: Servicio implícito · Área · Subpresupuesto · Paquete de partidas · Partida», 18 grupos de hermanas, 2 para revisar (se confirmó el rol), fila de muestra por grupo, «Aprobar niveles» e importación. Cronograma: mapa propio (Área · Fase · Actividad resumen · Tarea), 2 para revisar, importado: 65 actividades, 48 tareas, 17 resúmenes, 57 enlazadas al DP. `F5B-2.jpg`, `F5B-2b-cronograma.jpg` |
| F5B-3 | **Observado (parcial)** | Ver hallazgo H1. Conforme: la declaración por EDT sale pre-llenada («auto»), se declaró 1.8.1 a mano (Quitar, Elegir partida, metrado), todo «0.00 · completa». Cae: Agrupar muestra todo «Sin declarar: no se puede marcar», por lo que no se pudo comprobar por pantalla marcar hito, dos paquetes con una partida repartida, marca visual, seleccionar completo, mover, plegar ni «Crear paquete» desde el panel. Sí: el POST del paquete (API, Disciplina Civil, modo POR_PARTIDAS) devolvió 201 PT-001 y su vínculo se lee; el hito se escribió por API (HITO / requierePartidas=false, y se revirtió). Sin captura (pantalla sin contenido útil). |
| F5B-4 | Conforme (con reservas) | Lienzo con columnas fijas (7: WBS, Descripción, Und., Met., Costo unitario, HH por unidad, Falta repartir) y días, 8 semanas plegables, nodos por nivel, bloque PT-001 y «Partidas directas»; «Crear Plan Maestro» con `aria-disabled` al 0 % y 99 %; al 100 % repartido avisó «Falta la disciplina de 47 líneas de partida directa» (Disciplina obligatoria); tras asignarla (Civil/Mecánica/Tuberías) se creó y quedó **APROBADO v1**. Números: 48 líneas, metrado repartido 3522,58 = metrado total; PV = Σ(precio×metrado) = US$ 123 807,94 y HH 5312,08; **Curva S: PV semana 9 = 123,807.94** (EV y AC 0), coincide. `F5B-4-borrador.jpg`, `F5B-4.jpg`. Reservas: el brief dice «seis columnas», la pantalla muestra 7 fijas (la séptima es «Falta repartir»); el reparto de los metrados (48 filas) se hizo por **API PATCH** (todo el metrado el día de inicio de su actividad), no escribiendo en el lienzo; las líneas aparecieron como «directas» (salvo la de PT-001) por H1. |
| F5B-5 | Conforme (parcial) | Con Plan Maestro aprobado: DP → 409 «No se puede volver a cargar el presupuesto: el servicio tiene un Plan Maestro aprobado» con `perderia {vinculos 48, paquetes 1, planMaestroBorrador false}` y diálogo «No se puede volver a cargar el DP» (`F5B-5.jpg`); cronograma («Reemplazar») → 409 equivalente y diálogo. **Pendiente**: el caso «solo borrador» (aviso y confirmación `confirmarPerdida`) no se probó: haría falta otro servicio de prueba con borrador sin aprobar. |

## Hallazgos
- **H1 (Observado, alto)**: `GET /api/paquetes-trabajo` y `GET /api/cronograma` devuelven `vinculos: []` / `partidas: []` aunque `cronograma_actividad_partidas` tiene filas. Prueba: el PUT `/api/paquetes-trabajo/vinculos` (200) y luego el POST de paquete (que lee con el cliente admin y sí ve el vínculo, 201) y el Plan Maestro (48 líneas con metrado) confirman que los datos existen; la lectura con el cliente de servidor del usuario (`crearClienteServidor`) los ve vacíos (también para PS-0004/PS-0005: `vinc=0`). `paquete_trabajo_vinculos` sí se lee bien con ese mismo cliente. Causa probable: RLS/política de `cronograma_actividad_partidas` (la 079 sí habilita RLS en `paquete_trabajo_vinculos`; para la tabla puente no hay política en `db/`). Efecto: la pantalla Paquetes de Trabajo (Declarar «guarda» pero se ve vacío; Agrupar «Sin declarar»). Arreglo propuesto: leer con el cliente admin tras `exigirAlcance` (línea 83 de `src/app/api/paquetes-trabajo/route.ts`) o añadir la política; **el arreglo de código me fue denegado por el clasificador (cambio de cliente de lectura) y no lo apliqué**; queda para decisión de Victor.
- H2: «Guardar declaración» tardó ~17 s (PUT con 48 vínculos) y la aprobación del Plan Maestro ~14 s; el botón queda «Creando…» sin avance visible.
- H3: el cronograma importado resume «57 enlazadas al DP» con 48 tareas (cuenta también resúmenes enlazados por EDT; confirmar si es lo esperado).
- H4: en el alta de servicio, si no se marca al menos un documento del checklist da 400 «Debe seleccionar al menos un documento» sin mensaje visible en pantalla.
- Detalle de 5 niveles: «5 niveles» cuenta el Servicio implícito; un archivo con 5 niveles propios se rechaza («admite de 2 a 5 (con el Servicio)»).

## Migraciones observadas (sin comprobar por script)
Presentes según comportamiento: 073/074 (niveles y encabezados: mapa y nodos del Plan Maestro), 075 (reemplazar DP con niveles: import OK), 079 (`paquete_trabajo_vinculos`: POST de paquete + lectura), 072 (paquetes/`modo_medicion`), 085 (`disciplinas`: `/api/disciplinas` devuelve las 5) y **086** (`disciplina_id` en el Plan Maestro: asignación y gating de 47 directas). Plan Maestro con aprobación y Curva S: sin errores. No hubo fallo por tabla/columna inexistente. 076–078, 080–084 sin síntoma directo (no se ejerció: RDT/real por clave).

## Handoff
1. Decidir H1 (cliente admin en los GET, o política RLS en `cronograma_actividad_partidas`) y volver a probar F5B-3 por pantalla (Agrupar, hito, dos paquetes con una partida repartida, marcar, mover, plegar, «Crear paquete»).
2. Probar F5B-5 «solo borrador»: otro servicio PRUEBA con DP, cronograma y borrador (reutilizar `PRUEBA-DP-5-niveles.xlsx` y `PRUEBA-cronograma.xlsx`; se regeneran con los scripts del scratchpad desde el archivo Bancoductos).
3. Datos creados en PS-0006 para limpiar en F5-C (con autorización): servicio PS-0006, DP, cronograma, paquete PT-001 «PRUEBA-sonda», Plan Maestro v1 aprobado. Hoy el borrado del servicio queda bloqueado por el Plan Maestro aprobado (probar cómo lo trata F5-C).
4. Reponer: levantar con `npm run dev -- --webpack -p 3111` en el worktree; el servidor de esta tanda quedó detenido.
5. Capturas en `docs/02-trabajo-activo/03-evidencia/capturas/niveles-paquetes-plan-maestro-rdt/`. La carpeta `.playwright-mcp/` (temporales del navegador) quedó sin versionar en la raíz de `pg_control_proyectos`: no se commitea.

## Mejoras de trabajo
- El MCP de Playwright guarda sus temporales y capturas relativas en la carpeta de trabajo; pasar rutas absolutas en `filename`.
- Login por script: rellenar sin snapshot, enviar con Enter; la pantalla no hidrata de inmediato (esperar).
- Un PUT/GET aparentemente vacío no significa que no se guardó: contrastar leyendo por una ruta que use el cliente admin.

## Reglas de negocio detectadas
Ninguna nueva. Confirmadas en vivo: bloqueo de recarga con Plan Maestro aprobado; «Crear Plan Maestro» solo al 100 % y con Disciplina en las directas.

## Huérfanos
Servicio PS-0006 y sus registros (ver handoff 3). Sin otros.

## Llamadas
Aproximadamente 100 (por encima del tope de 80: el diagnóstico de H1 y la generación de archivos sintéticos consumieron ~25).
