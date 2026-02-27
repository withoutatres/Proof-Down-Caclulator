import streamlit as st

OZ_TO_ML = 29.5735

st.title("Proof Down Calculator")

# ---------- INPUT MODE ----------
strength_mode = st.radio(
    "Alcohol Strength Input",
    ["Proof", "ABV (%)"],
    horizontal=True
)

unit = st.selectbox(
    "Volume Units",
    ["oz", "mL"]
)

# ---------- PRESETS ----------
presets = {
    "— None —": None,
    "Barrel Proof Bourbon (~130 proof)": 130,
    "Navy Strength (~114 proof)": 114,
    "Overproof Rum (151 proof)": 151,
    "Neutral Spirit (190 proof)": 190,
}

preset_choice = st.selectbox("Preset Spirit", presets.keys())

# ---------- POUR SIZE ----------
pour_size = st.number_input(
    f"Pour Size ({unit})",
    min_value=0.0,
    value=1.0 if unit == "oz" else 30.0
)

# Convert pour size to oz internally
pour_size_oz = pour_size if unit == "oz" else pour_size / OZ_TO_ML

# ---------- STRENGTH INPUTS ----------
if strength_mode == "Proof":
    default_start = presets[preset_choice] if presets[preset_choice] else 135
    starting_strength = st.number_input(
        "Starting Proof",
        min_value=0,
        step=1,
        value=default_start
    )
    desired_strength = st.number_input(
        "Desired Proof",
        min_value=0,
        step=1,
        value=80
    )

    starting_abv = starting_strength / 2 / 100
    desired_abv = desired_strength / 2 / 100

else:
    starting_strength = st.number_input(
        "Starting ABV (%)",
        min_value=0.0,
        max_value=100.0,
        value=67.5
    )
    desired_strength = st.number_input(
        "Desired ABV (%)",
        min_value=0.0,
        max_value=100.0,
        value=40.0
    )

    starting_abv = starting_strength / 100
    desired_abv = desired_strength / 100

# ---------- CALCULATION ----------
if desired_abv >= starting_abv:
    st.error("Desired strength must be lower than starting strength.")
elif pour_size_oz <= 0:
    st.error("Pour size must be greater than zero.")
else:
    alcohol_oz = pour_size_oz * starting_abv
    final_volume_oz = alcohol_oz / desired_abv
    water_oz = final_volume_oz - pour_size_oz
    water_ml = water_oz * OZ_TO_ML

    # Display results in selected unit
    water_display = water_oz if unit == "oz" else water_ml

    st.subheader("Results")
    st.write(
        f"Add **{water_display:.2f} {unit}** of water"
    )

    # ---------- VISUAL INDICATOR ----------
    water_fraction = water_oz / final_volume_oz
    alcohol_fraction = alcohol_oz / final_volume_oz

    st.subheader("Final Mixture")
    st.write("Alcohol")
    st.progress(alcohol_fraction)

    st.write("Water")
    st.progress(water_fraction)

    # ---------- DETAILS ----------
    with st.expander("Back of the Envelope"):
        st.write(f"Starting ABV: {starting_abv * 100:.2f}%")
        st.write(f"Desired ABV: {desired_abv * 100:.2f}%")
        st.write(f"Pure Alcohol: {alcohol_oz:.3f} oz")
        st.write(f"Final Volume: {final_volume_oz:.2f} oz")

# ---------- DISCLAIMER ----------
st.markdown("---")
st.caption(
    "This calculator provides estimates for information and entertainment purposes only."
)
