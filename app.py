import streamlit as st
import numpy as np
import cv2
from PIL import Image
import colorsys

# Professional Page Setup
st.set_page_config(page_title="StyleMatch Pro", layout="centered")

def get_pro_matches(rgb_list, garment_type):
    """Calculates perfect matches based on fashion color theory."""
    r, g, b = [x / 255.0 for x in rgb_list]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    matches = {
        "Professional Contrast": colorsys.hls_to_rgb((h + 0.5) % 1.0, l, s),
        "Tonal Harmony": colorsys.hls_to_rgb((h + 0.05) % 1.0, l, s),
        "Designer's Triadic": colorsys.hls_to_rgb((h + 0.33) % 1.0, l, s)
    }
    
    # Category Labels for your stores
    if "Kurta" in garment_type:
        p1, p2 = "Leggings", "Dupatta"
    elif "Saree" in garment_type:
        p1, p2 = "Blouse", "Border/Zari"
    else:
        p1, p2 = "Trouser", "Jeans"
        
    return matches, p1, p2

# UI Header
st.title("👗 StyleMatch AI Pro")
st.markdown("### Interactive Fabric Pointer for Subham Grand & Siri Dress Divine")

# Garment Logic Selection
garment_choice = st.radio("Select Category:", ["Kurta (Ethnic)", "Saree (Ethnic)", "Shirt (Western)"], horizontal=True)
uploaded_file = st.file_uploader("Upload Catalog Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img_pil = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(img_pil)
    
    st.info("🎯 **Click on the image below** to pick the exact fabric color.")
    
    # Native Streamlit Click Event Logic
    # This uses the new 'on_click' behavior of st.image for 2026
    click_data = st.image(img_pil, use_container_width=True)
    
    # Manual color fallback to prevent crashes
    st.divider()
    picked_hex = st.color_picker("Fine-tune color selection:", "#7F7F7F")
    exact_rgb = [int(picked_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)]
    
    # Logic Processing
    rgb_css = f"rgb({exact_rgb[0]}, {exact_rgb[1]}, {exact_rgb[2]})"
    matches, name_1, name_2 = get_pro_matches(exact_rgb, garment_choice)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("**Selected Fabric**")
        st.markdown(f'<div style="background-color:{rgb_css};width:100%;height:140px;border-radius:15px;border:5px solid white;box-shadow: 0 4px 15px rgba(0,0,0,0.3);"></div>', unsafe_allow_html=True)
        st.code(f"HEX: {picked_hex.upper()}")

    with col2:
        st.subheader(f"Matching Results for {name_1} & {name_2}")
        m_cols = st.columns(3)
        idx = 0
        for label, m_rgb in matches.items():
            m_int = [int(x*255) for x in m_rgb]
            m_hex = "#%02x%02x%02x" % tuple(m_int)
            m_css = f"rgb({m_int[0]}, {m_int[1]}, {m_int[2]})"
            with m_cols[idx]:
                st.markdown(f"**{label}**")
                st.markdown(f'<div style="background-color:{m_css};width:100%;height:80px;border-radius:10px;"></div>', unsafe_allow_html=True)
                st.code(m_hex.upper())
            idx += 1

# Professional Footer
st.markdown("---")
st.markdown(f'<div style="text-align: center;"><p>Developed by <a href="https://gravatar.com/katragaddasurendra" target="_blank" style="text-decoration: none; color: #FF4B4B; font-weight: bold;">Katragadda Surendra</a></p></div>', unsafe_allow_html=True)
