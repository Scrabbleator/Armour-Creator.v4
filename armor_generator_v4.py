import streamlit as st
import os
import openai
import requests
from PIL import Image
from io import BytesIO

# Retrieve API Key from Streamlit Secrets
openai.api_key = "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"

# Debugging: Check if API Key is loaded
if openai.api_key:
    st.write(f"✅ API Key Set: {openai.api_key[:5]}*****")  # Show only first 5 characters
else:
    st.error("❌ OpenAI API Key not found! Please set it in Streamlit Secrets.")

# App Title
st.title("Custom Armor Generator - AI Integration")
st.subheader("Customize your armor and generate AI visuals in real-time.")

# Sidebar: Armor Customization
st.sidebar.header("Customize Your Armor")

# Under-Armor Options
under_armor = st.sidebar.selectbox(
    "Under Armor (Base Layer)",
    ["None", "Arming Doublet", "Chainmail Hauberk", "Leather Jerkin", "Brigandine"]
)

# Over-Armor Options
over_armor = st.sidebar.multiselect(
    "Over Armor (Accessories)",
    ["None", "Hooded Cloak", "Flowing Cape", "Heraldic Surcoat", "Fur-Lined Mantle"]
)

# Armor Material
armor_material = st.sidebar.selectbox(
    "Armor Material",
    ["Steel", "Bronze", "Gold", "Blackened Iron"]
)

# Helmet Options
helmet = st.sidebar.selectbox(
    "Helmet",
    ["None", "Great Helm", "Bascinet", "Sallet", "Visored Helm"]
)

# Shoulder Armor Options
shoulder_armor = st.sidebar.selectbox(
    "Shoulder Armor",
    ["None", "Spaulders", "Pauldrons", "Scaled Shoulders"]
)

# Engraving Style
engraving_style = st.sidebar.selectbox(
    "Engraving Style",
    ["None", "Floral", "Runes", "Geometric"]
)

# Decorative Design Options
design = st.sidebar.selectbox(
    "Decorative Design",
    ["None", "Floral Engravings", "Geometric Patterns", "Heraldic Symbols", "Mythical Creatures"]
)

# Color Customization
st.sidebar.header("Color Customizations")
base_layer_color = st.sidebar.color_picker("Base Layer Color (Tunic/Gambeson)", "#B87333")
armor_accent_color = st.sidebar.color_picker("Armor Accent Color", "#FFD700")
cloak_color = st.sidebar.color_picker("Cloak or Cape Color", "#5B84B1")

# Generate AI Prompt
st.header("Generated AI Prompt")

prompt = f"A warrior clad in {armor_material.lower()} armor. "
if under_armor != "None":
    prompt += f"Underneath, they wear a {under_armor.lower()} dyed {base_layer_color}. "
if over_armor and "None" not in over_armor:
    prompt += f"Over the armor, they wear {', '.join(over_armor).lower()}, dyed {cloak_color}. "
if helmet != "None":
    prompt += f"They wear a {helmet.lower()} on their head. "
if shoulder_armor != "None":
    prompt += f"Their shoulders are protected by {shoulder_armor.lower()}. "
if design != "None":
    prompt += f"The armor is adorned with {design.lower()} designs. "
if engraving_style != "None":
    prompt += f"The engravings feature {engraving_style.lower()} patterns. "
prompt += f"The armor is accented with {armor_accent_color}."

st.text_area("AI Prompt", value=prompt, height=150)

# AI Image Generation Function
def generate_armor_image(prompt):
    if not openai.api_key:
        st.error("❌ OpenAI API Key is missing. Please set it in Streamlit Secrets.")
        return None

    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    image_url = response['data'][0]['url']
    return image_url

# Display AI-Generated Image
st.header("Generated Armor Image")

if st.button("Generate Armor Image"):
    with st.spinner("Generating image..."):
        try:
            image_url = generate_armor_image(prompt)
            if image_url:
                response = requests.get(image_url)
                image = Image.open(BytesIO(response.content))
                st.image(image, caption="AI-Generated Armor")

                # Allow users to download the image
                buf = BytesIO()
                image.save(buf, format="PNG")
                byte_im = buf.getvalue()

                st.download_button(
                    label="Download Armor Image",
                    data=byte_im,
                    file_name="custom_armor.png",
                    mime="image/png"
                )
        except Exception as e:
            st.error(f"Error generating image: {e}")
