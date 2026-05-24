import sys
import json
import pathlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Read data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Create a 2x2 subplot figure
subplot_titles = [d['subplot_title'] for d in chart_data]
fig = make_subplots(rows=2, cols=2, subplot_titles=subplot_titles,
                    horizontal_spacing=0.07, vertical_spacing=0.15)

# Iterate through the subplot data and add traces
for i, subplot_spec in enumerate(chart_data):
    row = (i // 2) + 1
    col = (i % 2) + 1

    # Iterate through the series for the current subplot
    # Draw trend line first so the actuals line is on top
    sorted_series = sorted(subplot_spec['series'], key=lambda s: s['name'] != 'Trend')
    for series in sorted_series:
        series_name_lower = series['name'].lower()
        line_style = {
            'color': colors.get(series_name_lower),
            'width': 2.5 if series_name_lower == 'actual' else 1.5
        }

        fig.add_trace(go.Scatter(
            x=series['x'],
            y=series['y'],
            mode='lines',
            line=line_style,
            showlegend=False
        ), row=row, col=col)

# Update layout for a professional look
title_text = f"<b>{texts['title']}</b>" if texts.get('title') else ""

fig.update_layout(
    title_text=title_text,
    title_x=0.5,
    title_y=0.97,
    title_font_size=16,
    font_family="Arial",
    width=1100,
    height=750,
    margin=dict(t=100, b=60, l=60, r=40),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

# Left-align subplot titles and set font size
for annotation in fig['layout']['annotations']:
    annotation['x'] = 0
    annotation['xanchor'] = 'left'
    annotation['font'] = dict(size=14, color='#444444')
    annotation['y'] = annotation['y'] * 1.01 # Add a small padding from the top

# Apply grid and axis styling to all axes
grid_color = '#E5E5E5'
fig.update_xaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor=grid_color,
    zeroline=False,
    showline=True,
    linewidth=1,
    linecolor=grid_color,
    tickformat='d',
    mirror=True
)
fig.update_yaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor=grid_color,
    zeroline=False,
    showline=True,
    linewidth=1,
    linecolor=grid_color,
    mirror=True
)

# Generate output filename and save the image
output_filename = json_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")