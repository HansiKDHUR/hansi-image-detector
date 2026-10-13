import streamlit as st
from PIL import Image, ImageChops, ImageEnhance, ImageStat

st.set_page_config(page_title="Hansi Detector")
st.title("🔍 Hansi's Detector - Fixed")
st.caption("No more false positives")

uploaded = st.file_uploader("Image upload karanna", type=["jpg","png","jpeg","webp"])

if uploaded:
    img = Image.open(uploaded).convert('RGB')
    st.image(img, width=350, caption="Uploaded")

    # ELA Quality 95 - Best for original photos
    img.save("/tmp/temp.jpg", "JPEG", quality=95)
    temp = Image.open("/tmp/temp.jpg")

    ela = ImageChops.difference(img, temp)
    max_d = max([e[1] for e in ela.getextrema()]) or 1
    ela = ImageEnhance.Brightness(ela).enhance(255.0/max_d)

    # Remove borders to avoid false white
    w,h = ela.size
    ela_crop = ela.crop((w*0.05, h*0.05, w*0.95, h*0.95))

    stat = ImageStat.Stat(ela_crop.convert('L'))
    mean_score = stat.mean[0]

    st.image(ela, width=350, caption="ELA (Black = Original, White = Edited)")
    st.metric("Originality Score", f"{mean_score:.2f}")

    # CORRECTED THRESHOLDS based on your images
    if mean_score < 8:
        st.success(f"✅ 100% ORIGINAL - No edit (Score {mean_score:.1f})")
        st.balloons()
    elif mean_score < 12:
        st.info(f"ℹ️ ORIGINAL - Normal photo (Score {mean_score:.1f}) - Save wela thiyanawa")
    elif mean_score < 18:
        st.warning(f"⚠️ SUSPECT - Filter / Re-save (Score {mean_score:.1f})")
    else:
        st.error(f"🚨 EDITED - Photoshop/Paint edit detected! (Score {mean_score:.1f})")
