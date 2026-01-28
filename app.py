import streamlit as st
import numpy as np
import cv2
from PIL import Image
from sklearn.cluster import KMeans
import colorsys

# Professional Page Setup
st.set_page_config(page_title="StyleMatch Global", layout="wide")

# Professional Boutique CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);
    }
    h1 {
        font-weight: 800;
        background: -webkit-linear-gradient(#FF8C00, #FF0080);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    .designer-card {
        background: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        text-align: center;
    }
    .swatch {
        height: 100px;
        border-radius: 15px;
        margin-bottom: 10px;
        border: 3px solid #fff;
    }
    </style>
    """, unsafe_allow_html=True)

def extract_accurate_dye(image):
    """High-precision extraction for both deep and light colors."""
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    h, w, _ = img_cv.shape
    # Tight 15% center focus to ignore beige studio walls
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

# UI Header
st.title("STYLEMATCH INTERNATIONAL")

col_img, col_res = st.columns([1.5, 1])

with col_res:
    garment_choice = st.selectbox("Catalog Category", ["Kurta (Ethnic)", "Saree (Ethnic)", "Shirt (Western)"])
    uploaded_file = st.file_uploader("Upload Product Shot", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img_pil = Image.open(uploaded_file).convert("RGB")
    
    with st.spinner("Analyzing Professional Pairings..."):
        exact_rgb = extract_accurate_dye(img_pil)
        hex_val = "#%02x%02x%02x" % tuple(exact_rgb)
        rgb_css = f"rgb({exact_rgb[0]}, {exact_rgb[1]}, {exact_rgb[2]})"
        
        # Professional Naming Logic
        p1, p2 = ("Leggings", "Dupatta") if "Kurta" in garment_choice else ("Blouse", "Border Detail")
        
        # Global Harmony Logic
        r_f, g_f, b_f = [x / 255.0 for x in exact_rgb]
        h_f, l_f, s_f = colorsys.rgb_to_hls(r_f, g_f, b_f)
        matches = {
            "Contrast Match": colorsys.hls_to_rgb((h_f + 0.5) % 1.0, l_f, s_f),
            "Tonal Harmony": colorsys.hls_to_rgb((h_f + 0.08) % 1.0, l_f, s_f),
            "Designer Set": colorsys.hls_to_rgb((h_f + 0.33) % 1.0, l_f, s_f)
        }

    with col_img:
        st.image(img_pil, use_container_width=True)

    with col_res:
        st.markdown(f"""
            <div class="designer-card">
                <p style="font-weight: bold;">Fabric Hue</p>
                <div class="swatch" style="background-color:{rgb_css}; height: 120px;"></div>
                <code>{hex_val.upper()}</code>
            </div>
        """, unsafe_allow_html=True)
        st.color_picker("Fine-tune", hex_val, label_visibility="collapsed")

    st.divider()
    st.markdown(f"<h3 style='text-align: center;'>Pairings for {p1} & {p2}</h3>", unsafe_allow_html=True)
    
    
    
    m_cols = st.columns(3)
    idx = 0
    for label, m_rgb in matches.items():
        m_int = [int(x*255) for x in m_rgb]
        m_hex = "#%02x%02x%02x" % tuple(m_int)
        m_css = f"rgb({m_int[0]}, {m_int[1]}, {m_int[2]})"
        with m_cols[idx]:
            st.markdown(f"""
                <div class="designer-card">
                    <p style="font-size: 0.9em;">{label}</p>
                    <div class="swatch" style="background-color:{m_css};"></div>
                    <code>{m_hex.upper()}</code>
                </div>
            """, unsafe_allow_html=True)
        idx += 1

# --- FINAL PROFESSIONAL FOOTER ---
st.markdown("---")
footer_html = """
<div style="text-align: center; padding-bottom: 20px;">
    <p style="font-size: 0.9em; color: #636e72;">
        Developed by <a href="https://gravatar.com/katragaddasurendra" target="_blank" style="text-decoration: none; color: #FF0080; font-weight: bold;">Katragadda Surendra</a>
    </p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
