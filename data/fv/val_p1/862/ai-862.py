import sys
import json
import os
import plotly.graph_objects as go

# Ensure a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Ensure the JSON file exists
if not os.path.exists(json_file_path):
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Load all data and text from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Prepare data for Plotly
x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=y_values,
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False  # Prevents text labels from being clipped
))

# Configure the layout
fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        font=dict(family="Arial", size=16, color='black')
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        type='category',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='outside',
        showgrid=True,
        gridcolor='black',
        gridwidth=1
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 950],  # Extend range to prevent clipping of top label
        dtick=100,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='outside',
        showgrid=True,
        gridcolor='black',
        gridwidth=1
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(l=80, r=40, t=80, b=100),
    showlegend=False
)

# Add the source note at the bottom
if texts.get('source_note'):
    fig.add_annotation(
        text=texts['source_note'],
        align='center',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.5,
        y=-0.22,  # Position below x-axis title
        font=dict(family="Arial", size=12, color='black')
    )

# Determine output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart successfully generated and saved to {output_image_path}")