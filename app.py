import streamlit as st
import numpy as np
import cv2
from PIL import Image
from sklearn.cluster import KMeans
import colorsys

# Professional Page Config
st.set_page_config(page_title="StyleMatch Elite", layout="wide", initial_sidebar_state="expanded")

# Apple/Microsoft Style CSS
st.markdown("""
    <style>
    /* Glassmorphism Effect */
    .stApp {
        background-color: #f5f5f7;
        color: #1d1d1f;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-right: 1px solid #d2d2d7;
    }
    
    /* Modern Card Container */
    .element-container img {
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Result Swatch Styling */
    .color-card {
        background: white;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 20px;
        border: 1px solid #d2d2d7;
    }
    
    .swatch {
        height: 100px;
        border-radius: 12px;
        margin-bottom: 12px;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    /* Professional Typography */
    h1 {
        font-weight: 600;
        letter-spacing: -0.022em;
        color: #1d1d1f;
    }
    </style>
    """, unsafe_allow_html=True)

def extract_accurate_dye(image):
    """Precision extraction focusing on center fabric mass."""
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    h, w, _ = img_cv.shape
    cy, cx = h // 2, w // 2
    rh, rw = int(h * 0.08), int(w * 0.08)
    crop = img_cv[cy-rh:cy+rh, cx-rw:cx+rw]
    
    pixels = cv2.resize(crop, (60, 60)).reshape((-1, 3))
    clt = KMeans(n_clusters=4, n_init=5)
    clt.fit(pixels)
    
    best_rgb = [128, 128, 128]
    max_score = -1
    for color in clt.cluster_centers_:
        r, g, b = color[::-1] / 255.0
        h_v, l_v, s_v = colorsys.rgb_to_hls(r, g, b)
        score = (s_v * 0.7) + (l_v * 0.3) 
        if 0.1 < l_v < 0.97:
            if score > max_score:
                max_score = score
                best_rgb = color[::-1]
    return [int(c) for c in best_rgb]

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.title("StyleMatch")
    st.markdown("### Configuration")
    garment_choice = st.selectbox(
        "Garment Type", 
        ["Kurta (Ethnic)", "Saree (Ethnic)", "Shirt (Western)"]
    )
    uploaded_file = st.file_uploader("Upload Product Photo", type=["jpg", "png", "jpeg"])
    st.divider()
    st.caption("Developed by Katragadda Surendra")

# --- MAIN WORKSPACE ---
if uploaded_file:
    img_pil = Image.open(uploaded_file).convert("RGB")
    
    # Process
    with st.spinner("Synchronizing Fabric Data..."):
        exact_rgb = extract_accurate_dye(img_pil)
        hex_val = "#%02x%02x%02x" % tuple(exact_rgb)
        rgb_css = f"rgb({exact_rgb[0]}, {exact_rgb[1]}, {exact_rgb[2]})"
        
        # Dynamic Labeling
        p1, p2 = ("Leggings", "Dupatta") if "Kurta" in garment_choice else ("Blouse", "Border")
        
        # Color Harmony Pairings
        r_f, g_f, b_f = [x / 255.0 for x in exact_rgb]
        h_f, l_f, s_f = colorsys.rgb_to_hls(r_f, g_f, b_f)
        matches = {
            "Contrast Pair": colorsys.hls_to_rgb((h_f + 0.5) % 1.0, l_f, s_f),
            "Tonal Blend": colorsys.hls_to_rgb((h_f + 0.06) % 1.0, l_f, s_f),
            "Designer Set": colorsys.hls_to_rgb((h_f + 0.33) % 1.0, l_f, s_f)
        }

    # Layout
    col_img, col_res = st.columns([1.2, 1])
    
    with col_img:
        st.image(img_pil, use_container_width=True)

    with col_res:
        st.markdown(f"""
            <div class="color-card">
                <h3 style="margin-top:0;">Source Pigment</h3>
                <div class="swatch" style="background-color:{rgb_css}; height:150px;"></div>
                <p style="font-family:monospace; font-weight:bold; font-size:1.2em;">{hex_val.upper()}</p>
            </div>
        """, unsafe_allow_html=True)
        st.color_picker("Fine-tune Selection", hex_val)

    st.divider()
    st.markdown(f"### Professional Pairings for {p1} & {p2}")
    
    # Grid for matches
    m_cols = st.columns(3)
    idx = 0
    for label, m_rgb in matches.items():
        m_int = [int(x*255) for x in m_rgb]
        m_hex = "#%02x%02x%02x" % tuple(m_int)
        m_css = f"rgb({m_int[0]}, {m_int[1]}, {m_int[2]})"
        with m_cols[idx]:
            st.markdown(f"""
                <div class="color-card">
                    <p style="font-weight:600; color:#86868b; margin-bottom:8px;">{label}</p>
                    <div class="swatch" style="background-color:{m_css};"></div>
                    <p style="font-family:monospace;">{m_hex.upper()}</p>
                </div>
            """, unsafe_allow_html=True)
        idx += 1
else:
    st.markdown("### Upload an image to begin the professional color analysis.")

# Footer
st.markdown("---")
st.markdown(f'<div style="text-align: center; color:#86868b; font-size:0.9em;">Katragadda Surendra | Professional App Developer</div>', unsafe_allow_html=True)
