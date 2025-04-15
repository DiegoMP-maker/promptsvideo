import random
import streamlit as st
import json
import os

# Optimized agent for creating video prompts for Sora
class SoraPromptCreator:
    def __init__(self):
        # Load knowledge base from JSON file
        knowledge_path = os.path.join("knowledge.json")
        with open(knowledge_path, "r", encoding="utf-8") as file:
            self.knowledge_base = json.load(file)

        self.styles = list(self.knowledge_base.keys())

        # Manually defined image paths to avoid naming errors
        self.style_images = {
            "Blade Runner 2049, cyberpunk": "images/blade_runner_2049_cyberpunk.jpg",
            "Terrence Malick, dreamlike cinematography": "images/terrence_malick.jpg",
            "Studio Ghibli, magical realism": "images/magical_realism.jpg",
            "Andrei Tarkovsky, slow and contemplative": "images/andrei_tarkovsky.jpg",
            "Wes Anderson, symmetrical and colorful": "images/wes_anderson.jpg",
            "Latin American magical realism": "images/latin_american_magical_realism.jpg",
            "Dystopian futurism": "images/dystopian_futurism.jpg",
            "Japanese minimalism": "images/japanese_minimalism.jpg",
            "German expressionism, harsh shadows and unsettling atmosphere": "images/german_expressionism.jpg",
            "Italian neorealism, natural light and urban settings": "images/italian_neorealism.jpg",
            "Film Noir, high contrast and dark aesthetics": "images/film_noir.jpg",
            "80s Sci-Fi, neon and vaporwave": "images/80s_sci_fi.jpg",
            "Abstract visual poetry": "images/abstract_visual_poetry.jpg"
        }

    def get_style_description(self, style):
        return self.knowledge_base[style].get("description", "")

    def get_style_prompt(self, style):
        return self.knowledge_base[style].get("prompt", "")

    def generate_scene_prompt(self, user_input, genre, scene_type, selected_style=None, duration_seconds=5, details=None):
        additional_details = details or "No additional effects specified."

        prompt = f"""
Scene description: {user_input}

Genre: {genre}

Scene Type: {scene_type}

Style references: {selected_style or random.choice(self.styles)}

Duration: {duration_seconds} seconds

Special details: {additional_details}
        """
        return prompt.strip()

    def offer_styles(self):
        return self.styles

    def get_style_image(self, style):
        return self.style_images.get(style, None)

# Streamlit App UI
st.set_page_config(page_title="Cinematic Style Gallery", layout="wide")
st.title("🎥 Cinematic Visual Styles Gallery for Sora Prompts")

agent = SoraPromptCreator()

st.subheader("📝 Enter your base text (poem, short story, visual idea)")
default_text = "A man walks alone through a city submerged in fog, his memories appearing and disappearing like flashes."
user_text = st.text_area("Base Text", default_text, height=150)

# Genre selector
genres = [
    "Short film", "Music video", "Instagram Reel", "Spotify Clip", "Experimental film",
    "Conceptual art video", "Documentary", "Commercial advertisement", "Fashion film",
    "Animation", "Art installation video", "Interactive film", "Theater performance",
    "Virtual reality experience", "360° immersive video"
]
selected_genre = st.selectbox("🎬 Select the Visual Genre", genres)

# Scene type selector
types_of_scene = ["Single scene", "Sequence of scenes"]
selected_scene_type = st.radio("🎞️ Scene Type", types_of_scene, horizontal=True)

# Duration and effects
duration_seconds = st.radio("⏱️ Scene Duration", (5, 10), horizontal=True)
selected_effects = st.multiselect("🧩 Advanced Visual Effects", [
    "Slow motion", "Glitch transition", "Analog film grain texture", "Fade to black transition",
    "Bokeh effect", "Handheld camera", "Dramatic zoom", "Time-lapse", "Motion blur", "Tilt-shift",
    "POV camera", "Floating steadicam", "360° panoramic", "Hyperrealistic zoom"
])
effects_description = "; ".join(selected_effects) if selected_effects else None

st.markdown("---")
st.subheader("✨ Choose a Visual Style to Generate Your Prompt")

cols = st.columns(3)
prompt_generated = None

for idx, style in enumerate(agent.offer_styles()):
    with cols[idx % 3]:
        img_path = agent.get_style_image(style)
        st.image(img_path, use_container_width=True, caption=style)
        st.caption(agent.get_style_description(style))

        with st.expander("See Style Prompt"):
            st.code(agent.get_style_prompt(style))

        button_placeholder = st.empty()
        if button_placeholder.button("Select", key=f"button_{idx}"):
            prompt_generated = agent.generate_scene_prompt(
                user_text,
                genre=selected_genre,
                scene_type=selected_scene_type,
                selected_style=style,
                duration_seconds=duration_seconds,
                details=effects_description
            )

            st.success("✅ Prompt Generated")

            edited_prompt = st.text_area(
                label="✏️ Edit your prompt before downloading",
                value=prompt_generated,
                height=300,
                key=f"edited_prompt_{idx}"
            )

            st.download_button(
                label="📥 Download Edited Prompt",
                data=edited_prompt,
                file_name=f"prompt_{style.replace(' ', '_')}.txt"
            )

st.markdown("---")
st.caption("Click on a style to generate your Sora video prompt.")
