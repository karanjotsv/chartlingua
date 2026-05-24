import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for plotting from the JSON structure
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Prepare data lists for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
labels = [item['label'] for item in chart_data]

# Initialize the figure
fig = go.Figure()

# Add the bar trace with data and styling from the JSON
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=labels,
    textposition='outside',
    marker_color=colors,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    cliponaxis=False  # Prevent text labels from being clipped at the top
))

# Format the title text
title_text = f"<b>{texts['title']}</b>" if texts.get('title') else ""

# Configure the layout of the chart
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center',
        font=dict(family="Arial", size=16)
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(family="Arial")
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        range=[0, 8.1],
        dtick=2,
        tickfont=dict(family="Arial")
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    font=dict(
        family="Arial"
    ),
    margin=dict(t=80, b=120, l=40, r=40)  # Adjust margins for title and x-axis labels
)

# Determine the output filename from the input JSON path
base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully saved to {output_filename}")