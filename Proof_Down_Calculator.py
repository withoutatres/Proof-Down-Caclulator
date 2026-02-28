import streamlit as st

OZ_TO_ML = 29.5735

# ---------- TITLE ----------
st.title("Proof Down Calculator by Without a Tres")

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
    "Obtainium (151 proof)": 151,
    "ALW (140 proof)": 140,
    "Two Souls Bourbon (137 proof)": 137,
    "Augusta Old Route 8 (135 proof)": 135,
    "Old Bones Rye (133 proof)": 133,
    "OFSBBP Rye (130 proof)": 130,
    "Two Souls Pumpernickel (127 proof)": 127,
    "Bookers (~122 proof)": 122,
    "Bottled in Bond (100 proof)": 100,
}

preset_choice = st.selectbox("Preset Menu", presets.keys())

# ---------- POUR SIZE ----------
pour_size = st.number_input(
    f"Pour Size ({unit})",
    min_value=0.0,
    value=1.0 if unit == "oz" else 30.0
)

pour_size_oz = pour_size if unit == "oz" else pour_size / OZ_TO_ML

# ---------- STRENGTH INPUTS ----------
if strength_mode == "Proof":
    default_start = presets[preset_choice] if presets[preset_choice] else 130
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
        value=110
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

    water_display = water_oz if unit == "oz" else water_ml

    st.subheader("Results")
    st.write(f"Add **{water_display:.2f} {unit}** of water")

    # ---------- VISUAL INDICATOR ----------
    final_abv = desired_strength / 2
    water_pct = 100 - final_abv

    import pandas as pd

    composition_df = pd.DataFrame({
        "Component": ["Alcohol Content", "Water Content"],
        "Percentage": [final_abv, water_pct]
    })

    st.subheader("Final Composition")

    st.bar_chart(
        composition_df.set_index("Component")
    )



    # ---------- DETAILS ----------
    with st.expander("Back of the Envelope"):
        st.write(f"Starting ABV: {starting_abv * 100:.2f}%")
        st.write(f"Desired ABV: {desired_abv * 100:.2f}%")
        st.write(f"Pure Alcohol: {alcohol_oz:.3f} oz")
        st.write(f"Final Volume: {final_volume_oz:.2f} oz")

# ---------- DISCLAIMER ----------
st.markdown("---")
st.caption(
    "This calculator provides estimates for informational and entertainment purposes only. "
    "Results may vary based on measurement accuracy and conditions. "
    "Please drink responsibly 🥃"
)
