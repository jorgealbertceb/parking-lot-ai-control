# 🚗 Proyecto de Detección de Plazas Libres y Ocupadas en un Parking utilizando IA

En este documento se describen los principales errores encontrados durante el desarrollo de este proyecto, así como las soluciones implementadas. ¡Esperamos que esta información sea útil tanto para entender el progreso como para futuras mejoras! 🎯

---

## 🛠️ Errores y Soluciones

### **1. Problema con la detección imprecisa en el video inicial**

#### 📄 Descripción del problema:
Al trabajar con el video inicial, `video_prueba.mp4`, se utilizó **Roboflow** para dividirlo en frames y etiquetar las plazas de parking como libres u ocupadas. Se entrenó un modelo basado en **YOLOv11x**, pero al evaluar los resultados en el video generado (`runs/detect/predict/video_prueba.mp4`), se detectaron los siguientes problemas:

- El modelo identificaba incorrectamente partes de la carretera como plazas de parking libres.
- Aunque se reconocían las etiquetas `Car parked` y `Clear to parked`, la precisión no era suficiente.

#### 🛠️ Solución:
1. **Recorte del video:**  
   - Para simplificar el problema y mejorar la precisión del modelo, se recortó el video original, limitando el análisis a las áreas más relevantes.  
   - El video recortado se encuentra disponible en: `video_prueba_recortado.mp4`.

---

### **2. Mejor definición de las plazas y precisión en la detección**

#### 📄 Descripción del problema:
El método inicial basado en etiquetas y bounding boxes no era lo suficientemente preciso para distinguir plazas de parking en áreas complejas.

#### 🛠️ Solución:
1. **Uso de Ultralytics y ParkingPtsSelection():**  
   - Se implementó la función `ParkingPtsSelection()` de la biblioteca **Ultralytics Solutions**, que permite definir manualmente las plazas de parking mediante polígonos en una interfaz gráfica con **Tkinter**.
   - Esta herramienta facilita que el modelo reconozca las plazas exactas al dibujar rectángulos o polígonos alrededor de cada una.

2. **Entrenamiento con vistas de drone:**  
   - Se utilizó el modelo **YOLOv11m** debido a su mejor balance entre velocidad y precisión.
   - El dataset utilizado contenía **más de 8,000 objetos** vistos desde drones, lo que permite al modelo identificar vehículos desde una perspectiva aérea.

---

### **3. Resultados esperados tras las mejoras**

Con estas implementaciones, se lograron los siguientes avances:

- ✅ **Mayor precisión:** Reducción de falsos positivos relacionados con áreas no destinadas a aparcamiento.  
- 🚀 **Velocidad optimizada:** Gracias al modelo YOLOv11m.  
- 🔄 **Escalabilidad:** Ahora es posible aplicar la solución a otros escenarios con vistas aéreas de parkings.

---

## 📁 Archivos relacionados

- **Video inicial:** [`video_prueba.mp4`](./path/to/video_prueba.mp4)  
- **Video con resultados iniciales:** [`runs/detect/predict/video_prueba.mp4`](./path/to/runs/detect/predict/video_prueba.mp4)  
- **Video recortado:** [`video_prueba_recortado.mp4`](./path/to/video_prueba_recortado.mp4)  

---

Este documento se actualizará conforme se identifiquen nuevos desafíos y soluciones durante el desarrollo. ¡Gracias por tu interés en este proyecto! 😊
