-- T1-03: cierre de los 18 avisos de la bandeja de Victor (orden directa, P3). No incluye ningun aviso de aprobacion de RQ (no hay ninguno).
-- Aplicar solo si no se cierran por la API /api/notificaciones/<id>/atender.
update notificaciones
set estado='ATENDIDO', visto=true,
    respuesta='Cerrado por limpieza de pruebas (orden de Victor, 2026-10-16)',
    respondido_en=now()
where id in (
  '524c21bb-d654-421e-a902-397b5e750415',
  'b1fea47f-53d7-4b61-924f-2e04b8c50877',
  '8416db96-a9d2-4e8c-94c7-5cf6a8fbaa31',
  '8b7708d3-03d2-4c02-90ed-a9770dcd595f',
  '8f0d2b30-0193-4af4-b0ee-9acb7027f131',
  'd033aba4-b2c0-43c9-b8f9-637e064d67ca',
  'fc34f350-0c65-4bcb-b628-0257a40b07dc',
  'e7ec612c-8118-49f5-9669-c4a7406f66b5',
  '63611972-df92-4c33-9151-373d3df79ce3',
  '423d97c9-c619-4f62-86a7-5f8992c7700b',
  'f2573a4c-7a95-447a-8733-32e01d70fdb8',
  '0841b6fa-af0d-4a85-b7a3-56cd16532258',
  'b25862bf-3f93-4b9d-a5e0-038c8d68657c',
  'f633858f-ae27-4017-8ab1-f05f37d910c4',
  'e9af29a3-a97f-47f3-94bd-8bf3fdcd02c7',
  '0d039e7b-0169-4ab9-ac61-33cd92e7d19c',
  '013feefd-a9e5-4269-8e75-1d16f785df56',
  'ecb63653-eb61-4eb9-8e85-108492633f7b'
);
