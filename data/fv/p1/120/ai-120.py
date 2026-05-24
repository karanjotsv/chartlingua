import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = Path(sys.argv[1])
output_filename_base = json_file_path.stem

# Read data from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: The file {json_file_path} was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file {json_file_path} is not a valid JSON file.")
    sys.exit(1)

# Extract data and settings from the JSON structure
data = chart_data['chart_data']
labels = [item['label'] for item in data]
values = [item['value'] for item in data]
slice_colors = chart_data['colors']
text_colors = [item['text_color'] for item in data]
font_sizes = [item['font_size'] for item in data]

# Generate the text to display on each slice
texts_on_pie = []
for item in data:
    # Split label by <br> to bold each line individually
    label_parts = item['label'].split('<br>')
    bold_label = '<b>' + '</b><br><b>'.join(label_parts) + '</b>'
    
    # Format text: Water has no %, others do
    if item['label'] == 'Water':
        display_text = f"{bold_label}<br><b>{item['value']}</b>"
    else:
        display_text = f"{bold_label}<br><b>{item['value']}%</b>"
    texts_on_pie.append(display_text)

# Create the pie chart figure
fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    text=texts_on_pie,
    textinfo='text',
    marker=dict(colors=slice_colors, line=dict(color='#FFFFFF', width=1)),
    textfont=dict(
        family="Arial",
        size=font_sizes,
        color=text_colors
    ),
    textposition='outside',
    hole=0,
    sort=False,
    direction='clockwise',
    rotation=92 # Start the first slice near the top
))

# Update layout for a clean appearance
fig.update_layout(
    showlegend=False,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=80, r=80, t=20, b=20),
    font=dict(family="Arial")
)

# Define the output file path
output_image_path = f"{output_filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")