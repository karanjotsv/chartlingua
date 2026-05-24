import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load Data from JSON ---
# The script expects the JSON file path as the first command-line argument.
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

json_filepath = Path(sys.argv[1])
if not json_filepath.is_file():
    print(f"Error: File not found at {json_filepath}")
    sys.exit(1)

try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_filepath}")
    sys.exit(1)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])
x_labels = texts.get('x_axis_labels', [])

# --- 2. Create the Chart Figure ---
fig = go.Figure()

# --- 3. Add Traces (Data Series) ---
# Iterate through the data series from the JSON to create a bar for each.
# The order is preserved from the JSON file.
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=x_labels,
        y=series.get('y'),
        name=series.get('name'),
        marker_color=colors[i % len(colors)],  # Cycle through colors if not enough
        text=series.get('y'),
        textposition='outside',
        texttemplate='%{y}',
        cliponaxis=False  # Prevents text from being clipped at the top of the plot area
    ))

# --- 4. Configure Layout and Styling ---
# Combine title and subtitle using HTML for flexible styling.
title_text = ""
if texts.get("title"):
    title_text += f'<b>{texts["title"]}</b>'
if texts.get("subtitle"):
    title_text += f'<br><sub>{texts["subtitle"]}</sub>'

# Combine source and note for the annotation.
source_text = ""
if texts.get("source"):
    source_text += texts["source"]
if texts.get("note"):
    source_text += f'<br>{texts["note"]}'

fig.update_layout(
    barmode='group',
    font=dict(family="Arial", size=12, color="black"),
    title=dict(text=title_text, x=0.05, xanchor='left'),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 700],
        gridcolor='#E5E5E5',
        showline=False,
        zeroline=False
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.3,
        xanchor='left',
        x=0
    ),
    margin=dict(l=80, r=40, b=150, t=50),
    annotations=[
        dict(
            showarrow=False,
            text=source_text,
            xref="paper",
            yref="paper",
            x=1,
            y=-0.3,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=10)
        )
    ]
)

fig.update_traces(
    textfont=dict(family='Arial', size=12, color='black')
)

# --- 5. Output the Chart as a PNG Image ---
# The output filename is derived from the input JSON filename.
output_filename = json_filepath.stem + '.png'
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")