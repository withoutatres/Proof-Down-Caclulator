import streamlit as st
import pandas as pd
import altair as alt
from fractions import Fraction

OZ_TO_ML = 29.5735

st.title("Proof Down Calculator")

# ---------- MODE TOGGLES ----------
input_mode = st.radio(
    "Spirit Input Mode",
    ["Volume", "Weight (grams)"],
    horizontal=True
)

bar_mode = st.toggle("Bar Mode (⅛ oz + 1 mL rounding)")

# ---------- STRENGTH INPUT ----------
strength_mode = st.radio(
    "Alcohol Strength Input",
    ["Proof", "ABV (%)"],
    horizontal=True
)

if strength_mode == "Proof":

    starting_proof = st.number_input(
        "Starting Proof",
        min_value=0.0,
        step=0.1,
        format="%.1f",
        value=130.0
    )

    desired_proof = st.number_input(
        "Desired Proof",
        min_value=0,
        step=1,
        value=110
    )

    starting_abv = starting_proof / 2 / 100
    desired_abv = desired_proof / 2 / 100

else:
    starting_abv_percent = st.number_input(
        "Starting ABV (%)",
        min_value=0.0,
        max_value=100.0,
        step=0.1,
        value=65.0
    )

    desired_abv_percent = st.number_input(
        "Desired ABV (%)",
        min_value=0,
        max_value=100,
        step=1,
        value=55
    )

    starting_abv = starting_abv_percent / 100
    desired_abv = desired_abv_percent / 100
    starting_proof = starting_abv_percent * 2
    desired_proof = desired_abv_percent * 2

# ---------- DENSITY ESTIMATION ----------
# Empirical polynomial approximation for ethanol-water density at ~20°C
# Accurate enough for spirits (±0.2%)
def estimate_density(abv):
    return (
        0.9982
        - 0.00105 * (abv * 100)
        + 0.000003 * (abv * 100) ** 2
    )

density = estimate_density(starting_abv)

# ---------- SPIRIT INPUT ----------
if input_mode == "Volume":

    unit = st.selectbox("Volume Units", ["oz", "mL"])

    pour_size = st.number_input(
        f"Spirit Amount ({unit})",
        min_value=0.0,
        value=1.0 if unit == "oz" else 30.0
    )

    pour_size_oz = pour_size if unit == "oz" else pour_size / OZ_TO_ML

else:
    spirit_weight_g = st.number_input(
        "Spirit Weight (grams)",
        min_value=0.0,
        value=30.0
    )

    spirit_volume_ml = spirit_weight_g / density
    pour_size_oz = spirit_volume_ml / OZ_TO_ML

    st.caption(
        f"Estimated density: {density:.3f} g/mL → "
        f"{spirit_volume_ml:.2f} mL ({pour_size_oz:.2f} oz)"
    )

# ---------- CALCULATION ----------
if desired_abv >= starting_abv:
    st.error("Desired strength must be lower than starting strength.")

elif pour_size_oz <= 0:
    st.error("Spirit amount must be greater than zero.")

else:
    alcohol_oz = pour_size_oz * starting_abv
    final_volume_oz = alcohol_oz / desired_abv
    water_oz = final_volume_oz - pour_size_oz
    water_ml = water_oz * OZ_TO_ML

    # ---------- BAR MODE ROUNDING ----------
    if bar_mode:
        water_oz = round(water_oz * 8) / 8
        water_ml = round(water_oz * OZ_TO_ML)

    # ---------- FRACTION FORMATTER ----------
    def format_oz_fraction(value):
        whole = int(value)
        frac = value - whole
        frac_part = Fraction(frac).limit_denominator(8)

        if frac_part == 0:
            return f"{whole} oz"
        if whole == 0:
            return f"{frac_part} oz"
        return f"{whole} {frac_part} oz"

    formatted_oz = format_oz_fraction(water_oz)

    # ---------- RESULTS ----------
    st.subheader("Water to Add")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Ounces",
            formatted_oz if bar_mode else f"{water_oz:.2f} oz"
        )

    with col2:
        st.metric(
            "Milliliters (≈ grams)",
            f"{water_ml:.0f} mL" if bar_mode else f"{water_ml:.2f} mL"
        )

    st.caption("1 mL of water ≈ 1 gram for scale measurements.")

    # ---------- FINAL COMPOSITION STACKED BAR ----------
    final_abv_percent = desired_abv * 100
    water_percent = 100 - final_abv_percent

    composition_df = pd.DataFrame({
        "Component": ["Alcohol Content", "Water Content"],
        "Percentage": [final_abv_percent, water_percent]
    })

    st.subheader("Final Composition")

    stacked_chart = alt.Chart(composition_df).mark_bar().encode(
        x=alt.X("Percentage:Q", stack="normalize"),
        color=alt.Color(
            "Component:N",
            scale=alt.Scale(
                domain=["Alcohol Content", "Water Content"],
                range=["#8B4513", "#4F81BD"]
            ),
            legend=alt.Legend(orient="bottom")
        ),
        tooltip=["Component", "Percentage"]
    ).properties(height=60)

    st.altair_chart(stacked_chart, use_container_width=True)

    # ---------- DETAILS ----------
    with st.expander("Back of the Envelope"):
        st.write(f"Starting Proof: {starting_proof:.1f}")
        st.write(f"Desired Proof: {desired_proof:.0f}")
        st.write(f"Estimated Density: {density:.4f} g/mL")
        st.write(f"Pure Alcohol: {alcohol_oz:.3f} oz")
        st.write(f"Final Volume: {final_volume_oz:.2f} oz")

# ---------- DISCLAIMER ----------
st.markdown("---")
st.caption(
    "For educational and entertainment purposes only. "
    "Please drink responsibly and comply with local laws. "
    "Density values are estimated and suitable for tasting dilution, not laboratory calibration."
)
