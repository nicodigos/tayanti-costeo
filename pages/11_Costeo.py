import streamlit as st
import pandas as pd
from repos import costeo_repo

st.title("Costeo")

rows = costeo_repo.list_all()

if not rows:
    st.info("No cost data available.")
else:
    df = pd.DataFrame(rows)

    # optional formatting
    df["costo_total"] = df["costo_total"].astype(float).round(2)
    df["costo_unitario"] = df["costo_unitario"].astype(float).round(4)

    st.subheader("Costo por receta")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
