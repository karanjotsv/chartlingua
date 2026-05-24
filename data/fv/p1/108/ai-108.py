import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_file_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data_json = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_file_path}")
    sys.exit(1)


# Extract data and texts for the chart
chart_data = chart_data_json.get('chart_data', [])
texts = chart_data_json.get('texts', {})
colors = chart_data_json.get('colors', [])

# Prepare data for Plotly
labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart
fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    sort=False,  # Preserve the order from the JSON file
    direction='clockwise',
    textposition='outside',
    textinfo='label',
    hoverinfo='label+percent',
    pull=[0, 0, 0, 0, 0, 0, 0.02] # Slight pull for the last 'Other' slice to avoid label overlap
)])

# Combine title and subtitle
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout for a clean and accurate look
fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    font={
        'family': "Arial",
        'size': 14
    },
    showlegend=False,
    margin=dict(t=100, b=80, l=40, r=40),
    paper_bgcolor='white',
    plot_bgcolor='white',
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.5,
            y=-0.1,
            xanchor='center',
            yanchor='top',
            align='center',
            font=dict(
                family="Arial",
                size=10,
                color="#808080"
            )
        )
    ]
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
try:
    fig.write_image(output_image_filename, scale=2)
    print(f"Chart saved as {output_image_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    print("Please ensure you have 'kaleido' installed (`pip install kaleido`)")
    sys.exit(1)