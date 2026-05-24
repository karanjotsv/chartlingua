import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly Pie chart
values = [d['value'] for d in chart_data]
# The legend in the original image has the label and value.
# We will combine them with an HTML line break for the Plotly legend.
legend_labels = [f"{d['label']}<br>{d['value']}%" for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=legend_labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(width=0)
    ),
    hole=0,
    sort=False,
    direction='clockwise',
    textinfo='none',
    hoverinfo='label+percent',
    domain=dict(x=[0.0, 0.7]) # Allocate left 70% of the space for the pie
))

# Combine title and subtitle
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Combine source and note for an annotation
source_note_parts = []
if texts.get('source'):
    source_note_parts.append(texts['source'])
if texts.get('note'):
    source_note_parts.append(texts['note'])
source_note_text = "<br>".join(source_note_parts)

# Set up layout properties
layout_options = {
    'title': {
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'family': "Arial", 'size': 32, 'color': 'black'}
    },
    'legend': {
        'orientation': 'v',
        'yanchor': 'middle',
        'y': 0.5,
        'xanchor': 'left',
        'x': 0.75,
        'font': {'family': "Arial", 'size': 18, 'color': 'black'},
        'bgcolor': 'rgba(0,0,0,0)'
    },
    'font': {'family': "Arial", 'size': 14, 'color': 'black'},
    'paper_bgcolor': 'white',
    'plot_bgcolor': 'white',
    'margin': {'l': 20, 'r': 20, 't': 100, 'b': 40},
    'shapes': [
        {
            'type': 'rect',
            'xref': 'paper', 'yref': 'paper',
            'x0': 0, 'y0': 0, 'x1': 1, 'y1': 1,
            'line': {'color': 'darkgrey', 'width': 2}
        }
    ]
}

if source_note_text:
    fig.add_annotation(
        text=source_note_text,
        xref="paper", yref="paper",
        x=0.01, y=-0.01,
        xanchor="left", yanchor="top",
        align="left",
        showarrow=False,
        font=dict(family="Arial", size=12, color="grey")
    )
    # Increase bottom margin to accommodate the source/note text
    layout_options['margin']['b'] = 80

fig.update_layout(**layout_options)

# Generate output filename from input JSON path
base_path = os.path.splitext(json_path)[0]
output_filename = f"{base_path}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")