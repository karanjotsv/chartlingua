import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Derive the output filename from the input JSON path
try:
    filename_base = json_file_path.rsplit('.', 1)[0]
except IndexError:
    filename_base = json_file_path

# Load data from JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_json = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

chart_data = chart_json['chart_data']
texts = chart_json['texts']
colors = chart_json['colors']

# Initialize figure
fig = go.Figure()

# Add data series to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines',
        name=series['name'],
        line=dict(color=colors[i], width=2.5)
    ))

# Build title string
title_text = f"<b>{texts.get('title', '')}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Build annotation string for source and note
annotation_text = ""
if texts.get('source'):
    annotation_text += texts['source']
if texts.get('note'):
    if annotation_text:
        annotation_text += "<br>"
    annotation_text += texts['note']

# Update layout
fig.update_layout(
    font_family="Arial",
    title=dict(
        text=title_text,
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=40, t=80, b=100)
)

# Update axes appearance
fig.update_xaxes(
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=False,
    showgrid=False,
    tickmode='array',
    tickvals=[1990, 1992, 1994, 1996, 1998, 2000, 2002, 2004, 2006, 2008, 2010],
    zeroline=False
)

fig.update_yaxes(
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=False,
    showgrid=True,
    gridcolor='lightgrey',
    range=[0, 2400],
    tickvals=[0, 600, 1200, 1800, 2400],
    zeroline=False
)

# Add source/note annotation if it exists
if annotation_text:
    fig.add_annotation(
        showarrow=False,
        text=annotation_text,
        xref="paper",
        yref="paper",
        x=0,
        y=-0.2, # Positioned below the x-axis title
        xanchor='left',
        yanchor='top',
        align='left',
        font=dict(size=12)
    )

# Write image file
output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")