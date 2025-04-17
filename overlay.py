import streamlit as st
import time
import random

st.set_page_config(page_title="🎮 AAK Session HUD", layout="wide")

st.title("🎮 AAK Real-Time Session HUD")
st.markdown("This overlay simulates live session feedback — keystroke bursts, mouse speed, task alignment.")

# HUD containers
col1, col2, col3 = st.columns(3)

keystroke_display = col1.empty()
mouse_display = col2.empty()
alignment_display = col3.empty()

# Simulated live update
for _ in range(100):
    keystrokes = random.randint(0, 20)
    mouse_speed = round(random.uniform(0.5, 3.5), 2)
    alignment_score = round(random.uniform(60, 100), 1)

    keystroke_display.metric("⌨️ Keystroke Burst", f"{keystrokes} keys")
    mouse_display.metric("🖱️ Mouse Speed", f"{mouse_speed} px/s")
    alignment_display.metric("🎯 Task Match", f"{alignment_score} %")

    time.sleep(1)

