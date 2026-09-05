import streamlit as st
from novita_client import NovitaClient
from PIL import Image
from io import BytesIO
import base64

# Initialize NovitaClient
client = NovitaClient("sk_e8KJWg7LN2-7VJc6UbUYjkLIsfjyh_URo7aMJx8Vlgg")

st.title("Image to Video Generator")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open and display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Resize image if necessary
    max_width = 576
    max_height = 1024
    img_width, img_height = image.size

    if img_width > max_width or img_height > max_height:
        aspect_ratio = img_width / img_height
        if img_width > max_width:
            img_width = max_width
            img_height = int(img_width / aspect_ratio)
        if img_height > max_height:
            img_height = max_height
            img_width = int(img_height * aspect_ratio)
        image = image.resize((img_width, img_height), Image.LANCZOS)

    # Convert image to base64
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    image_data = f"data:image/jpeg;base64,{image_base64}"

    # Generate video
    if st.button("Generate Video"):
        res = client.img2video(
            model_name="SVD-XT",
            image=image_data,
            frames_num=25,
            frames_per_second=6,
            seed=-1,
            image_file_resize_mode="ORIGINAL_RESOLUTION",
            steps=20
        )

        # Save and display video
        video_bytes = res.video_bytes[0]
        video_file = BytesIO(video_bytes)
        st.video(video_file)
        st.success("Video generated successfully!")
