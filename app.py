import streamlit as st
import numpy as np
import cv2
from sklearn.cluster import KMeans
import colorsys

st.set_page_config(page_title="StyleMatch AI - Fabric Focus", layout="centered")

def get_garment_color(image, k=5):
    # 1. Focus on the center (Crop out 50% of the edges to avoid background)
    h, w, _ = image.shape
    start_h, start_w = h // 4, w // 4
    end_h, end_w = 3 * h // 4, 3 * w // 4
    crop_img = image[start_h:end_h, start_w:end_w]
    
    # 2. Resize for speed
    pixels = cv2.resize(crop_img, (100, 100)).reshape((-1, 3))
    
    # 3. Cluster colors
    clt = KMeans(n_clusters=k, n_init=10)
    clt.fit(pixels)
    colors = clt.cluster_centers_

    # 4. Logic: Find the most saturated (purest) color to avoid shadows/whites
    best_color = colors[0]
    max_score = -1
    
    for color in colors:
        r, g, b = color / 255.0
        h_val, l_val, s_val = colorsys.rgb_to_hls(r, g, b)
        
        # Scoring: High saturation + Moderate brightness = True Fabric Color
        # This ignores white backgrounds and black shadows
        score = s_val * (1 - abs(l_val - 0.5)) 
        
        if score > max_score:
            max_score = score
            best_color = color
            
    return [int(c) for c in best_color], crop_img

st.title("👗 StyleMatch AI: Fabric Focus")
st.info("The app now automatically crops the center of your photo to ignore backgrounds!")

uploaded_file = st.file_uploader("Upload Garment Photo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Process
    dom_color, focus_area = get_garment_color(img)
    rgb_str = f"rgb({dom_color[0]}, {dom_color[1]}, {dom_color[2]})"
    
    # Display results
    col1, col2 = st.columns(2)
    with col1:
        st.image(img, caption="Original Photo", use_container_width=True)
    with col2:
        st.image(focus_area, caption="Area Analyzed (Garment Only)", use_container_width=True)

    st.subheader("Detected Fabric Color")
    st.markdown(f'<div style="background-color:{rgb_str};width:100%;height:80px;border-radius:15px;border:4px solid white;box-shadow: 0 4px 15px rgba(0,0,0,0.3)"></div>', unsafe_allow_html=True)
    
    # Recommendations
    r, g, b = [x/255.0 for x in dom_color]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    matches = {
        "Perfect Contrast (Blouse)": colorsys.hls_to_rgb((h + 0.5) % 1.0, l, s),
        "Elegant Harmony (Border)": colorsys.hls_to_rgb((h + 0.1) % 1.0, l, s),
        "Modern Pop (Accessories)": colorsys.hls_to_rgb((h + 0.33) % 1.0, l, s)
    }

    st.divider()
    cols = st.columns(3)
    for i, (name, match_rgb) in enumerate(matches.items()):
        final_rgb = [int(x*255) for x in match_rgb]
        color_code = f"rgb({final_rgb[0]}, {final_rgb[1]}, {final_rgb[2]})"
        with cols[i]:
            st.write(f"**{name}**")
            st.markdown(f'<div style="background-color:{color_code};width:100%;height:100px;border-radius:10px;"></div>', unsafe_allow_html=True)
            st.caption(color_code)
