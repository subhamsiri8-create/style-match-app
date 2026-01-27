import streamlit as st
import numpy as np
import cv2
from sklearn.cluster import KMeans
import colorsys

# Professional Page Configuration
st.set_page_config(page_title="StyleMatch AI | Katragadda Surendra", layout="centered")

def get_exact_fabric_hue(image, k=8):
    """Isolates the true fabric color by filtering out background and shadows."""
    h, w, _ = image.shape
    # Focus on the center fabric area to avoid background fur noise
    crop = image[int(h*0.15):int(h*0.5), int(w*0.2):int(w*0.8)]
    pixels = cv2.resize(crop, (100, 100)).reshape((-1, 3))
    
    clt = KMeans(n_clusters=k, n_init=10)
    clt.fit(pixels)
    
    best_rgb = clt.cluster_centers_[0]
    max_score = -1
    
    for color in clt.cluster_centers_:
        r, g, b = color / 255.0
        h_val, l_val, s_val = colorsys.rgb_to_hls(r, g, b)
        # Score prioritizing high saturation while avoiding white/black extremes
        score = s_val * (1 - abs(l_val - 0.5)) 
        if score > max_score:
            max_score = score
            best_rgb = color
    return [int(c) for c in best_rgb]

def get_garment_recommendations(rgb_list, garment_type):
    r, g, b = [x / 255.0 for x in rgb_list]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    # Precise Color Theory Matches
    match_map = {
        "Contrasting Match": colorsys.hls_to_rgb((h + 0.5) % 1.0, l, s),
        "Tonal Harmony": colorsys.hls_to_rgb((h + 0.05) % 1.0, l, s),
        "Designer's Pick": colorsys.hls_to_rgb((h + 0.33) % 1.0, l, s)
    }
    
    # Contextual Naming Logic
    if "Kurta" in garment_type:
        p1, p2 = "Leggings", "Chunny"
    elif "Saree" in garment_type:
        p1, p2 = "Blouse", "Accessories"
    else:
        p1, p2 = "Trouser", "Accessories"
        
    return match_map, p1, p2

# Professional UI
st.title("👗 StyleMatch AI Pro")
st.markdown("### Professional Matching for Subham Grand & Siri Dress Divine")

# Selection for specific garment logic
garment_choice = st.radio(
    "Select garment to match:", 
    ["Kurta (Ethnic)", "Saree (Ethnic)", "Shirt / T-shirt (Western)"], 
    horizontal=True
)
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.cvtColor(cv2.imdecode(file_bytes, 1), cv2.COLOR_BGR2RGB)
    
    with st.spinner("Analyzing exact fabric color..."):
        exact_rgb, = [get_exact_fabric_hue(img)]
        rgb_css = f"rgb({exact_rgb[0]}, {exact_rgb[1]}, {exact_rgb[2]})"
        matches, name_1, name_2 = get_garment_recommendations(exact_rgb, garment_choice)
    
    # Display Detection
    col1, col2 = st.columns([2, 1])
    with col1:
        st.image(img, use_container_width=True, caption="Detected Fabric")
    with col2:
        st.write("**Exact Fabric Color**")
        st.markdown(f'<div style="background-color:{rgb_css};width:100%;height:150px;border-radius:15px;border:5px solid white;box-shadow: 0 4px 15px rgba(0,0,0,0.2);"></div>', unsafe_allow_html=True)
        st.code(f"HEX: #%02x%02x%02x" % tuple(exact_rgb))

    st.divider()
    st.subheader(f"Professional Matches for {name_1} & {name_2}")
    
    cols = st.columns(3)
    for i, (label, m_rgb) in enumerate(matches.items()):
        m_int = [int(x*255) for x in m_rgb]
        m_css = f"rgb({m_int[0]}, {m_int[1]}, {m_int[2]})"
        with cols[i]:
            st.markdown(f"**{label}**")
            st.markdown(f'<div style="background-color:{m_css};width:100%;height:120px;border-radius:12px;"></div>', unsafe_allow_html=True)
            st.caption(f"Suggested for {name_1} & {name_2}")

# Professional Footer with Developer Credit
st.markdown("---")
st.markdown(
    f'<div style="text-align: center;"><p>Developed by <a href="https://gravatar.com/katragaddasurendra" target="_blank" style="text-decoration: none; color: #FF4B4B; font-weight: bold;">Katragadda Surendra</a></p></div>',
    unsafe_allow_html=True
)
