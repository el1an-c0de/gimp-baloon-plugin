# Add Balloon — plugin de GIMP

Plugin de GIMP 3.x que agrega texto centrado (con wrap automático, fuente, color y contorno configurables) dentro de una selección activa — pensado para poner diálogos/globos de texto sobre páginas de manga o cómic.

Este proyecto es un **fork** de [gimp-baloon-plugin](https://github.com/nicolalandro/gimp-baloon-plugin) de [nicolalandro](https://github.com/nicolalandro). El plugin original estaba escrito contra una API de desarrollo temprana de GIMP 3.0 que cambió antes del release estable; este fork lo actualiza para funcionar con la API estable de **GIMP 3.2** y agrega funcionalidades nuevas (plantillas, contorno de texto, selector de fuente/color, traducción al español, etc.).

La idea de simplificar el flujo de trabajo de rotulado (posicionar, alinear y gestionar estilos de texto) está inspirada en [TyperTools](https://swirt.github.io/typertools/) — una extensión de Photoshop diseñada para rotulistas ("typesetters") que trabajan con guiones de manga y cómics.

## Qué hace

Menú: **Select → Add Balloon...** (requiere una selección activa en la imagen).

Al ejecutarlo se abre un diálogo con:

- Cuadro de texto, con wrap automático dentro de la selección.
- Selector de fuente.
- Selector de color de texto.
- Contorno (checkbox) + color de contorno + grosor.
- Plantillas ("Título", "Subtítulo", etc.) que guardan fuente, tamaño, color y contorno, con botones para guardar y eliminar.

Al confirmar, crea una capa de texto real de GIMP (no rasterizada, sigue siendo editable), centrada horizontal y verticalmente dentro de la selección, sin fondo ni grupo de capas.

## Requisitos

- GIMP **3.2** o superior (usa la API estable de Python-Fu de GIMP 3.x).

## Instalación

### Linux (GIMP vía Flatpak)

1. Copiar la carpeta `add_balloon` **completa** (incluye `add_balloon.py` y la carpeta `locale/` con las traducciones) a:
   ```
   ~/.config/GIMP/3.2/plug-ins/add_balloon/
   ```
2. Dar permiso de ejecución:
   ```bash
   chmod +x ~/.config/GIMP/3.2/plug-ins/add_balloon/add_balloon.py
   ```
3. Reiniciar GIMP.

### Windows

1. Abrir GIMP una vez (para que genere `%APPDATA%\GIMP\3.2\`) y cerrarlo.
2. Copiar la carpeta `add_balloon` **completa** (incluye `add_balloon.py` y la carpeta `locale/` con las traducciones) a:
   ```
   %APPDATA%\GIMP\3.2\plug-ins\add_balloon\
   ```
   (por ejemplo: `C:\Users\<usuario>\AppData\Roaming\GIMP\3.2\plug-ins\add_balloon\`)
3. Reiniciar GIMP.

### Plantillas

Las plantillas guardadas se persisten en `add_balloon_presets.json`, en la misma carpeta que `add_balloon.py`. Se crea solo al guardar la primera plantilla desde el diálogo del plugin.

## Uso
En ambos casos:
- Seleccionar zona, en el menú **Select → Add Balloon...** 
- Seleccionar zona, **clic derecho → Select → Add Balloon...** 
- Puedes crear un Keyboard Shortcut, **Menú Edit → Keyboard Shortcut → Buscar Add Balloons → Agregar combinación de teclas** 

## Notas técnicas

### Idioma

El plugin sigue el idioma configurado en GIMP (Edit → Preferences → Interface → Language; requiere reiniciar GIMP). El código está escrito en inglés como idioma base, y la traducción al español vive en `add_balloon/locale/es/LC_MESSAGES/add_balloon.mo`. Si copiás solo `add_balloon.py` sin la carpeta `locale/`, el plugin va a seguir funcionando, pero siempre en inglés sin importar el idioma configurado en GIMP — por eso la carpeta `add_balloon` se copia completa en los pasos de instalación.

### Centrado del texto

El centrado se calcula respecto al recuadro (bounding box) de la selección, no a su forma real — en una selección circular, por ejemplo, el texto se centra en el cuadrado que la contiene, que es el comportamiento esperado. En versiones anteriores de este fork, el texto podía quedar desplazado hacia la derecha (más notorio en selecciones no rectangulares, donde cualquier desvío se nota más): la causa era usar un movimiento relativo (`transform_translate`) para posicionar el texto en vez de fijar su posición absoluta. Ya está corregido usando `set_offsets`.

### Edición de una capa ya creada (limitación conocida en Windows)

Las capas de texto que crea el plugin se centran con `resize()` (activa modo de caja fija) + recorte al texto real + reposicionamiento. GIMP no ofrece una forma de avisarle después a la capa "tu caja de edición ahora es esta otra", así que la herramienta Texto interactiva puede detectar una discrepancia al reabrir la capa para editarla.

En la práctica esto se ve así: doble clic sobre la capa para editar el texto → GIMP muestra un aviso de "¿editar de todos modos?" → al confirmar, el texto puede rasterizarse y desplazarse de su posición centrada.

**No es necesario arreglar la capa manualmente si esto pasa**: es más simple borrar la capa y volver a correr el plugin (rápido gracias a las plantillas) que editar la capa existente.

## Créditos

- Proyecto original: [nicolalandro/gimp-baloon-plugin](https://github.com/nicolalandro/gimp-baloon-plugin)
- Inspiración de flujo de trabajo: [TyperTools](https://swirt.github.io/typertools/) (extensión de Photoshop)

## Licencia

El proyecto original no declara una licencia. Mientras eso no cambie, este fork tampoco incluye una licencia explícita.
