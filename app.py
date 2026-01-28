import streamlit as st
import numpy as np
import cv2
from PIL import Image
from sklearn.cluster import KMeans
import colorsys

# Professional Page Setup
st.set_page_config(page_title="StyleMatch AI Pro", layout="centered")

def extract_accurate_dye(image):
    """High-precision extraction for both deep and light colors."""
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    h, w, _ = img_cv.shape
    
    # 15% Precision Center-Crop: Ignores beige backgrounds and floor noise
    cy, cx = h // 2, w // 2
    rh, rw = int(h * 0.075), int(w * 0.075)
    crop = img_cv[cy-rh:cy+rh, cx-rw:cx+rw]
    
    # K-Means clustering to isolate the primary fabric pigment
    pixels = cv2.resize(crop, (60, 60)).reshape((-1, 3))
    clt = KMeans(n_clusters=4, n_init=5)
    clt.fit(pixels)
    
    best_rgb = [128, 128, 128]
    max_score = -1
    for color in clt.cluster_centers_:
        r, g, b = color[::-1] / 255.0
        h_v, l_v, s_v = colorsys.rgb_to_hls(r, g, b)
        
        # Scoring balanced to capture light pastels and deep silks
        score = (s_v * 0.65) + (l_v * 0.35) 
        
        # Filter: Ignore background whites/beiges (>0.97) and deep shadows (<0.1)
        if 0.1 < l_v < 0.97:
            if score > max_score:
                max_score = score
                best_rgb = color[::-1]
                
    return [int(c) for c in best_rgb]

# --- UI Layout ---
st.title("👗 StyleMatch AI Pro")
st.markdown("### 🎯 Accuracy-First Color Extraction for Your Catalog")

# Logic Selection for Your Brands
garment_choice = st.radio(
    "Select Category:", 
    ["Kurta (Ethnic)", "Saree (Ethnic)", "Shirt (Western)"], 
    horizontal=True
)
uploaded_file = st.file_uploader("Upload Catalog Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img_pil = Image.open(uploaded_file).convert("RGB")
    
    with st.spinner("Extracting verified fabric pigment..."):
        exact_rgb = extract_accurate_dye(img_pil)
        hex_val = "#%02x%02x%02x" % tuple(exact_rgb)
        rgb_css = f"rgb({exact_rgb[0]}, {exact_rgb[1]}, {exact_rgb[2]})"
        
        # Labels customized for Subham Grand products
        if "Kurta" in garment_choice:
            p1, p2 = "Leggings", "Dupatta"
        elif "Saree" in garment_choice:
            p1, p2 = "Blouse", "Contrast Border"
        else:
            p1, p2 = "Trouser", "Jeans"
        
        # Color Theory Harmonization
        r_f, g_f, b_f = [x / 255.0 for x in exact_rgb]
        h_f, l_f, s_f = colorsys.rgb_to_hls(r_f, g_f, b_f)
        matches = {
            "Professional Contrast": colorsys.hls_to_rgb((h_f + 0.5) % 1.0, l_f, s_f),
            "Tonal Harmony": colorsys.hls_to_rgb((h_f + 0.07) % 1.0, l_f, s_f),
            "Designer Choice": colorsys.hls_to_rgb((h_f + 0.33) % 1.0, l_f, s_f)
        }
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.image(img_pil, use_container_width=True)
    with col2:
        st.write("**Verified Fabric Color**")
        st.markdown(f'<div style="background-color:{rgb_css};width:100%;height:140px;border-radius:15px;border:5px solid white;box-shadow: 0 4px 15px rgba(0,0,0,0.3);"></div>', unsafe_allow_html=True)
        st.code(hex_val.upper())
        st.divider()
        st.color_picker("Fine-tune if needed:", hex_val)

    st.divider()
    st.subheader(f"Matching Results for {p1} & {p2}")
    
    # Flat loop to ensure no IndentationErrors
    m_cols = st.columns(3)
    idx = 0
    for label, m_rgb in matches.items():
        m_int = [int(x*255) for x in m_rgb]
        m_hex = "#%02x%02x%02x" % tuple(m_int)
        m_css = f"rgb({m_int[0]}, {m_int[1]}, {m_int[2]})"
        with m_cols[idx]:
            st.markdown(f"**{label}**")
            st.markdown(f'<div style="background-color:{m_css};width:100%;height:100px;border-radius:12px;"></div>', unsafe_allow_html=True)
            st.code(m_hex.upper())
            st.caption(f"Best for {p1}/{p2}")
        idx += 1

# Professional Footer
st.markdown("---")
st.markdown(f'<div style="text-align: center;"><p>Developed by <a href="https://gravatar.com/katragaddasurendra" target="_blank" style="text-decoration: none; color: #FF4B4B; font-weight: bold;">Katragadda Surendra</a></p></div>', unsafe_allow_html=True)
