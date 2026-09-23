# Mejora de trabajo — acceso directo a Postgres sin salida IPv6

> Origen: tarea [2026-09-21-curva-s-fase-3-agente-d.md](../Tareas%20de%20implementacion/2026-09-21-curva-s-fase-3-agente-d.md) (Agente A, commit `b8b3ac7` en `pg_control_proyectos`). Extraído el 2026-09-23.

## Qué pasó

Para el plan de PR enriquecido (Fase 1 y 2), Victor autorizó dar la cadena de conexión directa de Postgres (`PR_DB_URL`) a los agentes en la nube, para que corrieran sus propias migraciones sin pausar a confirmar cada una. Al intentar usarla, `PR_DB_URL` resultó **inalcanzable desde el sandbox por falta de salida IPv6** al puerto directo de Postgres de Supabase.

## Cómo se resolvió

El agente aplicó sus migraciones vía la **Management API de Supabase** en lugar de la conexión directa Postgres. Si vuelve a pasar (sandbox sin salida IPv6), usar esa vía y dejarlo anotado en la tarea correspondiente.

## Alcance de la excepción (no cambia la regla general)

Dar la cadena de conexión directa fue una excepción puntual, acotada a esos dos agentes y esa tarea — ver `docs/Tareas de implementacion/tareas-futuras.md`. La regla general sigue siendo: sin esa cadena de conexión, cada migración se confirma con Victor antes de correrla.
