import sys
import json
import plotly.graph_objects as go

# Ensure a file path is provided
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Derive the output filename base from the input JSON path
filename_base = json_path.split('/')[-1].split('.')[0]

# Load data and settings from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for the chart
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', {})

labels = [item['label'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors.get('series'),
    hoverinfo='label+percent',
    textinfo='value',
    texttemplate='%{value:.1f}%',
    textfont=dict(
        family="Arial",
        size=16,
        color=colors.get('text')
    ),
    sort=False,
    direction='clockwise',
    rotation=23.4
)

# Create the figure and update the layout
fig = go.Figure(data=[pie_trace])

# Build title string
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        xanchor='center',
        font=dict(
            size=24
        )
    ),
    font=dict(
        family="Arial",
        color=colors.get('text')
    ),
    paper_bgcolor=colors.get('background'),
    plot_bgcolor=colors.get('background'),
    showlegend=True,
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.2,
        xanchor='center',
        x=0.5,
        font=dict(
            color=colors.get('legend_text')
        )
    ),
    margin=dict(t=100, b=120, l=40, r=40)
)

# Generate and save the image
output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")