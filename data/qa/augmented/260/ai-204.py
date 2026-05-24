import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

# Create the figure
fig = go.Figure()

# Add bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0] if colors else None,
    text=y_values,
    textposition='outside',
    texttemplate='%{text:.2f}',
    cliponaxis=False  # Prevent text labels from being clipped
))

# Combine title and subtitle using HTML tags for styling
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    if title_text:
        title_text += "<br>"
    title_text += f"<sub>{texts['subtitle']}</sub>"

# Update layout for a clean, professional look
fig.update_layout(
    title_text=title_text if title_text else None,
    title_x=0.05,
    yaxis_title_text=texts.get('y_axis_title'),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        showgrid=False,
        linecolor='black',
        tickmode='array',
        tickvals=x_values,
        ticktext=[str(x) for x in x_values]
    ),
    yaxis=dict(
        range=[0, 17.5],
        tickmode='array',
        tickvals=[0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5],
        gridcolor='#E0E0E0',
        linecolor='black',
        zeroline=False
    ),
    margin=dict(t=60, b=80, l=100, r=40),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref="paper", yref="paper",
            x=1.0, y=-0.18,
            xanchor='right', yanchor='top',
            align='right',
            font=dict(size=10, color="#666666")
        )
    ]
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved as {output_filename}")