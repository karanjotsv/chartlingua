import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>", file=sys.stderr)
    sys.exit(1)

json_file_path = sys.argv[1]

# Load chart configuration from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_file_path}", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON in file {json_file_path}", file=sys.stderr)
    sys.exit(1)

# Extract data, texts, and colors from the configuration
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
legend_labels = texts['legend_labels']

# Prepare data series for Plotly
categories = [item['category'] for item in chart_data]
num_series = len(legend_labels)
series_data = [[item['values'][i] for item in chart_data] for i in range(num_series)]

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each data series
for i in range(num_series):
    fig.add_trace(go.Bar(
        x=categories,
        y=series_data[i],
        name=legend_labels[i],
        marker_color=colors[i]
    ))

# Combine title and subtitle for the main chart title
title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

# Combine source and note for an annotation below the chart
source_note_parts = []
if texts.get('source'):
    source_note_parts.append(texts['source'])
if texts.get('note'):
    source_note_parts.append(texts['note'])
source_note_text = "<br>".join(source_note_parts)

# Apply layout settings to the figure
fig.update_layout(
    barmode='group',
    font_family="Arial",
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        tickangle=-45
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 60],
        gridcolor='#D3D3D3'
    ),
    plot_bgcolor='white',
    legend=dict(
        orientation='v',
        yanchor='top',
        y=1,
        xanchor='right',
        x=1
    ),
    margin=dict(l=80, r=40, t=50, b=180),
    annotations=[
        dict(
            showarrow=False,
            text=source_note_text,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.38,
            xanchor='left',
            yanchor='top',
            align='left'
        )
    ] if source_note_text else []
)

# Derive the output PNG filename from the input JSON filename
output_image_path = os.path.splitext(json_file_path)[0] + '.png'

# Save the generated chart to a PNG file
fig.write_image(output_image_path, scale=2)