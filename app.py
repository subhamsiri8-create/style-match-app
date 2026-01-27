import streamlit as st
import numpy as np
import cv2
from sklearn.cluster import KMeans
import colorsys

# Page Config
st.set_page_config(page_title="StyleMatch AI | Professional", layout="centered")

def get_exact_fabric_color(image, k=5):
    """Crops the image to focus on fabric and extracts the most vibrant hue."""
    h, w, _ = image.shape
    # Focus on the center-top where the main body of the saree/shirt usually is
    crop = image[int(h*0.1):int(h*0.5), int(w*0.2):int(w*0.8)]
    
    pixels = cv2.resize(crop, (100, 100)).reshape((-1, 3))
    clt = KMeans(n_clusters=k, n_init=10)
    clt.fit(pixels)
    
    best_rgb = clt.cluster_centers_[0]
    max_vibrancy = -1
    
    for color in clt.cluster_centers_:
        r, g, b = color / 255.0
        h_val, l_val, s_val = colorsys.rgb_to_hls(r, g, b)
        # Score ignores neutrals (white/grey/black) and picks high saturation
        score = s_val * (1 - abs(l_val - 0.5))
        if score > max_vibrancy:
            max_vibrancy = score
            best_rgb = color
            
    return [int(c) for c in best_rgb], crop

def get_matches(rgb_list):
    r, g, b = [x / 255.0 for x in rgb_list]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    # Professional matching logic
    return {
        "Contrasting Blouse/Pant": colorsys.hls_to_rgb((h + 0.5) % 1.0, l, s),
        "Elegant Harmony": colorsys.hls_to_rgb((h + 0.05) % 1.0, l, s),
        "Modern Statement": colorsys.hls_to_rgb((h + 0.33) % 1.0, l, s),
        "Soft Complement": colorsys.hls_to_rgb((h + 0.45) % 1.0, l + (0.1 if l < 0.5 else -0.1), s)
    }

# UI Header
st.title("👗 StyleMatch AI Pro")
st.markdown("#### Precise Color Detection for High-End Ethnic Wear")

uploaded_file = st.file_uploader("Upload Garment", type=["jpg", "png", "jpeg"])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.cvtColor(cv2.imdecode(file_bytes, 1), cv2.COLOR_BGR2RGB)
    
    with st.spinner("Analyzing fabric texture and hue..."):
        exact_rgb, focus_zone = get_exact_fabric_color(img)
        rgb_css = f"rgb({exact_rgb[0]}, {exact_rgb[1]}, {exact_rgb[2]})"
        matches = get_matches(exact_rgb)
    
    # Display Detection
    col1, col2 = st.columns([2, 1])
    with col1:
        st.image(img, use_container_width=True, caption="Original Fabric")
    with col2:
        st.write("**Detected Base**")
        st.markdown(f'<div style="background-color:{rgb_css};width:100%;height:150px;border-radius:15px;border:4px solid white;box-shadow: 0 4px 15px rgba(0,0,0,0.2);"></div>', unsafe_allow_html=True)
        st.code(f"HEX: #%02x%02x%02x" % tuple(exact_rgb))

    st.divider()
    
    # Matching Results
    st.subheader("Perfect Style Pairings")
    cols = st.columns(4)
    for i, (label, m_rgb) in enumerate(matches.items()):
        m_int = [int(x*255) for x in m_rgb]
        m_css = f"rgb({m_int[0]}, {m_int[1]}, {m_int[2]})"
        with cols[i]:
            st.markdown(f"**{label}**")
            st.markdown(f'<div style="background-color:{m_css};width:100%;height:120px;border-radius:10px;margin-bottom:10px;"></div>', unsafe_allow_html=True)
            st.caption(f"Code: {m_css}")

# Professional Footer
st.markdown("---")
footer_html = """
<div style="text-align: center;">
    <p>Developed by <a href="https://gravatar.com/katragaddasurendra" target="_blank" style="text-decoration: none; color: #FF4B4B; font-weight: bold;">Katragadda Surendra</a></p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
