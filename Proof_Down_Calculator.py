import streamlit as st

st.set_page_config(page_title="Whiskey Proof Down Calculator", layout="centered")

st.title("🥃 Whiskey Proof Down Calculator")

# -----------------------------
# PRESET WHISKEY LEVELS
# -----------------------------
preset = st.selectbox(
    "Preset Starting Proof",
    [
        "Custom",
        "Bottled in Bond (100)",
        "Barrel Proof (120)",
        "High Barrel Proof (130)",
        "Hazmat (140+)"
    ]
)

if preset == "Bottled in Bond (100)":
    starting_proof = 100.0
elif preset == "Barrel Proof (120)":
    starting_proof = 120.0
elif preset == "High Barrel Proof (130)":
    starting_proof = 130.0
elif preset == "Hazmat (140+)":
    starting_proof = 140.0
else:
    starting_proof = st.number_input(
        "Starting Proof",
        min_value=40.0,
        max_value=200.0,
        value=120.0,
        step=0.1,
        format="%.1f"
    )

desired_proof = st.number_input(
    "Desired Proof (whole number)",
    min_value=40,
    max_value=int(starting_proof),
    value=100,
    step=1
)

mode = st.radio("Measurement Mode", ["Volume Mode", "Weight Mode"])

# -----------------------------
# CONSTANTS
# -----------------------------
ETHANOL_DENSITY = 0.789  # g/ml
WATER_DENSITY = 1.0      # g/ml
ML_PER_OZ = 29.5735

starting_abv = starting_proof / 200
desired_abv = desired_proof / 200

# -----------------------------
# VOLUME MODE
# -----------------------------
if mode == "Volume Mode":

    pour_size = st.number_input(
        "Pour Size (oz)",
        min_value=0.1,
        value=1.0,
        step=0.1
    )

    alcohol_oz = pour_size * starting_abv
    total_volume_needed = alcohol_oz / desired_abv
    water_oz = total_volume_needed - pour_size
    water_ml = water_oz * ML_PER_OZ
    water_g = water_ml * WATER_DENSITY

# -----------------------------
# WEIGHT MODE
# -----------------------------
else:

    spirit_weight_g = st.number_input(
        "Weight of Spirit (grams)",
        min_value=1.0,
        value=30.0,
        step=1.0
    )

    spirit_ml = spirit_weight_g / (
        (starting_abv * ETHANOL_DENSITY) +
        ((1 - starting_abv) * WATER_DENSITY)
    )

    alcohol_ml = spirit_ml * starting_abv
    total_volume_needed = alcohol_ml / desired_abv
    water_ml = total_volume_needed - spirit_ml
    water_oz = water_ml / ML_PER_OZ
    water_g = water_ml * WATER_DENSITY

# -----------------------------
# ROUNDING TOGGLE
# -----------------------------
round_mode = st.selectbox(
    "Bar Mode Rounding",
    ["Exact", "Nearest 1/4 oz", "Nearest 1/8 oz"]
)

if round_mode == "Nearest 1/4 oz":
    water_oz = round(water_oz * 4) / 4
elif round_mode == "Nearest 1/8 oz":
    water_oz = round(water_oz * 8) / 8

water_ml = water_oz * ML_PER_OZ
water_g = water_ml * WATER_DENSITY

# -----------------------------
# RESULTS
# -----------------------------
st.markdown("---")
st.subheader("💧 Water to Add")

st.markdown(f"""
<div style="
    background-color:#fff4e6;
    padding:20px;
    border-radius:12px;
    border:2px solid #ffcc80;
    text-align:center;
">
    <div style="font-size:28px; font-weight:bold;">
        {water_oz:.2f} oz
    </div>
    <div style="font-size:18px;">
        {water_ml:.1f} ml
    </div>
    <div style="font-size:18px;">
        {water_g:.1f} grams
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# FINAL COMPOSITION BAR
# -----------------------------
st.subheader("Final Composition")

final_abv_percent = desired_abv * 100
water_percent = 100 - final_abv_percent

st.markdown(f"""
<div style="
    width:100%;
    height:40px;
    border-radius:10px;
    overflow:hidden;
    display:flex;
    font-weight:bold;
    color:white;
    text-align:center;
">

    <div style="
        width:{final_abv_percent}%;
        background-color:#8B4513;
        display:flex;
        align-items:center;
        justify-content:center;
    ">
        Alcohol {final_abv_percent:.0f}%
    </div>

    <div style="
        width:{water_percent}%;
        background-color:#4F81BD;
        display:flex;
        align-items:center;
        justify-content:center;
    ">
        Water {water_percent:.0f}%
    </div>

</div>
""", unsafe_allow_html=True)

# -----------------------------
# DISCLAIMER
# -----------------------------
st.markdown("---")
st.caption(
    "This calculator provides estimates for informational and entertainment purposes only. "
    "Results are approximate and not laboratory-grade measurements. "
    "Please drink responsibly and comply with all applicable laws."
)
