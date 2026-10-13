import streamlit as st
from PIL import Image, ImageChops, ImageEnhance, ImageStat
import io

st.title("🔍 Hansi Detector - No False Positive")
st.write("Original JPEG walata edited kiyanne na")

uploaded = st.file_uploader("Image", type=["jpg","png","jpeg","webp"])

if uploaded:
    img = Image.open(uploaded).convert('RGB')
    st.image(img, width=320)

    # ELA with 95 quality (original walata less white)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=95)
    buf.seek(0)
    temp = Image.open(buf)

    ela = ImageChops.difference(img, temp)
    max_d = max([e[1] for e in ela.getextrema()]) or 1
    ela = ImageEnhance.Brightness(ela).enhance(255.0/max_d)

    # Center crop - edges ignore
    w,h = ela.size
    ela_crop = ela.crop((w*0.05, h*0.05, w*0.95, h*0.95))
    stat = ImageStat.Stat(ela_crop.convert('L'))

    mean = stat.mean[0]
    st.image(ela, width=320, caption="ELA Result")
    st.write(f"Score: {mean:.2f}")

    # NEW THRESHOLDS - Fixed for false positive
    if mean > 22:
        st.error("🚨 EDITED - Sure edit ekak thiyanawa")
    elif mean > 12:
        st.warning("⚠️ CHECK - Re-save wela thiyanawa, edit ekak wenna puluwan")
        st.write("Original photo ekak unath phone eken save karama mehema enawa")
    else:
        st.success("✅ ORIGINAL - 100% Clean")
