# T1b — Ajuste de estilo del sello (Worker 1)

Rama `local-worker-1`, commit `9f3ddf9` (sobre 734a151). Sin push. `FotoCampo.tsx` sin cambios.

## Valores finales
- Fuente: pila `Roboto, system-ui, "Segoe UI", sans-serif`; peso 400 (antes 600).
- Sin contorno. Sombra: `rgba(0,0,0,0.75)`, desenfoque 0,3 x letra, desplazamiento vertical 0,04 x letra, 1 pasada.
- Interlineado 1,1 x letra (antes 1,25).
- Letra: `FRACCION_LETRA_SELLO` = 0,03 (sin cambio). A 463 px da 14 px; a 1600 px, 48 px.
- Margen inferior 1 % del lado mayor; derecho 0,5 % (antes 2 % en ambos). Medido en la referencia: el texto casi toca el borde derecho.
- `tamanoSello` devuelve ahora `margenDerecho`; `ContextoSello` cambia (sin stroke; con shadow*).

## Comparacion (evidencia)
`muestra-sello-v2-3pct.jpg` y `comparacion-sello-v2-vs-referencia.png` en la carpeta de evidencia.
Letra, grosor, espaciado, posicion y ancho de bloque coinciden con la referencia (lineas de 14 px, bases a 15-16 px, ancho de la linea mas larga ~26 %). Fuente Roboto Regular registrada solo en el script de muestra.

## Pruebas
vitest informes 69/69; npm test 194 archivos / 2097 pasan, 1 omitida (igual a la base); eslint de los 3 archivos limpio; npm run lint 9 errores / 22 avisos (igual a la base); `npx tsc --noEmit` sin errores (por confirmar como comando oficial).

## Pregunta abierta
Roboto en la app: en Android existe, pero en Samsung u otros celulares/navegadores de escritorio puede caer a `system-ui`. Recomendado: cargar Roboto con `next/font/google` (ya se usa para Geist) con `display: 'swap'` y asegurarse de esperar `document.fonts.load('400 48px Roboto')` antes de dibujar el sello en el lienzo. Sin implementar.

## Archivo temporal
`D:\VICTOR\CLAUDE CODE\pg_control_proyectos\prueba-sello-T3.jpg` (de otro subagente) sigue en la raiz del repositorio de documentos; no se toco.
