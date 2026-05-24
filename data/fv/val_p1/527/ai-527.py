import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Data source: https://unfccc.int/documents/223579 (Turkey's 7th National Communication under the UNFCCC, 2019)
# Chart visualizes data for the year 2018.

# Check for the required command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>", file=sys.stderr)
    sys.exit(1)

# Define file paths
json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'", file=sys.stderr)
    sys.exit(1)
    
output_image_path = json_file_path.with_suffix('.png')

# Load data from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data and texts from the JSON object
chart_data = config['chart_data']
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]
texts = config['texts']
colors = config['colors']

# Create the pie chart figure
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    textposition='outside',
    textinfo='label',
    sort=False,
    direction='clockwise',
    rotation=90
)])

# Update the layout for a clean and accurate presentation
fig.update_layout(
    title_text=texts['title'],
    title_x=0.5,
    font=dict(
        family="Arial",
        size=14
    ),
    title_font_size=18,
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(t=100, b=50, l=80, r=80),
    uniformtext_minsize=12,
    uniformtext_mode='hide'
)

# Write the output image file
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")