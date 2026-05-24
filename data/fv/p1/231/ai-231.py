import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Argument and File Handling ---
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# --- 2. Data and Configuration Extraction ---
data_series = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', {})
layout_options = chart_data.get('layout_options', {})
style_options = chart_data.get('style_options', {})

# --- 3. Chart Creation ---
fig = go.Figure()

# Add data traces
series_colors = colors.get('series_colors', [])
line_widths = style_options.get('line_widths', [])

for i, series in enumerate(data_series):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines',
        name=series.get('name', ''),
        line=dict(
            color=series_colors[i] if i < len(series_colors) else None,
            width=line_widths[i] if i < len(line_widths) else 2
        )
    ))

# --- 4. Layout Configuration ---
title_str = texts.get('title', '')
subtitle_str = texts.get('subtitle', '')
full_title = f"{title_str}<br><sub>{subtitle_str}</sub>" if subtitle_str else title_str

fig.update_layout(
    title=dict(
        text=full_title,
        x=0.05,
        xanchor='left'
    ),
    plot_bgcolor=colors.get('background_color', '#FFFFFF'),
    paper_bgcolor=colors.get('background_color', '#FFFFFF'),
    font=dict(
        family="Arial",
        size=12,
        color=colors.get('text_color', '#000000')
    ),
    showlegend=False,
    margin=dict(t=50, r=25, b=50, l=50),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        range=layout_options.get('x_axis_range'),
        tickvals=layout_options.get('x_axis_ticks'),
        showline=True,
        linewidth=1,
        linecolor=colors.get('axis_color'),
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=layout_options.get('y_axis_range'),
        tickvals=layout_options.get('y_axis_ticks'),
        showline=True,
        linewidth=1,
        linecolor=colors.get('axis_color'),
        showgrid=False,
        zeroline=False
    )
)

# --- 5. Output ---
output_path = json_path.with_suffix('.png')
fig.write_image(output_path, scale=2)
print(f"Chart saved to {output_path}")