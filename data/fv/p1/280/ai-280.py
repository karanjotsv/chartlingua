import sys
import json
import plotly.graph_objects as go
import os

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read the JSON data from the file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# Extract data for plotting
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Prepare data for Plotly trace
categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=[f'{v:,}' for v in values],  # Format text with commas
    textposition='outside',
    cliponaxis=False
))

# Update layout
fig.update_layout(
    title_text=texts['title'],
    title_x=0.5,
    title_y=0.95,
    xaxis_tickangle=-45,
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False,
        range=[0, 8000]
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False
    ),
    plot_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(l=60, r=40, t=80, b=200),
    showlegend=False
)

# Set specific font for text on bars to match the original
fig.update_traces(textfont=dict(family="Arial", size=12, color='black'))

# Generate output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")