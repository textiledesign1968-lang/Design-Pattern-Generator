import streamlit as st
from PIL import Image, ImageOps
import numpy as np

st.set_page_config(page_title="Design Pattern Generator", layout="wide")
st.title("🎨 Design Pattern Generator")

# Upload motif
uploaded_file = st.file_uploader("Upload a motif (PNG or JPG)", type=["png", "jpg", "jpeg"])
if uploaded_file:
    motif = Image.open(uploaded_file).convert("RGBA")
    
    st.sidebar.header("Pattern Settings")
    repeat_type = st.sidebar.selectbox(
        "Select repeat type",
        [
            "Straight",
            "Half Drop",
            "Brick",
            "Mirror",
            "Ogee",
            "Toss",
            "Hex",
            "Diamond",
            "Radial"
        ]
    )
    rows = st.sidebar.slider("Rows", 1, 20, 5)
    cols = st.sidebar.slider("Columns", 1, 20, 5)
    rotation = st.sidebar.slider("Rotation (for toss/hex/diamond)", 0, 360, 0)
    
    # Create blank canvas
    width, height = motif.size
    canvas_width = cols * width
    canvas_height = rows * height
    canvas = Image.new("RGBA", (canvas_width, canvas_height), (255, 255, 255, 0))
    
    for row in range(rows):
        for col in range(cols):
            x = col * width
            y = row * height
            temp = motif.copy()
            
            # Apply repeat pattern offsets
            if repeat_type == "Half Drop" and row % 2 == 1:
                x += width // 2
            elif repeat_type == "Brick" and row % 2 == 1:
                x += width // 2
            elif repeat_type == "Mirror":
                if (row + col) % 2 == 1:
                    temp = ImageOps.mirror(temp)
            elif repeat_type == "Ogee":
                if row % 2 == 1:
                    y += height // 2
            elif repeat_type == "Toss":
                temp = temp.rotate(np.random.randint(0, 360))
            elif repeat_type == "Hex":
                if row % 2 == 1:
                    x += width // 2
            elif repeat_type == "Diamond":
                if (row + col) % 2 == 0:
                    temp = temp.rotate(45)
            elif repeat_type == "Radial":
                # For simplicity, place motifs rotated around center
                cx = canvas_width // 2
                cy = canvas_height // 2
                temp = temp.rotate(rotation)
                x = cx + int(np.cos(np.radians(rotation * col)) * 100) - width//2
                y = cy + int(np.sin(np.radians(rotation * row)) * 100) - height//2

            canvas.paste(temp, (x, y), temp)
    
    st.image(canvas, use_column_width=True)
    
    # Download button
    buf = st.sidebar.button("Download PNG")
    if buf:
        canvas.save("pattern.png")
        st.success("Pattern saved as pattern.png! Check your local downloads.")
