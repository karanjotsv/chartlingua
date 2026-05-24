import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data for plotting
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]
errors = [item['error'] for item in data]

# Create the bar chart trace
bar_trace = go.Bar(
    x=categories,
    y=values,
    marker_color=colors['bar_color'],
    error_y=dict(
        type='data',
        array=errors,
        visible=True,
        color=colors['error_bar_color'],
        thickness=1.5,
        width=4
    ),
    name=''
)

# Initialize the figure
fig = go.Figure(data=[bar_trace])

# Combine title and subtitle
title_text = f"<b>{texts['title']}</b>"
if texts['subtitle']:
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Combine source and note for annotation
source_text_parts = []
if texts.get('source'):
    source_text_parts.append(texts['source'])
if texts.get('note'):
    source_text_parts.append(texts['note'])
source_text = "<br>".join(source_text_parts)

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        tickangle=-90,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=False
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 105],
        tickvals=[0, 50, 100],
        side='right',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        showgrid=False
    ),
    plot_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    margin=dict(l=50, r=80, b=250, t=120),
    showlegend=False,
    bargap=0.2
)

# Add dashed line at 90%
fig.add_shape(
    type="line",
    x0=-0.5, y0=90, x1=len(categories) - 0.5, y1=90,
    line=dict(
        color=colors['dashed_line_color'],
        width=2,
        dash="dash",
    )
)

# Add source annotation
if source_text:
    fig.add_annotation(
        text=source_text,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.4, # Adjust this value to position the text below the x-axis labels
        xanchor='left',
        yanchor='top'
    )

# Determine output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")