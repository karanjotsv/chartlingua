import sys
import json
import os
import plotly.graph_objects as go

# Check if the command-line argument for the JSON file is provided
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

# Load data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data_json = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON object
chart_data = chart_data_json.get('chart_data', [])
texts = chart_data_json.get('texts', {})
colors = chart_data_json.get('colors', ['#1f77b4'])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=values,
    textposition='outside',
    textfont=dict(family="Arial", size=14, color='black'),
    cliponaxis=False # Prevent text from being clipped at the top
))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title_text=None, # No main title from JSON
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=14),
        showgrid=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showline=False,
        showgrid=True,
        gridwidth=1,
        gridcolor='#E5E5E5',
        zeroline=False,
        showticklabels=False, # Y-axis ticks are not visible in the original
        range=[0, max(values) * 1.2] # Provide headroom for text labels
    ),
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=80),
    annotations=[
        dict(
            text=texts.get('source', ''),
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.2, # Position below the chart
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=12, color='#666666')
        )
    ]
)

# Determine the output image filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully generated and saved as {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)