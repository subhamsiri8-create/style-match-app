import streamlit as st
import numpy as np
import cv2
from PIL import Image
from sklearn.cluster import KMeans
import colorsys

# Professional Page Setup
st.set_page_config(page_title="StyleMatch AI Pro", layout="centered")

def get_pro_color_name(rgb):
    """Stable color mapping using native math to prevent library crashes."""
    universal_colors = {
        "Midnight Navy": (15, 25, 55), "Deep Maroon": (128, 0, 0),
        "Golden Mustard": (218, 165, 32), "Emerald Green": (0, 155, 119),
        "Ruby Red": (178, 34, 34), "Royal Blue": (65, 105, 225),
        "Teal Green": (0, 128, 128), "Deep Purple": (128, 0, 128),
        "Charcoal Grey": (54, 69, 79), "Silver Grey": (192, 192, 192),
        "Warm Beige": (245, 245, 220), "Copper Zari": (184, 115, 51)
    }
    closest_name = "Designer Shade"
    min_dist = float('inf')
    for name, target_rgb in universal_colors.items():
        dist = np.sqrt(sum((np.array(rgb) - np.array(target_rgb))**2))
        if dist < min_dist:
            min_dist = dist
            closest_name = name
    return closest_name

def extract_precise_fabric(image):
    """Targets center fabric mass to ignore studio backgrounds."""
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    h, w, _ = img_cv.shape
    # Targeted center crop to avoid beige studio walls and floors
    cy, cx = h // 2, w // 2
    rh, rw = int(h * 0.12), int(w * 0.12)
    crop = img_cv[cy-rh:cy+rh, cx-rw:cx+rw]
    
    pixels = cv2.resize(crop, (80, 80)).reshape((-1, 3))
    clt = KMeans(n_clusters=4, n_init=5)
    clt.fit(pixels)
    
    best_rgb = [128, 128, 128]
    max_s = -1
    for color in clt.cluster_centers_:
        r, g, b = color[::-1] / 255.0
        h_v, l_v, s_v = colorsys.rgb_to_hls(r, g, b)
        # Prioritize true dye vibrancy over shadows
        score = s_v * (1 - abs(l_v - 0.5))
        if score > max_s:
            max_s = score
            best_rgb = color[::-1]
    return [int(c) for c in best_rgb]

# UI Header
st.title("👗 StyleMatch AI Pro")
st.markdown("### Precision Cataloging for Subham Grand & Siri Dress Divine")

# Category Logic Selection
garment_choice = st.radio(
    "Select Garment Category:", 
    ["Kurta (Ethnic)", "Saree (Ethnic)", "Shirt / T-shirt (Western)"], 
    horizontal=True
)
uploaded_file = st.file_uploader("Upload Product Photo", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img_pil = Image.open(uploaded_file).convert("RGB")
    
    with st.spinner("Analyzing professional color pairings..."):
        exact_rgb = extract_precise_fabric(img_pil)
        color_name = get_pro_color_name(exact_rgb)
        hex_val = "#%02x%02x%02x" % tuple(exact_rgb)
        rgb_css = f"rgb({exact_rgb[0]}, {exact_rgb[1]}, {exact_rgb[2]})"
        
        # Dynamic Labeling based on User Needs
        if "Kurta" in garment_choice:
            p1, p2 = "Matching Leggings", "Matching Dupatta"
        elif "Saree" in garment_choice:
            p1, p2 = "Matching Blouse", "Contrast Border/Zari"
        else:
            p1, p2 = "Matching Trouser", "Jeans / Chinos"
        
        # Color Theory Pairing
        r_f, g_f, b_f = [x / 255.0 for x in exact_rgb]
        h_f, l_f, s_f = colorsys.rgb_to_hls(r_f, g_f, b_f)
        matches = {
            "Contrast": colorsys.hls_to_rgb((h_f + 0.5) % 1.0, l_f, s_f),
            "Tonal": colorsys.hls_to_rgb((h_f + 0.05) % 1.0, l_f, s_f),
            "Designer": colorsys.hls_to_rgb((h_f + 0.33) % 1.0, l_f, s_f)
        }
    
    # Results Display
    col1, col2 = st.columns([2, 1])
    with col1:
        st.image(img_pil, use_container_width=True, caption="Verified Catalog Image")
    with col2:
        st.write(f"**Fabric Hue: {color_name}**")
        st.markdown(f'<div style="background-color:{rgb_css};width:100%;height:140px;border-radius:15px;border:5px solid white;box-shadow: 0 4px 15px rgba(0,0,0,0.3);"></div>', unsafe_allow_html=True)
        st.code(f"HEX: {hex_val}")
        st.divider()
        st.color_picker("Fine-tune color:", hex_val)

    st.divider()
    st.subheader(f"Expert Pairings for {p1} & {p2}")
    
    # Using a flat column loop to prevent IndentationErrors
    m_cols = st.columns(3)
    idx = 0
    for label, m_rgb in matches.items():
        m_int = [int(x*255) for x in m_rgb]
        m_name = get_pro_color_name(m_int)
        m_css = f"rgb({m_int[0]}, {m_int[1]}, {m_int[2]})"
        with m_cols[idx]:
            st.markdown(f"**{label}**")
            st.markdown(f'<div style="background-color:{m_css};width:100%;height:100px;border-radius:12px;"></div>', unsafe_allow_html=True)
            st.write(f"**{m_name}**")
            st.caption(f"Suggested for {p1}/{p2}")
        idx += 1

# Professional Footer
st.markdown("---")
footer_html = """
<div style="text-align: center;">
    <p>Developed by <a href="https://gravatar.com/katragaddasurendra" target="_blank" style="text-decoration: none; color: #FF4B4B; font-weight: bold;">Katragadda Surendra</a></p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
