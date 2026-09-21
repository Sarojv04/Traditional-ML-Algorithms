import numpy as np
import plotly.graph_objects as go
import streamlit as st
from scipy.stats import norm

st.set_page_config(page_title="Normal Distribution Visualizer", layout="wide")

# Sidebar

st.sidebar.title("Controls")
page = st.sidebar.selectbox("Navigation", ["Normal Distribution", "About"])

X_MIN, X_MAX = -10, 10


def normal_distribution_page():
    st.title("How Mean and Standard Deviation Shape a Normal Distribution")

    mean = st.sidebar.slider("Mean", -10.0, 10.0, -3.0, 0.1)
    std = st.sidebar.slider("Standard Deviation", 0.1, 5.0, 3.1, 0.1)
    show_pdf = st.sidebar.checkbox("PDF curve", value=True)
    show_hist = st.sidebar.checkbox("Histogram", value=True)
    bin_size = st.sidebar.number_input(
        "Bin Size", min_value=0.05, max_value=2.0, value=0.6, step=0.05
    )
    n_samples = st.sidebar.number_input(
        "Sample size", min_value=100, max_value=100_000, value=5_000, step=500
    )

    # Fixed seed -> histogram doesn't "jump" randomly on every slider move
    rng = np.random.default_rng(42)
    base_z = rng.standard_normal(int(n_samples))

    # Reference: standard normal N(0, 1)
    ref_mean, ref_std = 0.0, 1.0
    ref_samples = ref_mean + ref_std * base_z

    # Custom: N(mean, std). Reusing the same z-scores makes it visually clear
    # that mean = shift and std = stretch of the very same shape.
    samples = mean + std * base_z

    x = np.linspace(X_MIN, X_MAX, 800)

    fig = go.Figure()

    BLUE = "#4C9BE8"
    ORANGE = "#F28E2B"

    if show_hist:
        for data, name, color in [
            (ref_samples, "Reference N(0, 1)", BLUE),
            (samples, f"N({mean:.1f}, {std:.1f})", ORANGE),
        ]:
            fig.add_trace(
                go.Histogram(
                    x=data,
                    histnorm="probability density",
                    xbins=dict(start=X_MIN, end=X_MAX, size=bin_size),
                    name=name,
                    marker_color=color,
                    opacity=0.6,
                    legendgroup=name,
                )
            )

    if show_pdf:
        for m, s, name, color in [
            (ref_mean, ref_std, "Reference N(0, 1)", BLUE),
            (mean, std, f"N({mean:.1f}, {std:.1f})", ORANGE),
        ]:
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=norm.pdf(x, m, s),
                    mode="lines",
                    name=name + " PDF",
                    line=dict(color=color, width=2),
                    legendgroup=name,
                    showlegend=not show_hist,
                )
            )

    # Vertical line at the chosen mean
    fig.add_vline(x=mean, line=dict(color=ORANGE, dash="dash", width=1))

    fig.update_layout(
        barmode="overlay",
        template="plotly_dark",
        height=550,
        xaxis=dict(range=[X_MIN, X_MAX], title="x"),
        yaxis=dict(title="Density"),
        legend=dict(orientation="h", y=1.08),
        margin=dict(l=20, r=20, t=40, b=20),
    )

    st.plotly_chart(fig, width="stretch")

  
    # Stats + interpretation
   
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Mean (μ)", f"{mean:.2f}")
    c2.metric("Std Dev (σ)", f"{std:.2f}")
    c3.metric("Variance (σ²)", f"{std**2:.2f}")
    c4.metric("Peak height", f"{norm.pdf(mean, mean, std):.3f}")

    st.markdown("#### What you're seeing")
    st.markdown(
        f"""
- **Mean (μ = {mean:.1f})** slides the curve left/right. It only changes *where* the center sits, not the shape.
- **Standard deviation (σ = {std:.1f})** stretches the curve. Larger σ gives a wider, flatter bell; smaller σ gives a narrow, tall one.
- The total area under every curve is always **1**, so when the curve gets wider it must get shorter.
- **68-95-99.7 rule** for this curve:
  - 68% of values fall in **[{mean - std:.2f}, {mean + std:.2f}]**
  - 95% fall in **[{mean - 2*std:.2f}, {mean + 2*std:.2f}]**
  - 99.7% fall in **[{mean - 3*std:.2f}, {mean + 3*std:.2f}]**
"""
    )


def about_page():
    st.title("About this app")
    st.markdown(
        r"""
This app shows how the two main parameters of a normal distribution work: **Mean** and **Standard Deviation (SD)**.

**What you're seeing:**
The blue and orange curves update as you move the sliders. The app shows whether your curve is wider or narrower than the blue curve and gives the range where about **99.7% of the values** fall.

### Try these five steps:

1. **Move only the Mean** and watch the curve move left or right.
2. **Move only the SD** and watch the curve become wider or narrower.
3. **Set SD to 0.1** and see how the curve becomes very tall and narrow.
4. **Set SD to 5** and see how the curve becomes much wider and flatter.
5. **Change the Bin Size** and see how the histogram becomes more or less jagged or blocky.

"""
    )


if page == "Normal Distribution":
    normal_distribution_page()
else:
    about_page()