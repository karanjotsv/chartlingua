import sys
import json
import plotly.graph_objects as go
import os

# Ensure a command-line argument is provided
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read the JSON data file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data for plotting
data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Format text labels with bold tags and thousands separators
formatted_values_html = [f"<b>{v:,}</b>" for v in values]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors,
    text=formatted_values_html,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=14,
        color='black'
    )
))

# Construct the title
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Update the layout for a clean, accurate look
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.98,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=16)
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        showgrid=True,
        gridcolor='#cccccc',
        linecolor='black',
        zeroline=False,
        ticks='outside',
        ticklen=5
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#cccccc',
        linecolor='black',
        zeroline=False,
        range=[0, max(values) * 1.1],
        dtick=1000,
        ticks='outside',
        ticklen=5,
        separatethousands=True
    ),
    margin=dict(t=120, b=100, l=60, r=40),
)

# Generate the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")