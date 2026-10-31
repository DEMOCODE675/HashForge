"""Interactive 256-bit visualizer with changed-bit highlighting and grouped layout."""

from typing import List, Optional
import streamlit as st


def render_bit_grid(
    binary_str: str,
    diff_mask: Optional[List[bool]] = None,
    title: str = "Binary Digest View (256 Bits)",
    bits_per_row: int = 32,
    bits_per_group: int = 8,
) -> None:
    """Render a structured, color-coded grid of 256 bits grouped into bytes and rows.

    Args:
        binary_str: 256-character string of '0' and '1'.
        diff_mask: Optional list of booleans indicating which bits changed.
        title: Header label for visualizer.
        bits_per_row: Number of bits to display per row (default 32 bits = 4 bytes).
        bits_per_group: Grouping for byte spacing (default 8 bits = 1 byte).
    """
    total_bits = len(binary_str)

    html_rows = []
    for row_start in range(0, total_bits, bits_per_row):
        row_end = min(row_start + bits_per_row, total_bits)
        row_label = f"Bits {row_start:03d}–{row_end - 1:03d}"

        # Build groups of bytes
        byte_groups_html = []
        for g_start in range(row_start, row_end, bits_per_group):
            g_end = min(g_start + bits_per_group, row_end)
            bit_spans = []

            for bit_idx in range(g_start, g_end):
                bit_val = binary_str[bit_idx]
                is_changed = diff_mask[bit_idx] if diff_mask is not None and bit_idx < len(diff_mask) else False

                if is_changed:
                    css_cls = "hf-bit hf-bit-changed"
                    tooltip = f"Bit {bit_idx}: FLIPPED ({bit_val})"
                else:
                    css_cls = "hf-bit hf-bit-unchanged"
                    tooltip = f"Bit {bit_idx}: {bit_val}"

                bit_spans.append(f'<span class="{css_cls}" title="{tooltip}">{bit_val}</span>')

            byte_groups_html.append(f'<span class="hf-bit-byte-group">{"".join(bit_spans)}</span>')

        row_html = f"""
        <div class="hf-bit-row">
            <span class="hf-bit-row-label">{row_label}</span>
            <span>{"".join(byte_groups_html)}</span>
        </div>
        """
        html_rows.append(row_html)

    # Render complete container with legend
    legend_html = ""
    if diff_mask is not None:
        changed_count = sum(1 for m in diff_mask if m)
        unchanged_count = total_bits - changed_count
        legend_html = f"""
        <div style="display: flex; gap: 20px; font-size: 0.78rem; margin-bottom: 12px; color: #94A3B8;">
            <div style="display: flex; align-items: center; gap: 6px;">
                <span class="hf-bit hf-bit-unchanged" style="display:inline-block;">0</span>
                <span>Unchanged Bits ({unchanged_count})</span>
            </div>
            <div style="display: flex; align-items: center; gap: 6px;">
                <span class="hf-bit hf-bit-changed" style="display:inline-block;">1</span>
                <span>Flipped / Perturbed Bits ({changed_count})</span>
            </div>
        </div>
        """

    full_html = f"""
    <div class="hf-bit-grid-container">
        <div style="font-size: 0.82rem; font-weight: 700; color: #E2E8F0; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">
            {title}
        </div>
        {legend_html}
        <div>
            {"".join(html_rows)}
        </div>
    </div>
    """
    st.markdown(full_html, unsafe_allow_html=True)


def render_bit_diff_matrix(
    orig_bin: str,
    mod_bin: str,
    diff_mask: List[bool],
    title: str = "Bit-by-Bit Comparative Alignment",
) -> None:
    """Render original and modified binary streams in synchronized lockstep with diff flags."""
    render_bit_grid(
        mod_bin,
        diff_mask=diff_mask,
        title=f"{title} (Modified Hash with Highlighted Flips)",
    )

