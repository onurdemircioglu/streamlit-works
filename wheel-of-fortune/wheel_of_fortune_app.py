import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import io
import random
import time
from matplotlib import cm

# Function to draw the wheel with rotation and custom colors
def draw_wheel(options, angle, color_map_name):
    fig, ax = plt.subplots(figsize=(5, 5))
    cmap = cm.get_cmap(color_map_name, len(options))
    colors = [cmap(i) for i in range(len(options))]

    wedges, _ = ax.pie([1]*len(options), labels=options, startangle=angle, colors=colors)

    # Make the pie a circle
    ax.set_aspect('equal')

    # Set fixed axis limits to leave room for the pointer
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.2, 1.4)

    # Draw a red triangle pointer pointing DOWN toward the wheel
    pointer_x = [0, -0.05, 0.05]
    pointer_y = [1.15, 1.3, 1.3]  # This line has been changed
    ax.fill(pointer_x, pointer_y, color='red', zorder=5)



    # Save the figure to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return buf



# UI Setup
st.title("🎡 Animated Wheel of Fortune with Colors")
options = st.text_area("Enter options (one per line):", "Alper\nCaner\nAyşenur\nYenice\nOnur\nACY",height=200).splitlines()
options = [opt.strip() for opt in options if opt.strip()]

if len(options) < 2:
    st.warning("Please enter at least 2 options.")
    st.stop()

# Select color map
color_maps = ['tab10', 'Set3', 'Pastel1', 'rainbow', 'viridis', 'plasma', 'cool', 'spring']
color_map = st.selectbox("Choose a color scheme:", color_maps, index=1)

# Display static wheel
st.subheader("Wheel Preview")
buf = draw_wheel(options, angle=0, color_map_name=color_map)
st.image(buf)

# Spin the wheel
if st.button("🎯 Spin the Wheel!"):
    placeholder = st.empty()
    total_rotation = random.randint(720, 1440)
    steps = 60
    for i in range(steps):
        angle = total_rotation * (i + 1) / steps
        buf = draw_wheel(options, angle, color_map)
        placeholder.image(buf)
        time.sleep(0.03 + (i * 0.003))

    final_angle = total_rotation % 360
    slice_angle = 360 / len(options)

    # Matplotlib draws slices counter-clockwise starting from the x-axis,
    # but we want the pointer at the top (90 degrees), so we shift accordingly
    adjusted_angle = (90 - final_angle) % 360  # This line has been changed

    selected_index = int(adjusted_angle // slice_angle)
    winner = options[selected_index]



    st.success(f"🏆 The wheel stopped on: **{winner}** 🎉")
