import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Ensure the file exists before proceeding
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Derive the base filename for the output PNG from the input JSON path
filename_base = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{filename_base}.png"

# Read and parse the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON in file '{json_file_path}'")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred while reading the file: {e}")
    sys.exit(1)

# Extract data from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Create the figure object
fig = go.Figure()

# Add traces to the figure by iterating through the chart data
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines',
        line=dict(color=colors[i % len(colors)], width=2.5) # Use modulo to prevent index errors
    ))

# Build the title string
title_text = ""
if texts.get("title"):
    title_text += f'<span style="font-size: 18px;"><b>{texts["title"]}</b></span>'
if texts.get("subtitle"):
    title_text += f'<br><span style="font-size: 14px; color: #555;">{texts["subtitle"]}</span>'

# Update the layout of the figure
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left',
        y=0.95,
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        range=[0, 200],
        tickmode='linear',
        tick0=0,
        dtick=20,
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[-100, 100],
        tickmode='linear',
        tick0=-100,
        dtick=20,
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='black'
    ),
    legend=dict(
        x=0.98,
        y=0.7,
        xanchor='right',
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(0,0,0,0)',
        borderwidth=0
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=40, t=60, b=50)
)

# Save the figure to a PNG file
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)