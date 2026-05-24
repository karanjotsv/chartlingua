import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Ensure a command-line argument is provided
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

# Read the JSON file from the command-line argument
json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the JSON structure
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Prepare data for Plotly
labels_for_hover = [item['label'].replace('<br>', ' ') for item in chart_data]
values = [item['value'] for item in chart_data]
text_on_slice = [f"{item['label']}<br>{item['value']}%" for item in chart_data]

# Create the pie chart figure
fig = go.Figure(data=[go.Pie(
    labels=labels_for_hover,
    values=values,
    marker=dict(colors=colors, line=dict(color='black', width=1.5)),
    text=text_on_slice,
    textinfo='text',
    hoverinfo='label+percent',
    pull=[0.05, 0.05, 0.05, 0.05, 0.05],
    sort=False,  # Preserve the order from the JSON file
    direction='clockwise',
    textfont=dict(family="Arial", size=16, color="white")
)])

# Configure the layout of the chart
fig.update_layout(
    title_text=texts['title'],
    title_x=0.5,
    title_font=dict(family="Arial", size=24, color='black'),
    showlegend=False,
    paper_bgcolor='white',
    margin=dict(t=120, b=80, l=40, r=40),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.98,
            y=0.02,
            xanchor='right',
            yanchor='bottom',
            font=dict(family="Arial", size=12, color='black')
        )
    ]
)

# Define the output filename based on the input JSON filename
output_filename = json_path.with_suffix('.png')

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")