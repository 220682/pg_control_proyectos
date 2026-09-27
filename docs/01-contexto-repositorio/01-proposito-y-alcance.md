# Propósito y alcance

## Dos repositorios, dos objetos distintos

- **`pg_control_proyectos`** (este repositorio): fuente documental y arquitectónica del sistema de control de proyectos. No es la aplicación web de producción. Aquí vive la lógica de negocio, los flujos, los formatos, las decisiones de diseño y el estándar de trabajo de los agentes.
- **`py_control_proyectos_web`**: la aplicación web real. El código de la app, sus pantallas, su base de datos y sus migraciones viven ahí, no en este repositorio.

## Qué pertenece a cada uno

| Pertenece a `pg_control_proyectos` | Pertenece a `py_control_proyectos_web` |
|---|---|
| Reglas de negocio, flujos, especificaciones | Código de la app, componentes, rutas |
| Planes, progreso, evidencia (registro documental) | Migraciones SQL, esquema de base de datos |
| Estándar de trabajo de agentes | Implementación de pantallas y UI |
| Mockups y sistema de diseño (referencia) | Tests automatizados de la app |

## El Responsable humano de este repositorio

El Responsable humano de `pg_control_proyectos` es **Victor**. Es quien aprueba los Gates (§ ver `00-estandar-agentes/04-flujo-sdd-y-planes.md`), decide el objetivo de cada plan y resuelve las consultas directas de un Worker ante un conflicto de negocio no anticipado (excepción D6).

## Límites de cambios y de validación disponibles

- Este repositorio no tiene lint, build, tests ni migraciones verificados (ver `AGENTS.md` § Stack y comandos). Cualquier comando que no esté confirmado ahí se considera "por confirmar" y no se inventa.
- Las validaciones de código real (Playwright, tests automatizados) se ejecutan en `py_control_proyectos_web`, no en este repositorio.
- No se debe asumir que aquí se desarrolla runtime de ningún tipo: es una base documental que luego se materializa en la app real.
