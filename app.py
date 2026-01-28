import streamlit as st
import numpy as np
import cv2
from PIL import Image
from sklearn.cluster import KMeans
import colorsys

# Professional Page Setup for international display
st.set_page_config(page_title="StyleMatch Global", layout="wide")

# International Style CSS: Vibrant Accents & Sleek Layouts
st.markdown("""
    <style>
    /* Gradient Background for International Look */
    .stApp {
        background: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);
        color: #2d3436;
    }
    
    /* Header with Gold/Sunset Accent */
    h1 {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 800;
        background: -webkit-linear-gradient(#FF8C00, #FF0080);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: -1px;
    }

    /* Designer Glassmorphism Cards */
    .designer-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }

    /* Result Swatch Styling */
    .swatch {
        height: 120px;
        border-radius: 20px;
        margin-bottom: 15px;
        border: 4px solid #fff;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def extract_precise_dye(image):
    """High-accuracy extraction to isolate fabric from studio sets."""
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    h, w, _ = img_cv.shape
    cy, cx = h // 2, w // 2
    # Tight 15% center focus to ignore beige store walls
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
        # Optimized for international color palettes (pastels to deep hues)
        score = (s_v * 0.65) + (l_v * 0.35) 
        if 0.1 < l_v < 0.97:
            if score > max_score:
                max_score = score
                best_rgb = color[::-1]
    return [int(c) for c in best_rgb]

# --- MAIN UI ---
st.title("STYLEMATCH INTERNATIONAL")
st.markdown("<p style='text-align: center; font-size: 1.1em; color: #636e72;'>Premium Styling Engine for Subham Grand & Siri Dress Divine</p>", unsafe_allow_html=True)

col_ctrl, col_main = st.columns([1, 2.5])

with col_ctrl:
    st.markdown("### 01. Configure")
    garment_choice = st.selectbox("Category", ["Kurta (Ethnic)", "Saree (Ethnic)", "Shirt (Western)"])
    uploaded_file = st.file_uploader("Upload Product Shot", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        st.markdown("### 02. Fine-tune")
        st.info("Adjust results for perfect lighting sync.")

if uploaded_file:
    img_pil = Image.open(uploaded_file).convert("RGB")
    
    with st.spinner("Synchronizing with Global Color Standards..."):
        exact_rgb = extract_precise_dye(img_pil)
        hex_val = "#%02x%02x%02x" % tuple(exact_rgb)
        rgb_css = f"rgb({exact_rgb[0]}, {exact_rgb[1]}, {exact_rgb[2]})"
        
        # International Naming Logic
        p1, p2 = ("Leggings", "Dupatta") if "Kurta" in garment_choice else ("Blouse", "Border Detail")
        
        # Global Harmony Logic
        r_f, g_f, b_f = [x / 255.0 for x in exact_rgb]
        h_f, l_f, s_f = colorsys.rgb_to_hls(r_f, g_f, b_f)
        matches = {
            "Bold Contrast": colorsys.hls_to_rgb((h_f + 0.5) % 1.0, l_f, s_f),
            "Ethereal Tonal": colorsys.hls_to_rgb((h_f + 0.08) % 1.0, l_f, s_f),
            "Avant-Garde Set": colorsys.hls_to_rgb((h_f + 0.33) % 1.0, l_f, s_f)
        }

    with col_main:
        # Source Display Card
        st.markdown(f"""
            <div class="designer-card">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <h3>Source Extraction</h3>
                    <h4 style="color:#FF0080;">{hex_val.upper()}</h4>
                </div>
                <div class="swatch" style="background-color:{rgb_css}; height: 180px;"></div>
            </div>
        """, unsafe_allow_html=True)
        
        # Color theory diagrams help visualize these pairings
        
        
        # Image Display
        st.image(img_pil, use_container_width=True)

    st.divider()
    st.markdown(f"<h2 style='text-align: center;'>Global Pairings for {p1} & {p2}</h2>", unsafe_allow_html=True)
    
    # Designer Swatch Grid
    m_cols = st.columns(3)
    idx = 0
    for label, m_rgb in matches.items():
        m_int = [int(x*255) for x in m_rgb]
        m_hex = "#%02x%02x%02x" % tuple(m_int)
        m_css = f"rgb({m_int[0]}, {m_int[1]}, {m_int[2]})"
        with m_cols[idx]:
            st.markdown(f"""
                <div class="designer-card" style="text-align: center; padding: 15px;">
                    <p style="font-weight: bold; margin-bottom: 10px;">{label}</p>
                    <div class="swatch" style="background-color:{m_css}; height: 100px;"></div>
                    <code style="background: transparent; color: #FF0080; font-size: 1.1em;">{m_hex.upper()}</code>
                </div>
            """, unsafe_allow_html=True)
        idx += 1
else:
    with col_main:
        st.markdown("""
            <div class="designer-card" style="text-align: center; padding: 100px;">
                <h2 style="color: #b2bec3;">READY FOR ANALYSIS</h2>
                <p>Upload a catalog image to extract high-precision color data.</p>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f'<div style="text-align: center; font-weight: bold; color: #636e72;">Developed by Katragadda Surendra | International Application Developer</div>', unsafe_allow_html=True)
