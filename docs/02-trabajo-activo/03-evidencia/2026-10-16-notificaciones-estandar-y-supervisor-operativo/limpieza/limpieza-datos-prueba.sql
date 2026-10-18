-- =====================================================================================
-- LIMPIEZA DE DATOS DE PRUEBA DEL PLAN «NOTIFICACIONES»  (preparado el 2026-10-18)
-- Para pegar ENTERO en el editor SQL de Supabase. No lo aplica ningun agente: lo revisa y lo aplica Victor.
-- Lee limpieza-notas.md (misma carpeta) antes de aplicar. Respaldo: respaldo-antes-de-limpiar.json.
--
-- Que borra (todo por id exacto, salvo donde se indica):
--   A. El servicio PS-0005 «PRUEBA T7» (id e15799ae-d964-4db7-b33f-39dc9c1a3860) con todo lo que cuelga de el
--      (miembros, checklist, documentos, avisos, historial) por ON DELETE CASCADE.
--   B. En PS-0000 (id 0a20df2f-c5e9-4296-9c08-f89af499182d, que NO se borra): los requerimientos
--      PS-0000-LL-SO-001, -002 y -003 con sus items y comentarios (cascada), y el RDT RECHAZADO del 14-10
--      creado por jeyger22 durante T7B.
--   C. Los avisos (tabla notificaciones) generados por esas pruebas: 30 por id exacto (los que ve el administrador)
--      y los de otras personas por referencia exacta (id del RQ o del RDT) o por el codigo exacto del RQ.
-- Que NO borra: el RDT VALIDADO del 17-10 (afecta el PR de PS-0000: queda como SECCION OPCIONAL comentada, al final),
--   los 33 RDT anteriores al plan, el RDT del 18-10 cargado por Victor, las cuentas de prueba, los avisos reales,
--   los avisos «informe.emitido» y los mensajes «hola» de Victor.
-- Si algo no coincide con lo esperado, las GUARDAS de abajo abortan todo (la transaccion se revierte sola).
-- =====================================================================================

begin;

-- -------------------------------------------------------------------------------------
-- 0. GUARDAS: confirman que el id corresponde a lo de prueba. Si no, se aborta TODO.
-- -------------------------------------------------------------------------------------
do $$
begin
  if (select count(*) from proyectos
       where id = 'e15799ae-d964-4db7-b33f-39dc9c1a3860'
         and numero = 'PS-0005' and nombre = 'PRUEBA T7' and cliente = 'PRUEBA') <> 1 then
    raise exception 'GUARDA: el id e15799ae... no es PS-0005 PRUEBA T7 (cliente PRUEBA). No se borra nada.';
  end if;

  if (select count(*) from proyecto_requerimientos
       where proyecto_id = '0a20df2f-c5e9-4296-9c08-f89af499182d'
         and (id, codigo) in (('2cbd3bf7-78cc-480b-9877-d6fa98d49e9b'::uuid, 'PS-0000-LL-SO-003'),
                              ('f5733231-0830-41e8-8ff2-1a930d29813e'::uuid, 'PS-0000-LL-SO-002'),
                              ('9fff5fc7-7118-4ccc-aafe-5da8fe5ba826'::uuid, 'PS-0000-LL-SO-001'))) <> 3 then
    raise exception 'GUARDA: los 3 requerimientos PS-0000-LL-SO-001/002/003 no coinciden por id y codigo.';
  end if;

  -- El RDT rechazado del 14-10 de jeyger (T7B): fecha, estado, especialidad PRUEBA y autor exactos.
  if (select count(*) from rdt_partes
       where id = 'dcf5e7b8-0468-452b-8628-ac2b96a3b356'
         and proyecto_id = '0a20df2f-c5e9-4296-9c08-f89af499182d'
         and fecha_lima = date '2026-10-14' and estado_validacion = 'RECHAZADO'
         and especialidad = 'PRUEBA' and creado_por_id = 'c414ba1c-81e2-47e1-a9a1-e71823c3a78c') <> 1 then
    raise exception 'GUARDA: el RDT rechazado dcf5e7b8... no coincide (fecha 14-10, RECHAZADO, PRUEBA, autor jeyger).';
  end if;

  -- Dependencias que impedirian borrar el servicio (RESTRICT) o que no deberian existir en PS-0005.
  if (select count(*) from rdts where proyecto_id = 'e15799ae-d964-4db7-b33f-39dc9c1a3860') <> 0 then
    raise exception 'GUARDA: PS-0005 tiene RDT subidos como archivo (tabla rdts); revisar antes de borrar.';
  end if;
  if (select count(*) from rdt_partes where proyecto_id = 'e15799ae-d964-4db7-b33f-39dc9c1a3860') <> 0 then
    raise exception 'GUARDA: PS-0005 tiene RDT estructurados; no se esperaba.';
  end if;
  if (select count(*) from proyecto_cronograma where proyecto_id = 'e15799ae-d964-4db7-b33f-39dc9c1a3860') <> 0 then
    raise exception 'GUARDA: PS-0005 tiene cronograma; no se esperaba (hay que desvincular actividades antes).';
  end if;
