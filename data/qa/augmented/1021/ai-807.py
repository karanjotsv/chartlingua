import sys
import json
import plotly.graph_objects as go
import argparse
from pathlib import Path

# --- Argument Parsing ---
parser = argparse.ArgumentParser(description='Generate a bar chart from a JSON file.')
parser.add_argument('json_path', type=Path, help='Path to the input JSON file.')
if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()
json_path = args.json_path

# --- File Handling ---
if not json_path.is_file():
    print(f"Error: File not found at {json_path}", file=sys.stderr)
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

output_path = json_path.with_suffix(".png")

# --- Data Extraction ---
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
text_labels = [f"{item['value']:g}%" for item in chart_data]

# --- Chart Creation ---
fig = go.Figure()

# Add Bar Trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=text_labels,
    textposition='outside',
    marker_color=colors[0] if colors else '#1f77b4',
    cliponaxis=False
))

# --- Layout and Styling ---
annotations = []
if texts.get('source_left'):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=0, y=-0.2,
            xanchor='left', yanchor='bottom',
            text=texts['source_left'],
            font=dict(family="Arial", size=12, color="#007bff"),
            showarrow=False
        )
    )

if texts.get('source_right'):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=1, y=-0.2,
            xanchor='right', yanchor='bottom',
            text=texts['source_right'],
            font=dict(family="Arial", size=12, color="grey"),
            showarrow=False
        )
    )

fig.update_layout(
    title_text=texts.get('title'),
    font=dict(family="Arial"),
    plot_bgcolor='#f5f5f5',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 7],
        tickvals=[0, 1, 2, 3, 4, 5, 6, 7],
        ticksuffix='%',
        showgrid=True,
        gridcolor='white',
        zeroline=False
    ),
    margin=dict(l=80, r=40, t=50, b=100),
    annotations=annotations
)

# --- Output ---
fig.write_image(str(output_path), scale=2)
print(f"Chart saved to {output_path}")