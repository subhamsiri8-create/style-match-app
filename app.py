import streamlit as st
import numpy as np
import cv2
from sklearn.cluster import KMeans
import colorsys

st.set_page_config(page_title="StyleMatch AI", layout="centered")

def get_dominant_color(image, k=1):
    # Resize to speed up processing
    img = cv2.resize(image, (100, 100), interpolation=cv2.INTER_AREA)
    img = img.reshape((-1, 3))
    
    # Find the most dominant color
    clt = KMeans(n_clusters=k, n_init=10)
    clt.fit(img)
    return clt.cluster_centers_[0].astype(int)

def get_recommendations(rgb):
    # Convert RGB to HLS (Hue, Lightness, Saturation)
    r, g, b = rgb / 255.0
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    # Calculate matches
    matches = {
        "Complementary (Bold)": colorsys.hls_to_rgb((h + 0.5) % 1.0, l, s),
        "Analogous (Safe)": colorsys.hls_to_rgb((h + 0.08) % 1.0, l, s),
        "Triadic (Stylish)": colorsys.hls_to_rgb((h + 0.33) % 1.0, l, s)
    }
    return matches

st.title("👗 StyleMatch AI")
st.write("Upload your Saree, Shirt, or T-shirt to find the perfect match!")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Process Image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)
    opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
    
    st.image(opencv_image, caption="Your Upload", use_container_width=True)
    
    with st.spinner('Analyzing colors...'):
        dom_color = get_dominant_color(opencv_image)
        recommendations = get_recommendations(dom_color)
        
    st.subheader("Detected Base Color")
    st.markdown(f'<div style="background-color:rgb{tuple(dom_color)};width:100%;height:50px;border-radius:10px"></div>', unsafe_all_white_space=True)
    
    st.divider()
    st.subheader("Recommended Matches")
    
    cols = st.columns(3)
    for i, (label, rgb) in enumerate(recommendations.items()):
        with cols[i]:
            final_rgb = tuple((np.array(rgb) * 255).astype(int))
            st.write(f"**{label}**")
            st.markdown(f'<div style="background-color:rgb{final_rgb};width:100%;height:100px;border-radius:10px;margin-bottom:10px"></div>', unsafe_all_white_space=True)
            st.caption(f"Best for: {'Blouse/Trouser' if i==0 else 'Accessories' if i==1 else 'Dupatta/Shoes'}")
