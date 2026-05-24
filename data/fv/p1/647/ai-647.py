import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>", file=sys.stderr)
    sys.exit(1)

json_file_path = sys.argv[1]

# Check if the specified file exists
if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}", file=sys.stderr)
    sys.exit(1)

# Derive the base filename for the output image from the input JSON file path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

# Read and parse the JSON data file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except Exception as e:
    print(f"Error reading or parsing JSON file: {e}", file=sys.stderr)
    sys.exit(1)

# Extract chart data and styling from the loaded JSON
chart_data = data['chart_data']
colors = data['colors']
texts = data['texts']

# Prepare data arrays for the Plotly trace
labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]
display_texts = [item['display_text'] for item in chart_data]
text_colors = [item['text_color'] for item in chart_data]

# Initialize the figure
fig = go.Figure()

# Add the donut chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    hole=0.4,
    marker=dict(
        colors=colors,
        line=dict(color='#FFFFFF', width=1)
    ),
    text=display_texts,
    textinfo='text',
    textposition='inside',
    textfont=dict(
        family="Arial",
        size=18
    ),
    textfont_color=text_colors,
    hoverinfo='label+percent',
    sort=False,
    rotation=105
))

# Configure the layout of the chart
fig.update_layout(
    showlegend=False,
    margin=dict(l=20, r=20, t=20, b=20),
    paper_bgcolor='white',
    plot_bgcolor='white',
    font_family="Arial"
)

# Save the generated chart as a PNG image
try:
    fig.write_image(output_image_path, scale=2)
    print(f"Chart saved to {output_image_path}")
except Exception as e:
    print(f"Error saving image: {e}", file=sys.stderr)
    sys.exit(1)