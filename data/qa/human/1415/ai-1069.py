import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script requires the path to the JSON file as a command-line argument.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# --- 2. Extract data and texts from the JSON structure ---
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

values = [d['value'] for d in chart_data]
labels = [d['label'] for d in chart_data]

# --- 3. Create the Chart Figure ---
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    values=values,
    marker=dict(colors=colors, line=dict(color='white', width=2)),
    textfont=dict(size=20),
    textfont_color=['black', 'white'], # Set text color per slice
    texttemplate='<b>%{value}%</b>',
    hoverinfo='none',
    sort=False,
    direction='clockwise',
    rotation=155,
    pull=[0.05, 0] # Pull the first slice (26%)
))

# --- 4. Configure Layout, Titles, and Annotations ---
# Combine title and subtitle with HTML for styling
title_text = (
    f"<span style='font-size: 26px;'><b>{texts['title']}</b></span><br>"
    f"<span style='font-size: 16px;color:#505050;'>{texts['subtitle']}</span>"
)

# Combine source and note for the footer annotation
source_text = f"{texts['source']}<br><b>{texts['note']}</b>"

# Create annotations for the labels outside the pie chart and the source note
annotations = [
    # Annotation for the first data point (26%)
    dict(
        x=0.2, y=0.3, xref="paper", yref="paper",
        text=labels[0],
        showarrow=True,
        arrowhead=0,
        ax=-50,
        ay=-80,
        align='left',
        font=dict(size=14, color='#333333')
    ),
    # Annotation for the second data point (73%)
    dict(
        x=0.8, y=0.8, xref="paper", yref="paper",
        text=labels[1],
        showarrow=True,
        arrowhead=0,
        ax=50,
        ay=-50,
        align='left',
        font=dict(size=14, color='#333333')
    ),
    # Annotation for the source and note at the bottom
    dict(
        x=0, y=-0.1, xref="paper", yref="paper",
        text=source_text,
        showarrow=False,
        xanchor='left',
        yanchor='top',
        align='left',
        font=dict(size=12, color='#333333')
    )
]

fig.update_layout(
    title_text=title_text,
    title_x=0.02,
    title_y=0.97,
    font_family="Arial",
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(t=160, b=120, l=40, r=40),
    annotations=annotations
)

# --- 5. Output the Chart to a PNG File ---
output_path = json_path.with_suffix(".png")
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")