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
        value=125.0,
        step=0.1,
        format="%.1f"
    )

desired_proof = st.number_input(
    "Desired Proof (whole number)",
    min_value=40,
    max_value=int(starting_proof),
    value=105,
    step=1
)

mode = st.radio("Measurement Mode", ["Volume Mode", "Weight Mode"])

# -----------------------------
# CONSTANTS
# -----------------------------
ETHANOL_DENSITY = 0.789
WATER_DENSITY = 1.0
ML_PER_OZ = 29.5735

starting_abv = starting_proof / 200
desired_abv = desired_proof / 200

# -----------------------------
# CALCULATIONS
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

# -----------------------------
# ROUNDING
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
# RESULTS CARD
# -----------------------------
st.markdown("---")
st.subheader("💧 Water to Add")

st.markdown(f"""
<div style="
    background-color:#fbe9d0;
    padding:25px;
    border-radius:14px;
    border:2px solid #d9a441;
    text-align:center;
    color:#3e2c1c;
    box-shadow:0 4px 10px rgba(0,0,0,0.08);
">
    <div style="font-size:32px; font-weight:700;">
        {water_oz:.2f} oz &nbsp;/&nbsp; {water_ml:.1f} ml
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# FINAL COMPOSITION BAR (FIXED)
# Use a table instead of flexbox — renders reliably in Streamlit markdown
# -----------------------------
st.subheader("Final Composition")

final_abv_percent = round(desired_abv * 100, 1)
water_percent = round(100 - final_abv_percent, 1)

st.markdown(f"""
<table style="width:100%; border-collapse:collapse; border-radius:12px; overflow:hidden; height:42px;">
  <tr>
    <td style="
        width:{final_abv_percent}%;
        background-color:#8B4513;
        text-align:center;
        vertical-align:middle;
        color:white;
        font-weight:bold;
        font-size:14px;
        padding:0;
    ">
        {final_abv_percent:.0f}% Alcohol
    </td>
    <td style="
        width:{water_percent}%;
        background-color:#4F81BD;
        text-align:center;
        vertical-align:middle;
        color:white;
        font-weight:bold;
        font-size:14px;
        padding:0;
    ">
        {water_percent:.0f}% Water
    </td>
  </tr>
</table>
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
