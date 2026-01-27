import streamlit as st
import numpy as np
import cv2
from sklearn.cluster import KMeans
import colorsys

st.set_page_config(page_title="StyleMatch AI - Perfect Color", layout="centered")

def get_exact_color(image, k=5):
    # 1. Focus on center 40% of image to avoid background fur/edges
    h, w, _ = image.shape
    cy, cx = h // 2, w // 2
    offset_h, offset_w = int(h * 0.2), int(w * 0.2)
    crop = image[cy-offset_h:cy+offset_h, cx-offset_w:cx+offset_w]
    
    # 2. Extract dominant colors using KMeans
    pixels = cv2.resize(crop, (100, 100)).reshape((-1, 3))
    clt = KMeans(n_clusters=k, n_init=10)
    clt.fit(pixels)
    
    # 3. Filter for 'Vibrant' color (ignores blacks, whites, and greys)
    best_rgb = clt.cluster_centers_[0]
    max_vibrancy = -1
    for color in clt.cluster_centers_:
        r, g, b = color / 255.0
        h_val, l_val, s_val = colorsys.rgb_to_hls(r, g, b)
        # Vibrancy score prioritizes saturation while avoiding shadows
        vibrancy = s_val * (1 - abs(l_val - 0.5)) 
        if vibrancy > max_vibrancy:
            max_vibrancy = vibrancy
            best_rgb = color
            
    return [int(c) for c in best_rgb], crop

def generate_perfect_matches(rgb_list):
    r, g, b = [x / 255.0 for x in rgb_list]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    # Matching rules based on fashion color theory
    return {
        "Complementary (Contrast)": colorsys.hls_to_rgb((h + 0.5) % 1.0, l, s),
        "Analogous (Harmonious)": colorsys.hls_to_rgb((h + 0.08) % 1.0, l, s),
        "Triadic (Vibrant)": colorsys.hls_to_rgb((h + 0.33) % 1.0, l, s),
        "Split-Complementary": colorsys.hls_to_rgb((h + 0.42) % 1.0, l, s)
    }

st.title("👗 StyleMatch AI: Exact Detection")
st.write("Ensuring the exact fabric color is matched by filtering out shadows and background.")

uploaded_file = st.file_uploader("Upload Garment Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.cvtColor(cv2.imdecode(file_bytes, 1), cv2.COLOR_BGR2RGB)
    
    exact_rgb, focused_crop = get_exact_color(img)
    rgb_css = f"rgb({exact_rgb[0]}, {exact_rgb[1]}, {exact_rgb[2]})"
    
    col1, col2 = st.columns(2)
    with col1: st.image(img, caption="Original Photo")
    with col2: st.image(focused_crop, caption="Detection Zone (Exact Color)")

    st.subheader("Exact Fabric Color Detected")
    st.markdown(f'<div style="background-color:{rgb_css};width:100%;height:80px;border-radius:12px;border:3px solid white;box-shadow: 0 4px 10px rgba(0,0,0,0.2);"></div>', unsafe_allow_html=True)
    
    matches = generate_perfect_matches(exact_rgb)
    st.divider()
    st.subheader("Perfect Pairings")
    
    cols = st.columns(len(matches))
    for i, (name, m_rgb) in enumerate(matches.items()):
        m_int = [int(x*255) for x in m_rgb]
        m_css = f"rgb({m_int[0]}, {m_int[1]}, {m_int[2]})"
        with cols[i]:
            st.write(f"**{name}**")
            st.markdown(f'<div style="background-color:{m_css};width:100%;height:100px;border-radius:8px;"></div>', unsafe_allow_html=True)
            # Fashion context
            advice = ["Blouse/Trouser", "Accessories", "Dupatta/Scarf", "Footwear"]
            st.caption(f"Best for: {advice[i]}")
