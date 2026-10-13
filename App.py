import streamlit as st
from PIL import Image, ImageChops, ImageEnhance

st.title("🔍 Hansi's AI - Dot Detector")
st.write("Paint/Photoshop/AI walin dot ekak dammath ahuwenawa!")

uploaded = st.file_uploader("Image upload karanna", type=["jpg","png","jpeg"])

if uploaded:
    image = Image.open(uploaded).convert('RGB')
    st.image(image, caption="Original")

    image.save("temp.jpg", "JPEG", quality=90)
    temp = Image.open("temp.jpg")
    ela = ImageChops.difference(image, temp)

    max_d = max([ex[1] for ex in ela.getextrema()]) or 1
    ela = ImageEnhance.Brightness(ela).enhance(255.0/max_d * 1.5)

    avg = sum(ela.convert('L').getdata()) / (ela.size[0]*ela.size[1])

    st.image(ela, caption="ELA Result - Sudu thana = Edited")

    if avg > 15:
        st.error(f"🚨 EDITED - {min(avg*3,99):.1f}% Confidence! Dot ekak thibbath detect una!")
    else:
        st.success(f"✅ ORIGINAL - {100-avg:.1f}%")
