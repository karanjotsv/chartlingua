import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts
data_series = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Initialize figure
fig = go.Figure()

# Add traces
for i, series in enumerate(data_series):
    color = colors[i % len(colors)]
    dash_style = 'solid' if series.get('line_style') == 'solid' else 'dot'
    
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines',
        yaxis=series.get('yaxis'),
        line=dict(color=color, dash=dash_style, width=2.5)
    ))

# Prepare layout annotations
layout_annotations = texts.get('annotations', [])

if texts.get('y_axis_unit'):
    layout_annotations.append(
        dict(
            text=texts['y_axis_unit'],
            xref="paper", yref="paper",
            x=0, y=1.05,
            xanchor='left', yanchor='bottom',
            showarrow=False,
            font=dict(family="Arial", size=14)
        )
    )

if texts.get('y2_axis_unit'):
    layout_annotations.append(
        dict(
            text=texts['y2_axis_unit'],
            xref="paper", yref="paper",
            x=1, y=1.05,
            xanchor='right', yanchor='bottom',
            showarrow=False,
            font=dict(family="Arial", size=14)
        )
    )

# Update layout
fig.update_layout(
    template='plotly_white',
    font=dict(family="Arial", size=14),
    showlegend=False,
    margin=dict(l=100, r=100, t=50, b=80),
    xaxis=dict(
        title=dict(text=texts.get('x_axis_title'), standoff=10),
        tickmode='array',
        tickvals=[1965, 1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010],
        range=[1960, 2013],
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title=dict(text=texts.get('y_axis_title'), standoff=35),
        side='left',
        range=[0, 180000000],
        tickvals=[0, 20000000, 60000000, 100000000, 140000000, 180000000],
        showgrid=True,
        gridcolor='lightgray',
        tickfont=dict(size=12)
    ),
    yaxis2=dict(
        title=dict(text=texts.get('y2_axis_title'), standoff=45),
        side='right',
        overlaying='y',
        showgrid=False,
        range=[0, 6000000],
        tickvals=[0, 1000000, 2000000, 3000000, 4000000, 5000000, 6000000],
        tickfont=dict(size=12)
    ),
    annotations=layout_annotations
)

# Set font for annotations from JSON
for i in range(len(texts.get('annotations', []))):
    fig.layout.annotations[i].font = dict(family="Arial", size=14)


# Generate output filename and save the image
base_filename, _ = os.path.splitext(os.path.basename(json_path))
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")