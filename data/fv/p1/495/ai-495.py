import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read the chart data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data lists from the JSON structure
labels = [item['label'] for item in data]
values = [item['value'] for item in data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)),
    texttemplate='%{label}<br>%{value}%',
    textposition='inside',
    textfont=dict(color='white'),
    hoverinfo='label+percent',
    sort=False,  # Preserve the original data order
    direction='clockwise',
    rotation=90 # Starts the first slice at the top (12 o'clock)
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Update the layout for a clean and accurate presentation
fig.update_layout(
    title_text=f"<b>{texts['title']}</b>" if texts.get('title') else "",
    title_x=0.02,
    title_y=0.98,
    title_xanchor='left',
    title_yanchor='top',
    font=dict(
        family="Arial"
    ),
    showlegend=False,
    margin=dict(t=70, b=20, l=20, r=20),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Determine the output filename from the input JSON filename
output_filename = json_file_path.with_suffix('.png')

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")