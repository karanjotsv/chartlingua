import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = sys.argv[1]
json_path = Path(json_file_path)

# Ensure the JSON file exists
if not json_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Derive output filename from JSON filename
output_filename = f"{json_path.stem}.png"

# Load data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors,
    texttemplate='%{y:.2f}%',
    textposition='inside',
    textfont=dict(
        family="Arial",
        size=14,
        color=['black' if v > 0 else 'white' for v in values] # Dynamic text color
    ),
    hoverinfo='none',
    insidetextanchor='end'
))

# Update layout to match the original image
fig.update_layout(
    title_text=f"<b>{texts['title']}</b>",
    title_x=0.05,
    title_y=0.95,
    title_font=dict(family="Arial", size=24, color='#595959'),
    
    xaxis_title=f"<b>{texts['x_axis_title']}</b>",
    yaxis_title=texts['y_axis_title'],
    
    font=dict(family="Arial", size=12, color="black"),
    
    yaxis=dict(
        range=[-5, 15.5],
        dtick=5,
        tickformat='.2f',
        ticksuffix='%',
        gridcolor='#e0e0e0',
        zeroline=True,
        zerolinewidth=1.5,
        zerolinecolor='black'
    ),
    
    xaxis=dict(
        showgrid=False
    ),
    
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(t=100, b=100, l=80, r=40)
)

# Write the image to a file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")