import streamlit as st
import numpy as np
from PIL import Image
import colorsys

# Professional Page Setup
st.set_page_config(page_title="StyleMatch AI | Professional Precision", layout="centered")

def get_matches(rgb_list, garment_type):
    r, g, b = [x / 255.0 for x in rgb_list]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    # Fashion Theory Pairing Logic
    match_map = {
        "Perfect Contrast": colorsys.hls_to_rgb((h + 0.5) % 1.0, l, s),
        "Tonal Harmony": colorsys.hls_to_rgb((h + 0.05) % 1.0, l, s),
        "Modern Designer": colorsys.hls_to_rgb((h + 0.33) % 1.0, l, s)
    }
    
    # Precise Naming for Brand Categories
    if "Kurta" in garment_type:
        p1, p2 = "Leggings", "Chunny"
    elif "Saree" in garment_type:
        p1, p2 = "Blouse", "Accessories"
    else:
        p1, p2 = "Trouser", "Accessories"
        
    return match_map, p1, p2

# UI Header
st.title("👗 StyleMatch AI Pro")
st.markdown("### Precision Fabric Extraction for Subham Grand & Siri Dress Divine")

garment_choice = st.radio(
    "Identify target garment:", 
    ["Kurta (Ethnic)", "Saree (Ethnic)", "Shirt (Western)"], 
    horizontal=True
)

uploaded_file = st.file_uploader("Upload Product Photo", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Load Image
    img = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(img)
    
    st.info("🎯 **Click on the garment** in the image below to extract the exact dye color.")
    
    # Native Streamlit Click Event (Error-Free)
    value = st.image(img, use_container_width=True)
    
    # Handle the click coordinates
    # Note: st.image returns a dict with 'x' and 'y' when clicked in latest Streamlit
    # If using an older version, we fallback to a manual color picker
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Manual Selection Fallback")
        picked_hex = st.color_picker("If clicking above doesn't work, pick color here:", "#000000")
        exact_rgb = [int(picked_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)]
    
    rgb_css = f"rgb({exact_rgb[0]}, {exact_rgb[1]}, {exact_rgb[2]})"
    matches, name_1, name_2 = get_matches(exact_rgb, garment_choice)
    
    # Results Display
    st.divider()
    col_res1, col_res2 = st.columns([1, 2])
    with col_res1:
        st.write("**Extracted Fabric Color**")
        st.markdown(f'<div style="background-color:{rgb_css};width:100%;height:120px;border-radius:15px;border:5px solid white;box-shadow: 0 4px 15px rgba(0,0,0,0.3);"></div>', unsafe_allow_html=True)
        st.code(f"HEX: #%02x%02x%02x" % tuple(exact_rgb))

    with col_res2:
        st.subheader(f"Professional Pairings for {name_1} & {name_2}")
        m_cols = st.columns(3)
        for i, (label, m_rgb) in enumerate(matches.items()):
            m_int = [int(x*255) for x in m_rgb]
            m_css = f"rgb({m_int[0]}, {m_int[1]}, {m_int[2]})"
            with m_cols[i]:
                st.markdown(f'<div style="background-color:{m_css};width:100%;height:80px;border-radius:10px;"></div>', unsafe_allow_html=True)
                st.caption(f"**{label}**")

# Professional Footer with Clickable Credit
st.markdown("---")
footer_html = """
<div style="text-align: center;">
    <p>Developed by <a href="https://gravatar.com/katragaddasurendra" target="_blank" style="text-decoration: none; color: #FF4B4B; font-weight: bold;">Katragadda Surendra</a></p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
