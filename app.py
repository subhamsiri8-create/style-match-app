import streamlit as st
import numpy as np
import cv2
from sklearn.cluster import KMeans
import colorsys

# Page Configuration
st.set_page_config(page_title="StyleMatch AI | Professional", layout="centered")

def get_exact_fabric_color(image, k=8):
    """Aggressively filters background noise and shadows to find the true dye color."""
    h, w, _ = image.shape
    
    # 1. Create a Tight Center Mask (ignores fur background/edges)
    # We take the center 40% of the image
    ch, cw = h // 2, w // 2
    rh, rw = int(h * 0.2), int(w * 0.2)
    focus_zone = image[ch-rh:ch+rh, cw-rw:cw+rw]
    
    # 2. Extract colors using high-precision clustering
    pixels = cv2.resize(focus_zone, (100, 100)).reshape((-1, 3))
    clt = KMeans(n_clusters=k, n_init=15)
    clt.fit(pixels)
    
    # 3. Precision Filtering: Find the 'True' Fabric Hue
    # We ignore very light (white/background) and very dark (shadows) pixels
    best_rgb = clt.cluster_centers_[0]
    max_vibrancy_score = -1
    
    for color in clt.cluster_centers_:
        r, g, b = color / 255.0
        h_val, l_val, s_val = colorsys.rgb_to_hls(r, g, b)
        
        # Scoring Logic: High saturation is prioritized. 
        # We penalize colors that are too bright (fur) or too dark (shadows).
        vibrancy_score = s_val * (1 - abs(l_val - 0.5))
        
        if vibrancy_score > max_vibrancy_score:
            max_vibrancy_score = vibrancy_score
            best_rgb = color
            
    return [int(c) for c in best_rgb], focus_zone

def get_professional_matches(rgb_list):
    r, g, b = [x / 255.0 for x in rgb_list]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    # Fashion-forward pairing logic
    return {
        "Contrasting Blouse": colorsys.hls_to_rgb((h + 0.5) % 1.0, l, s),
        "Tonal/Harmonious": colorsys.hls_to_rgb((h + 0.05) % 1.0, l, s),
        "Designer Accents": colorsys.hls_to_rgb((h + 0.33) % 1.0, l, s),
        "Soft Neutral": colorsys.hls_to_rgb(h, 0.9, 0.1) # Soft cream/beige base
    }

# UI Header
st.title("👗 StyleMatch AI Pro")
st.markdown("### High-Precision Color Detection for Ethnic Wear")

uploaded_file = st.file_uploader("Upload Garment Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.cvtColor(cv2.imdecode(file_bytes, 1), cv2.COLOR_BGR2RGB)
    
    with st.spinner("Analyzing fabric hue and texture..."):
        exact_rgb, focus_area = get_exact_fabric_color(img)
        rgb_css = f"rgb({exact_rgb[0]}, {exact_rgb[1]}, {exact_rgb[2]})"
        matches = get_professional_matches(exact_rgb)
    
    # Visual Layout
    col1, col2 = st.columns([2, 1])
    with col1:
        st.image(img, use_container_width=True, caption="Original Garment")
    with col2:
        st.write("**Detected True Color**")
        st.markdown(f'<div style="background-color:{rgb_css};width:100%;height:140px;border-radius:15px;border:5px solid white;box-shadow: 0 4px 15px rgba(0,0,0,0.3);"></div>', unsafe_allow_html=True)
        st.code(f"HEX: #%02x%02x%02x" % tuple(exact_rgb))
        st.caption("Background and shadows filtered out.")

    st.divider()
    st.subheader("Curated Style Recommendations")
    
    cols = st.columns(4)
    labels = list(matches.keys())
    values = list(matches.values())
    
    for i in range(4):
        m_int = [int(x*255) for x in values[i]]
        m_css = f"rgb({m_int[0]}, {m_int[1]}, {m_int[2]})"
        with cols[i]:
            st.markdown(f"**{labels[i]}**")
            st.markdown(f'<div style="background-color:{m_css};width:100%;height:100px;border-radius:10px;"></div>', unsafe_allow_html=True)
            st.caption(f"Code: {m_css}")

# Professional Footer
st.markdown("---")
footer_html = """
<div style="text-align: center; padding: 10px;">
    <p style="font-size: 16px;">Developed by 
        <a href="https://gravatar.com/katragaddasurendra" target="_blank" style="text-decoration: none; color: #FF4B4B; font-weight: bold;">
            Katragadda Surendra
        </a>
    </p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
