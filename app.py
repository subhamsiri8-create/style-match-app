import streamlit as st
import numpy as np
from PIL import Image
import cv2
from sklearn.cluster import KMeans
import colorsys
import webcolors

# Professional Page Setup
st.set_page_config(page_title="StyleMatch AI | Professional", layout="centered")

def get_color_name(rgb_list):
    """Translates RGB values into the closest professional color name."""
    try:
        # Try exact match first
        return webcolors.rgb_to_name(tuple(rgb_list))
    except ValueError:
        # Find the closest match if exact name doesn't exist
        min_colors = {}
        for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - rgb_list[0]) ** 2
            gd = (g_c - rgb_list[1]) ** 2
            bd = (b_c - rgb_list[2]) ** 2
            min_colors[(rd + gd + bd)] = name
        return min_colors[min(min_colors.keys())]

def get_exact_fabric_color(image):
    try:
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        h, w, _ = img.shape
        # Precision Crop: Center 40% to avoid background and skin
        cy, cx = h // 2, w // 2
        offset_h, offset_w = int(h * 0.2), int(w * 0.2)
        crop = img[cy-offset_h:cy+offset_h, cx-offset_w:cx+offset_w]
        
        pixels = cv2.resize(crop, (100, 100)).reshape((-1, 3))
        clt = KMeans(n_clusters=5, n_init=10)
        clt.fit(pixels)
        
        best_rgb = [128, 128, 128]
        max_score = -1
        for color in clt.cluster_centers_:
            r, g, b = color[::-1] / 255.0
            h_v, l_v, s_v = colorsys.rgb_to_hls(r, g, b)
            # Prioritize fabric saturation
            score = s_v * (1 - abs(l_v - 0.5))
            if score > max_score:
                max_score = score
                best_rgb = color[::-1]
        return [int(c) for c in best_rgb]
    except:
        return [128, 128, 128]

def get_matches(rgb_list, garment_type):
    r, g, b = [x / 255.0 for x in rgb_list]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    # Fashion Theory Pairings
    match_map = {
        "Perfect Contrast": colorsys.hls_to_rgb((h + 0.5) % 1.0, l, s),
        "Tonal Harmony": colorsys.hls_to_rgb((h + 0.05) % 1.0, l, s),
        "Modern Designer": colorsys.hls_to_rgb((h + 0.33) % 1.0, l, s)
    }
    
    if "Kurta" in garment_type:
        p1, p2 = "Leggings", "Chunny"
    elif "Saree" in garment_type:
        p1, p2 = "Blouse", "Accessories"
    else:
        p1, p2 = "Trouser", "Accessories"
        
    return match_map, p1, p2

# UI Header
st.title("👗 StyleMatch AI Pro")
st.markdown("### Precision Color Naming for Subham Grand & Siri Dress Divine")

garment_choice = st.radio("Match target:", ["Kurta (Ethnic)", "Saree (Ethnic)", "Shirt (Western)"], horizontal=True)
uploaded_file = st.file_uploader("Upload Product Photo", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    
    with st.spinner("Analyzing fabric hue and color name..."):
        exact_rgb = get_exact_fabric_color(img)
        color_name = get_color_name(exact_rgb).title()
        hex_val = "#%02x%02x%02x" % tuple(exact_rgb)
        rgb_css = f"rgb({exact_rgb[0]}, {exact_rgb[1]}, {exact_rgb[2]})"
        matches, name_1, name_2 = get_matches(exact_rgb, garment_choice)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.image(img, use_container_width=True, caption="Source Image")
    with col2:
        st.write(f"**Detected: {color_name}**")
        st.markdown(f'<div style="background-color:{rgb_css};width:100%;height:120px;border-radius:15px;border:5px solid white;box-shadow: 0 4px 15px rgba(0,0,0,0.3);"></div>', unsafe_allow_html=True)
        st.code(f"HEX: {hex_val}")
        st.caption("Manual Fine-Tune:")
        picked_hex = st.color_picker("Adjust color:", hex_val)

    st.divider()
    st.subheader(f"Matching {name_1} & {name_2} Suggestions")
    cols = st.columns(3)
    for i, (label, m_rgb) in enumerate(matches.items()):
        m_int = [int(x*255) for x in m_rgb]
        m_name = get_color_name(m_int).title()
        m_css = f"rgb({m_int[0]}, {m_int[1]}, {m_int[2]})"
        with cols[i]:
            st.markdown(f"**{label}**")
            st.markdown(f'<div style="background-color:{m_css};width:100%;height:80px;border-radius:10px;"></div>', unsafe_allow_html=True)
            st.write(f"**{m_name}**")
            st.caption(f"For {name_1} or {name_2}")

# Footer
st.markdown("---")
st.markdown(f'<div style="text-align: center;"><p>Developed by <a href="https://gravatar.com/katragaddasurendra" target="_blank" style="text-decoration: none; color: #FF4B4B; font-weight: bold;">Katragadda Surendra</a></p></div>', unsafe_allow_html=True)
