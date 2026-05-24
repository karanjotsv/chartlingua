import sys
import json
import plotly.graph_objects as go
import os

# Check if a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)


# Extract data and texts from the JSON object
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly pie chart
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors),
    textinfo='percent',
    texttemplate='%{value}%',
    insidetextfont=dict(family="Arial", size=14),
    hovertemplate='%{label}: %{value}%<extra></extra>',
    sort=False,  # Preserve the original order from the JSON data
    direction='clockwise',
    rotation=70 # Adjust starting angle to match the original chart
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Update layout for title, legend, and other styling
fig.update_layout(
    title_text=texts.get('title', ''),
    title_x=0.5,
    title_y=0.95,
    title_xanchor='center',
    title_yanchor='top',
    title_font=dict(family="Arial", size=24, color='black'),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=0.9,
        xanchor="center",
        x=0.5,
        font=dict(family="Arial", size=12)
    ),
    font=dict(family="Arial", size=12, color='black'),
    margin=dict(t=100, b=40, l=40, r=40),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Determine the output filename from the input JSON filename
filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully generated and saved as '{output_filename}'")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)