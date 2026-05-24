import sys
import json
import os
import plotly.graph_objects as go

# Check if the path to the JSON file is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred while reading the file: {e}")
    sys.exit(1)

# Extract data for plotting
data = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Prepare data for the bar chart
categories = [item['category'] for item in data]
values = [item['values'][0] for item in data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='inside',
    texttemplate='%{y}',
    textangle=-90,
    textfont=dict(
        family="Arial",
        size=12,
        color="white"
    ),
    marker_color=colors[0] if colors else '#376EB2',
    insidetextanchor='middle'
))

# Update layout
fig.update_layout(
    title_text=texts.get('title', ''),
    title_x=0.5,
    title_y=0.95,
    title_xanchor='center',
    title_yanchor='top',
    font=dict(
        family="Arial",
        size=14
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        type='category' # Ensure categories are treated as discrete items
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        showline=False
    ),
    plot_bgcolor='#E9E9E9',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(t=80, b=50, l=50, r=50)
)

# Determine the output filename from the input JSON path
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved as '{output_filename}'")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)