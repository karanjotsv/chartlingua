import sys
import json
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Load chart data and configuration from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Create a figure with subplots to simulate the broken y-axis effect
fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.03,
    row_heights=[0.65, 0.35],
    specs=[[{}], [{"secondary_y": True}]]
)

# Iterate through the data series in the JSON and add them to the correct subplot
categories = chart_data['categories']
for i, series in enumerate(chart_data['series']):
    if series['plot'] == 'top':
        fig.add_trace(go.Scatter(
            x=categories,
            y=series['y'],
            name=series['name'],
            mode='lines+markers',
            marker=dict(symbol='square', size=5, color=colors[i]),
            line=dict(color=colors[i], width=2)
        ), row=1, col=1)
    elif series['plot'] == 'bottom':
        # This trace goes on the secondary y-axis of the bottom subplot
        fig.add_trace(go.Scatter(
            x=categories,
            y=series['y'],
            name=series['name'],
            mode='lines+markers',
            marker=dict(symbol='square', size=5, color=colors[i]),
            line=dict(color=colors[i], width=2),
            showlegend=False
        ), row=2, col=1, secondary_y=True)

# Update the overall layout of the chart
fig.update_layout(
    font=dict(family="Arial", size=10),
    title=dict(text=f"<b>{texts['title']}</b>", x=0.5, y=0.97, xanchor='center', font=dict(size=14)),
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.35,
        xanchor="center",
        x=0.5
    ),
    margin=dict(t=80, b=220, l=100, r=100),
    height=700,
    width=900
)

# Configure the axes for both subplots
# Top subplot axes
fig.update_yaxes(
    title_text=texts['y_axis_title_left'],
    range=[1000, 7500],
    dtick=1000,
    showgrid=True, gridwidth=1, gridcolor='#E0E0E0',
    showline=True, linewidth=1, linecolor='black',
    row=1, col=1
)
fig.update_xaxes(showticklabels=False, row=1, col=1) # Hide x-axis labels for the top plot

# Bottom subplot axes
fig.update_xaxes(
    title_text=texts['x_axis_title'],
    tickvals=[1970, 1975, 1980, 1985, 1990, 1994, 2001],
    showline=True, linewidth=1, linecolor='black',
    row=2, col=1
)
# Hide the primary (left) y-axis on the bottom subplot
fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False, row=2, col=1, secondary_y=False)
# Configure the secondary (right) y-axis for the bottom plot
fig.update_yaxes(
    range=[0, 900],
    dtick=200,
    showgrid=False, # The original doesn't have grid lines extending from this axis
    showline=True, linewidth=1, linecolor='black',
    row=2, col=1, secondary_y=True
)

# Add annotations from the JSON configuration
for ann in texts['annotations']:
    fig.add_annotation(
        text=ann['text'], x=ann['x'], y=ann['y'],
        xref=ann['xref'], yref=ann['yref'],
        showarrow=ann.get('showarrow', False),
        font=dict(size=11),
        align=ann.get('align', 'center'),
        yanchor=ann.get('yanchor', 'middle')
    )

# Add the source text as a layout annotation for proper positioning
fig.add_annotation(
    text=texts['source'],
    xref="paper", yref="paper",
    x=0, y=-0.45,
    xanchor='left', yanchor='bottom',
    showarrow=False, align='left'
)

# Add the right-side Y-axis title as an annotation to control its vertical position
fig.add_annotation(
    text=texts['y_axis_title_right_annotation'],
    xref="paper", yref="paper",
    x=1.08, y=0.55,
    xanchor='center', yanchor='middle',
    showarrow=False, textangle=-90,
    font=dict(size=12)
)

# Add shapes to the chart
# Gray background for the bottom plot
fig.add_shape(
    type="rect", xref="paper", yref="paper",
    x0=fig.layout.xaxis.domain[0], x1=fig.layout.xaxis.domain[1], y0=0, y1=0.35,
    fillcolor="#f0f0f0", layer="below", line_width=0
)
# Vertical dashed line indicating the start of the COPS grant period
fig.add_vline(x=1994, line_width=1, line_dash="dash", line_color="gray")
# Horizontal line for the "COPS grant period" annotation
fig.add_shape(type='line', x0=1994, x1=2001, y0=6900, y1=6900, xref='x1', yref='y1', line=dict(color='black', width=1))

# Add axis break marks as small diagonal lines
break_y_pos = 0.35 # Position corresponds to the top of the bottom subplot
fig.add_shape(type='line', xref='paper', yref='paper', x0=0.08, y0=break_y_pos-0.01, x1=0.10, y1=break_y_pos+0.01, line=dict(color='black', width=1))
fig.add_shape(type='line', xref='paper', yref='paper', x0=0.965, y0=break_y_pos-0.01, x1=0.985, y1=break_y_pos+0.01, line=dict(color='black', width=1))

# Generate and save the image file
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")