end $$;

-- -------------------------------------------------------------------------------------
-- 1. CONTEO «ANTES» (vista temporal + foto). La comprobacion final lo compara con «despues».
-- -------------------------------------------------------------------------------------
create temp view _conteo_limpieza as
  select 1 as orden, 'PS-0005: proyectos' as concepto, count(*) as filas
    from proyectos where id = 'e15799ae-d964-4db7-b33f-39dc9c1a3860'
  union all select 2, 'PS-0005: proyecto_documentos (esperado 2)', count(*)
    from proyecto_documentos where proyecto_id = 'e15799ae-d964-4db7-b33f-39dc9c1a3860'
  union all select 3, 'PS-0005: proyecto_miembros', count(*)
    from proyecto_miembros where proyecto_id = 'e15799ae-d964-4db7-b33f-39dc9c1a3860'
  union all select 4, 'PS-0005: notificaciones (6 visibles + las ocultas de otros)', count(*)
    from notificaciones where proyecto_id = 'e15799ae-d964-4db7-b33f-39dc9c1a3860'
  union all select 5, 'PS-0000: proyecto_requerimientos de prueba (esperado 3)', count(*)
    from proyecto_requerimientos where id in ('2cbd3bf7-78cc-480b-9877-d6fa98d49e9b','f5733231-0830-41e8-8ff2-1a930d29813e','9fff5fc7-7118-4ccc-aafe-5da8fe5ba826')
  union all select 6, 'PS-0000: requerimiento_lineas (esperado 4)', count(*)
    from requerimiento_lineas where requerimiento_id in ('2cbd3bf7-78cc-480b-9877-d6fa98d49e9b','f5733231-0830-41e8-8ff2-1a930d29813e','9fff5fc7-7118-4ccc-aafe-5da8fe5ba826')
  union all select 7, 'PS-0000: requerimiento_comentarios (esperado 5)', count(*)
    from requerimiento_comentarios where requerimiento_id in ('2cbd3bf7-78cc-480b-9877-d6fa98d49e9b','f5733231-0830-41e8-8ff2-1a930d29813e','9fff5fc7-7118-4ccc-aafe-5da8fe5ba826')
  union all select 8, 'PS-0000: rdt_partes RDT rechazado 14-10 (esperado 1)', count(*)
    from rdt_partes where id = 'dcf5e7b8-0468-452b-8628-ac2b96a3b356'
  union all select 9, 'PS-0000: rdt_actividades de ese RDT (esperado 1)', count(*)
    from rdt_actividades where parte_id = 'dcf5e7b8-0468-452b-8628-ac2b96a3b356'
  union all select 10, 'PS-0000: rdt_tareo de ese RDT (esperado 1)', count(*)
    from rdt_tareo where parte_id = 'dcf5e7b8-0468-452b-8628-ac2b96a3b356'
  union all select 11, 'PS-0000: rdt_partes_historial de ese RDT (esperado 1)', count(*)
    from rdt_partes_historial where rdt_parte_id = 'dcf5e7b8-0468-452b-8628-ac2b96a3b356'
  union all select 12, 'PS-0000: avisos por referencia/codigo de RQ y RDT de prueba (esperado >= 27 con los visibles)', count(*)
    from notificaciones
    where proyecto_id = '0a20df2f-c5e9-4296-9c08-f89af499182d'
      and (referencia_id in ('2cbd3bf7-78cc-480b-9877-d6fa98d49e9b','f5733231-0830-41e8-8ff2-1a930d29813e','9fff5fc7-7118-4ccc-aafe-5da8fe5ba826',
                             '99f82005-60f0-4fc2-8697-fc939bf13e6e','dcf5e7b8-0468-452b-8628-ac2b96a3b356')
           or mensaje like '%PS-0000-LL-SO-001%' or mensaje like '%PS-0000-LL-SO-002%' or mensaje like '%PS-0000-LL-SO-003%')
  union all select 13, 'Entorno: mensajes «PRUEBA T7» de otras personas (esperado 1: el del administrador)', count(*)
    from notificaciones
    where proyecto_id is null and tipo = 'MENSAJE' and mensaje like 'PRUEBA T7%' and creado_en >= timestamptz '2026-10-18 00:00:00+00'
  union all select 14, 'Control: rdt_partes de PS-0000 (leidos 36 el 18-10; debe quedar en 35: solo sale el rechazado)', count(*)
    from rdt_partes where proyecto_id = '0a20df2f-c5e9-4296-9c08-f89af499182d';

