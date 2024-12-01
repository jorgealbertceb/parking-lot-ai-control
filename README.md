# 🚗 Proyecto de Detección de Plazas Libres y Ocupadas en un Parking utilizando IA

En este proyecto se desarrolló una aplicación basada en IA para detectar el estado de las plazas de aparcamiento en un parking utilizando modelos de visión por computadora. Este README detalla los pasos para instalar y ejecutar el proyecto, así como los errores y soluciones encontrados durante el desarrollo. 🎯

---

## 🎥 Video demostración del proyecto

Para ver cómo funciona la aplicación en acción, consulta el siguiente video:
![Video](data/Videos/Resultados/video_demostracion.mp4)

---

## 📥 Instalación y Configuración

1. **Requisitos previos:**
   - **Python 3.8 o superior:** Asegúrate de tener instalado Python. Puedes descargarlo desde [python.org](https://www.python.org/).
   - **Librerías necesarias:** Instala las librerías requeridas ejecutando:
     ```bash
     pip install -r requirements.txt
     ```

2. **Archivos de prueba:**
   - Videos de prueba disponibles en `data/Videos`.
   - Imágenes redimensionadas y adaptadas disponibles en `data/Imagenes`.

---

## 🚀 Pasos para ejecutar la aplicación

1. **Ejecuta App1 y App2 en local:**
   - Asegúrate de instalar las dependencias mencionadas anteriormente.
   - Lanza ambas aplicaciones desde la terminal:
     ```bash
     python app1.py
     python app2.py
     ```
   - Abre el archivo HTML generado en tu navegador web.

2. **Flujo de trabajo en la aplicación:**

   - **App1: Selección de plazas de parking:**
     1. En la interfaz web, pulsa el botón **App1**.
     2. Selecciona una imagen del parking desde `data/Imagenes`.
     3. Usa la herramienta interactiva para marcar las plazas de parking.
     4. Pulsa **Submit** y luego **Flag** para guardar las coordenadas.
     5. El archivo CSV generado estará disponible en `flagged/log.csv`.

   - **App2: Predicción del estado de las plazas:**
     1. Vuelve al menú principal y selecciona **App2**.
     2. Sube los siguientes archivos:
        - El **CSV** generado por App1.
        - Un **video** correspondiente al parking (por ejemplo: para `imagen_parking1`, usa `video_parking1_recortado`).
     3. Pulsa **Hacer predicción** y espera aproximadamente 3 minutos.
     4. Los resultados se guardarán en la carpeta `runs`:
        - **Archivo JSON** con las plazas detectadas: `runs/rectangles.json`
        - **Video** con la predicción aplicada: `runs/parking_management.mp4`

---

## 🛠️ Errores y Soluciones

### **1. Problema con la detección imprecisa en el video inicial:**
   - **Descripción:**
     - Al trabajar con el video inicial (`video_prueba.mp4`), se identificaron falsos positivos en áreas no correspondientes a plazas de parking.
   - **Solución:**
     - Recorte del video: Limitamos el análisis a las áreas relevantes.
     - El video recortado está disponible en: `video_prueba_recortado.mp4`.

### **2. Mejor definición de las plazas y precisión en la detección:**
   - **Descripción:**
     - El método inicial con **bounding boxes** no distinguía correctamente las plazas en áreas complejas.
   - **Solución:**
     - **Definición manual con ParkingPtsSelection():**  
       Se implementó una herramienta gráfica basada en **Tkinter** para definir polígonos alrededor de cada plaza.
     - **Entrenamiento optimizado:**  
       Se utilizó el modelo **YOLOv11s**, entrenado con un dataset de **más de 8,000 objetos** vistos desde drones.

### **3. Resultados esperados tras las mejoras:**
   Con estas implementaciones, se lograron los siguientes avances:
   - ✅ **Mayor precisión:** Reducción de falsos positivos relacionados con áreas no destinadas a aparcamiento.
   - 🚀 **Velocidad optimizada:** Gracias al modelo **YOLOv11s**.
   - 🔄 **Escalabilidad:** Ahora es posible aplicar la solución a otros escenarios con vistas aéreas de parkings.

---

## 📁 Archivos Relacionados

- **Video inicial:** `video_prueba.mp4`
- **Video con resultados iniciales:** `runs/detect/predict/video_prueba.mp4`
- **Video recortado:** `video_prueba_recortado.mp4`

---

Este documento se actualizará conforme se identifiquen nuevos desafíos y soluciones durante el desarrollo. ¡Gracias por tu interés en este proyecto! 😊
