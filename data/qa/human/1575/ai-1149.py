import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check if a file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file {json_path} was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file {json_path} is not a valid JSON file.")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly, reversing the order for horizontal bar charts
# Plotly plots y-axis categories from bottom to top, so we reverse to match the image
categories = [d['category'] for d in chart_data][::-1]
values = [d['value'] for d in chart_data][::-1]
labels = [d['label'] for d in chart_data][::-1]
bar_colors = colors[::-1]

# Create the figure object
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    text=labels,
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=12
    ),
    marker_color=bar_colors,
    orientation='h',
    hoverinfo='none',
    cliponaxis=False # Allows text to render outside the plot area
))

# Update the layout of the chart to match the original image
fig.update_layout(
    # Set global font
    font=dict(family="Arial"),
    
    # Configure the title and its position
    title=dict(
        text=texts.get('title'),
        font=dict(size=20),
        x=0.01,
        xanchor='left',
        y=0.95,
        yanchor='top'
    ),
    
    # Use a white background for the plot area
    plot_bgcolor='white',
    
    # Hide the legend as there's only one data series
    showlegend=False,

    # Configure the x-axis
    xaxis=dict(
        showgrid=True,
        gridcolor='#e5e5e5',
        gridwidth=1,
        zeroline=False,
        showline=False,
        showticklabels=True,
        tickprefix='$',
        tickformat=',.0f'
    ),
    
    # Configure the y-axis
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        ticks='outside',
        ticklen=8
    ),
    
    # Add annotations for the source text
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.28,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(size=11, color='#666666')
        )
    ],

    # Set margins to prevent clipping of title and source text
    margin=dict(l=100, r=120, t=80, b=220)
)

# Determine the output filename from the input JSON path
base_filename = Path(json_path).stem
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image with a high resolution
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")