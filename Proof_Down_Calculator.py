import streamlit as st

OZ_TO_ML = 29.5735

st.title("Proof Down Calculator")

# Inputs
pour_size_oz = st.number_input("Pour Size (oz)", min_value=0.0, value=1.0)
starting_proof = st.number_input("Starting Proof", min_value=0.0, value=135.0)
desired_proof = st.number_input("Desired Proof", min_value=0.0, value=80.0)

if desired_proof >= starting_proof:
    st.error("Desired proof must be lower than starting proof.")
elif pour_size_oz <= 0:
    st.error("Pour size must be greater than zero.")
else:
    # Convert proof to ABV
    starting_abv = starting_proof / 2 / 100
    desired_abv = desired_proof / 2 / 100

    # Alcohol content (constant)
    alcohol_oz = pour_size_oz * starting_abv

    # Final volume needed
    final_volume_oz = alcohol_oz / desired_abv

    # Water to add
    water_oz = final_volume_oz - pour_size_oz
    water_ml = water_oz * OZ_TO_ML

    st.subheader("Results")
    st.write(f"Add this much water: **{water_oz:.2f} oz**")
    st.write(f"OR add this much water: **{water_ml:.2f} mL**")

    with st.expander("Back of the Envelope"):
        st.write(f"Starting Proof ABV: {starting_abv * 100:.2f}%")
        st.write(f"Desired Proof ABV: {desired_abv * 100:.2f}%")
        st.write(f"Total Alcohol: {alcohol_oz:.3f} oz")
        st.write(f"Total Volume Needed: {final_volume_oz:.2f} oz")