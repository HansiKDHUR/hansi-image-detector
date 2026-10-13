import streamlit as st
from PIL import Image, ImageChops, ImageEnhance, ImageStat, ExifTags
import io

st.set_page_config(page_title="Hansi AI Detector Pro")
st.title("🔍 Hansi's PRO Detector")
st.write("Photoshop | Paint | AI | Filter - Siyalla Detect!")

uploaded = st.file_uploader("Image eka danna", type=["jpg","png","jpeg","webp"])

if uploaded:
    image = Image.open(uploaded).convert('RGB')
    st.image(image, width=350)

    # 1. METADATA CHECK
    try:
        exif = image._getexif()
        if exif:
            software = [v for k,v in exif.items() if "Software" in str(ExifTags.TAGS.get(k))]
            if software:
                st.warning(f"⚠️ Software Found in metadata: {software}")
    except:
        pass

    # 2. ELA CHECK (90 quality)
    buf = io.BytesIO()
    image.save(buf, "JPEG", quality=90)
    buf.seek(0)
    temp = Image.open(buf)
    ela = ImageChops.difference(image, temp)
    max_d = max([ex[1] for ex in ela.getextrema()]) or 1
    ela = ImageEnhance.Brightness(ela).enhance(255.0/max_d * 2.5)

    st.image(ela, width=350, caption="ELA - White area = Edited")

    stat = ImageStat.Stat(ela.convert('L'))
    mean = stat.mean[0]
    stddev = stat.stddev[0]
    extrema = stat.extrema[0]

    # 3. FINAL VERDICT
    st.divider()
    st.subheader("Result:")

    if mean > 20 or stddev > 30:
        st.error(f"🚨 EDITED CONFIRMED - Score {mean:.1f}")
        st.write("✓ Photoshop / Paint / AI edit ekak thiyanawa")
        if extrema[1] > 200:
            st.write("✓ Bright white spots = Pasted / Drawn area")
    elif mean > 10:
        st.warning(f"⚠️ POSSIBLY EDITED - Score {mean:.1f}")
        st.write("Re-save karala athi, hari filter ekak dala athi")
    else:
        st.success(f"✅ ORIGINAL - Score {mean:.1f}")
        st.write("Edit ekak na wage")

    with st.expander("Technical Details"):
        st.write(f"Mean: {mean:.2f}, StdDev: {stddev:.2f}, Max: {extrema[1]}")
