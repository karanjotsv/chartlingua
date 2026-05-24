import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json>")
    sys.exit(1)

# Read data from the specified JSON file
json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly. The JSON is ordered top-to-bottom.
# For Plotly's categorical y-axis, the list order is rendered bottom-to-top.
# We reverse the lists to maintain the original visual order (e.g., Apple at the top).
categories = [item['category'] for item in data]
values = [item['value'] for item in data]
categories.reverse()
values.reverse()

# Create the figure
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    x=values,
    y=categories,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    texttemplate='%{text}',
    textposition='outside',
    hoverinfo='none',
    cliponaxis=False # Prevent text labels from being clipped
))

# Build title string
title_text = ""
if texts.get("title"):
    title_text += f'<b>{texts["title"]}</b>'
if texts.get("subtitle"):
    title_text += f'<br><sub>{texts["subtitle"]}</sub>' if title_text else f'<sub>{texts["subtitle"]}</sub>'

# Build annotations list for source text
annotations = []
if texts.get("source"):
    annotations.append(
        dict(
            text=texts["source"],
            xref="paper", yref="paper",
            x=0.98, y=-0.12,
            showarrow=False,
            xanchor='right', yanchor='top',
            font=dict(size=12, color="#808080")
        )
    )

# Configure layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.01,
        xanchor='left'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#E5E5E5',
        griddash='dot',
        zeroline=False,
        showline=False,
        showticklabels=True,
        range=[0, 400],
        dtick=50
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="#333333"
    ),
    margin=dict(l=120, r=60, t=40, b=100),
    annotations=annotations,
    showlegend=False,
    bargap=0.4
)

# Generate and save the output image
base_filename = Path(json_path).stem
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")