import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get file path from command-line argument
json_path = pathlib.Path(sys.argv[1])

# Verify the JSON file exists
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for the pie chart
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
# Create the text for each slice, combining category and value as seen in the image
pie_text = [f"{item['category']}<br>{item['value']}%" for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    text=pie_text,
    textinfo='text',
    textposition='outside',
    marker=dict(
        colors=colors,
        line=dict(color='white', width=2)
    ),
    hole=0,
    sort=False,  # This is crucial to preserve the original data order
    direction='clockwise',
    showlegend=False
))

# Update layout for styling, font, and margins
fig.update_layout(
    margin=dict(l=100, r=100, t=40, b=40),
    font=dict(
        family="Arial",
        size=16,
        color="black"
    ),
    paper_bgcolor='white',
    plot_bgcolor='white',
    showlegend=False,
    uniformtext_minsize=12,
    uniformtext_mode='hide'
)

# Generate the output filename from the input JSON filename
output_filename_base = json_path.stem
output_png_path = f"{output_filename_base}.png"

# Save the chart as a PNG image
fig.write_image(output_png_path, scale=2)

print(f"Chart saved to {output_png_path}")