# Diagrama — Commit / Push / Merge / Gates durante la implementación

> Complementa `2026-09-27-reestructuracion-documental-y-estandar-de-trabajo.md` y el flujo SDD→Cierre. Este diagrama se enfoca solo en la mecánica de Git y los dos Gates de Victor, separando los dos repositorios involucrados. Se renderiza automáticamente al ver este archivo en GitHub.

```mermaid
flowchart TD
    Gate1{"GATE 1<br/>¿Victor aprueba<br/>plan + Punch List?"}
    Gate2{"GATE 2<br/>¿Victor aprueba<br/>el cierre?"}
    Conflicto{"¿Conflicto de<br/>regla de negocio?"}
    InformeListo{"¿Informe de auditoría<br/>listo para cierre?"}

    subgraph DOCS["pg_control_proyectos — documentación (siempre directo a main, sin rama)"]
        A["Planner: escribe 01-planes/&lt;tema&gt;.md<br/>(SDD + plan + Punch List, un solo archivo)"]
        B["commit + push a main"]
        I["Worker: escribe hallazgos en<br/>flujos de negocio / aprendizaje continuo / evidencia"]
        J["commit + push a main"]
        L["Auditor: emite Informe de Auditoría<br/>(APLICAR AHORA / PROPONER A VICTOR / NO PROMOVER)"]
        M["commit + push a main"]
        Q["Se aplican los cambios aprobados a<br/>AGENTS.md / README raíz / docs/README.md / estándar"]
        R["commit + push a main"]
        S(["Cierre: el plan es 100%<br/>recién cuando todo está pusheado"])
        A --> B --> Gate1
        I --> J
        L --> M
        Q --> R --> S
    end

    subgraph CODE["py_control_proyectos_web — código real (rama por Worker, merge solo en Gate 2)"]
        D["Orquestador asigna rama<br/>&lt;entorno&gt;-worker-N + worktree"]
        E["Worker implementa en su rama"]
        F["commit local"]
        G["push a &lt;entorno&gt;-worker-N<br/>(~35% de avance, nunca a medias de un ítem)"]
        K["Auditor: git log / git branch --contains<br/>confirma que los commits están en la rama correcta"]
        P["Merge &lt;entorno&gt;-worker-N → main<br/>(solo autorizado tras Gate 2)"]
        D --> E --> F --> G
    end

    Gate1 -- "No, ajustar" --> A
    Gate1 -- "Sí, autoriza toda la implementación" --> D
    G --> Conflicto
    Conflicto -- "Sí: Worker pregunta a Victor,<br/>anota en plan/progreso" --> E
    Conflicto -- "No" --> I
    J --> K --> L
    M --> InformeListo
    InformeListo -- "No, vuelve al Worker" --> E
    InformeListo -- "Sí" --> Gate2
    Gate2 -- "No, vuelve al Worker/Auditor" --> E
    Gate2 -- "Sí" --> P --> Q

    classDef gate fill:#fbe7e4,stroke:#c0392b,color:#15233a,stroke-width:2px;
    classDef docs fill:#e3ebfa,stroke:#2b5fb0,color:#15233a;
    classDef code fill:#e0f3ef,stroke:#0f8a76,color:#15233a;
    classDef auditor fill:#f9e6ee,stroke:#b23e73,color:#15233a;

    class Gate1,Gate2,Conflicto,InformeListo gate;
    class A,B,I,J,Q,R,S docs;
    class D,E,F,G,P code;
    class K,L,M auditor;
```

## Lectura rápida

- **Azul (DOCS)** = escritura directa a `main` en este repositorio, sin rama ni merge — es documentación de proceso, no código.
- **Verde (CODE)** = trabajo real de Worker en `py_control_proyectos_web`, siempre en su rama `<entorno>-worker-N`, nunca en `main` hasta el merge.
- **Rosa** = acciones del Auditor (chequeo de rama + informe).
- **Rojo** = los dos Gates de Victor y las dos decisiones internas (conflicto de negocio, informe listo) — son los únicos puntos donde el camino puede volver atrás.
- El **merge** (`P`) ocurre una sola vez, después del Gate 2 — es el único paso que realmente publica el código en `main`.
