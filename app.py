import streamlit as st
import numpy as np
import cv2
from sklearn.cluster import KMeans
import colorsys

# Professional Page Setup
st.set_page_config(page_title="StyleMatch AI | Professional", layout="centered")

def get_exact_garment_color(image, k=10):
    """
    Isolates the garment by cropping to the center-mass of the image
    and filtering for the most vibrant fabric hue.
    """
    h, w, _ = image.shape
    
    # 1. Human-Centric Crop: Focus on the center 50% (where the garment usually is)
    # This naturally excludes most skin tones (face/hands) and background fur.
    ch, cw = h // 2, w // 2
    rh, rw = int(h * 0.25), int(w * 0.25)
    crop = image[ch-rh:ch+rh, cw-rw:cw+rw]
    
    # 2. Extract colors using high-precision clustering
    pixels = cv2.resize(crop, (100, 100)).reshape((-1, 3))
    clt = KMeans(n_clusters=k, n_init=10)
    clt.fit(pixels)
    
    best_rgb = clt.cluster_centers_[0]
    max_vibrancy = -1
    
    # 3. Fabric-First Logic: Filter out Skin Tones & Backgrounds
    for color in clt.cluster_centers_:
        r, g, b = color / 255.0
        h_val, l_val, s_val = colorsys.rgb_to_hls(r, g, b)
        
        # Skin Tone Filter (Approximate Hue range for skin is 0-50 in degrees)
        # We also ignore very low saturation (grey background) and extremes of Lightness.
        is_skin = (h_val < 0.15 or h_val > 0.9) and (0.2 < s_val < 0.6)
        
        # Scoring: Prioritize pure fabric saturation over everything else
        score = s_val * (1 - abs(l_val - 0.5))
        if is_skin:
            score *= 0.5 # De-prioritize skin tones
            
        if score > max_vibrancy:
            max_vibrancy = score
            best_rgb = color
            
    return [int(c) for c in best_rgb], crop

def get_pro_recommendations(rgb_list, garment_type):
    r, g, b = [x / 255.0 for x in rgb_list]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    # Fashion Theory Pairing
    match_map = {
        "Contrasting Match": colorsys.hls_to_rgb((h + 0.5) % 1.0, l, s),
        "Tonal Harmony": colorsys.hls_to_rgb((h + 0.08) % 1.0, l, s),
        "Designer's Pick": colorsys.hls_to_rgb((h + 0.33) % 1.0, l, s)
    }
    
    # Custom Naming for Subham Grand & Siri Dress Divine
    if "Kurta" in garment_type:
        p1, p2 = "Leggings", "Chunny"
    elif "Saree" in garment_type:
        p1, p2 = "Blouse", "Accessories"
    else:
        p1, p2 = "Trouser", "Accessories"
        
    return match_map, p1, p2

# UI Header
st.title("👗 StyleMatch AI Pro")
st.markdown("### Exact Fabric Extraction for Professional Cataloging")

# Professional Selection Logic
garment_choice = st.radio(
    "Identify the garment:", 
    ["Kurta (Ethnic)", "Saree (Ethnic)", "Shirt / T-shirt (Western)"], 
    horizontal=True
)
uploaded_file = st.file_uploader("Upload Person with Garment", type=["jpg", "png", "jpeg"])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.cvtColor(cv2.imdecode(file_bytes, 1), cv2.COLOR_BGR2RGB)
    
    with st.spinner("Extracting exact fabric hue from person..."):
        exact_rgb, focus_zone = get_exact_garment_color(img)
        rgb_css = f"rgb({exact_rgb[0]}, {exact_rgb[1]}, {exact_rgb[2]})"
        matches, name_1, name_2 = get_pro_recommendations(exact_rgb, garment_choice)
    
    # Results Layout
    col1, col2 = st.columns([2, 1])
    with col1:
        st.image(img, use_container_width=True, caption="Analyzed Image")
    with col2:
        st.write("**Exact Fabric Color**")
        st.markdown(f'<div style="background-color:{rgb_css};width:100%;height:150px;border-radius:15px;border:5px solid white;box-shadow: 0 4px 15px rgba(0,0,0,0.3);"></div>', unsafe_allow_html=True)
        st.code(f"HEX: #%02x%02x%02x" % tuple(exact_rgb))
        st.caption("AI focused on the center mass and fabric saturation.")

    st.divider()
    st.subheader(f"Professional Pairings for {name_1} & {name_2}")
    
    cols = st.columns(3)
    for i, (label, m_rgb) in enumerate(matches.items()):
        m_int = [int(x*255) for x in m_rgb]
        m_css = f"rgb({m_int[0]}, {m_int[1]}, {m_int[2]})"
        with cols[i]:
            st.markdown(f"**{label}**")
            st.markdown(f'<div style="background-color:{m_css};width:100%;height:120px;border-radius:12px;"></div>', unsafe_allow_html=True)
            st.caption(f"Perfect for your {name_1} or {name_2}")

# Professional Footer with Developer Credit
st.markdown("---")
footer_html = f"""
<div style="text-align: center;">
    <p>Developed by <a href="https://gravatar.com/katragaddasurendra" target="_blank" style="text-decoration: none; color: #FF4B4B; font-weight: bold;">Katragadda Surendra</a></p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
