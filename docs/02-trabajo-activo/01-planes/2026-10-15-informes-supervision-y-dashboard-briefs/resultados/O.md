# Resumen de cierre — Tanda O (Worker 3)

Rama local-worker-3, un commit (O1-O7). O8: no probado en base (Victor no indicó base).

## Estado
- O1-O7: Conforme (revisado, no probado en base; migración 100 sin aplicar).
- O8: no probado en base.

## Hallazgos
- Reglas de negocio: ninguna nueva; se aplicó lo del brief (factor 1,25 repartido por horas; stand-by suma a HM y costo).
- Mejoras de trabajo: en vitest, `beforeEach(() => mock.mockClear())` devuelve la función y vitest la ejecuta como teardown; usar llaves.
- Observaciones sobre la política: el brief pide validar en PATCH /api/rdts/partes/[id], pero ese PATCH solo valida/rechaza y no recibe tareo; la validación vive en POST, en la RPC y en el formulario (parte.ts). El PATCH/GET [id] solo devuelve los campos nuevos al reabrir.
- Huérfanos: ninguno.
- Pendientes: FormularioCrearRdt y PDF (tanda P) deben mostrar/editar horasExtra, horasStandby y estado; la RPC rechaza extra > total y estados inválidos con excepción (el POST ya los filtra antes con 400).
