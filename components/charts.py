"""Plotly interactive visualizations for HashForge experimental data."""

from typing import Any, Dict, List, Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def apply_dark_theme(fig: go.Figure) -> go.Figure:
    """Apply HashForge dark cyberpunk theme to a Plotly figure."""
    fig.update_layout(
        paper_bgcolor="#0B0F17",
        plot_bgcolor="#111827",
        font=dict(
            family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
            color="#F8FAFC",
            size=12,
        ),
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis=dict(
            gridcolor="#1F2937",
            zerolinecolor="#374151",
            linecolor="#1F2937",
        ),
        yaxis=dict(
            gridcolor="#1F2937",
            zerolinecolor="#374151",
            linecolor="#1F2937",
        ),
        legend=dict(
            bgcolor="rgba(17, 24, 39, 0.8)",
            bordercolor="#1F2937",
            borderwidth=1,
        ),
    )
    return fig


def create_avalanche_histogram(
    trials_df: pd.DataFrame,
    algorithm: str = "SHA-256",
    bin_size: float = 2.0,
) -> go.Figure:
    """Create an interactive histogram of avalanche percentage distribution.

    Args:
        trials_df: DataFrame containing 'avalanche_pct' column.
        algorithm: Algorithm name for chart title.
        bin_size: Histogram bin width.

    Returns:
        Plotly Figure.
    """
    mean_val = trials_df["avalanche_pct"].mean()

    fig = go.Figure()

    # Main histogram trace
    fig.add_trace(
        go.Histogram(
            x=trials_df["avalanche_pct"],
            xbins=dict(start=20.0, end=80.0, size=bin_size),
            marker=dict(
                color="#00F0FF",
                line=dict(color="#0B0F17", width=1),
                opacity=0.85,
            ),
            name=f"{algorithm} Trials",
            hovertemplate="Avalanche Range: %{x}%<br>Trial Count: %{y}<extra></extra>",
        )
    )

    # Theoretical 50% Reference Line
    fig.add_vline(
        x=50.0,
        line_width=2.5,
        line_dash="dash",
        line_color="#10B981",
        annotation_text="Theoretical Ideal (50%)",
        annotation_position="top left",
        annotation_font=dict(color="#10B981", size=11),
    )

    # Empirical Mean Line
    fig.add_vline(
        x=mean_val,
        line_width=2.0,
        line_dash="dot",
        line_color="#F59E0B",
        annotation_text=f"Empirical Mean ({mean_val:.2f}%)",
        annotation_position="top right",
        annotation_font=dict(color="#F59E0B", size=11),
    )

    fig.update_layout(
        title=f"<b>Avalanche Effect Distribution</b> — {algorithm} ({len(trials_df)} Trials)",
        xaxis_title="Avalanche Percentage (%)",
        yaxis_title="Trial Frequency",
        bargap=0.08,
    )

    return apply_dark_theme(fig)


def create_trial_timeline_chart(
    trials_df: pd.DataFrame,
    algorithm: str = "SHA-256",
) -> go.Figure:
    """Create a trial-by-trial scatter/line plot of avalanche percentages.

    Args:
        trials_df: DataFrame containing 'trial' and 'avalanche_pct'.
        algorithm: Algorithm name.

    Returns:
        Plotly Figure.
    """
    fig = go.Figure()

    # 50% baseline reference
    fig.add_hline(
        y=50.0,
        line_width=2.0,
        line_dash="dash",
        line_color="#10B981",
        annotation_text="50% Strict Avalanche Reference",
        annotation_position="bottom right",
        annotation_font=dict(color="#10B981", size=11),
    )

    # Trial points and connecting line
    fig.add_trace(
        go.Scatter(
            x=trials_df["trial"],
            y=trials_df["avalanche_pct"],
            mode="lines+markers",
            name=f"{algorithm} Avalanche",
            line=dict(color="#00F0FF", width=1.5),
            marker=dict(
                size=6,
                color="#00F0FF",
                symbol="circle",
                line=dict(color="#111827", width=1),
            ),
            customdata=trials_df[["bit_index", "hamming_distance"]],
            hovertemplate=(
                "<b>Trial #%{x}</b><br>"
                "Bit Flipped: %{customdata[0]}<br>"
                "Hamming Distance: %{customdata[1]} / 256<br>"
                "Avalanche: <b>%{y:.2f}%</b><extra></extra>"
            ),
        )
    )

    fig.update_layout(
        title=f"<b>Trial-by-Trial Avalanche Dispersion</b> — {algorithm}",
        xaxis_title="Trial Number",
        yaxis_title="Avalanche Percentage (%)",
        yaxis=dict(range=[20, 80]),
    )

    return apply_dark_theme(fig)


def create_algorithm_comparison_chart(
    df_sha256: pd.DataFrame,
    df_sha3: pd.DataFrame,
) -> go.Figure:
    """Create a dual-distribution comparison chart comparing SHA-256 and SHA3-256."""
    fig = go.Figure()

    fig.add_trace(
        go.Box(
            y=df_sha256["avalanche_pct"],
            name="SHA-256",
            marker_color="#00F0FF",
            boxpoints="outliers",
        )
    )

    fig.add_trace(
        go.Box(
            y=df_sha3["avalanche_pct"],
            name="SHA3-256",
            marker_color="#10B981",
            boxpoints="outliers",
        )
    )

    fig.add_hline(
        y=50.0,
        line_width=2.0,
        line_dash="dash",
        line_color="#F59E0B",
        annotation_text="Ideal 50%",
        annotation_position="bottom right",
    )

    fig.update_layout(
        title="<b>Statistical Avalanche Dispersion Comparison</b> (SHA-256 vs SHA3-256)",
        yaxis_title="Avalanche Percentage (%)",
        yaxis=dict(range=[20, 80]),
    )

    return apply_dark_theme(fig)

