import sys
import json
import plotly.graph_objects as go
import pathlib

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
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

# Extract data, texts, and colors from the JSON structure
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly pie chart
labels = [item.get('label', '') for item in chart_data]
values = [item.get('value', 0) for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    sort=False,  # This is crucial to preserve the order from the JSON file
    direction='clockwise',
    textinfo='none',  # No text on the pie slices
    hoverinfo='label+percent'
))

# Configure the layout
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    title_font=dict(family="Arial", size=20, color='black'),
    font=dict(family="Arial", size=12, color='black'),
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5,
        traceorder='normal'
    ),
    margin=dict(l=50, r=50, t=100, b=120),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Determine the output filename from the input JSON path
base_filename = pathlib.Path(json_file_path).stem
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully generated and saved as '{output_filename}'")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)