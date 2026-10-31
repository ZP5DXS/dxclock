# 🌍 DX Clock — HF Monitoring Dashboard

**ES:** Monitor de radioafición para visualizar actividad HF, spots DX, DXpeditions, propagación y alertas de indicativos en una sola pantalla.  
**EN:** Amateur-radio dashboard bringing together HF activity, DX spots, DXpeditions, propagation indicators and callsign alerts.

**📡 Abrir / Launch:** https://zp5dxs.github.io/dxclock/  
**Autor / Author:** ZP5DXS · Paraguay  
**Idiomas de la interfaz / UI languages:** Español · English · Português

> [🇪🇸 Documentación en español](#-documentación-en-español) · [🇬🇧 English documentation](#-english-documentation)

---

# 🇪🇸 Documentación en español

## ¿Qué es DX Clock?

DX Clock es un panel web para radioaficionados, inspirado en la idea de tener el estado de las bandas a simple vista. Reúne información de clusters DX, redes de recepción, expediciones, condiciones solares y actividad por bandas en una interfaz diseñada para el *shack*, monitores secundarios y pantallas 16:9.

No requiere una cuenta ni instalar un programa de escritorio: se utiliza desde un navegador compatible con JavaScript moderno. Su información depende de servicios externos; **un spot no equivale a un QSO confirmado y la actividad detectada no garantiza propagación hacia tu QTH**.

## Funcionalidades

### 🌐 Mapa mundial
- Mapa mundial interactivo con zoom, desplazamiento y restablecimiento.
- Spots representados mediante **círculos (FT8), triángulos (CW) y cuadrados (SSB)**.
- Colores asociados a las bandas y filtros por banda/modo.
- Agrupación visual de spots próximos.
- Etiquetas destacadas de DXpeditions y estaciones clasificadas como raras, con líneas que conectan etiqueta y posición.
- Visualización del **terminador día/noche** y una franja crepuscular (*grayline*).
- Capas separadas: SVG geográfico, Canvas 2D para spots y SVG superior para las etiquetas relevantes.

Las ubicaciones de algunos spots pueden ser aproximadas cuando el origen no informa coordenadas precisas. Los carteles pueden omitirse cuando no queda espacio disponible, para evitar superposiciones.

### 📻 DX Cluster y bandas
- Spots de CW, SSB y FT8, según los datos recibidos de las fuentes.
- Indicativos, banderas, frecuencia, banda, modo y reportes agrupados.
- Clasificaciones de rareza cuando están disponibles.
- Indicadores de actividad relativa por banda y selección de bandas.
- Filtros geográficos de continentes según la configuración de la interfaz.

### 🏝️ DXpeditions
- Información de expediciones anunciadas y su período de operación.
- Distinción entre estados activos y próximos, según los datos disponibles.
- Actividad reciente asociada a los indicativos de expedición.
- Frecuencias, modos, banderas y etiquetas en el mapa cuando se dispone de datos suficientes.
- Clasificaciones de rareza conservadas cuando las fuentes las proporcionan.

### 🔔 Ham Alert: indicativos vigilados
Una lista personal para destacar estaciones de interés.

1. Abrí **Configuración**.
2. Buscá **Ham Alert** y agregá indicativos (por ejemplo, `HF0PAS` o `ZS6HB`).
3. Podés eliminar indicativos o desactivar las alertas desde el mismo menú.
4. Cuando uno de esos indicativos aparece en un spot reciente, se muestra una **notificación en pantalla**.
5. Los indicativos vigilados reciben un distintivo rojo **ALERT** en el cluster y, si corresponde, en la sección de DXpeditions, **sin perder su categoría de rareza**.

La lista se guarda **localmente en ese navegador** (`localStorage`), no se sincroniza entre dispositivos. Se admiten hasta 100 indicativos en la implementación actual. Las alertas dependen de que la web esté abierta y de que sus fuentes reciban el spot; **no son notificaciones push externas ni alertas de audio garantizadas**. Se evita repetir la misma alerta en ciclos consecutivos de actualización.

### ☀️ Propagación y actividad solar
- Reloj UTC y reloj local con ajuste de zona horaria.
- Indicadores solares como **SFI**, **Kp** y **A-index**, cuando están disponibles.
- Indicaciones visuales de condiciones diurnas/nocturnas por banda.
- Imagen solar SDO si está disponible.
- Video solar opcional, deshabilitado en el funcionamiento predeterminado de bajo consumo.

Los índices y estimaciones son orientativos; no sustituyen herramientas de predicción específicas por trayectoria ni medidas reales de recepción.

### 🎨 Interfaz y visualización
- Temas claro, oscuro, negro y verde; estética *pixel* opcional.
- Interfaz en español, inglés y portugués.
- Indicativo de estación configurable.
- Pantalla completa.
- Preferencias conservadas en el navegador.
- Diseñado para escritorio y pantallas dedicadas; el rendimiento en Android TV Box depende del dispositivo y del navegador.

## 🚀 Uso rápido

1. Abrí **https://zp5dxs.github.io/dxclock/**.
2. Entrá a **Configuración** y ajustá indicativo, idioma, reloj y tema.
3. Seleccioná el modo y las bandas que querés observar.
4. Configurá los indicativos de **Ham Alert** si te interesa una estación particular.
5. Usá el modo de pantalla completa para una pantalla del shack.

### Parámetros de URL

| Parámetro | Efecto |
|---|---|
| `?lite=1` | Fuerza el perfil visual ligero. |
| `?effects=1` | Habilita efectos visuales opcionales. |
| `?movie=1` | Solicita el video solar cuando no está activo el modo ligero. |

Ejemplo para pantallas pequeñas:  
`https://zp5dxs.github.io/dxclock/?lite=1`

Los parámetros pueden combinarse con `&`. El modo ligero puede activarse automáticamente en navegadores que informan poca memoria mediante `navigator.deviceMemory`.

## ⚡ Optimización y consumo

Se incorporaron mejoras para reducir el trabajo continuo del navegador:

- Marcadores de spots dibujados con **Canvas 2D** en lugar de cientos de nodos SVG individuales.
- Separación del mapa, los spots y las etiquetas relevantes en capas.
- Menos redibujados duplicados del mapa y actualizaciones controladas de la grayline.
- Animaciones continuas y filtros gráficos costosos desactivados por defecto.
- Video solar desactivado por defecto.
- Protección contra consultas de spots solapadas.
- Redibujado del Canvas condicionado a la visibilidad de la pestaña.
- Colocación de carteles con detección de colisiones.

**Referencia de prueba:** durante el desarrollo se observó una reducción de CPU aproximada de 63 % a 3 % en un equipo concreto. No es un benchmark reproducible ni una garantía para otros navegadores. Para comparar, medí CPU, memoria y GPU en condiciones equivalentes.

## 🧩 Arquitectura

```text
Navegador / Browser
  ├── index.html           Interfaz y lógica del frontend
  ├── dxclock-v2.css       Estilos adicionales
  ├── dxcc_names.js        Nombres y utilidades DXCC
  ├── SVG                  Geografía, terminador y etiquetas
  ├── Canvas 2D            Marcadores de spots
  └── localStorage         Preferencias e indicativos vigilados
             │
             ├── cluster.zp5dxs.org  Spots, DXpeditions, audiencia
             ├── vailrerbn.com       Reportes RBN
             ├── hamqth.com          Spots DX
             ├── NOAA SWPC          Datos solares
             └── NASA SDO           Imagen solar
```

**Importante:** el frontend usa servicios remotos existentes. Publicar los archivos estáticos no crea un backend propio ni garantiza que las APIs estén disponibles. Algunas fuentes pueden fallar por red, cambios en sus interfaces, CORS, límites de servicio o mantenimiento.

### Estructura del repositorio

```text
dxclock/
├── index.html
├── dxclock-v2.css
├── dxcc_names.js
├── dxcc_names.json
├── dxpeditions.json
├── README.md
├── scripts/
│   └── update_dx.py
└── .github/
    └── workflows/
        └── update-dx.yml
```

El script `scripts/update_dx.py` puede actualizar `dxpeditions.json` a partir del calendario público NG3K. El workflow incluido programa su ejecución periódica en GitHub Actions. **La vista en vivo de DXpeditions del frontend también consulta el endpoint remoto**; el archivo JSON local no sustituye automáticamente esa API.

## 🛠️ Desarrollo y despliegue

Este repositorio contiene un frontend estático. Para probarlo localmente:

```bash
git clone https://github.com/ZP5DXS/dxclock.git
cd dxclock
python3 -m http.server 8000
```

Abrí `http://localhost:8000/` en el navegador.

Para publicarlo en GitHub Pages, configurá el repositorio para servir la rama y la carpeta que contienen `index.html`. Al desplegar una actualización, recargá sin caché si seguís viendo la versión anterior.

Si hacés un *fork*, tené en cuenta que los endpoints `cluster.zp5dxs.org` están definidos en el frontend. Para operar con infraestructura propia hay que adaptar las URLs y disponer de servicios compatibles. No es necesario ni recomendable modificar el servidor original para personalizar los estilos de la copia.

## 📺 Pantallas 24/7 y Android TV

Para uso continuo:
- Preferí `?lite=1` en hardware modesto.
- Usá un navegador actualizado y compatible con Canvas, SVG y JavaScript moderno.
- Configurá pantalla completa y, si el sistema lo permite, lanzamiento automático del navegador con la URL de DX Clock.
- Verificá por separado que la TV Box arranque al recibir energía: esa función depende del firmware.
- Comprobá estabilidad, memoria y recuperación de Internet durante varias horas antes de usarlo como panel permanente.

El proyecto **no incluye** una aplicación Android nativa ni un servicio que garantice el arranque automático del dispositivo.

## ⚠️ Limitaciones y privacidad

- Las frecuencias y spots son reportes de terceros; pueden estar duplicados, incompletos o desactualizados.
- La geolocalización basada en país o indicativo puede ser aproximada.
- Los indicadores de rareza dependen de datos externos, no implican confirmación de entidad DXCC.
- Ham Alert solo puede detectar estaciones presentes en las fuentes consultadas.
- Las preferencias y la lista de vigilancia se almacenan en `localStorage`.
- La versión actual envía un identificador de visitante y eventos de sesión al servicio de audiencia de `cluster.zp5dxs.org` para métricas de visitas y usuarios en línea.
- Las solicitudes a las APIs y los recursos remotos están sujetas a las políticas de los respectivos proveedores.

## 🤝 Contribuciones y licencia

Las propuestas, correcciones y *pull requests* son bienvenidas. Si encontrás un error, indicá navegador, dispositivo, pasos para reproducirlo y, si es posible, registros de consola.

**Licencia:** este repositorio no incluye actualmente un archivo `LICENSE` identificado. Que el código sea visible públicamente no significa que exista una licencia de reutilización abierta; agregá una licencia explícita al repositorio si querés autorizar uso, modificación y distribución por terceros.

**73 de ZP5DXS — Paraguay.**

---

# 🇬🇧 English documentation

## What is DX Clock?

DX Clock is a browser-based amateur-radio monitoring dashboard inspired by the idea of seeing current HF conditions at a glance. It brings together DX clusters, reception reports, DXpeditions, solar information and band activity in an interface designed for the shack, secondary monitors and 16:9 displays.

No account or desktop installation is required: open it in a browser supporting modern JavaScript. Data depends on external services. **A spot is not a confirmed QSO, and observed global activity does not guarantee propagation to your QTH.**

## Features

### 🌐 Interactive world map
- World map with zoom, panning and reset controls.
- **Circles for FT8, triangles for CW and squares for SSB.**
- Band colors and mode/band filters.
- Visual grouping of nearby reports.
- Highlighted DXpeditions and rare stations with callsign labels.
- Astronomical **day/night terminator** and enhanced **grayline/twilight band**.
- Separate rendering layers: geographical SVG, Canvas 2D spots and an SVG overlay for important labels.

Positions may be approximate when spot sources do not provide accurate coordinates. Some callouts may be omitted in crowded areas to prevent overlap.

### 📻 DX Cluster and band activity
- CW, SSB and FT8 spots, subject to source coverage.
- Callsigns, country flags, frequencies, bands, modes and grouped reports.
- Rarity categories when provided by the data.
- Relative band-activity indicators and band selection.
- Continent-based filters available in Settings.

### 🏝️ DXpeditions
- Announced expedition callsigns and operating windows.
- Active and upcoming status information, where available.
- Recent activity associated with expedition callsigns.
- Bands, modes, frequencies, flags and map labels when sufficient information is available.
- Existing rarity classifications preserved.

### 🔔 Ham Alert: watched callsigns
Maintain a personal list of stations you want to spot.

1. Open **Settings**.
2. Find **Ham Alert** and add callsigns (for example, `HF0PAS` or `ZS6HB`).
3. Remove callsigns or disable notifications from the same menu.
4. A **notification on the page** appears when a watched callsign is found in a recent spot.
5. Watched stations receive a red **ALERT** badge in the DX Cluster and, when applicable, DXpeditions, **without losing their rarity category**.

The current implementation supports up to 100 callsigns and saves them in browser `localStorage`. Lists are **not synchronized across devices**. Alerts only work while the page is running and receiving spots; they are not remote push notifications or guaranteed audible alarms. Repeated notifications for the same report are suppressed.

### ☀️ Solar conditions and clocks
- Large UTC clock and configurable local clock.
- **SFI**, **Kp** and **A-index** when available.
- Day/night band-condition indications.
- NASA SDO solar image.
- Optional solar movie, disabled by default for lower overhead.

Solar indices and generic estimates are indicative, not path-specific propagation forecasts or confirmed reception reports.

### 🎨 Customization
- Light, dark, black and green themes; optional pixel styling.
- Spanish, English and Portuguese interface.
- Configurable station callsign.
- Fullscreen mode and local preference storage.
- Desktop-oriented layout with use on dedicated displays; Android TV Box performance varies by hardware and browser.

## 🚀 Quick start

1. Visit **https://zp5dxs.github.io/dxclock/**.
2. Open **Settings** and adjust callsign, language, clock and theme.
3. Select a mode or one or more bands.
4. Add callsigns to **Ham Alert**, if needed.
5. Enter fullscreen mode for a dedicated shack display.

### URL parameters

| Parameter | Behavior |
|---|---|
| `?lite=1` | Forces lightweight visual mode. |
| `?effects=1` | Enables optional visual effects. |
| `?movie=1` | Requests the solar movie, except in lightweight mode. |

Low-resource device example:  
`https://zp5dxs.github.io/dxclock/?lite=1`

Parameters can be combined using `&`. Browsers exposing low available memory through `navigator.deviceMemory` may activate lightweight mode automatically.

## ⚡ Performance and optimization

The frontend has been optimized to reduce ongoing browser work:

- Spot symbols rendered in **Canvas 2D** rather than hundreds of separate SVG nodes.
- Separation of the base map, spot markers and important labels into different layers.
- Reduced duplicate redraws and minute-level grayline refresh.
- Continuous animations and costly SVG effects disabled by default.
- Solar movie disabled by default.
- Protection against overlapping spot requests.
- Visibility-aware Canvas repaint scheduling.
- Collision-aware placement of map callouts.

**Observed development result:** CPU usage decreased from approximately 63% to 3% in one specific test environment. This is not a standardized benchmark or a promise for other hardware. Compare CPU, memory and GPU under equivalent conditions.

## 🧩 Architecture

```text
Browser
  ├── index.html           UI and frontend logic
  ├── dxclock-v2.css       Additional styles
  ├── dxcc_names.js        DXCC names/helpers
  ├── SVG                  Geography, terminator and callouts
  ├── Canvas 2D            Spot markers
  └── localStorage         Preferences and watched callsigns
             │
             ├── cluster.zp5dxs.org  Spots, DXpeditions, audience
             ├── vailrerbn.com       RBN reception reports
             ├── hamqth.com          DX spots
             ├── NOAA SWPC          Solar data
             └── NASA SDO           Solar image
```

**Important:** the static frontend depends on existing remote services. Publishing these files does not deploy a replacement backend or guarantee API availability. Data sources can fail due to network issues, interface changes, CORS, quotas or maintenance.

### Repository structure

```text
dxclock/
├── index.html
├── dxclock-v2.css
├── dxcc_names.js
├── dxcc_names.json
├── dxpeditions.json
├── README.md
├── scripts/
│   └── update_dx.py
└── .github/
    └── workflows/
        └── update-dx.yml
```

The `scripts/update_dx.py` utility updates `dxpeditions.json` from the public NG3K calendar. The included GitHub Actions workflow schedules this update. **The frontend's live DXpedition view also calls a remote API**; the local JSON file is not automatically a replacement for that endpoint.

## 🛠️ Local development and deployment

This repository contains a static frontend. Run it locally with:

```bash
git clone https://github.com/ZP5DXS/dxclock.git
cd dxclock
python3 -m http.server 8000
```

Open `http://localhost:8000/`.

For GitHub Pages hosting, configure Pages to publish the branch and folder containing `index.html`. Hard-refresh after deployment if the old version is still cached.

If you fork the project, note that `cluster.zp5dxs.org` endpoints are currently embedded in frontend code. Running an independent deployment requires compatible backend services and updated URLs. Customizing a fork's CSS does not require changes to the original VPS.

## 📺 24/7 display and Android TV

For continuous operation:
- Prefer `?lite=1` on low-end devices.
- Use an up-to-date browser with modern JavaScript, SVG and Canvas support.
- Configure fullscreen and browser auto-launch where the operating system allows it.
- Separately check whether the TV Box automatically powers up after power is restored; this is firmware-specific.
- Test multi-hour stability, memory use and recovery after connectivity loss.

The project does **not** provide a native Android app or a guaranteed auto-boot mechanism.

## ⚠️ Data limitations and privacy

- Spots are third-party reports and may be duplicated, incomplete or stale.
- Locations inferred from callsign or country can be approximate.
- Rarity labels depend on external inputs and do not confirm DXCC credit.
- Ham Alert can only match stations present in available spot feeds.
- Settings and watched callsigns are stored in browser `localStorage`.
- The current implementation sends a visitor identifier and session events to `cluster.zp5dxs.org` for online-user and visit metrics.
- Requests to external APIs and media resources are subject to their respective providers' policies.

## 🤝 Contributions and licensing

Issues, bug fixes and pull requests are welcome. For bug reports, include browser, device, reproduction steps and console output when possible.

**License:** no `LICENSE` file was identified in the current repository snapshot. Public source visibility does not itself grant open-source reuse rights. Add an explicit license if you wish to authorize third-party use, modification and redistribution.

**73 de ZP5DXS — Paraguay.**
