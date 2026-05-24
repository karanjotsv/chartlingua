import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Read data from JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for the trace
categories = chart_data['categories']
series_data = chart_data['series'][0]['data']

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=series_data,
    marker_color=colors[0],
    text=series_data,
    textposition='outside',
    cliponaxis=False,
    texttemplate='%{text}',
    textfont=dict(family="Arial", size=12)
))

# Update layout for a clean and accurate look
annotations = []
if texts.get('note'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.2,
            xanchor='left', yanchor='top',
            text=texts['note'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="#000000")
        )
    )

if texts.get('source'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.2,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="#666666")
        )
    )

fig.update_layout(
    title_text=texts.get('title'),
    font=dict(family="Arial", size=14),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 150],
        tick0=0,
        dtick=25,
        showgrid=True,
        gridcolor='#e5e5e5',
        tickfont=dict(size=12)
    ),
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=120),
    annotations=annotations
)

# Determine output filename
base_filename = os.path.splitext(json_path)[0]
output_filename = f"{base_filename}.png"

# Save the figure to a file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")