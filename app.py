import streamlit as st
import numpy as np
import cv2
from sklearn.cluster import KMeans
import colorsys

# Page Setup
st.set_page_config(page_title="StyleMatch AI | Professional", layout="centered")

def get_exact_color(image, k=8):
    """Crops background and detects the exact fabric dye color."""
    h, w, _ = image.shape
    # Focus on the core fabric area to avoid background fur
    crop = image[int(h*0.15):int(h*0.5), int(w*0.2):int(w*0.8)]
    pixels = cv2.resize(crop, (100, 100)).reshape((-1, 3))
    
    clt = KMeans(n_clusters=k, n_init=10)
    clt.fit(pixels)
    
    best_rgb = clt.cluster_centers_[0]
    max_score = -1
    
    for color in clt.cluster_centers_:
        r, g, b = color / 255.0
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        # Score ignores 'muddy' shadows and white backgrounds
        score = s * (1 - abs(l - 0.5)) 
        if score > max_score:
            max_score = score
            best_rgb = color
    return [int(c) for c in best_rgb]

def get_style_recommendations(rgb_list, garment_type):
    r, g, b = [x / 255.0 for x in rgb_list]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    # Matching Logic
    match_map = {
        "Contrasting": colorsys.hls_to_rgb((h + 0.5) % 1.0, l, s),
        "Harmonious": colorsys.hls_to_rgb((h + 0.08) % 1.0, l, s),
        "Modern Designer": colorsys.hls_to_rgb((h + 0.33) % 1.0, l, s)
    }
    
    # Naming Logic based on input
    item_name = "Blouse" if "Saree" in garment_type else "Trouser"
    return match_map, item_name

# Header
st.title("👗 StyleMatch Pro")
st.markdown("### Expert Color Matching for Ethnic & Western Wear")

garment_choice = st.radio("What are you matching today?", ["Saree (Ethnic)", "Shirt / T-shirt (Western)"], horizontal=True)
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.cvtColor(cv2.imdecode(file_bytes, 1), cv2.COLOR_BGR2RGB)
    
    with st.spinner("Isolating fabric hue..."):
        exact_rgb = get_exact_color(img)
        rgb_css = f"rgb({exact_rgb[0]}, {exact_rgb[1]}, {exact_rgb[2]})"
        matches, target_item = get_style_recommendations(exact_rgb, garment_choice)
    
    # Visual Output
    col1, col2 = st.columns([2, 1])
    with col1:
        st.image(img, use_container_width=True, caption="Original Fabric")
    with col2:
        st.write("**Detected Fabric**")
        st.markdown(f'<div style="background-color:{rgb_css};width:100%;height:150px;border-radius:15px;border:5px solid white;box-shadow: 0 4px 15px rgba(0,0,0,0.2);"></div>', unsafe_allow_html=True)
        st.code(f"HEX: #%02x%02x%02x" % tuple(exact_rgb))

    st.divider()
    st.subheader(f"Recommended {target_item} Colors")
    cols = st.columns(3)
    
    for i, (label, m_rgb) in enumerate(matches.items()):
        m_int = [int(x*255) for x in m_rgb]
        m_css = f"rgb({m_int[0]}, {m_int[1]}, {m_int[2]})"
        with cols[i]:
            st.markdown(f"**{label} {target_item}**")
            st.markdown(f'<div style="background-color:{m_css};width:100%;height:120px;border-radius:12px;"></div>', unsafe_allow_html=True)
            st.caption(f"Code: {m_css}")

# Professional Footer
st.markdown("---")
st.markdown(
    f'<div style="text-align: center;"><p>Developed by <a href="https://gravatar.com/katragaddasurendra" target="_blank" style="text-decoration: none; color: #FF4B4B; font-weight: bold;">Katragadda Surendra</a></p></div>',
    unsafe_allow_html=True
)
