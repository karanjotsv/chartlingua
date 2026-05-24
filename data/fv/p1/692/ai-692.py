import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for the chart
chart_data = chart_details.get('chart_data', [])
texts = chart_details.get('texts', {})
colors = chart_details.get('colors', [])

# Prepare data for Plotly pie chart
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    hoverinfo='label+percent',
    textinfo='percent',
    textfont_size=14,
    textposition='outside',
    sort=False,
    direction='clockwise',
    rotation=178  # Rotates the chart to position the first slice as in the image
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Update layout for styling, titles, and fonts
fig.update_layout(
    title_text=texts.get('title'),
    title_x=0.5,
    title_y=0.95,
    title_font_size=24,
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    paper_bgcolor='#E6E6FA',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5,
        font_size=14
    ),
    margin=dict(t=120, b=120, l=40, r=40)
)

# Determine the output image filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully generated and saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)