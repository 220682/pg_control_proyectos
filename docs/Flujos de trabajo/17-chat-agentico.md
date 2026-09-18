# 17 — Chat agéntico

**No habilitado. Sin diseño técnico.** Pedido por Victor el 2026-09-16, dentro de la conversación del flujo 15 (Cronograma) pero **no exclusivo de Cronograma** — es un agente del sistema.

Idea: tras leer un archivo que el usuario sube (presupuesto, cronograma, y a futuro cualquier otro formato), el agente inicia una conversación contándole lo que encontró — *"he leído el presupuesto/cronograma y he encontrado lo siguiente..."* — y a partir de ahí interactúa con el usuario para terminar de extraer/completar los datos que el parser automático no pudo resolver solo, siguiendo una convención estricta de cómo debe quedar esa extracción al final.

Encaja con dos informes estáticos (no conversacionales) que ya existen o están pedidos:
- Informe de extracción del Cronograma (flujo 15, ya construido).
- Informe completo de errores de importación del DP (pedido 2026-09-13, no implementado — ver `docs/Mejoras continuas/`).

Ambos serían la base de datos que este agente usaría después para conversar. Por eso Victor pidió, por ahora, solo el informe estático, sin habilitar la parte conversacional.

Sin decidir todavía: qué agente/modelo lo implementaría, dónde viviría en la arquitectura, cómo se validaría que la respuesta del usuario encaja con la convención esperada, y si es un agente por tipo de archivo o uno solo para varios formatos.