create temp table _antes_limpieza as select * from _conteo_limpieza;

-- Vista previa para exportar a CSV desde el editor ANTES de aplicar (todos los avisos que se borran por criterio).
-- Se deja comentada porque el editor solo muestra el resultado de la ultima sentencia:
-- select id, creado_en, evento, destinatario_usuario_id, destinatario_rol_id, estado, left(mensaje, 90) as mensaje
--   from notificaciones
--  where proyecto_id in ('e15799ae-d964-4db7-b33f-39dc9c1a3860','0a20df2f-c5e9-4296-9c08-f89af499182d')
--    and (proyecto_id = 'e15799ae-d964-4db7-b33f-39dc9c1a3860'
--         or referencia_id in ('2cbd3bf7-78cc-480b-9877-d6fa98d49e9b','f5733231-0830-41e8-8ff2-1a930d29813e','9fff5fc7-7118-4ccc-aafe-5da8fe5ba826','99f82005-60f0-4fc2-8697-fc939bf13e6e','dcf5e7b8-0468-452b-8628-ac2b96a3b356')
--         or mensaje like '%PS-0000-LL-SO-00_%')
--  order by creado_en;

-- -------------------------------------------------------------------------------------
-- 2. AVISOS (tabla notificaciones). Primero los avisos, luego lo que los origino.
-- -------------------------------------------------------------------------------------

-- 2.1 Avisos que ve el administrador, por id exacto (no incluye los de PS-0005: caen con el servicio, paso 5).
delete from notificaciones where id in (
    '0f3f2939-e135-4adc-9b5c-bfcbc0a45fb2', -- servicio.asignado · PS-0000 · 18-10 (Logistica 1)
    '53b67926-565e-45e4-b9ce-bd262bf81218', -- servicio.retirado · PS-0000 · 18-10 (Logistica 1)
    '23e39e7b-38ec-4ca9-b414-08d04abbdf6e', -- rq.pendiente_aprobacion SO-003
    '30eac7ee-c127-4823-9127-2f3c679562ab', -- rq.pendiente_aprobacion SO-003
    'dcb40451-9c20-4838-b1d4-98d792af9446', -- rq.devuelto SO-003
    '2b6fb35d-e420-4cdd-ba48-b8f752319b69', -- rq.pendiente_aprobacion SO-003
    'ba077890-8b86-441b-9818-64d49670a098', -- rq.pendiente_aprobacion SO-003
    'fbd189b3-3edb-4fc2-8bff-4584698cc2ae', -- rq.devuelto SO-003
    'b7635b1a-4b0c-4260-b20b-2d4f4eaaaa6c', -- rdt.validado (RDT 17-10)
    '79a53cb6-0745-44ef-b12a-f5ace65a4158', -- rdt.rechazado (RDT 14-10)
    '03cd582e-b5b3-43c3-84dc-6a28c9b27a73', -- rq.comentario SO-003
    '6da7069a-649a-4c87-8665-765fd70ec398', -- rdt.registrado (RDT 14-10)
    '2e48ea02-04a3-46e0-bf44-61962b6b5e38', -- rdt.registrado (RDT 14-10)
    '3aea3c35-07b4-4e83-bc65-73a4a7245399', -- rdt.registrado (RDT 17-10)
    '2887cf89-3ea0-4094-90da-78cfa6a2c792', -- rdt.registrado (RDT 17-10)
    'da63c035-ad7c-4e66-8be0-182c14190793', -- mensaje.manual «PRUEBA T7 mensaje de Entorno (sin servicio)»
    '08572954-da83-4c41-9818-d3831a9399de', -- rq.pendiente_aprobacion SO-003
    'a78c8a79-e536-4bb6-9434-a068329a442e', -- rq.pendiente_aprobacion SO-003
    '148bf997-1859-4cd5-b943-d22452300cb6', -- rq.devuelto SO-003
    'e118f036-46f3-4619-8ee6-2f5eaad7bf9d', -- rq.pendiente_aprobacion SO-003
    '81cf0c23-1fd4-4722-bf6f-e17fbc2accee', -- rq.pendiente_aprobacion SO-003
    '6e0ee3e3-af5c-41dd-a311-6a4b01958e74', -- rq.aprobado_solicitante SO-002
    '6638d86d-cd25-4d1d-b2e1-493bb4360395', -- rq.aprobado_logistica SO-002
    '3f167e25-5e63-4d5f-a19c-0eea9dcfc45a', -- rq.pendiente_aprobacion SO-002
    '451cba11-00eb-4b0a-8b82-ae523aed58d0', -- rq.pendiente_aprobacion SO-002
    'c8de8200-2368-47a2-af60-7cd60057798f', -- rq.comentario SO-001 «PRUEBA T1B»
    'f044a840-e860-47e4-b771-ba8ba19792c4', -- rq.aprobado_solicitante SO-001
    '09d8a3e3-ee2f-4bfa-aeaa-eadc21d678da', -- rq.aprobado_logistica SO-001
    '400db5b1-1b77-476e-94ef-02a5a79de292', -- rq.pendiente_aprobacion SO-001
    '46dab7a6-73ef-4ef0-9db1-12d37b4482af'  -- rq.pendiente_aprobacion SO-001
);
-- Filas esperadas: 30.

