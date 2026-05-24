import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
data = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors,
    texttemplate='%{y}%',
    textposition='outside',
    cliponaxis=False  # Prevents text from being clipped at the top
))

# Build title string
title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Update layout for a professional look and feel
fig.update_layout(
    title_text=title_text,
    title_x=0.05,
    title_font=dict(size=20, family="Arial"),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 26],
        tickvals=[0, 5, 10, 15, 20, 25],
        tickformat='%g%%',
        gridcolor='#EAEAEA',
        zeroline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        tickangle=-45,
        automargin=True
    ),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=40, t=50, b=200), # Increased bottom margin for rotated labels
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.4, # Position below the x-axis labels
            xanchor='right',
            yanchor='bottom',
            font=dict(size=10)
        )
    ]
)

fig.update_traces(textfont_size=12)

# Generate the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")