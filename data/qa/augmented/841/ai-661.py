import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read the JSON data from the file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
chart_data = chart_details.get('chart_data', [])
texts = chart_details.get('texts', {})
colors = chart_details.get('colors', [])

# Prepare data for plotting
# Reverse the data to match the visual top-to-bottom order of the original chart
categories = [item['category'] for item in reversed(chart_data)]
values = [item['value'] for item in reversed(chart_data)]

# Create the figure object
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    texttemplate='%{x:.1f}%',
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False
))

# Build title string from JSON data
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout for a professional and accurate appearance
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(text=title_text, x=0.05, xanchor='left'),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        range=[-12, 85],
        tickmode='linear',
        tick0=-10,
        dtick=10,
        ticksuffix='%',
        showgrid=True,
        gridwidth=1,
        gridcolor='#EAEAEA',
        griddash='dot',
        zeroline=False,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1,
        linecolor='black',
        linewidth=1
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=100, r=40, t=50, b=80),
    annotations=[
        dict(
            text=texts.get("source", ""),
            showarrow=False,
            xref="paper", yref="paper",
            x=1, y=-0.1,  # Positioned at the bottom right
            xanchor='right', yanchor='top',
            font=dict(size=12)
        )
    ]
)

# Define output filename based on the input JSON filename
output_filename = json_path.with_suffix('.png')

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")