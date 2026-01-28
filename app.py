import streamlit as st
import numpy as np
import cv2
from PIL import Image
from sklearn.cluster import KMeans
import colorsys

# Professional Page Setup
st.set_page_config(page_title="StyleMatch Elite", layout="wide")

# High-Standard UI Injection
st.markdown("""
    <style>
    /* Professional Background & Typography */
    .stApp {
        background: radial-gradient(circle at top left, #ffffff, #f0f2f6);
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Elegant Title Gradient */
    .main-title {
        font-weight: 800;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: -1px;
        margin-bottom: 30px;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.07);
        margin-bottom: 20px;
    }

    /* Precision Swatches */
    .swatch {
        height: 120px;
        border-radius: 14px;
        border: 2px solid #ffffff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

def extract_accurate_dye(image):
    """High-precision extraction for professional fabric analysis."""
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    h, w, _ = img_cv.shape
    # Targeted center-crop to isolate fabric from studio noise
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
        # Luminance-aware scoring for pastels and deep silks
        score = (s_v * 0.65) + (l_v * 0.35) 
        if 0.12 < l_v < 0.96:
            if score > max_score:
                max_score = score
                best_rgb = color[::-1]
    return [int(c) for c in best_rgb]

# --- UI WORKSPACE ---
st.markdown("<h1 class='main-title'>STYLEMATCH ELITE PRO</h1>", unsafe_allow_html=True)

col_ctrl, col_main = st.columns([1, 2.8])

with col_ctrl:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("Configuration")
    garment_choice = st.selectbox("Catalog Category", ["Kurta (Ethnic)", "Saree (Ethnic)", "Shirt (Western)"])
    uploaded_file = st.file_uploader("Upload Catalog Image", type=["jpg", "png", "jpeg"])
    st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file:
    img_pil = Image.open(uploaded_file).convert("RGB")
    
    with st.spinner("Extracting Precise Fabric Hue..."):
        exact_rgb = extract_accurate_dye(img_pil)
        hex_val = "#%02x%02x%02x" % tuple(exact_rgb)
        rgb_css = f"rgb({exact_rgb[0]}, {exact_rgb[1]}, {exact_rgb[2]})"
        
        # Professional Pairing Labels
        p1, p2 = ("Leggings", "Dupatta") if "Kurta" in garment_choice else ("Blouse", "Border Detail")
        
        # Color Theory Logic
        r_f, g_f, b_f = [x / 255.0 for x in exact_rgb]
        h_f, l_f, s_f = colorsys.rgb_to_hls(r_f, g_f, b_f)
        matches = {
            "Professional Contrast": colorsys.hls_to_rgb((h_f + 0.5) % 1.0, l_f, s_f),
            "Tonal Harmony": colorsys.hls_to_rgb((h_f + 0.08) % 1.0, l_f, s_f),
            "Designer Set": colorsys.hls_to_rgb((h_f + 0.33) % 1.0, l_f, s_f)
        }

    with col_main:
        # Result Header Card
        st.markdown(f"""
            <div class='glass-card'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <h3 style='margin:0;'>Extracted Fabric Pigment</h3>
                    <code style='font-size:1.5em; color:#1e3c72;'>{hex_val.upper()}</code>
                </div>
                <div class='swatch' style='background-color:{rgb_css}; height: 160px; margin-top:15px;'></div>
            </div>
        """, unsafe_allow_html=True)
        
        # Original Image Display
        st.image(img_pil, use_container_width=True)

    st.divider()
    st.markdown(f"<h2 style='text-align: center;'>Elite Pairings for {p1} & {p2}</h2>", unsafe_allow_html=True)
    
    
    
    m_cols = st.columns(3)
    idx = 0
    for label, m_rgb in matches.items():
        m_int = [int(x*255) for x in m_rgb]
        m_hex = "#%02x%02x%02x" % tuple(m_int)
        m_css = f"rgb({m_int[0]}, {m_int[1]}, {m_int[2]})"
        with m_cols[idx]:
            st.markdown(f"""
                <div class='glass-card'>
                    <p style='font-weight: 700; color: #576574;'>{label}</p>
                    <div class='swatch' style='background-color:{m_css};'></div>
                    <code style='background:transparent; font-size:1.1em;'>{m_hex.upper()}</code>
                </div>
            """, unsafe_allow_html=True)
        idx += 1
else:
    with col_main:
        st.markdown("""
            <div class='glass-card' style='text-align: center; padding: 80px;'>
                <h3 style='color: #8395a7;'>System Ready</h3>
                <p>Please upload a high-resolution catalog photo to begin analysis.</p>
            </div>
        """, unsafe_allow_html=True)

# --- PROFESSIONAL CLICKABLE FOOTER ---
st.markdown("---")
footer_html = """
<div style="text-align: center; padding-bottom: 30px;">
    <p style="font-size: 0.9em; color: #8395a7;">
        Developed by <a href="https://gravatar.com/katragaddasurendra" target="_blank" style="text-decoration: none; color: #1e3c72; font-weight: 800;">Katragadda Surendra</a>
    </p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
