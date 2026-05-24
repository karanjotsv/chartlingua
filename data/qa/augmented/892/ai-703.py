import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Derive output filename from input JSON filename
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

# Read and decode the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_file_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_file_path}' contains invalid JSON.")
    sys.exit(1)

# Extract data, texts, and colors from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', ['#1f77b4'])

# Prepare data for plotting
categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=colors[0],
    text=[f'{v:.1f}' for v in values],
    textposition='outside',
    cliponaxis=False,  # Ensures text is not clipped by the plotting area
    textfont=dict(family="Arial", size=12, color='black')
))

# Configure the layout
max_value = max(values) if values else 0
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        range=[0, max_value * 1.25]  # Add padding for text labels
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black'
    ),
    margin=dict(l=250, r=40, t=40, b=80),  # Adjust margins for labels
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=1.0, y=-0.2,
            xanchor='right', yanchor='top',
            text=texts.get('source'),
            showarrow=False,
            font=dict(family="Arial", size=12)
        )
    ]
)

# Generate the image file
fig.write_image(output_image_path, scale=2)

print(f"Chart successfully generated at: {output_image_path}")