-- 2.2 Avisos de OTRAS personas que el administrador no ve (p. ej. la fila del rol Jefe de Proyectos, avisos al
--     solicitante, a la cola de Logistica), por referencia exacta (id del RQ o del RDT) o por el codigo exacto del RQ.
--     Guarda: si alguno fuera anterior al 2026-10-17 (inicio de las pruebas) o de otro servicio, se aborta.
do $$
begin
  if exists (
    select 1 from notificaciones
     where (referencia_id in ('2cbd3bf7-78cc-480b-9877-d6fa98d49e9b','f5733231-0830-41e8-8ff2-1a930d29813e','9fff5fc7-7118-4ccc-aafe-5da8fe5ba826',
                              '99f82005-60f0-4fc2-8697-fc939bf13e6e','dcf5e7b8-0468-452b-8628-ac2b96a3b356')
            or mensaje like '%PS-0000-LL-SO-001%' or mensaje like '%PS-0000-LL-SO-002%' or mensaje like '%PS-0000-LL-SO-003%')
       and (creado_en < timestamptz '2026-10-17 00:00:00+00' or proyecto_id is distinct from '0a20df2f-c5e9-4296-9c08-f89af499182d')
  ) then
    raise exception 'GUARDA 2.2: hay avisos que coinciden por referencia/codigo pero son anteriores al 17-10 o de otro servicio; revisar.';
  end if;
end $$;

delete from notificaciones
 where proyecto_id = '0a20df2f-c5e9-4296-9c08-f89af499182d'
   and (referencia_id in ('2cbd3bf7-78cc-480b-9877-d6fa98d49e9b','f5733231-0830-41e8-8ff2-1a930d29813e','9fff5fc7-7118-4ccc-aafe-5da8fe5ba826',
                          '99f82005-60f0-4fc2-8697-fc939bf13e6e','dcf5e7b8-0468-452b-8628-ac2b96a3b356')
        or mensaje like '%PS-0000-LL-SO-001%' or mensaje like '%PS-0000-LL-SO-002%' or mensaje like '%PS-0000-LL-SO-003%');
-- Filas esperadas: entre 7 y 20 (no se pueden contar de antemano: son las filas de otros destinatarios, p. ej. la
-- cola del rol Jefe de Proyectos en cada «pendiente de aprobacion» y «RDT registrado»; el administrador ve 5 + 2 grupos
-- de dos filas, o sea al menos 7 filas ocultas). Lo que importa: tras este paso la comprobacion final da 0 restantes.

-- 2.3 Mensajes de Entorno «PRUEBA T7 ...» de otras personas (el del administrador ya se borro en 2.1).
delete from notificaciones
 where proyecto_id is null and tipo = 'MENSAJE' and mensaje like 'PRUEBA T7%'
   and creado_en >= timestamptz '2026-10-18 00:00:00+00';
