import streamlit as st
import numpy as np
from PIL import Image
import cv2
from sklearn.cluster import KMeans
import colorsys

# Professional Page Setup
st.set_page_config(page_title="StyleMatch AI | Professional", layout="centered")

def get_exact_fabric_color(image):
    # Convert PIL to OpenCv
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    h, w, _ = img.shape
    
    # Precision Crop: Focus on center 40% to ignore backgrounds and skin
    cy, cx = h // 2, w // 2
    offset_h, offset_w = int(h * 0.2), int(w * 0.2)
    crop = img[cy-offset_h:cy+offset_h, cx-offset_w:cx+offset_w]
    
    # Cluster to find dominant colors
    pixels = cv2.resize(crop, (100, 100)).reshape((-1, 3))
    clt = KMeans(n_clusters=5, n_init=10)
    clt.fit(pixels)
    
    # Score clusters to find the most 'vibrant' one (ignores shadows/whites)
    best_rgb = clt.cluster_centers_[0]
    max_score = -1
    for color in clt.cluster_centers_:
        r, g, b = color[::-1] / 255.0 # BGR to RGB
        h_val, l_val, s_val = colorsys.rgb_to_hls(r, g, b)
        score = s_val * (1 - abs(l_val - 0.5))
        if score > max_score:
            max_score = score
            best_rgb = color[::-1]
            
    return [int(c) for c in best_rgb]

def get_matches(rgb_list, garment_type):
    r, g, b = [x / 255.0 for x in rgb_list]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    match_map = {
        "Perfect Contrast": colorsys.hls_to_rgb((h + 0.5) % 1.0, l, s),
        "Tonal Harmony": colorsys.hls_to_rgb((h + 0.05) % 1.0, l, s),
        "Modern Designer": colorsys.hls_to_rgb((h + 0.33) % 1.0, l, s)
    }
    
    # Brand-Specific Naming
    if "Kurta" in garment_type:
        p1, p2 = "Leggings", "Chunny"
    elif "Saree" in garment_type:
        p1, p2 = "Blouse", "Accessories"
    else:
        p1, p2 = "Trouser", "Accessories"
        
    return match_map, p1, p2

st.title("👗 StyleMatch AI Pro")
st.markdown("### Precision Extraction for Subham Grand & Siri Dress Divine")

garment_choice = st.radio("Match target:", ["Kurta (Ethnic)", "Saree (Ethnic)", "Shirt (Western)"], horizontal=True)
uploaded_file = st.file_uploader("Upload Product Photo", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    
    with st.spinner("Analyzing fabric hue..."):
        exact_rgb = get_exact_fabric_color(img)
        rgb_css = f"rgb({exact_rgb[0]}, {exact_rgb[1]}, {exact_rgb[2]})"
        matches, name_1, name_2 = get_matches(exact_rgb, garment_choice)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.image(img, use_container_width=True, caption="Source Image")
    with col2:
        st.write("**Extracted Color**")
        st.markdown(f'<div style="background-color:{rgb_css};width:100%;height:150px;border-radius:15px;border:5px solid white;box-shadow: 0 4px 15px rgba(0,0,0,0.3);"></div>', unsafe_allow_html=True)
        st.code(f"HEX: #%02x%02x%02x" % tuple(exact_rgb))
        
        # Manual Fallback
        st.divider()
        st.caption("Manual Fine-Tune:")
        picked_hex = st.color_picker("Pick if detection is off:", rgb_css)

    st.divider()
    st.subheader(f"Professional Pairings for {name_1} & {name_2}")
    cols = st.columns(3)
    for i, (label, m_rgb) in enumerate(matches.items()):
        m_int = [int(x*255) for x in m_rgb]
        m_css = f"rgb({m_int[0]}, {m_int[1]}, {m_int[2]})"
        with cols[i]:
            st.markdown(f"**{label}**")
            st.markdown(f'<div style="background-color:{m_css};width:100%;height:100px;border-radius:10px;"></div>', unsafe_allow_html=True)
            st.caption(f"Best for {name_1} or {name_2}")

st.markdown("---")
st.markdown(f'<div style="text-align: center;"><p>Developed by <a href="https://gravatar.com/katragaddasurendra" target="_blank" style="text-decoration: none; color: #FF4B4B; font-weight: bold;">Katragadda Surendra</a></p></div>', unsafe_allow_html=True)
