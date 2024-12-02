# python app/app_2.py --server.port 7861

import pandas as pd
import json
import gradio as gr
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import uuid
import os

# Función para procesar el CSV y generar el JSON
def create_json_from_csv(csv_file):
    # Leer el archivo CSV
    data = pd.read_csv(csv_file)
    rectangles = []

    # Procesar las filas del DataFrame
    for index, row in data.iterrows():
        try:
            # Parsear la columna "Points" como JSON
            points_dict = json.loads(row["Points"])
            raw_coordinates = points_dict["data"]

            # Procesar cada conjunto de coordenadas
            for rect in raw_coordinates:
                x1, y1 = rect[0], rect[1]  # Esquina superior izquierda
                x2, y2 = rect[3], rect[4]  # Esquina inferior derecha

                # Crear el rectángulo
                rectangle = {
                    "points": [
                        [x1, y1],
                        [x2, y1],
                        [x2, y2],
                        [x1, y2]
                    ]
                }
                rectangles.append(rectangle)
        except Exception as e:
            return f"Error procesando la fila {index}: {e}"

    # Convertir la lista de rectángulos en JSON
    rectangles_json = json.dumps(rectangles, indent=4)

    # Guardar el JSON en un archivo
    output_file = "runs/rectangles.json"
    with open(output_file, "w") as f:
        f.write(rectangles_json)

def is_point_inside_polygon(point, polygon):
    """Comprueba si un punto (x, y) está dentro del polígono definido por las plazas."""
    x, y = point
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

def check_occupancy(detections, parking_coordinates):
    """Comprueba si las detecciones ocupan alguna plaza."""
    for park in parking_coordinates:
        park['occupied'] = False  # Reiniciar el estado de ocupación
        for detection in detections:
            det_x1, det_y1, det_x2, det_y2 = detection['bbox']
            vehicle_center = ((det_x1 + det_x2) / 2, (det_y1 + det_y2) / 2)  # Centro del vehículo

            # Verificar si el centro del vehículo está dentro del polígono de la plaza
            if is_point_inside_polygon(vehicle_center, park['points']):
                park['occupied'] = True
                break
    return parking_coordinates

