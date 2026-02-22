import imageio
from image_ai import generate_image
import uuid
import os

def generate_video(prompt):
    frames = []

    for i in range(3):
        img_path = generate_image(prompt + f", scene {i}")
        frames.append(imageio.imread(img_path))

    filename = f"{uuid.uuid4().hex}.mp4"
    video_path = os.path.join("static/outputs", filename)

    imageio.mimsave(video_path, frames, fps=1)

    return video_path