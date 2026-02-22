import torch
from diffusers import StableDiffusionPipeline
import uuid
import os

device = "cpu"

pipe = StableDiffusionPipeline.from_pretrained(
    "stabilityai/sd-turbo",
    torch_dtype=torch.float32
)

pipe = pipe.to(device)
pipe.enable_attention_slicing()

def generate_image(prompt):
    with torch.no_grad():
        image = pipe(
            prompt,
            num_inference_steps=4,
            guidance_scale=0.0
        ).images[0]

    filename = f"{uuid.uuid4().hex}.png"
    path = os.path.join("static/outputs", filename)
    image.save(path)

    return path