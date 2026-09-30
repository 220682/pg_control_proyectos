> Parte de los contratos técnicos compartidos (índice: `00-contratos-tecnicos.md`). Un carril **no cambia** un contrato por su cuenta: si lo necesita, se detiene y devuelve la pregunta al Orquestador. Lo marcado «por confirmar» lo verifica el Worker en el código. Verificado en `main` `45c9e0a`, solo lectura, 2026-09-30.

## C1 · Niveles (dueño: carril 1)

```ts
type RolNivel = 'SERVICIO' | 'AREA' | 'SUBPRESUPUESTO' | 'PAQUETE_PARTIDAS' | 'PARTIDA';            // DP
type RolNivelCronograma = 'SERVICIO' | 'AREA' | 'FASE' | 'ACTIVIDAD_RESUMEN' | 'TAREA';             // nombres por confirmar (hito = duración 0, como hoy)
type MapaNiveles = { origen: 'DP' | 'CRONOGRAMA'; niveles: { nivel: number; rol: string }[]; confirmado: boolean };
type NodoEstructura = {                                   // lo que consumen las pantallas de todos los carriles
  id: string; codigo: string; nombre: string; nivel: number; rol: string;
  padreId: string | null; tipo: 'ENCABEZADO' | 'PARTIDA' | 'ACTIVIDAD' | 'TAREA' | 'HITO'; orden: number;
};
```
- El orden de roles es fijo: Servicio > Área > Subpresupuesto > Paquete de partidas > Partida. Servicio y Partida obligatorios; Partida siempre el último nivel. El nivel extra de 5 niveles entra en el nivel 2 («Área»).
- Módulo: `src/lib/niveles/` (nuevo, carril 1). Expone `construirArbol(filas, mapa): NodoEstructura[]`. **Hasta la integración**, los carriles 2, 3 y 4 construyen sus pantallas recibiendo `NodoEstructura[]` por props y usan datos simulados o el agrupador actual (`agruparPorSubpresupuesto`, `src/lib/dp/subpresupuestos.ts`); no importan `src/lib/niveles/`.
- Hoy (verificado): subpresupuesto = WBS de 1 segmento (`/^\d+$/`) y paquete de partidas = 2 segmentos (`/^\d+\.\d+$/`) en `src/lib/dp/parser-cd.ts`; tablas `dp_subpresupuestos` (`db/031`) y `dp_paquetes` (`db/034`); `reemplazar_dp` vigente = firma de 13 parámetros en `db/071`. Esas dos tablas se conservan pobladas hasta migrar todos los consumidores.
- Bloqueo de recarga: `src/lib/proyectos/bloqueo-recarga.ts` (carril 1). `evaluarRecarga(admin, proyectoId, origen: 'DP' | 'CRONOGRAMA'): Promise<{ bloqueadoPorPlanAprobado: boolean; perderia: { vinculos: number; paquetes: number; planMaestroBorrador: boolean } }>`. Lee solo tablas que ya existen (`proyecto_plan_maestro`, `paquetes_trabajo`, `cronograma_actividad_partidas`). Con plan `APROBADO` la API responde 409 sin opción de confirmar; sin él, exige `confirmarPerdida: true` tras mostrar el aviso. El borrador no bloquea.
