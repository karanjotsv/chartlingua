import sys
import json
import plotly.graph_objects as go

# Check for the required command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Derive the output filename from the input JSON path
base_filename = json_file_path.rsplit('.', 1)[0]
output_image_path = f"{base_filename}.png"

# Read and parse the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_file_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_file_path}' is not a valid JSON file.")
    sys.exit(1)

# Extract data and text from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the donut chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    hole=0.65,
    marker=dict(colors=colors),
    textinfo='percent',
    textfont=dict(size=20, color='white'),
    hoverinfo='label+percent',
    sort=False,  # Preserve the order from the JSON file
    direction='clockwise'
))

# Update layout for title, font, legend, and margins
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.1,
        xanchor="center",
        x=0.5
    ),
    margin=dict(t=130, b=80, l=40, r=40),
    showlegend=True
)

# Generate and save the image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")