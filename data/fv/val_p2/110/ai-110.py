import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = sys.argv[1]

# Check if the file exists
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Derive the base filename for the output image
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='white', width=1) # Add white borders between slices
    ),
    texttemplate='%{label}<br>%{value}%',
    textposition='inside',
    insidetextfont=dict(color='black'),
    hoverinfo='label+percent',
    sort=False,  # Preserve the order from the JSON file
    rotation=90, # Start the first slice at the top (12 o'clock)
    direction='clockwise'
)

# Create the figure
fig = go.Figure(data=[pie_trace])

# Update layout
fig.update_layout(
    title=dict(
        text=f"<b>{texts.get('title', '')}</b>",
        x=0.5,
        xanchor='center',
        yanchor='top',
        y=0.95
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    showlegend=False,
    margin=dict(l=40, r=40, t=100, b=100), # Adjust margins for title and source
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            xref="paper",
            yref="paper",
            x=0.98,
            y=-0.1,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10)
        )
    ]
)

# Write the output image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error writing image file: {e}")
    sys.exit(1)