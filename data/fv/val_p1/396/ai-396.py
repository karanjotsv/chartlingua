import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = pathlib.Path(sys.argv[1])

# Define the output image path based on the JSON filename
output_path = json_path.with_suffix(".png")

# Load data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except (json.JSONDecodeError, FileNotFoundError) as e:
    print(f"Error: Could not read or parse the JSON file at {json_path}. Details: {e}")
    sys.exit(1)

# Extract data and texts from the loaded JSON
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly Pie trace
labels = [item.get('label', '') for item in chart_data]
values = [item.get('value', 0) for item in chart_data]
legend_labels = [f"{label} {value}%" for label, value in zip(labels, values)]

# Initialize the figure
fig = go.Figure()

# Add the Pie chart trace
fig.add_trace(go.Pie(
    labels=legend_labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#696969', width=1)
    ),
    sort=False,  # This is crucial to preserve the order from the JSON file
    direction='clockwise',
    rotation=153,  # Adjusts the start angle to match the source image
    textinfo='none',
    hoverinfo='label+percent',
    domain=dict(x=[0.0, 0.75]) # Reserve space on the right for the legend
))

# Construct the title string using HTML for formatting
title_text = f"<b>{texts.get('title', '')}</b>"
if texts.get('subtitle'):
    title_text += f"<br>{texts['subtitle']}"

# Update the layout of the figure for a clean and accurate presentation
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=28)
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    showlegend=True,
    legend=dict(
        x=0.78,
        y=0.7,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(255,255,255,0)',
        bordercolor='rgba(0,0,0,0)'
    ),
    margin=dict(l=40, r=40, t=100, b=40),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Write the figure to a PNG file with a high resolution
fig.write_image(output_path, scale=2)

print(f"Chart successfully generated and saved to {output_path}")