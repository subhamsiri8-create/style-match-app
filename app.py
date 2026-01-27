import streamlit as st
import numpy as np
import cv2
from sklearn.cluster import KMeans
import colorsys

st.set_page_config(page_title="StyleMatch AI", layout="centered")

def get_dominant_color(image, k=1):
    # Resize to speed up and smooth out textures (like silk sheen)
    img = cv2.resize(image, (100, 100), interpolation=cv2.INTER_AREA)
    img = img.reshape((-1, 3))
    clt = KMeans(n_clusters=k, n_init=10)
    clt.fit(img)
    # Ensure values are standard Python ints, not numpy types
    return [int(c) for c in clt.cluster_centers_[0]]

def get_recommendations(rgb_list):
    r, g, b = [x / 255.0 for x in rgb_list]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    # Matching Logic
    matches = {
        "Complementary (Contrast)": colorsys.hls_to_rgb((h + 0.5) % 1.0, l, s),
        "Analogous (Harmonious)": colorsys.hls_to_rgb((h + 0.05) % 1.0, l, s),
        "Triadic (Vibrant)": colorsys.hls_to_rgb((h + 0.33) % 1.0, l, s)
    }
    return matches

st.title("👗 StyleMatch AI")
st.write("Upload your outfit to find matching colors instantly.")

uploaded_file = st.file_uploader("Upload Saree, Shirt, or T-shirt", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    st.image(img, caption="Your Upload", use_container_width=True)
    
    dom_color = get_dominant_color(img)
    # Format the RGB string correctly for CSS
    rgb_str = f"rgb({dom_color[0]}, {dom_color[1]}, {dom_color[2]})"
    
    st.subheader("Detected Base Color")
    st.markdown(f'<div style="background-color:{rgb_str};width:100%;height:60px;border-radius:10px;border:1px solid #eee"></div>', unsafe_allow_html=True)
    
    recommendations = get_recommendations(dom_color)
    
    st.divider()
    st.subheader("Recommended Matches")
    cols = st.columns(3)
    
    labels = list(recommendations.keys())
    values = list(recommendations.values())
    
    for i in range(3):
        with cols[i]:
            match_rgb = [int(x * 255) for x in values[i]]
            match_str = f"rgb({match_rgb[0]}, {match_rgb[1]}, {match_rgb[2]})"
            st.write(f"**{labels[i]}**")
            st.markdown(f'<div style="background-color:{match_str};width:100%;height:100px;border-radius:10px;box-shadow: 2px 2px 5px rgba(0,0,0,0.1)"></div>', unsafe_allow_html=True)
            # Contextual advice
            advice = ["Blouse / Trouser", "Accessories", "Dupatta / Tie"]
            st.caption(f"Best for: {advice[i]}")
