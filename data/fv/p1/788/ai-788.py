import sys
import json
import plotly.graph_objects as go
import os

# Ensure a command-line argument is provided for the JSON file path
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_file_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_file_path}' contains invalid JSON.")
    sys.exit(1)

# Extract data and text from the loaded JSON
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

labels = [item.get('category') for item in chart_data]
values = [item.get('value') for item in chart_data]

# Create the pie chart figure
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#000000', width=1)),
    hoverinfo='label+percent',
    texttemplate='%{value}%',
    textfont=dict(family="Arial", size=14, color='black'),
    sort=False,
    direction='clockwise',
    rotation=-45
)])

# Build the title string from the JSON data
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br>{texts['subtitle']}"

# Update the figure layout
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    font=dict(family="Arial", size=12, color="white"),
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.9,
        xanchor="left",
        x=1.02,
        traceorder='normal' # Ensures legend items match data order
    ),
    paper_bgcolor='black',
    plot_bgcolor='black',
    margin=dict(l=20, r=450, t=120, b=20) # Ample right margin for legend
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_image_path, scale=2)

print(f"Chart successfully generated and saved as '{output_image_path}'")