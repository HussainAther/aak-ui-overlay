import streamlit as st
import time
import json
import os
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="🎮 AAK Session HUD", layout="wide")
st.title("🎮 AAK Real-Time Session HUD")

# Setup containers
col1, col2, col3, col4 = st.columns(4)
keystroke_display = col1.empty()
mouse_display = col2.empty()
idle_display = col3.empty()
alignment_display = col4.empty()

sparkline_area = st.empty()
log_area = st.expander("📩 Claude Interventions (Recent)")

# Buffers for plotting
keystroke_history = []
idle_history = []
timestamps = []

# Live HUD update loop
for _ in range(100):
    try:
        with open("live_metrics.json", "r") as f:
            data = json.load(f)

        ks = data["keystrokes"]
        mm = data["mouse_movement"]
        idle = data["idle_seconds"]
        ts = data["timestamp"]
        match_score = data.get("task_alignment_score", 100)

        # Update metrics
        keystroke_display.metric("⌨️ Keystrokes", ks)
        mouse_display.metric("🖱️ Mouse Movement", mm)
        idle_display.metric("⏱️ Idle Time", f"{idle} sec")
        alignment_display.metric("🎯 Task Match", f"{match_score} %")

        # History
        keystroke_history.append(ks)
        idle_history.append(idle)
        timestamps.append(ts)

        df = pd.DataFrame({
            "timestamp": timestamps,
            "keystrokes": keystroke_history,
            "idle_seconds": idle_history
        })

        sparkline_area.line_chart(df.set_index("timestamp"))

        # Load and show Claude logs
        if os.path.exists("copilot_log.jsonl"):
            with open("copilot_log.jsonl", "r") as f:
                lines = f.readlines()[-5:]
                for line in lines:
                    try:
                        entry = json.loads(line)
                        log_area.markdown(
                            f"**🕒 {entry['timestamp']}**  \n"
                            f"**🤖 Claude:** {entry['ai_response']}  \n"
                            f"**🧑 User:** {entry['user_response']}  \n"
                            "---"
                        )
                    except:
                        continue

    except Exception as e:
        st.warning(f"Live data error: {e}")

    time.sleep(1)

