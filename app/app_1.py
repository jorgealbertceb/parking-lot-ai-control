## INTERFAZ QUE PERMITE SELECCIONAR RECTÁNGULOS

# python app/app_1.py --server.port 7860

import gradio as gr
from gradio_image_prompter import ImagePrompter

demo = gr.Interface(
    lambda prompts: (prompts["image"], prompts["points"]),
    ImagePrompter(show_label=False),
    [gr.Image(show_label=False), gr.Dataframe(label="Points")],
)
demo.launch()