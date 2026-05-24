import sys
import json
import pathlib
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Create subplots
fig = make_subplots(
    rows=2,
    cols=3,
    subplot_titles=[d['media_type'] for d in chart_data]
)

# Iterate through each media type to populate subplots
for i, media_data in enumerate(chart_data):
    row = i // 3 + 1
    col = i % 3 + 1

    # Add traces for each reason
    for j, reason_data in enumerate(media_data['reasons']):
        hex_color = colors[j % len(colors)]
        h = hex_color.lstrip('#')
        rgb = tuple(int(h[k:k+2], 16) for k in (0, 2, 4))
        fill_color_rgba = f'rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.5)'

        fig.add_trace(go.Scatter(
            x=media_data['x_values'],
            y=reason_data['y_values'],
            name=reason_data['name'],
            legendgroup=reason_data['name'],
            showlegend=(i == 0),
            mode='lines',
            line=dict(width=1.5, color=hex_color),
            fill='tozeroy',
            fillcolor=fill_color_rgba
        ), row=row, col=col)

# Update layout
title_text = f"<b>{texts.get('title', '')}</b><br><span style='font-size: 13px;'>{texts.get('subtitle', '')}</span>"
xaxis_tickvals = [1, 60, 3600, 86400, 604800, 2.6e6, 3.15e7, 3.15e8]
xaxis_ticktext = ['1s', '1m', '1h', '1d', '1wk 1mo', '1yr', '10yrs']


fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    margin=dict(l=40, r=40, b=180, t=100),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.15,
        xanchor="center",
        x=0.5,
        title_text=texts.get('legend_title', '')
    ),
    xaxis5_title=texts.get('xaxis_title', '')
)

# Update all axes
fig.update_xaxes(
    type='log',
    tickvals=xaxis_tickvals,
    ticktext=xaxis_ticktext,
    gridcolor='lightgrey',
    linecolor='black',
    mirror=True,
    ticks='outside'
)

fig.update_yaxes(
    showticklabels=False,
    showgrid=False,
    zeroline=False,
    linecolor='black',
    mirror=True,
    ticks=''
)

# Add annotations for notes
fig.add_annotation(
    text=texts.get('note', ''),
    xref="paper",
    yref="paper",
    x=0.5,
    y=-0.4,
    xanchor='center',
    yanchor='bottom',
    showarrow=False,
    align="left",
    font=dict(size=11)
)

# Style subplot titles to match original (left-aligned)
for ann in fig.layout.annotations:
    if ann.text in [d['media_type'] for d in chart_data]:
        ann.update(x=0.02, xanchor='left', font=dict(size=12))

# Generate output filename from JSON path
filename_base = pathlib.Path(json_path).stem
output_filename = f"{filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")