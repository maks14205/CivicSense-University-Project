import streamlit as st
import folium
from streamlit_folium import st_folium
import datetime
import random
import pandas as pd
from transformers import pipeline

# 1. Page Frame Configuration
st.set_page_config(
    page_title="CivicSense AI Dashboard", page_icon="🚨", layout="centered"
)

# 2. Custom Dark Tactical Visual Layout Theme
st.markdown(
    """
    <style>
    .stApp { background-color: #121214; color: #FFFFFF; }
    .header-container {
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px 0px; border-bottom: 1px solid #2A2A30;
    }
    .status-indicator { color: #00E676; font-size: 12px; font-weight: bold; }
    .kpi-box {
        background-color: #1E1E22; padding: 15px; border-radius: 8px;
        text-align: center; border: 1px solid #2A2A30;
    }
    .kpi-val { font-size: 24px; font-weight: bold; margin: 5px 0; }
    .kpi-label { font-size: 11px; color: #AAAAAA; text-transform: uppercase; }
    .incident-card-critical { 
        background-color: #1E1E22; padding: 15px; border-radius: 8px; 
        margin-bottom: 15px; cursor: pointer; border: 1px solid #2A2A30;
    }
    .incident-card-critical:hover {
        border: 1px solid #00E676; background-color: #242429;
    }
    .badge-status { color: white; padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: bold; }
    .time-elapsed { color: #AAAAAA; font-size: 12px; float: right; }
    .ai-analysis-box {
        background-color: #1A233D; border-left: 4px solid #00E676;
        padding: 10px; margin-top: 10px; border-radius: 4px; font-size: 13px;
    }
    .inspector-box {
        background-color: #1E1E22; padding: 20px; border-radius: 8px;
        border: 1px solid #00E676; margin: 15px 0;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# 3. Caching optimization for AI Text-Generation Engine
@st.cache_resource
def initialize_ai_pipeline():
    try:
        return pipeline("text2text-generation", model="google/flan-t5-small")
    except Exception:
        return None


ai_commander = initialize_ai_pipeline()

if "selected_incident_id" not in st.session_state:
    st.session_state.selected_incident_id = None

# 4. Kaggle Dataset Adapter Block
if "incident_db" not in st.session_state:
    try:
        raw_df = pd.read_csv("kaggle_disasters.csv")
        sample_df = raw_df.head(15).copy()

        parsed_records = []
        for idx, row in sample_df.iterrows():
            parsed_records.append(
                {
                    "id": idx + 1,
                    "type": str(
                        row.get("disaster_type", row.get("type", "General Disaster"))
                    ),
                    "district": str(
                        row.get(
                            "country",
                            row.get("location", row.get("district", "Incident Zone")),
                        )
                    ),
                    "lat": float(
                        row.get(
                            "latitude",
                            row.get("lat", 41.8781 + random.uniform(-0.04, 0.04)),
                        )
                    ),
                    "lon": float(
                        row.get(
                            "longitude",
                            row.get("lon", -87.6298 + random.uniform(-0.04, 0.04)),
                        )
                    ),
                    "status": str(
                        row.get("status", "CRITICAL" if idx % 2 == 0 else "ACTIVE")
                    ),
                    "pop_affected": int(
                        row.get(
                            "pop_affected",
                            row.get("casualties", random.randint(150, 2000)),
                        )
                    ),
                    "time": "Kaggle Log Record",
                    "details": str(
                        row.get(
                            "details",
                            row.get(
                                "description",
                                row.get(
                                    "text",
                                    "Field event recorded via global monitoring sensors.",
                                ),
                            ),
                        )
                    ),
                }
            )
        st.session_state.incident_db = parsed_records
    except FileNotFoundError:
        st.session_state.incident_db = [
            {
                "id": 1,
                "type": "Flash Flood",
                "district": "Global Data Fallback",
                "lat": 41.8885,
                "lon": -87.6234,
                "status": "CRITICAL",
                "pop_affected": 2400,
                "time": "Offline Mode",
                "details": "Please drop your kaggle_disasters.csv inside the project folder to populate live records.",
            }
        ]

if "personnel_deployed" not in st.session_state:
    st.session_state.personnel_deployed = 82

# 5. Sidebar Interaction Panel
with st.sidebar:
    st.header("📝 CivicSense")

    input_type = st.selectbox(
        "Disaster Type",
        ["Flash Flood", "Structure Fire", "Hazardous Leak", "Power Grid Failure"],
    )
    input_district = st.text_input("Incident Location Area", "West Loop Area")
    input_pop = st.number_input(
        "Estimated Impact (Citizens)", min_value=10, max_value=50000, value=500, step=50
    )
    input_status = st.radio("Threat Priority", ["CRITICAL", "ACTIVE"])
    input_details = st.text_area(
        "Field Situation Raw Text Log",
        "Water levels entering underground utility lines rapidly.",
    )

    # Extract reference center tracking points to inject relative new pins seamlessly
    ref_lat = sum(item["lat"] for item in st.session_state.incident_db) / len(
        st.session_state.incident_db
    )
    ref_lon = sum(item["lon"] for item in st.session_state.incident_db) / len(
        st.session_state.incident_db
    )

    if st.button("🚨 Broadcast Dispatch Alert", use_container_width=True):
        new_alert = {
            "id": len(st.session_state.incident_db) + 1,
            "type": input_type,
            "district": input_district,
            "lat": ref_lat + random.uniform(-0.04, 0.04),
            "lon": ref_lon + random.uniform(-0.04, 0.04),
            "status": input_status,
            "pop_affected": input_pop,
            "time": "Just Now",
            "details": input_details,
        }
        st.session_state.incident_db.append(new_alert)
        st.toast("Dispatched and logged into dynamic system storage!", icon="🔥")
        st.rerun()

# 6. Time Status Header
now = datetime.datetime.now()
st.markdown(
    f"""
    <div class="header-container">
        <div>
            <span style="font-size: 22px; font-weight: bold; letter-spacing: 0.5px;">📊 CivicSense AI</span><br>
            <span class="status-indicator">● LIVE KAGGLER ENGINE INITIALIZED</span>
        </div>
        <div style="text-align: right; color: #AAAAAA; font-family: monospace;">
            {now.strftime('%H:%M')} | {now.strftime('%b %d').upper()}
        </div>
    </div>
""",
    unsafe_allow_html=True,
)
st.write("")

# 7. DYNAMIC MAP ADAPTER CALCULATIONS (Centers completely on dataset boundaries)
all_lats = [float(incident["lat"]) for incident in st.session_state.incident_db]
all_lons = [float(incident["lon"]) for incident in st.session_state.incident_db]

avg_lat = sum(all_lats) / len(all_lats) if all_lats else 41.8781
avg_lon = sum(all_lons) / len(all_lons) if all_lons else -87.6298

# Intelligently configure zoom tracking: zoom in close if localized, zoom far out if items cross countries
lat_spread = max(all_lats) - min(all_lats) if all_lats else 0
dynamic_zoom = 2 if lat_spread > 5 else (12 if lat_spread < 0.1 else 5)

m = folium.Map(
    location=[avg_lat, avg_lon],
    zoom_start=dynamic_zoom,
    tiles="CartoDB dark_matter",
    zoom_control=True,
)

for incident in st.session_state.incident_db:
    marker_color = "#FF3333" if incident["status"] == "CRITICAL" else "#FFA500"
    folium.CircleMarker(
        location=[float(incident["lat"]), float(incident["lon"])],
        radius=9,
        color=marker_color,
        fill=True,
        fill_color=marker_color,
        fill_opacity=0.6,
        popup=f"{incident['type']} - {incident['district']}",
    ).add_to(m)

st_folium(m, width=700, height=320, key="main_map", returned_objects=[])
st.write("")

# 8. Interactive Drill-Down Inspector Window
if st.session_state.selected_incident_id is not None:
    selected_target = next(
        (
            item
            for item in st.session_state.incident_db
            if item["id"] == st.session_state.selected_incident_id
        ),
        None,
    )
    if selected_target:
        st.markdown(
            f"""
            <div class="inspector-box">
                <span style="float:right; color:#AAAAAA; font-size:12px;">ID: #{selected_target['id']}</span>
                <h3 style="margin-top:0; color:#00E676;">🔍 Operational Incident Inspector</h3>
                <hr style="border-color:#2A2A30; margin:10px 0;">
                <p><strong>Disaster Type:</strong> {selected_target['type']}</p>
                <p><strong>Operational Impact Zone Location:</strong> {selected_target['district']}</p>
                <p><strong>Estimated Affected Footprint:</strong> {selected_target['pop_affected']:,} Citizens</p>
                <p><strong>Raw Narrative Log:</strong> {selected_target['details']}</p>
                <p style="margin-bottom:0; font-size:11px; color:#AAAAAA;">Coordinates: Latitude {selected_target['lat']:.4f} | Longitude {selected_target['lon']:.4f}</p>
            </div>
        """,
            unsafe_allow_html=True,
        )
        if st.button("❌ Close Inspector Window", use_container_width=True):
            st.session_state.selected_incident_id = None
            st.rerun()

# 9. Dynamic Dashboard KPI Calculations
active_count = len(st.session_state.incident_db)
total_pop = sum(int(item["pop_affected"]) for item in st.session_state.incident_db)
pop_str = f"{total_pop/1000:.1f}k" if total_pop >= 1000 else str(total_pop)

col1, col2, col3 = st.columns(3)
col1.markdown(
    f'<div class="kpi-box"><div class="kpi-label">Active Incidents</div><div class="kpi-val" style="color: #FF3333;">{active_count}</div></div>',
    unsafe_allow_html=True,
)
col2.markdown(
    f'<div class="kpi-box"><div class="kpi-label">Personnel</div><div class="kpi-val" style="color: #00E676;">{st.session_state.personnel_deployed} <span style="font-size:14px; color:#AAAAAA;">/ 150</span></div></div>',
    unsafe_allow_html=True,
)
col3.markdown(
    f'<div class="kpi-box"><div class="kpi-label">Affected Pop</div><div class="kpi-val" style="color: #FFA500;">{pop_str} <span style="font-size:10px; color:#AAAAAA;"><br>DYNAMIC</span></div></div>',
    unsafe_allow_html=True,
)
st.write("")

# 10. Chronological Activity Log
st.markdown("### 🚨 LIVE OPERATIONS FEED & AI ANALYSIS")
st.caption(
    "💡 Click the text button inside any item box row to review drill-down inspector data sheets."
)

for incident in reversed(st.session_state.incident_db):
    b_color = "#FF3333" if incident["status"] == "CRITICAL" else "#FFA500"

    if ai_commander:
        prompt = f"Analyze event: {incident['type']} in {incident['district']}. Context: {incident['details']}. Task: Return a 1-sentence urgent crisis advice response."
        output = ai_commander(prompt, max_length=50, do_sample=False)
        ai_response = output[0]["generated_text"]
    else:
        ai_response = "Dispatch standard response vectors and secure incident zone checkpoints immediately."

    st.markdown(
        f"""
        <div class="incident-card-critical" style="border-left: 5px solid {b_color}; margin-bottom: 5px;">
            <span class="badge-status" style="background-color: {b_color};">{incident['status']}</span>
            <span class="time-elapsed">{incident['time']}</span>
            <h4 style="margin: 8px 0 4px 0; color: white;">{incident['type']} — {incident['district']}</h4>
            <p style="margin: 0; color: #DDDDDD; font-size: 14px;">{incident['details']}</p>
            <div class="ai-analysis-box">
                <strong>🤖 AI CRISIS SUMMARY:</strong><br>
                <span style="color: #00E676;">{ai_response}</span>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    if st.button(
        f"🔍 Inspect Logistic Sheet — {incident['type']} ({incident['district']})",
        key=f"inspect_{incident['id']}",
        use_container_width=True,
    ):
        st.session_state.selected_incident_id = incident["id"]
        st.rerun()
    st.write("")

# 11. Operational Unit Deployment Trigger
if st.button("🚨 REPLOY EMERGENCY RESPONSE PERSONNEL", use_container_width=True):
    st.session_state.personnel_deployed += 8
    st.toast("Dispatched +8 Emergency Response units.", icon="🚒")
    st.rerun()

# 12. Layout Structural Footer Row
st.write("---")
f1, f2, f3, f4 = st.columns(4)
f1.caption("🔴 Operational Stream")
f2.caption("⚠️ Incident Map")
f3.caption("👥 Units Assigned")
f4.caption("⚙️ AI Config")
