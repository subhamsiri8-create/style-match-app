import streamlit as st
import numpy as np
import cv2
from PIL import Image
from sklearn.cluster import KMeans
import colorsys

# Professional Page Setup
st.set_page_config(page_title="StyleMatch Elite | Professional", layout="wide")

# Custom CSS for a Colorful Professional Look
st.markdown("""
    <style>
    /* Main Background and Font */
    .stApp {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
    }
    
    /* Title Styling */
    h1 {
        color: #2c3e50;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        text-align: center;
        padding-bottom: 20px;
        border-bottom: 2px solid #e67e22;
    }
    
    /* Card Styling */
    .stImage, .stMarkdown, .stColorPicker {
        border-radius: 15px;
        transition: transform 0.3s ease;
    }
    
    /* Result Swatches */
    .color-swatch {
        height: 120px;
        border-radius: 12px;
        border: 4px solid white;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    
    /* Professional Labels */
    .label-box {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 8px;
        border-left: 5px solid #e67e22;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

def extract_accurate_dye(image):
    """High-precision extraction for both deep and light colors."""
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    h, w, _ = img_cv.shape
    cy, cx = h // 2, w // 2
    rh, rw = int(h * 0.075), int(w * 0.075)
    crop = img_cv[cy-rh:cy+rh, cx-rw:cx+rw]
    
    pixels = cv2.resize(crop, (60, 60)).reshape((-1, 3))
    clt = KMeans(n_clusters=4, n_init=5)
    clt.fit(pixels)
    
    best_rgb = [128, 128, 128]
    max_score = -1
    for color in clt.cluster_centers_:
        r, g, b = color[::-1] / 255.0
        h_v, l_v, s_v = colorsys.rgb_to_hls(r, g, b)
        score = (s_v * 0.65) + (l_v * 0.35) 
        if 0.1 < l_v < 0.97:
            if score > max_score:
                max_score = score
                best_rgb = color[::-1]
    return [int(c) for c in best_rgb]

# --- UI Header ---
st.title("👗 STYLEMATCH ELITE PRO")
st.markdown("<p style='text-align: center; color: #7f8c8d;'>Luxury Fabric Analysis for Subham Grand & Siri Dress Divine</p>", unsafe_allow_html=True)

# Layout Columns
left_panel, right_panel = st.columns([1, 1])

with left_panel:
    st.markdown("<div class='label-box'><b>1. Select Catalog Category</b></div>", unsafe_allow_html=True)
    garment_choice = st.radio("", ["Kurta (Ethnic)", "Saree (Ethnic)", "Shirt (Western)"], horizontal=True, label_visibility="collapsed")
    
    st.markdown("<div class='label-box'><b>2. Upload Professional Photo</b></div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

if uploaded_file:
    img_pil = Image.open(uploaded_file).convert("RGB")
    
    with st.spinner("✨ Analyzing Fabric Pigments..."):
        exact_rgb = extract_accurate_dye(img_pil)
        hex_val = "#%02x%02x%02x" % tuple(exact_rgb)
        rgb_css = f"rgb({exact_rgb[0]}, {exact_rgb[1]}, {exact_rgb[2]})"
        
        # Labels for boutique categories
        if "Kurta" in garment_choice:
            p1, p2 = "Designer Leggings", "Matching Dupatta"
        elif "Saree" in garment_choice:
            p1, p2 = "Boutique Blouse", "Contrast Border/Zari"
        else:
            p1, p2 = "Formal Trouser", "Designer Jeans"
        
        # Color Harmony Logic
        r_f, g_f, b_f = [x / 255.0 for x in exact_rgb]
        h_f, l_f, s_f = colorsys.rgb_to_hls(r_f, g_f, b_f)
        matches = {
            "Professional Contrast": colorsys.hls_to_rgb((h_f + 0.5) % 1.0, l_f, s_f),
            "Ethereal Tonal": colorsys.hls_to_rgb((h_f + 0.07) % 1.0, l_f, s_f),
            "Designer's Choice": colorsys.hls_to_rgb((h_f + 0.33) % 1.0, l_f, s_f)
        }

    with left_panel:
        st.image(img_pil, use_container_width=True)

    with right_panel:
        st.markdown("<div class='label-box'><b>🎯 Extracted Fabric Hue</b></div>", unsafe_allow_html=True)
        st.markdown(f'<div class="color-swatch" style="background-color:{rgb_css};"></div>', unsafe_allow_html=True)
        st.code(hex_val.upper())
        
        st.divider()
        st.markdown("<b>Fine-tune selection:</b>", unsafe_allow_html=True)
        picked_hex = st.color_picker("", hex_val, label_visibility="collapsed")

    st.divider()
    st.markdown(f"<h3 style='text-align: center;'>Expert Pairings for {p1} & {p2}</h3>", unsafe_allow_html=True)
    
    m_cols = st.columns(3)
    idx = 0
    for label, m_rgb in matches.items():
        m_int = [int(x*255) for x in m_rgb]
        m_hex = "#%02x%02x%02x" % tuple(m_int)
        m_css = f"rgb({m_int[0]}, {m_int[1]}, {m_int[2]})"
        with m_cols[idx]:
            st.markdown(f"<div style='text-align: center;'><b>{label}</b></div>", unsafe_allow_html=True)
            st.markdown(f'<div class="color-swatch" style="background-color:{m_css}; height: 100px;"></div>', unsafe_allow_html=True)
            st.code(m_hex.upper())
            st.caption(f"Perfect match for {p1}/{p2}")
        idx += 1

# Professional Footer
st.markdown("---")
footer_html = """
<div style="text-align: center; padding: 20px;">
    <p style="color: #95a5a6;">Crafted for Elite Retailers</p>
    <p>Developed by <a href="https://gravatar.com/katragaddasurendra" target="_blank" style="text-decoration: none; color: #e67e22; font-weight: bold;">Katragadda Surendra</a></p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