def draw_frame_with_parking_status(frame, parking_coordinates, background_color=(255, 255, 255), font_path="data/fuentes/Parkinsans-VariableFont_wght.ttf"):
    """Dibuja el estado del parking en el frame, incluyendo un fondo a la derecha para las plazas libres."""
    free_count = 0
    occupied_count = 0
    free_spaces = []  # Lista de plazas libres

    # Dibujar las plazas numeradas y su estado
    for idx, park in enumerate(parking_coordinates):
        points = np.array(park['points'])
        x1, y1 = points[:, 0].min(), points[:, 1].min()
        x2, y2 = points[:, 0].max(), points[:, 1].max()

        color = (0, 0, 255) if park['occupied'] else (0, 255, 0)  # Rojo para ocupada, verde para libre
        if park['occupied']:
            occupied_count += 1
        else:
            free_count += 1
            free_spaces.append(idx + 1)  # Guardar el número de plaza libre (1-indexado)

        # Dibujar rectángulo
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)  # Borde con grosor de 2

        # Agregar número de plaza en la esquina superior izquierda
        cv2.putText(frame, f'{idx + 1}', (x1 + 5, y1 + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Crear el fondo adicional (a la derecha)
    frame_height, frame_width = frame.shape[:2]
    new_width = frame_width + 300  # Añadir 300 píxeles para el fondo
    new_frame = np.ones((frame_height, new_width, 3), dtype=np.uint8) * np.array(background_color, dtype=np.uint8)

    # Copiar el video original al nuevo frame
    new_frame[:, :frame_width] = frame

    # Crear un área para mostrar las estadísticas en la parte superior de la columna
    y_offset = 30  # Espacio para las estadísticas arriba de las plazas libres
    start_x = frame_width + 20  # Comienza justo después del video original

    # Usar PIL para cargar la fuente
    pil_image = Image.fromarray(new_frame)
    draw = ImageDraw.Draw(pil_image)

    try:
        font = ImageFont.truetype(font_path, 20)  # Ajusta el tamaño de la fuente si es necesario
    except IOError:
        print("No se pudo cargar la fuente. Asegúrate de tener el archivo .ttf correctamente ubicado.")
        font = ImageFont.load_default()  # Cargar fuente por defecto si no se encuentra

    # Escribir estadísticas de plazas libres y ocupadas
    total_spaces = len(parking_coordinates)
    occupancy_rate = (occupied_count / total_spaces) * 100 if total_spaces > 0 else 0

    # Mostrar la tasa de ocupación
    draw.text((start_x, y_offset), f'Tasa de ocupación: {occupancy_rate:.1f}%', font=font, fill=(0, 0, 0))
    y_offset += 40  # Espacio para separar del listado

    # Mostrar plazas libres y ocupadas
    draw.text((start_x, y_offset), f'Plazas ocupadas: {occupied_count}', font=font, fill=(0, 0, 255))
    y_offset += 40  # Espacio entre las estadísticas
    draw.text((start_x, y_offset), f'Plazas libres: {free_count}', font=font, fill=(0, 255, 0))
    y_offset += 40  # Espacio para la tasa de ocupación

    # Listar las plazas libres
    for idx, space in enumerate(free_spaces):
        draw.text((start_x, y_offset), f'Plaza {space}', font=font, fill=(0, 0, 0))
        y_offset += 30  # Separar cada línea

    # Convertir la imagen de nuevo a un array de OpenCV
    new_frame = np.array(pil_image)

    return new_frame

def process_video(video, csv):
    """Procesa un video, analizando plaza por plaza y genera un nuevo video."""

    csv_path = csv

    create_json_from_csv(csv_path)
    
    frame_skip=50
    
    input_video_path = video  # Cambia este por tu video de entrada
    output_video_path = "runs/parking_management_processed.mp4"

    # Cargar coordenadas de las plazas desde el JSON
    with open('runs/rectangles.json', 'r') as file:
        parking_coordinates = json.load(file)  # Contiene las plazas como listas de puntos
    
    model = YOLO("models/visdrone_yolov11s.pt")  # Ruta a tu modelo entrenado

    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print(f"Error: No se pudo abrir el archivo de entrada {input_video_path}.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if frame_width == 0 or frame_height == 0:
        print("Error: Dimensiones del video de entrada no válidas.")
        return

    fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # Cambiar a un codec compatible
    out = cv2.VideoWriter(output_video_path, fourcc, 30.0, (frame_width + 300, frame_height))  # +300 para el fondo

    frame_count = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    parking_status = parking_coordinates

    try:
        while cap.isOpened() and frame_count < total_frames:
            ret, frame = cap.read()
            if not ret or frame is None:
                print(f"Advertencia: No se pudo leer el frame {frame_count}.")
                break

            if frame_count % frame_skip == 0:
                results = model(frame)
                detections = []
                for result in results:
                    for box in result.boxes.xyxy.cpu().numpy():
                        x1, y1, x2, y2 = box
                        detections.append({'bbox': [x1, y1, x2, y2]})
                parking_status = check_occupancy(detections, parking_coordinates)

            frame = draw_frame_with_parking_status(frame, parking_status)
            if frame is None or frame.size == 0:
                print(f"Error: El frame procesado no es válido.")
                break

            out.write(frame)
            print(f"Frame {frame_count} procesado y escrito al archivo de salida.")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            frame_count += 1

    except Exception as e:
        print(f"Error inesperado: {e}")

    finally:
        cap.release()
        out.release()
        cv2.destroyAllWindows()

def main():
    with gr.Blocks() as app:
        gr.Markdown("### Subir un CSV y un video para la detección")
        csv_input = gr.File(label="Sube el archivo CSV")
        video_input = gr.File(label="Sube el video")

        process_button = gr.Button("Procesar Video")
        process_button.click(
            process_video,
            inputs=[video_input, csv_input]
        )

    app.launch()

if __name__ == "__main__":
    main()