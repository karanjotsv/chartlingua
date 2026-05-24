import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])

# Ensure the JSON file exists
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and texts
data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly horizontal bar chart
# Data is reversed to match the visual top-to-bottom order from the image
categories = [item['category'] for item in data]
values = [item['value'] for item in data]
categories.reverse()
values.reverse()

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    texttemplate='%{text}',
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False  # Prevents text from being clipped at the chart edge
))

# Update layout for a clean and accurate appearance
fig.update_layout(
    title_text="", # No title in the original image
    font=dict(family="Arial", size=12, color='black'),
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=True,
        gridcolor='#e9e9e9',
        gridwidth=1,
        zeroline=False,
        showline=False,
        showticklabels=True
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=True
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=120, r=40, t=40, b=80), # Adjust margins for labels
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(family="Arial", size=12, color='#666666')
        )
    ]
)

# Define output filename and save the image
output_filename = json_path.with_suffix('.png').name
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")