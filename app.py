import streamlit as st
import numpy as np
import cv2
from streamlit_drawable_canvas import st_canvas
from sklearn.cluster import KMeans
import colorsys

# Professional Page Setup
st.set_page_config(page_title="StyleMatch AI | Precision Pointer", layout="centered")

def get_matches(rgb_list, garment_type):
    r, g, b = [x / 255.0 for x in rgb_list]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    # Professional Pairing Logic based on Color Theory
    match_map = {
        "Perfect Contrast": colorsys.hls_to_rgb((h + 0.5) % 1.0, l, s),
        "Tonal Harmony": colorsys.hls_to_rgb((h + 0.05) % 1.0, l, s),
        "Modern Designer": colorsys.hls_to_rgb((h + 0.33) % 1.0, l, s)
    }
    
    # Contextual Naming for Your Specific Brand Needs
    if "Kurta" in garment_type:
        p1, p2 = "Leggings", "Chunny"
    elif "Saree" in garment_type:
        p1, p2 = "Blouse", "Accessories"
    else:
        p1, p2 = "Trouser", "Accessories"
        
    return match_map, p1, p2

# UI Header
st.title("👗 StyleMatch Pro: Pointer Mode")
st.markdown("### Interactive Fabric Selection for Professional Cataloging")

garment_choice = st.radio("Target Garment:", ["Kurta (Ethnic)", "Saree (Ethnic)", "Shirt (Western)"], horizontal=True)

uploaded_file = st.file_uploader("Upload Product Photo", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Process Image for Display
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.cvtColor(cv2.imdecode(file_bytes, 1), cv2.COLOR_BGR2RGB)
    
    st.info("🎯 Click anywhere on the fabric below to pick the exact color.")
    
    # Interactive Pointer/Canvas
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=1,
        background_image=Image.fromarray(img) if 'Image' in globals() else None,
        update_streamlit=True,
        height=img.shape[0] * (700 / img.shape[1]),
        width=700,
        drawing_mode="point",
        point_display_radius=5,
        key="canvas",
    )

    # Extract Color from Click Coordinates
    exact_rgb = [0, 0, 0]
    if canvas_result.json_data is not None and len(canvas_result.json_data["objects"]) > 0:
        last_point = canvas_result.json_data["objects"][-1]
        x = int(last_point["left"])
        y = int(last_point["top"])
        
        # Map canvas coordinates back to original image
        scale_x = img.shape[1] / 700
        scale_y = img.shape[0] / (img.shape[0] * (700 / img.shape[1]))
        exact_rgb = img[int(y * scale_y), int(x * scale_x)]
    
    rgb_css = f"rgb({exact_rgb[0]}, {exact_rgb[1]}, {exact_rgb[2]})"
    matches, name_1, name_2 = get_matches(exact_rgb, garment_choice)
    
    # Results Display
    st.divider()
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("**Pointed Color**")
        st.markdown(f'<div style="background-color:{rgb_css};width:100%;height:100px;border-radius:15px;border:5px solid white;box-shadow: 0 4px 15px rgba(0,0,0,0.3);"></div>', unsafe_allow_html=True)
        st.code(f"HEX: #%02x%02x%02x" % tuple(exact_rgb))

    with col2:
        st.subheader(f"Professional Pairings for {name_1} & {name_2}")
        cols = st.columns(3)
        for i, (label, m_rgb) in enumerate(matches.items()):
            m_int = [int(x*255) for x in m_rgb]
            m_css = f"rgb({m_int[0]}, {m_int[1]}, {m_int[2]})"
            with cols[i]:
                st.markdown(f'<div style="background-color:{m_css};width:100%;height:80px;border-radius:10px;"></div>', unsafe_allow_html=True)
                st.caption(f"**{label}**")

# Professional Footer
st.markdown("---")
footer_html = """
<div style="text-align: center;">
    <p>Developed by <a href="https://gravatar.com/katragaddasurendra" target="_blank" style="text-decoration: none; color: #FF4B4B; font-weight: bold;">Katragadda Surendra</a></p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