-- Filas esperadas: 0 (el unico conocido es da63c035..., ya borrado en 2.1). Si da mas, son mensajes de prueba
-- con el mismo prefijo enviados a otras personas.

-- -------------------------------------------------------------------------------------
-- 3. REQUERIMIENTOS DE PRUEBA de PS-0000 (los items, comentarios y adjuntos caen en cascada).
-- -------------------------------------------------------------------------------------
delete from proyecto_requerimientos
 where proyecto_id = '0a20df2f-c5e9-4296-9c08-f89af499182d'
   and id in ('2cbd3bf7-78cc-480b-9877-d6fa98d49e9b',   -- PS-0000-LL-SO-003
              'f5733231-0830-41e8-8ff2-1a930d29813e',   -- PS-0000-LL-SO-002
              '9fff5fc7-7118-4ccc-aafe-5da8fe5ba826');  -- PS-0000-LL-SO-001
-- Filas esperadas: 3 (en cascada: 4 requerimiento_lineas y 5 requerimiento_comentarios).

-- -------------------------------------------------------------------------------------
-- 4. RDT RECHAZADO del 14-10 (creado por jeyger22 en T7B). No cuenta para el PR (solo cuentan los VALIDADO).
-- -------------------------------------------------------------------------------------
delete from rdt_partes_historial
 where rdt_parte_id = 'dcf5e7b8-0468-452b-8628-ac2b96a3b356';
-- Filas esperadas: 1 (la foto de la accion RECHAZAR, id 03db30de-7fc4-4b9a-94dc-028694f4e779).

delete from rdt_partes
 where id = 'dcf5e7b8-0468-452b-8628-ac2b96a3b356'
   and proyecto_id = '0a20df2f-c5e9-4296-9c08-f89af499182d'
   and estado_validacion = 'RECHAZADO';
-- Filas esperadas: 1 (en cascada: 1 rdt_actividades, 1 rdt_tareo, 1 rdt_tareo_horas; vinculos a partida: 0).

-- -------------------------------------------------------------------------------------
-- 5. SERVICIO PS-0005 «PRUEBA T7»: el borrado en cascada se lleva proyecto_documentos (2), proyecto_miembros,
--    avisos del servicio, y toda tabla hija con proyecto_id. Es lo mismo que hace el boton «Eliminar proyecto».
--    El archivo PRUEBA-T7-plano.txt en Storage NO lo borra el SQL (ver limpieza-notas.md).
-- -------------------------------------------------------------------------------------
delete from proyectos
 where id = 'e15799ae-d964-4db7-b33f-39dc9c1a3860'
   and numero = 'PS-0005' and nombre = 'PRUEBA T7' and cliente = 'PRUEBA';
-- Filas esperadas: 1 (en cascada: 2 proyecto_documentos, los proyecto_miembros y todos los avisos con proyecto_id = PS-0005).

-- -------------------------------------------------------------------------------------
-- 6. COMPROBACION DENTRO DE LA TRANSACCION: si queda algo de lo borrado, aborta y revierte todo.
-- -------------------------------------------------------------------------------------
do $$
declare
  restos int;
begin
  select count(*) into restos from (
    select 1 from proyectos where id = 'e15799ae-d964-4db7-b33f-39dc9c1a3860'
    union all select 1 from proyecto_requerimientos where id in ('2cbd3bf7-78cc-480b-9877-d6fa98d49e9b','f5733231-0830-41e8-8ff2-1a930d29813e','9fff5fc7-7118-4ccc-aafe-5da8fe5ba826')
    union all select 1 from rdt_partes where id = 'dcf5e7b8-0468-452b-8628-ac2b96a3b356'
    union all select 1 from notificaciones
      where proyecto_id = 'e15799ae-d964-4db7-b33f-39dc9c1a3860'
         or id in ('0f3f2939-e135-4adc-9b5c-bfcbc0a45fb2','53b67926-565e-45e4-b9ce-bd262bf81218','da63c035-ad7c-4e66-8be0-182c14190793','c8de8200-2368-47a2-af60-7cd60057798f')
         or referencia_id in ('2cbd3bf7-78cc-480b-9877-d6fa98d49e9b','f5733231-0830-41e8-8ff2-1a930d29813e','9fff5fc7-7118-4ccc-aafe-5da8fe5ba826','99f82005-60f0-4fc2-8697-fc939bf13e6e','dcf5e7b8-0468-452b-8628-ac2b96a3b356')
         or mensaje like '%PS-0000-LL-SO-001%' or mensaje like '%PS-0000-LL-SO-002%' or mensaje like '%PS-0000-LL-SO-003%'
  ) x;
  if restos <> 0 then
    raise exception 'COMPROBACION: quedan % filas de prueba tras la limpieza; se revierte todo.', restos;
  end if;
  -- Los RDT de PS-0000 deben haber bajado exactamente en 1 (el rechazado); el validado del 17-10 sigue (seccion opcional).
  if (select count(*) from rdt_partes where proyecto_id = '0a20df2f-c5e9-4296-9c08-f89af499182d')
     <> (select filas - 1 from _antes_limpieza where orden = 14) then
    raise exception 'COMPROBACION: la cantidad de RDT de PS-0000 no bajo exactamente en 1.';
  end if;
