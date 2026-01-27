import streamlit as st
import numpy as np
import cv2
from sklearn.cluster import KMeans
import colorsys

# Professional Page Setup
st.set_page_config(page_title="StyleMatch AI | Professional Precision", layout="centered")

def get_exact_fabric_hue(image, k=12):
    """Uses HSV masking to isolate vibrant fabric colors from backgrounds and skin."""
    h, w, _ = image.shape
    # Focus on the center mass to avoid background edges
    ch, cw = h // 2, w // 2
    rh, rw = int(h * 0.2), int(w * 0.2)
    crop = image[ch-rh:ch+rh, cw-rw:cw+rw]
    
    # Convert to HSV to find 'colorful' pixels
    hsv = cv2.cvtColor(crop, cv2.COLOR_RGB2HSV)
    # Mask: Saturation > 40 (colorful) and Value > 20 (not pure black)
    mask = cv2.inRange(hsv, (0, 40, 20), (180, 255, 245))
    fabric_pixels = crop[mask > 0]
    
    if len(fabric_pixels) < 10: # Fallback if no colorful pixels found
        fabric_pixels = crop.reshape((-1, 3))

    clt = KMeans(n_clusters=k, n_init=10)
    clt.fit(fabric_pixels)
    
    # Pick the cluster with the highest saturation
    best_rgb = clt.cluster_centers_[0]
    max_s = -1
    for color in clt.cluster_centers_:
        r, g, b = color / 255.0
        _, _, s = colorsys.rgb_to_hls(r, g, b)
        if s > max_s:
            max_s = s
            best_rgb = color
    return [int(c) for c in best_rgb]

def get_professional_matches(rgb_list, garment_type):
    r, g, b = [x / 255.0 for x in rgb_list]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    # Fashion Theory Pairing Logic
    match_map = {
        "Perfect Contrast": colorsys.hls_to_rgb((h + 0.5) % 1.0, l, s),
        "Tonal Harmony": colorsys.hls_to_rgb((h + 0.05) % 1.0, l, s),
        "Modern Designer": colorsys.hls_to_rgb((h + 0.33) % 1.0, l, s)
    }
    
    # Precise Naming for Your Specific Brand Needs
    if "Kurta" in garment_type:
        p1, p2 = "Leggings", "Chunny"
    elif "Saree" in garment_type:
        p1, p2 = "Blouse", "Accessories"
    else:
        p1, p2 = "Trouser", "Accessories"
        
    return match_map, p1, p2

# UI Header
st.title("👗 StyleMatch Pro")
st.markdown("### Professional Fabric Color Extraction & Matching")

garment_choice = st.radio("Target Garment:", ["Kurta (Ethnic)", "Saree (Ethnic)", "Shirt (Western)"], horizontal=True)

uploaded_file = st.file_uploader("Upload Product Photo", type=["jpg", "png", "jpeg"])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.cvtColor(cv2.imdecode(file_bytes, 1), cv2.COLOR_BGR2RGB)
    
    with st.spinner("Analyzing exact fabric hue..."):
        exact_rgb = get_exact_fabric_hue(img)
        rgb_css = f"rgb({exact_rgb[0]}, {exact_rgb[1]}, {exact_rgb[2]})"
        matches, name_1, name_2 = get_professional_matches(exact_rgb, garment_choice)
    
    # Results Layout
    col1, col2 = st.columns([2, 1])
    with col1:
        st.image(img, use_container_width=True, caption="Analyzed Image")
    with col2:
        st.write("**Exact Fabric Color**")
        st.markdown(f'<div style="background-color:{rgb_css};width:100%;height:150px;border-radius:15px;border:5px solid white;box-shadow: 0 4px 15px rgba(0,0,0,0.3);"></div>', unsafe_allow_html=True)
        st.code(f"HEX: #%02x%02x%02x" % tuple(exact_rgb))

    st.divider()
    st.subheader(f"Professional Pairings for {name_1} & {name_2}")
    
    cols = st.columns(3)
    for i, (label, m_rgb) in enumerate(matches.items()):
        m_int = [int(x*255) for x in m_rgb]
        m_css = f"rgb({m_int[0]}, {m_int[1]}, {m_int[2]})"
        with cols[i]:
            st.markdown(f"**{label}**")
            st.markdown(f'<div style="background-color:{m_css};width:100%;height:120px;border-radius:12px;"></div>', unsafe_allow_html=True)
            st.caption(f"Best for {name_1} or {name_2}")

# Professional Footer with Developer Credit
st.markdown("---")
footer_html = """
<div style="text-align: center;">
    <p>Developed by <a href="https://gravatar.com/katragaddasurendra" target="_blank" style="text-decoration: none; color: #FF4B4B; font-weight: bold;">Katragadda Surendra</a></p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
