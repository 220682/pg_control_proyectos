# Evidencia: correcciones de la prueba del RDT en PS-0001

Plan: [2026-10-21-correcciones-prueba-rdt-ps0001.md](../../01-planes/2026-10-21-correcciones-prueba-rdt-ps0001.md).

## Verificaciones corridas (2026-10-21, app `981b2fd`)

- `npx tsc --noEmit`: sin errores.
- `npm test` (vitest): 203 archivos y 2225 pruebas aprobadas, 1 omitida.
- `npm run build`: termina bien.
- `python -I scripts/verificar-referencias.py`: 0 huérfanos, 0 enlaces rotos.
- `python scripts/esperados_rdt_ps0001.py --regla-hh nueva`: HH reales 48/96/156/204/268; IP 0,666/0,766/0,761/0,789/0,788.

## No verificado

- `db/116` no se ha aplicado ni corrido contra la base (sin acceso desde el entorno del agente). Script de verificación de solo lectura: `db/pruebas/116_hh_transversales_verificacion.sql` en la app.
- Ninguna pantalla se probó en navegador (Playwright no conectó). Lo cubre la prueba v2.
