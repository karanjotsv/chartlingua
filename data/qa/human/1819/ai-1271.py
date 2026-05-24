import sys
import json
import os
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data in lists for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors),
    text=[f'{v}%' for v in values],
    textposition='outside',
    textfont=dict(family='Arial', size=12, color='#333333'),
    hoverinfo='none',
    cliponaxis=False
))

# Combine title and subtitle
title_text = f"<b>{texts['title']}</b><br><span style='font-size:14px;'>{texts['subtitle']}</span>"

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=title_text,
        y=0.98,
        x=0.01,
        xanchor='left',
        yanchor='top',
        font=dict(size=20)
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dash',
        zeroline=False,
        ticksuffix='%',
        domain=[0, 0.95],
        range=[0, max(values) * 1.1]
    ),
    yaxis=dict(
        autorange="reversed",
        showgrid=False,
        tickfont=dict(size=14)
    ),
    margin=dict(l=100, r=40, t=140, b=100),
    paper_bgcolor='#f5f5f5',
    plot_bgcolor='white',
    showlegend=False,
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.15,
            xanchor='left', yanchor='top',
            text=texts['source_note'],
            showarrow=False,
            align='left',
            font=dict(size=12)
        ),
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.15,
            xanchor='right', yanchor='top',
            text=texts['credit'],
            showarrow=False,
            align='right',
            font=dict(size=12)
        )
    ]
)

# Generate output filename from input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")