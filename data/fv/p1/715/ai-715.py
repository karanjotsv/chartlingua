import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Load data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data from the JSON structure
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})

# Prepare data for the main pie chart
main_labels = []
main_values = []
main_colors = []
breakdown_data = None

for item in chart_data:
    main_labels.append(item['label'])
    main_values.append(item['value'])
    main_colors.append(item['color'])
    if 'breakdown' in item:
        breakdown_data = item['breakdown']

# Prepare data for the breakdown pie chart
if breakdown_data:
    breakdown_labels = [d['label'] for d in breakdown_data]
    breakdown_values = [d['value'] for d in breakdown_data]
    breakdown_colors = [d['color'] for d in breakdown_data]
    
    # Custom text formatting for labels inside slices
    main_text = [f"<b>{d['label']}</b><br>{d['value']}%" for d in chart_data]
    breakdown_text = [f"<b>{d['label']}</b><br>{d['value']:g}%" for d in breakdown_data]

# Create the figure with two pie charts using domains
fig = go.Figure()

# Main pie chart
fig.add_trace(go.Pie(
    labels=main_labels,
    values=main_values,
    marker=dict(colors=main_colors, line=dict(color='#FFFFFF', width=1)),
    text=main_text,
    textinfo='text',
    textfont=dict(size=14, family="Arial"),
    hoverinfo='label+percent',
    domain={'x': [0, 0.48], 'y': [0.1, 0.9]},
    name='Main Sources',
    sort=False,
    direction='clockwise'
))

# Breakdown pie chart
if breakdown_data:
    fig.add_trace(go.Pie(
        labels=breakdown_labels,
        values=breakdown_values,
        marker=dict(colors=breakdown_colors, line=dict(color='#FFFFFF', width=1)),
        text=breakdown_text,
        textinfo='text',
        textfont=dict(size=14, family="Arial"),
        hoverinfo='label+percent',
        domain={'x': [0.52, 1.0], 'y': [0.1, 0.9]},
        name='Renewables Breakdown',
        sort=False,
        direction='clockwise'
    ))

# Configure layout
fig.update_layout(
    title_text=texts.get('title'),
    title_x=0.5,
    title_y=0.95,
    title_xanchor='center',
    title_yanchor='top',
    title_font=dict(size=20, family="Arial"),
    showlegend=False,
    font=dict(family="Arial"),
    width=1000,
    height=500,
    margin=dict(l=20, r=20, t=80, b=20),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

# Add connector lines between the two charts
fig.add_shape(
    type="line",
    xref="paper", yref="paper",
    x0=0.46, y0=0.8, x1=0.54, y1=0.9,
    line=dict(color="grey", width=1)
)
fig.add_shape(
    type="line",
    xref="paper", yref="paper",
    x0=0.46, y0=0.2, x1=0.54, y1=0.1,
    line=dict(color="grey", width=1)
)

# Generate the output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")