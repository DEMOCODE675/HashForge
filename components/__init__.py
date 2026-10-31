"""UI Component library for HashForge."""

from components.sidebar import render_sidebar, load_css
from components.metric_cards import render_metric_card, render_metric_row
from components.bit_visualizer import render_bit_grid, render_bit_diff_matrix
from components.hash_display import render_hash_card, render_copyable_hash
from components.comparison import render_comparison_summary
from components.charts import (
    create_avalanche_histogram,
    create_trial_timeline_chart,
    create_algorithm_comparison_chart,
)

__all__ = [
    "render_sidebar",
    "load_css",
    "render_metric_card",
    "render_metric_row",
    "render_bit_grid",
    "render_bit_diff_matrix",
    "render_hash_card",
    "render_copyable_hash",
    "render_comparison_summary",
    "create_avalanche_histogram",
    "create_trial_timeline_chart",
    "create_algorithm_comparison_chart",
]

