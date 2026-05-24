import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', {})

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the line trace
fig.add_trace(go.Scatter(
    x=categories,
    y=values,
    mode='lines+markers+text',
    line=dict(color=colors.get('line', '#000000')),
    marker=dict(color=colors.get('line', '#000000'), size=8),
    text=[str(v).replace('.', ',') for v in values],
    textposition='top center',
    textfont=dict(
        family="Arial",
        size=12,
        color=colors.get('text', '#000000')
    )
))

# Configure layout
title_text = f"<b>{texts.get('title', '')}</b><br>{texts.get('subtitle', '')}"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    xaxis=dict(
        tickvals=categories,
        tickmode='array',
        showgrid=False,
        showline=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        visible=False,
        range=[min(values) * 0.8, max(values) * 1.15] # Ensure space for labels
    ),
    font=dict(
        family="Arial",
        color=colors.get('text', '#000000')
    ),
    plot_bgcolor=colors.get('plot_bg', '#FFFFFF'),
    paper_bgcolor=colors.get('paper_bg', '#FFFFFF'),
    showlegend=False,
    margin=dict(l=20, r=40, t=100, b=80),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            xref="paper",
            yref="paper",
            x=0.95,
            y=-0.2,
            xanchor='right',
            yanchor='bottom',
            align='right'
        )
    ]
)

# Determine output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")