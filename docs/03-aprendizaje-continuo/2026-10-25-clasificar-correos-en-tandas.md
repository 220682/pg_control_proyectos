# 2026-10-25 — Clasificar un buzón grande: una ronda de aprendizaje con Sonnet y el resto con Haiku, sobre una exportación fuera del repositorio

## Origen

Plan [`2026-10-24-estado-del-servicio.md`](../02-trabajo-activo/01-planes/2026-10-24-estado-del-servicio.md), clasificación manual de los correos del 7 de septiembre al 25 de octubre (1 341 correos, 1 041 por ubicar). Método de trabajo, no regla del sistema.

## Método que funcionó

- **Exportar y trabajar fuera del repositorio.** Un script con el cliente de servidor de la app (`scripts/revision/cliente.mjs`, que lee `.env.local` sin mostrarlo) vuelca los correos a un JSON en el scratchpad de la sesión. Los correos son privados de la empresa: ni la exportación ni las salidas de los clasificadores entran al repo.
- **Ronda de aprendizaje.** 4 subagentes Sonnet con 60 correos al azar cada uno. Además de clasificar, cada uno deja un archivo de «reglas aprendidas» (pistas por servicio, casos ambiguos, dudas para el responsable, qué cambiaría del encargo). Con eso se escribe el encargo de la ronda siguiente.
- **Ronda masiva.** El encargo mejorado y 9 subagentes Haiku con ~90 correos cada uno (cuerpo ampliado a 2 500 caracteres). El encargo pasa de «clasificar todo» a una decisión de dos salidas: uno de los servicios vigentes o `AJENO`.
- **Lo que hizo falta en el encargo:** una tabla de pistas seguras por servicio (dominios, contrapartes, contratos u OC, nombre real del servicio en los correos, que no siempre es el del presupuesto), la lista cerrada de temas para que no aparezcan variantes del mismo, y la regla de «ante la duda, `AJENO` con confianza baja».
- **Las preguntas de negocio se hacen entre rondas, no durante.** La ronda de aprendizaje destapó que solo el 27 % de los correos era de los 4 servicios; esa decisión (qué hacer con lo ajeno y con lo administrativo) la tomó el responsable con tres opciones claras antes de lanzar la ronda masiva.

## Trampas encontradas

- **Verificar ids por script, no por conteo.** Varios subagentes escribieron el JSON a mano y comprobaron ids solo con búsquedas de texto. La validación (`mismo largo e ids en el mismo orden que la entrada`, resumen ≤ 180, destino válido) la corre quien coordina, con un script, antes de aplicar nada a la base.
- **El verificador de seguridad de comandos puede caer a mitad de una tanda.** Cuando falla, ni la terminal ni el navegador responden y los subagentes no pueden correr sus propias comprobaciones. Dejar el script de validación ya guardado en el scratchpad y no encadenar reintentos.
- **Credenciales dentro de los correos.** Dos correos traían usuario y contraseña en el texto. Los subagentes no las copian en sus resúmenes (se les pide); lo guardado en la base se decide aparte con el responsable.
- **Muchos correos administrativos no nombran el servicio** (alimentación del campamento, migración y activación de personal, movilización). Solo el contrato u OC los ata a un servicio y no siempre aparece; sin ese dato no se adivina.
