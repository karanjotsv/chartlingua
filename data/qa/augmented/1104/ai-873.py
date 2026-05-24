import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)

# Extract data and texts from the JSON object
data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Format text labels to match original (e.g., "35" instead of "35.0")
text_labels = []
for v in values:
    if v == int(v):
        text_labels.append(str(int(v)))
    else:
        text_labels.append(f'{v:.1f}')

# Create the figure
fig = go.Figure()

# Add bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=text_labels,
    textposition='outside',
    marker_color=colors[0] if colors else None,
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False  # Prevent text labels from being clipped
))

# Update layout
fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 500],
        showgrid=True,
        gridcolor='#E5E5E5',
        gridwidth=1,
        griddash='dot',
        showline=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=100),  # Adjust bottom margin for source
    annotations=[]
)

# Add source annotation if present
source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.2, # Position below the x-axis
        xanchor='right',
        yanchor='top',
        font=dict(family="Arial", size=12, color='grey')
    )

# Define output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)