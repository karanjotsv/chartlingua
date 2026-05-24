import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Read the JSON data
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data from JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
formatted_text = [f'{v:,}'.replace(',', ' ') for v in values]

# Create the figure
fig = go.Figure()

# Add bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=formatted_text,
    textposition='outside',
    marker_color=colors[0] if colors else None,
    textfont=dict(
        family="Arial",
        size=12
    ),
    cliponaxis=False # Allow text to be drawn outside the plotting area
))

# Configure layout
annotations = []
if texts.get('note'):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=0, y=-0.15,
        xanchor='left', yanchor='top',
        text=texts['note'],
        showarrow=False,
        font=dict(family="Arial", size=12, color="#666666")
    ))

if texts.get('source'):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=1, y=-0.15,
        xanchor='right', yanchor='top',
        text=texts['source'],
        showarrow=False,
        font=dict(family="Arial", size=12, color="#666666")
    ))

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=120),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#f0f0f0',
        linecolor='black',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 60000],
        showgrid=True,
        gridcolor='lightgrey',
        griddash='dot',
        tickformat=" ",
        zeroline=False,
        title_standoff=15
    ),
    annotations=annotations
)

# Generate output PNG file
output_filename_base = pathlib.Path(json_path).stem
output_path = f"{output_filename_base}.png"
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")