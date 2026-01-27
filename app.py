import streamlit as st
import numpy as np
import cv2
from sklearn.cluster import KMeans
import colorsys

st.set_page_config(page_title="StyleMatch AI Pro", layout="centered")

def get_vibrant_color(image, k=5):
    # 1. Resize and filter out background noise
    img = cv2.resize(image, (100, 100), interpolation=cv2.INTER_AREA)
    img = img.reshape((-1, 3))
    
    # 2. Find top 5 colors
    clt = KMeans(n_clusters=k, n_init=10)
    clt.fit(img)
    colors = clt.cluster_centers_

    # 3. Find the most "vibrant" color (highest saturation)
    vibrant_color = colors[0]
    max_sat = 0
    
    for color in colors:
        r, g, b = color / 255.0
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        # We want color, not white (high L) or black (low L)
        if s > max_sat and 0.2 < l < 0.8:
            max_sat = s
            vibrant_color = color
            
    return [int(c) for c in vibrant_color]

def get_recommendations(rgb_list):
    r, g, b = [x / 255.0 for x in rgb_list]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    # Fashion-forward matching logic
    matches = {
        "Contrasting Blouse": colorsys.hls_to_rgb((h + 0.5) % 1.0, l, s),
        "Matching Border/Thread": colorsys.hls_to_rgb((h + 0.08) % 1.0, l, s),
        "Modern/Designer Match": colorsys.hls_to_rgb((h + 0.33) % 1.0, l, s)
    }
    return matches

st.title("👗 StyleMatch AI Pro")
st.write("Optimized for Saree & Patterned Fabrics")

uploaded_file = st.file_uploader("Upload your outfit", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    st.image(img, caption="Your Uploaded Garment", use_container_width=True)
    
    # Advanced detection
    with st.spinner('Extracting true fabric color...'):
        dom_color = get_vibrant_color(img)
    
    rgb_str = f"rgb({dom_color[0]}, {dom_color[1]}, {dom_color[2]})"
    
    st.subheader("Detected True Color")
    st.markdown(f'<div style="background-color:{rgb_str};width:100%;height:70px;border-radius:15px;border:3px solid white;box-shadow: 0px 4px 10px rgba(0,0,0,0.2)"></div>', unsafe_allow_html=True)
    st.caption(f"App filtered out shadows and background to find this {rgb_str}")
    
    recommendations = get_recommendations(dom_color)
    
    st.divider()
    st.subheader("Perfect Pairings")
    cols = st.columns(3)
    
    labels = list(recommendations.keys())
    values = list(recommendations.values())
    
    for i in range(3):
        with cols[i]:
            match_rgb = [int(x * 255) for x in values[i]]
            match_str = f"rgb({match_rgb[0]}, {match_rgb[1]}, {match_rgb[2]})"
            st.write(f"**{labels[i]}**")
            st.markdown(f'<div style="background-color:{match_str};width:100%;height:120px;border-radius:10px;box-shadow: 2px 2px 8px rgba(0,0,0,0.1)"></div>', unsafe_allow_html=True)
            st.write(f"Code: {match_str}")
