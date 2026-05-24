import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# --- 2. Prepare Data for Plotting ---
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 3. Create Chart ---
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#000000', width=1)
    ),
    textinfo='label',
    textposition='outside',
    sort=False,
    direction='clockwise',
    rotation=90
))

# --- 4. Configure Layout ---
title_parts = [texts.get('title'), texts.get('subtitle')]
full_title = "<br>".join(filter(None, title_parts))

source_text = texts.get('source')

fig.update_layout(
    title_text=full_title if full_title else None,
    title_x=0.5,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    showlegend=False,
    margin=dict(l=150, r=150, t=60, b=60),
    annotations=[
        dict(
            text=source_text if source_text else "",
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.1,  # Position below the chart
            xanchor="left",
            yanchor="top",
            align="left"
        )
    ]
)

# --- 5. Output Image ---
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")