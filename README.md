# Add Balloon — plugin de GIMP

Plugin de GIMP 3.x que agrega texto centrado (con wrap automático, fuente, color y contorno configurables) dentro de una selección activa — pensado para poner diálogos/globos de texto sobre páginas de manga o cómic.

Este proyecto es un **fork** de [gimp-baloon-plugin](https://github.com/nicolalandro/gimp-baloon-plugin) de [nicolalandro](https://github.com/nicolalandro). El plugin original estaba escrito contra una API de desarrollo temprana de GIMP 3.0 que cambió antes del release estable; este fork lo actualiza para funcionar con la API estable de **GIMP 3.2** y agrega funcionalidades nuevas (plantillas, contorno de texto, espaciado de línea dinámico, selector de fuente/color, etc.).

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

1. Copiar la carpeta `add_balloon` (con `add_balloon.py` adentro) a:
   ```
   ~/.config/GIMP/3.2/plug-ins/add_balloon/add_balloon.py
   ```
2. Dar permiso de ejecución:
   ```bash
   chmod +x ~/.config/GIMP/3.2/plug-ins/add_balloon/add_balloon.py
   ```
3. Reiniciar GIMP.

### Windows

1. Abrir GIMP una vez (para que genere `%APPDATA%\GIMP\3.2\`) y cerrarlo.
2. Copiar `add_balloon.py` a:
   ```
   %APPDATA%\GIMP\3.2\plug-ins\add_balloon\add_balloon.py
   ```
   (por ejemplo: `C:\Users\<usuario>\AppData\Roaming\GIMP\3.2\plug-ins\add_balloon\add_balloon.py`)
3. Reiniciar GIMP.

### Uso
En ambos casos:
- Seleccionar zona, en el menú **Select → Add Balloon...** 
- Seleccionar zona, **clic derecho → Select → Add Balloon...** 
- Puedes crear un Keyboard Shortcut, **Menú Edit → Keyboard Shortcut → Buscar Add Balloons → Agregar combinación de teclas** 

aparece después de reiniciar GIMP, con una selección activa en la imagen.

### Plantillas

Las plantillas guardadas se persisten en `add_balloon_presets.json`, en la misma carpeta que `add_balloon.py`. Se crea solo al guardar la primera plantilla desde el diálogo del plugin.

## Créditos

- Proyecto original: [nicolalandro/gimp-baloon-plugin](https://github.com/nicolalandro/gimp-baloon-plugin)
- Inspiración de flujo de trabajo: [TyperTools](https://swirt.github.io/typertools/) (extensión de Photoshop)

## Licencia

El proyecto original no declara una licencia. Mientras eso no cambie, este fork tampoco incluye una licencia explícita.
