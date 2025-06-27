import streamlit as st
from pathlib import Path

# ------------------
# PAGE CONFIG
# ------------------
st.set_page_config(page_title="🎾 Tennis Video Overlay", layout="wide")

# ------------------
# CUSTOM CSS
# ------------------
custom_css = """
<style>
/* Background & fonts */
body {
    background-color: #f0fff0;
    color: #002147;
    font-family: 'Helvetica', sans-serif;
}

h1, h2, h3 {
    color: #006400; /* Deep green like tennis courts */
    font-weight: bold;
}

.stButton>button {
    background-color: #ffd700 !important; /* tennis ball yellow */
    color: black !important;
    border-radius: 10px;
    font-weight: bold;
}

.stCheckbox>label {
    font-size: 16px;
    font-weight: 500;
    color: #003366; /* dark blue */
}

.sidebar .sidebar-content {
    background-color: #e6ffe6;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ------------------
# LOAD FILES
# ------------------
VIDEO_PATH = Path("assets/video.mp4")
JSON_PATHS = {
    "ball": Path("assets/ball_data.json"),
    "players": Path("assets/player_data.json"),
    "shots": Path("assets/shots_data.json")
}
# These will be used inside your actual functions later

# ------------------
# SIDEBAR CONTROLS
# ------------------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/3/3e/Tennis_ball_2.png", width=100)
st.sidebar.title("🎾 Overlay Options")

st.sidebar.subheader("A. Video Overlays")

show_ball_traj = st.sidebar.checkbox("🎾 Ball Trajectory", value=True)
color_by_speed = st.sidebar.checkbox("Color by Speed", value=False) if show_ball_traj else False

show_player_traj = st.sidebar.checkbox("🏃 Player Trajectories", value=True)
player_tail = st.sidebar.checkbox("Show Player Tails", value=True) if show_player_traj else False

show_bounce = st.sidebar.checkbox("🟢 Show Bounce Points", value=True)
show_hit = st.sidebar.checkbox("🎯 Show Hit Points", value=True)
show_shot_data = st.sidebar.checkbox("📈 Show Shot Data", value=False)

st.sidebar.subheader("B. Minimap")
show_minimap = st.sidebar.checkbox("🗺️ Show Minimap", value=False)
minimap_player_tail = st.sidebar.checkbox("Minimap Player Tails", value=True) if show_minimap else False
minimap_shots = st.sidebar.checkbox("Minimap Shot Trajectories", value=True) if show_minimap else False

st.sidebar.subheader("C. Analytics")
show_analytics = st.sidebar.checkbox("📊 Show Analytics", value=False)

# ------------------
# MAIN AREA
# ------------------
st.title("🏟️ Tennis Video Overlay Tool")

# VIDEO PREVIEW
st.markdown("### 🎥 Original Match Video")
if VIDEO_PATH.exists():
    st.video(str(VIDEO_PATH))
else:
    st.error("Video not found. Please check path: `assets/video.mp4`")

# DOWNLOAD BUTTON
st.markdown("### ⬇️ Download")
st.button("🎾 Download Processed Video")

# ANALYTICS PANEL
if show_analytics:
    st.markdown("## 📊 Analytics Summary")
    st.info("This is where you could display stats like average rally length, player movement heatmaps, shot speeds, etc.")

# DEBUG / CONFIG PREVIEW
with st.expander("🔧 Debug Configuration"):
    st.json({
        "ball_trajectory": show_ball_traj,
        "color_by_speed": color_by_speed,
        "player_trajectory": show_player_traj,
        "player_tail": player_tail,
        "bounce": show_bounce,
        "hit": show_hit,
        "shot_data": show_shot_data,
        "minimap": show_minimap,
        "minimap_player_tail": minimap_player_tail,
        "minimap_shots": minimap_shots,
        "analytics": show_analytics
    })