end $$;

commit;

-- -------------------------------------------------------------------------------------
-- 7. COMPROBACION FINAL (resultado visible): antes / despues por concepto. Todas las filas de «despues» deben ser 0,
--    salvo el control de RDT de PS-0000 (debe quedar en antes - 1).
-- -------------------------------------------------------------------------------------
select a.concepto, a.filas as antes, d.filas as despues
  from _antes_limpieza a
  join _conteo_limpieza d on d.orden = a.orden
 order by a.orden;

-- =====================================================================================
-- SECCION OPCIONAL 1 (COMENTADA, APARTE): RDT VALIDADO del 17-10 de jeyger (id 99f82005-60f0-4fc2-8697-fc939bf13e6e).
-- RIESGO: es un RDT VALIDADO de PS-0000 (actividad 1.1.4 con metrado ejecutado 0, 8 HH de un AYUDANTE TOPOGRAFO). El PR, el
-- acumulado y el dashboard de PS-0000 se calculan completos desde todos los RDT VALIDADO; al borrarlo hay que recalcular
-- el PR (igual que hace el DELETE de la app), y el AC / HH reales de PS-0000 bajan 8 HH (el avance fisico no cambia: metrado 0).
-- Aplicar SOLO si Victor lo decide, en una ejecucion separada, despues de la limpieza principal. Quitar los «-- » para usarla.
-- =====================================================================================
-- begin;
-- do $$
-- begin
--   if (select count(*) from rdt_partes
--        where id = '99f82005-60f0-4fc2-8697-fc939bf13e6e'
--          and proyecto_id = '0a20df2f-c5e9-4296-9c08-f89af499182d'
--          and fecha_lima = date '2026-10-17' and estado_validacion = 'VALIDADO'
--          and especialidad = 'PRUEBA' and creado_por_id = 'c414ba1c-81e2-47e1-a9a1-e71823c3a78c') <> 1 then
--     raise exception 'GUARDA: el RDT validado 99f82005... no coincide.';
--   end if;
-- end $$;
-- delete from rdt_partes_historial where rdt_parte_id = '99f82005-60f0-4fc2-8697-fc939bf13e6e';
-- -- Filas esperadas: 1 (la foto de la accion VALIDAR, id 4fa195ec-752c-4c17-ac45-318c6fe24fcb).
-- delete from rdt_partes where id = '99f82005-60f0-4fc2-8697-fc939bf13e6e' and estado_validacion = 'VALIDADO';
-- -- Filas esperadas: 1 (en cascada: 1 rdt_actividades, 1 rdt_tareo, 1 rdt_tareo_horas, y el vinculo a partida si existe).
-- select recalcular_pr_desde_rdt('0a20df2f-c5e9-4296-9c08-f89af499182d');
-- -- Reconstruye el PR de PS-0000 desde los RDT VALIDADO que quedan (es la misma funcion que usa la app).
-- commit;

-- =====================================================================================
-- SECCION OPCIONAL 2 (COMENTADA, APARTE): devolver el celular de PRUEBA Logistica 1 a vacio (T7C dejo 999000111).
-- La cuenta se conserva; solo se limpia el dato de prueba del perfil. El correo pendiente de confirmar vive en
-- Supabase Auth (auth.users) y no se toca desde aqui.
-- =====================================================================================
-- update perfiles set celular = null
--  where id = '4aced21b-466c-492f-b872-83ddf0f40d36' and celular = '999000111';
-- -- Filas esperadas: 1.
