import streamlit as st
from PIL import Image, ImageOps
import numpy as np

st.set_page_config(page_title="Design Pattern Generator", layout="wide")
st.title("🎨 Design Pattern Generator")

# --------------- Repeat Options ---------------
repeat_options = [
    "Straight", "Half Drop", "Brick", "Mirror",
    "Ogee", "Toss", "Hex", "Diamond", "Radial"
]

# --------------- User Inputs on Main Page ---------------
uploaded_file = st.file_uploader("Upload your motif (PNG/JPG)", type=["png","jpg","jpeg"])

repeat_type = st.selectbox("Select repeat type", repeat_options)
rows = st.slider("Rows", 1, 20, 5)
cols = st.slider("Columns", 1, 20, 5)

# --------------- Pattern Generation ---------------
if uploaded_file:
    img = Image.open(uploaded_file)
    img = img.convert("RGBA")  # ensure alpha channel

    # --- Automatically resize if too large ---
    max_size = 1000  # max width or height
    img.thumbnail((max_size, max_size), Image.ANTIALIAS)

    w, h = img.size
    canvas = Image.new("RGBA", (w*cols, h*rows), (255,255,255,0))

    for i in range(rows):
        for j in range(cols):
            x = j*w
            y = i*h
            tile = img.copy()

            # Apply repeat types
            if repeat_type == "Mirror":
                if (i+j)%2 == 1:
                    tile = ImageOps.mirror(tile)
            elif repeat_type == "Half Drop":
                y_offset = int(h/2) if j%2 == 1 else 0
                y += y_offset
            elif repeat_type == "Brick":
                x_offset = int(w/2) if i%2 == 1 else 0
                x += x_offset
            elif repeat_type == "Ogee":
                x_offset = int(w/2) if i%2 == 1 else 0
                y_offset = int(h/2) if j%2 == 1 else 0
                x += x_offset
                y += y_offset
            elif repeat_type == "Toss":
                x += np.random.randint(-w//2, w//2)
                y += np.random.randint(-h//2, h//2)
            elif repeat_type == "Hex":
                x_offset = int(w/2) if i%2 == 1 else 0
                y += int(h*0.75)*i
                x += x_offset
            elif repeat_type == "Diamond":
                x_offset = int(w/2) if (i+j)%2==1 else 0
                y_offset = int(h/2) if (i+j)%2==1 else 0
                x += x_offset
                y += y_offset
            elif repeat_type == "Radial":
                x = int(cols*w/2 - w/2 + (j-cols/2)*w)
                y = int(rows*h/2 - h/2 + (i-rows/2)*h)

            canvas.paste(tile, (int(x), int(y)), tile)

    st.image(canvas, use_column_width=True)

    # Download Button
    if st.button("Download PNG"):
        canvas.save("pattern.png")
        st.success("Pattern saved as pattern.png! Check your downloads.")
