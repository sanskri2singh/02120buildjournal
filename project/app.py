"""Interactive carbon-cycle simulator.

Run from the repository root with:  streamlit run project/app.py
"""

import streamlit as st  # pyright: ignore[reportMissingImports]

import carbon

st.set_page_config(page_title="Volcanoes or Microbes?", layout="wide")

st.title("Volcanoes or Microbes?")
st.caption("Modeling the end-Permian carbon crisis · 02-120 final project")

# ---- Sidebar: model inputs ----
st.sidebar.header("Ocean")
Mi = st.sidebar.slider("Starting carbon (Mi)", 0.0, 10.0, 1.0, 0.1)
k = st.sidebar.slider("Burial rate constant (k)", 0.01, 1.0, 0.1, 0.01)

st.sidebar.header("Volcanic source")
volcanoes_on = st.sidebar.checkbox("Volcanoes on", value=True)
F = st.sidebar.slider("Volcanic input rate (F)", 0.0, 2.0, 0.5, 0.05, disabled=not volcanoes_on)
if not volcanoes_on:
    F = 0.0

st.sidebar.header("Microbial source")
st.sidebar.caption("Coming soon: Methanosarcina growth limited by nickel.")

st.sidebar.header("Simulation")
t_end = st.sidebar.slider("Run length (t_end)", 1.0, 100.0, 50.0, 1.0)
dt = st.sidebar.select_slider("Time step (dt)", options=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5], value=0.01)

# ---- Run the model ----
times, carbonamounts = carbon.simulate(Mi, F, k, t_end, dt)
exact = [carbon.exact_solution(t, Mi, F, k) for t in times]
growth = [carbon.findrate(F, k, M) for M in carbonamounts]
largest_gap = max(abs(e - M) for e, M in zip(exact, carbonamounts))

# ---- Summary numbers ----
col1, col2, col3 = st.columns(3)
col1.metric("Final carbon", f"{carbonamounts[-1]:.3f}")
col2.metric("Steady state (F/k)", f"{F / k:.3f}")
col3.metric("Largest gap from exact", f"{largest_gap:.2g}")

# ---- Plots ----
st.subheader("Ocean carbon over time")
st.line_chart(
    {"time": times, "simulated": carbonamounts, "exact": exact},
    x="time",
    y=["simulated", "exact"],
    x_label="time",
    y_label="ocean carbon (M)",
)

st.subheader("Growth rate (dM/dt)")
st.line_chart(
    {"time": times, "dM/dt": growth},
    x="time",
    y="dM/dt",
    x_label="time",
    y_label="dM/dt",
)
st.caption(
    "With a steady volcanic source, growth always slows down over time. "
    "Rothman et al. (2014) argue the end-Permian record shows growth speeding up, "
    "which needs a source that is itself growing, like a spreading microbe."
)

st.subheader("Carbon isotopes (δ13C)")
st.info("Coming soon: δ13C over time, to compare the fingerprints of volcanoes and microbes.")
