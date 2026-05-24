import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load Data from JSON ---
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_json = json.load(f)

# --- 2. Extract Data and Configuration ---
chart_data = chart_json.get('chart_data', {})
texts = chart_json.get('texts', {})
colors = chart_json.get('colors', [])
bar_border_color = chart_json.get('bar_border_color', '#000000')

categories = chart_data.get('categories', [])
series_list = chart_data.get('series', [])

# --- 3. Create the Chart Figure ---
fig = go.Figure()

# --- 4. Add Bar Traces ---
# The data is structured for potential multiple series, so we iterate
for i, series in enumerate(series_list):
    fig.add_trace(go.Bar(
        x=categories,
        y=series.get('data', []),
        name=series.get('name', ''),
        marker=dict(
            color=colors[i % len(colors)],
            line=dict(
                color=bar_border_color,
                width=1
            )
        )
    ))

# --- 5. Configure Layout and Styling ---
# Combine title and subtitle
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><span style='font-size: 14px;'>{texts['subtitle']}</span>"

# Combine source and note for a single annotation
source_text_parts = []
if texts.get('source'):
    source_text_parts.append(texts['source'])
if texts.get('note'):
    source_text_parts.append(texts['note'])
source_text = "<br>".join(source_text_parts)

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left',
        font=dict(
            family="Arial",
            size=18,
            color='black'
        )
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showticklabels=False,
        showline=False,
        zeroline=False,
        showgrid=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showticklabels=False,
        showline=False,
        zeroline=False,
        showgrid=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    showlegend=False,
    margin=dict(l=40, r=40, t=80, b=80),
    barmode='group'
)

# Add source annotation if it exists
if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper",
        yref="paper",
        x=0,
        y=-0.15,  # Positioned below the chart
        xanchor='left',
        yanchor='top',
        showarrow=False,
        align="left",
        font=dict(
            family="Arial",
            size=12,
            color='black'
        )
    )

# --- 6. Output the Chart ---
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")