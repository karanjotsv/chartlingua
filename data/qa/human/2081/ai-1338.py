import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load data from command-line argument ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_filepath = Path(sys.argv[1])
if not json_filepath.is_file():
    print(f"Error: File not found at {json_filepath}")
    sys.exit(1)

with open(json_filepath, 'r', encoding='utf-8') as f:
    config = json.load(f)

# --- 2. Extract data and texts from JSON ---
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='white', width=1)
    ),
    sort=False,  # This is crucial to preserve the original data order
    direction='clockwise',
    textposition='outside',
    texttemplate='%{label} %{value}%',
    hoverinfo='label+percent',
    pull=[0.01] * len(labels) # Small pull for slight separation
))

# --- 4. Configure layout and styling ---
# Combine title and subtitle
title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Combine source and note for annotation
source_text = ""
if texts.get("source"):
    source_text += texts["source"]
if texts.get("note"):
    source_text += f"<br>{texts['note']}"

annotations = []
if source_text:
    annotations.append(
        go.layout.Annotation(
            text=source_text,
            xref="paper", yref="paper",
            x=0.99, y=0.01,
            xanchor='right', yanchor='bottom',
            showarrow=False,
            align='right',
            font=dict(family="Arial", size=10, color="#888888")
        )
    )

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    font_family="Arial",
    showlegend=False,  # The original uses labels outside the pie, not a separate legend
    margin=dict(t=60, b=80, l=60, r=60),
    plot_bgcolor='white',
    paper_bgcolor='white',
    annotations=annotations,
    # Uniform text settings can help prevent overlapping labels
    uniformtext_minsize=10,
    uniformtext_mode='hide'
)

# --- 5. Output the chart as a PNG file ---
output_filename = json_filepath.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")