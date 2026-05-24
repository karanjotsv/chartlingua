import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Read the JSON data from the file
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
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Prepare data for Plotly
categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=values,
    texttemplate='%{y}',
    textposition='outside',
    cliponaxis=False
))

# Update layout for a professional look and to match the original
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title_text=texts['title'] if texts.get('title') else None,
    yaxis_title=texts['y_axis_title'],
    xaxis_title=texts['x_axis_title'],
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=120),
    xaxis=dict(
        showgrid=False,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        range=[0, 100],
        showgrid=True,
        gridcolor='#e0e0e0',
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12)
    ),
    annotations=[
        dict(
            text=texts.get('note', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.25,
            xanchor='left',
            yanchor='top',
            align='left'
        ),
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.25,
            xanchor='right',
            yanchor='top',
            align='right'
        )
    ]
)

# Further styling for data labels on top of the bars
fig.update_traces(textfont_size=12, textfont_color='black')


# Define the output filename based on the input JSON file's name
output_filename = json_file_path.stem + '.png'

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")