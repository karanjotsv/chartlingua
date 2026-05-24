import sys
import json
import plotly.graph_objects as go
import os

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON object
data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly pie chart
labels = [item['label'] for item in data]
values = [item['value'] for item in data]

# Create the pie chart trace
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    textinfo='label',
    textposition='inside',
    textfont=dict(family="Arial", size=16, color='black'),
    marker=dict(
        colors=colors,
        line=dict(color='black', width=1.5)
    ),
    hole=0,
    sort=False,
    direction='clockwise',
    rotation=90,
    hoverinfo='skip'
)])

# Configure the chart layout
fig.update_layout(
    title=dict(
        text=texts['title'],
        y=0.98,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(family="Arial", size=20, color='black')
    ),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(family="Arial", size=14, color='black'),
    margin=dict(t=80, b=80, l=40, r=40),
    annotations=[
        dict(
            text=f"<b>{texts['footer_title']}</b>",
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.5,
            y=-0.1,
            xanchor='center',
            yanchor='top',
            font=dict(family="Arial", size=18, color='black')
        ),
        dict(
            text=texts['note'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.25,
            xanchor='center',
            yanchor='middle',
            font=dict(family="Arial", size=16, color='black')
        )
    ]
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")