import streamlit as st
import numpy as np
import cv2
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import colorsys

# Professional Page Setup
st.set_page_config(page_title="StyleMatch AI | Professional Precision", layout="centered")

def get_matches(rgb_list, garment_type):
    r, g, b = [x / 255.0 for x in rgb_list]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    # Mathematical matching logic based on the HSL color wheel
    match_map = {
        "Perfect Contrast": colorsys.hls_to_rgb((h + 0.5) % 1.0, l, s),
        "Tonal Harmony": colorsys.hls_to_rgb((h + 0.05) % 1.0, l, s),
        "Modern Designer": colorsys.hls_to_rgb((h + 0.33) % 1.0, l, s)
    }
    
    # Naming Logic for your specific categories
    if "Kurta" in garment_type:
        p1, p2 = "Leggings", "Chunny"
    elif "Saree" in garment_type:
        p1, p2 = "Blouse", "Accessories"
    else:
        p1, p2 = "Trouser", "Accessories"
        
    return match_map, p1, p2

# UI Header
st.title("👗 StyleMatch AI Pro")
st.markdown("### Precision Color Extraction for Cataloging")

garment_choice = st.radio("Target Garment:", ["Kurta (Ethnic)", "Saree (Ethnic)", "Shirt (Western)"], horizontal=True)

uploaded_file = st.file_uploader("Upload Product Photo", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Load Image using PIL to ensure compatibility with st_canvas
    bg_image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(bg_image)
    
    st.info("🎯 **Click exactly on the fabric** (the navy blue or red areas) to extract the dye color.")
    
    # Calculate responsive canvas size
    canvas_width = 700
    canvas_height = img_array.shape[0] * (canvas_width / img_array.shape[1])
    
    # Interactive Pointer Canvas
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=1,
        background_image=bg_image,
        update_streamlit=True,
        height=canvas_height,
        width=canvas_width,
        drawing_mode="point",
        point_display_radius=6,
        key="fabric_pointer",
    )

    # Color Extraction Logic
    exact_rgb = [0, 0, 0]
    if canvas_result.json_data is not None and len(canvas_result.json_data["objects"]) > 0:
        # Get the last point clicked
        last_point = canvas_result.json_data["objects"][-1]
        x_scaled = int(last_point["left"])
        y_scaled = int(last_point["top"])
        
        # Map back to original high-res pixels
        orig_x = int(x_scaled * (img_array.shape[1] / canvas_width))
        orig_y = int(y_scaled * (img_array.shape[0] / canvas_height))
        
        # Extract color and average a 3x3 area for better accuracy
        sample = img_array[max(0, orig_y-1):min(img_array.shape[0], orig_y+2), 
                           max(0, orig_x-1):min(img_array.shape[1], orig_x+2)]
        exact_rgb = np.mean(sample, axis=(0,1)).astype(int)
    
        rgb_css = f"rgb({exact_rgb[0]}, {exact_rgb[1]}, {exact_rgb[2]})"
        matches, name_1, name_2 = get_matches(exact_rgb, garment_choice)
        
        # Display Results
        st.divider()
        col_res1, col_res2 = st.columns([1, 2])
        with col_res1:
            st.write("**Extracted Fabric Color**")
            st.markdown(f'<div style="background-color:{rgb_css};width:100%;height:120px;border-radius:15px;border:5px solid white;box-shadow: 0 4px 15px rgba(0,0,0,0.3);"></div>', unsafe_allow_html=True)
            st.code(f"HEX: #%02x%02x%02x" % tuple(exact_rgb))

        with col_res2:
            st.subheader(f"Professional Pairings for {name_1} & {name_2}")
            m_cols = st.columns(3)
            for i, (label, m_rgb) in enumerate(matches.items()):
                m_int = [int(x*255) for x in m_rgb]
                m_css = f"rgb({m_int[0]}, {m_int[1]}, {m_int[2]})"
                with m_cols[i]:
                    st.markdown(f'<div style="background-color:{m_css};width:100%;height:80px;border-radius:10px;"></div>', unsafe_allow_html=True)
                    st.caption(f"**{label}**")

# Professional Footer with Clickable Link
st.markdown("---")
footer_html = """
<div style="text-align: center;">
    <p>Developed by <a href="https://gravatar.com/katragaddasurendra" target="_blank" style="text-decoration: none; color: #FF4B4B; font-weight: bold;">Katragadda Surendra</a></p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
