import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
    
# Derive the output filename base from the input JSON path
filename_base = os.path.splitext(os.path.basename(json_path))[0]

# Load data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)


data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

# Prepare data for Plotly
labels = [item['category'] for item in data]
values = [item['value'] for item in data]

# Define text colors for each slice to ensure readability
# Based on original image: white text on dark slices, black on light slices
text_colors = ['white', 'white', 'white', 'black', 'black', 'white', 'black']

# Create the figure
fig = go.Figure()

# Add the pie chart trace
fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    pull=[0.05] * len(values),
    textinfo='value',
    textfont=dict(
        family='Arial',
        size=14,
        color=text_colors
    ),
    hoverinfo='label+percent+value',
    sort=False,
    direction='clockwise',
    rotation=80  # Adjust rotation to match the original chart's starting point
))

# Update layout
fig.update_layout(
    showlegend=True,
    font=dict(
        family="Arial",
        size=12
    ),
    legend=dict(
        x=0.9,
        y=0.95,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(0,0,0,0)',
        traceorder='normal'
    ),
    width=900,
    height=550,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=50, r=350, t=50, b=50) # Increased right margin for legend
)

# Generate the output image file
output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")