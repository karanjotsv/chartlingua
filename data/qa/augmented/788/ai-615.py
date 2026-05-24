import sys
import json
import os
import plotly.graph_objects as go

# Ensure a command-line argument for the JSON file path is provided
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the specified JSON file with UTF-8 encoding
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)

# Extract data and texts from the JSON object
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly; preserving original order
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace with data labels
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    text=[f"{v}%" for v in values],
    textposition='outside',
    cliponaxis=False  # Allow text to render outside the plot area
))

# Combine title and subtitle using HTML tags for formatting
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout for a clean, professional look
fig.update_layout(
    title_text=title_text,
    title_x=0.05,
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(t=60, b=120, l=80, r=40),
    yaxis=dict(
        title_text=texts.get('y_axis_label'),
        showgrid=True,
        gridcolor='lightgray',
        ticksuffix='%',
        range=[0, max(values) * 1.2],  # Dynamic range with padding for text
        dtick=1,
        zeroline=False
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_label'),
        showgrid=False
    ),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper', yref='paper',
            x=0.98, y=-0.22,  # Position at bottom right, adjusted for margin
            xanchor='right', yanchor='top',
            align='right',
            font=dict(family="Arial", size=12, color="gray")
        )
    ]
)

# Set the font for the bar labels
fig.update_traces(textfont_family="Arial", textfont_color='black')

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved successfully as {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)