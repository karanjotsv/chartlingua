import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Read the JSON data
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data and texts from the JSON object
data = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Prepare data for Plotly. Data is reversed to display the highest value at the top.
categories = [item['category'] for item in data][::-1]
values = [item['value'] for item in data][::-1]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=values,
    y=categories,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    textposition='outside',
    texttemplate='%{text}',
    textfont=dict(color='black', size=12),
    cliponaxis=False  # Prevents text labels from being clipped at the chart edge
))

# Update layout
fig.update_layout(
    title=texts.get('title'),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=150, r=80, t=50, b=80),  # Adjust margins for labels and source
    xaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        tickformat=',.0f'
    ),
    yaxis=dict(
        showgrid=False
    ),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.98,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10, color='grey')
        )
    ]
)

# Define the output filename from the input JSON path
output_image_path = json_file_path.with_suffix('.png')

# Save the figure as a PNG image
try:
    fig.write_image(output_image_path, scale=2)
    print(f"Chart saved to {output_image_path}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)