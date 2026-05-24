import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data and configuration from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Extract data for plotting, preserving the original order
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the horizontal bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0])
))

# Build the title string with subtitle if available
title_text = f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Apply layout and styling
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        autorange='reversed',  # This ensures the order from the JSON is displayed top-to-bottom
        showgrid=False
    ),
    plot_bgcolor='#f0f2f6',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12),
    margin=dict(l=60, r=40, t=80, b=80),
    showlegend=False
)

# Determine the output filename from the input JSON path
if '/' in json_path:
    base_name = json_path.split('/')[-1]
elif '\\' in json_path:
    base_name = json_path.split('\\')[-1]
else:
    base_name = json_path

if '.' in base_name:
    base_name = base_name.rsplit('.', 1)[0]

output_filename = f"{base_name}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")