import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Prepare data for Plotly
x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

# Create figure
fig = go.Figure()

# Add bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0] if colors else None,
    text=[f"{texts.get('y_axis_prefix', '')}{y:.2f}" for y in y_values],
    textposition='outside',
    cliponaxis=False,
    hoverinfo='skip'
))

# Update layout
title_text = f"<b>{texts.get('title', '')}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis={
        'title_text': texts.get('x_axis_title'),
        'showgrid': False,
        'tickmode': 'array',
        'tickvals': x_values,
        'ticktext': x_values
    },
    yaxis={
        'title_text': texts.get('y_axis_title'),
        'range': [0, 8.00],
        'showgrid': True,
        'gridcolor': '#D3D3D3',
        'tickprefix': texts.get('y_axis_prefix', ''),
        'tickformat': '.2f'
    },
    font={
        'family': "Arial",
        'size': 12,
        'color': "black"
    },
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(t=80, b=50, l=70, r=30)
)

fig.update_traces(textfont_size=11)

# Determine output filename
output_filename = pathlib.Path(json_path).stem + ".png"

# Save image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")