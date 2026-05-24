import sys
import json
import plotly.graph_objects as go
import math
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for plotting
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

labels = [d['category'] for d in data]
values = [d['value'] for d in data]

# Prepare text for inside the slices (only for larger values)
inside_text = [str(d['value']) if d['value'] >= 10 else '' for d in data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='white', width=1)),
    hoverinfo='label+percent',
    text=inside_text,
    textinfo='text',
    textfont=dict(family="Arial", size=16, color='white'),
    sort=False,
    direction='clockwise',
    rotation=137 # Adjusted to match the visual start angle
)

fig = go.Figure(data=[pie_trace])

# --- Create annotations for outside labels ---
annotations = []
total_value = sum(values)
current_angle = math.radians(137) # Must match rotation
pull_factors = {
    'Wikimedia Commons': 0.03,
    'Flickr': 0.03,
    'Own website': 0.03
} # small pull for better label placement if needed, but not used here.

for i in range(len(data)):
    slice_angle = (values[i] / total_value) * 2 * math.pi
    mid_angle = current_angle - slice_angle / 2

    # Annotation text position
    label_radius = 1.3
    x_text = label_radius * math.cos(mid_angle)
    y_text = label_radius * math.sin(mid_angle)

    # Arrow anchor position (on the pie chart's edge)
    arrow_radius = 1.05
    ax_coord = arrow_radius * math.cos(mid_angle)
    ay_coord = arrow_radius * math.sin(mid_angle)
    
    # Adjust text alignment based on quadrant
    if x_text > 0:
        align = 'left'
    else:
        align = 'right'

    annotations.append(go.layout.Annotation(
        x=x_text,
        y=y_text,
        text=f"{data[i]['category']}<br>{data[i]['percentage']}%",
        showarrow=True,
        arrowhead=0,
        ax=ax_coord,
        ay=ay_coord,
        xref="x",
        yref="y",
        axref="x",
        ayref="y",
        font=dict(family="Arial", size=12, color='#555555'),
        align=align
    ))
    
    current_angle -= slice_angle

# --- Configure layout ---
title_text = texts['title']
if texts['subtitle']:
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        xanchor='left',
        y=0.95,
        yanchor='top',
        font=dict(family="Arial", size=22, color='black')
    ),
    showlegend=False,
    font=dict(family="Arial"),
    margin=dict(l=40, r=40, t=100, b=40),
    # Set a square aspect ratio with defined range to place annotations correctly
    xaxis=dict(range=[-1.8, 1.8], visible=False, scaleanchor="y", scaleratio=1),
    yaxis=dict(range=[-1.8, 1.8], visible=False),
    annotations=annotations,
    paper_bgcolor='white',
    plot_bgcolor='white'
)


# --- Output the image ---
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")