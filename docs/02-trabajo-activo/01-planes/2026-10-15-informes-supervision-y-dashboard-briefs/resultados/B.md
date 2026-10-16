# Resumen de cierre — Tanda B (Worker 1)

Estado: B1 a B5 Conforme. Migracion 098 revisada, no probada en base (no aplicada).
Commits en local-worker-1 (pusheados): 1fa141d (B1-B2), 3cc7d94 (B3-B5).
Verificacion: npm test 1236/1236; tsc limpio; lint 9 errores y 22 avisos (igual que antes, 0 nuevos); next build --webpack ok.

## 1. Tareas de implementacion
- B1 db/098_informes_supervision.sql + linea 77 en db/README.md (4 tablas + contador, RLS sin politica, siguiente_codigo_informe(p_proyecto,p_tipo,p_ot), emitir_informe, trigger de inmutabilidad).
- B2 ocho funciones en permisos.ts (puedeVerInformes, puedeCrearInforme, puedeEmitirInforme, puedeTomarFotoCampo, puedeCrearInformeCostos, puedeVerInformeCostos, puedeNuevaVersionInformeAjeno, puedeDescargarInforme) + prueba por rol.
- B3 tipos.ts (contrato congelado), B4 periodo.ts, B5 formatos.ts y estados.ts, con pruebas.

## 2. Mejoras de trabajo
- Los heredocs de bash con ciertos apostrofes fallan en este entorno y no hay python: usar Write/Edit.

## 3. Reglas de negocio acordadas
- Ninguna nueva. Supuestos a confirmar (ver 4).

## 4. Observaciones sobre la politica
- Spec no define "Ultimas 2 semanas": se implemento como los 14 dias que terminan hoy.
- "Semana en curso" = lunes a hoy (Hasta no puede pasar de hoy).
- 3 meses = Hasta <= Desde + 3 meses - 1 dia (con recorte a fin de mes); cabe en el tope duro de 93 dias de la base.
- siguiente_codigo_informe recibe el N° OT como parametro (p_ot).
- COSTOS: crear exige crear + economia (admin, JP, JOT); ver/descargar, los 5 roles con economia.

## 5. Carpetas/archivos huerfanos
- Ninguno. db/095* ajeno no se toco.

## Correccion R5
- 3ce0a52 Tanda B: crear y emitir COSTOS lo hacen los 5 roles con economia (R5): crear, emitir y ver COSTOS = puedeVerEconomia (5 roles); puedeEmitirInformeCostos nueva; prueba por 13 roles; npm test 1236 ok, tsc limpio.
