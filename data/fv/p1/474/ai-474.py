import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the JSON file exists
if not pathlib.Path(json_path).is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read and parse the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_data_json = json.load(f)

# Extract data from JSON
chart_data = chart_data_json.get('chart_data', [])
texts = chart_data_json.get('texts', {})
colors = chart_data_json.get('colors', [])

# Prepare data for Plotly
values = [d['value'] for d in chart_data]
pie_text = [f"<b>{d['label']}</b><br>{d['value']}<br>{d['percentage']}%" for d in chart_data]
text_colors = [d['text_color'] for d in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    values=values,
    text=pie_text,
    marker=dict(colors=colors, line=dict(color='white', width=2)),
    hoverinfo='none',
    textinfo='text',
    textfont=dict(
        family='Arial',
        size=14,
        color=text_colors
    ),
    sort=False,
    direction='counterclockwise',
    rotation=-40
)

fig = go.Figure(data=[pie_trace])

# Combine title and subtitle
title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Configure layout
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top',
        font=dict(family='Arial', size=20)
    ),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(family='Arial', size=12),
    margin=dict(l=40, r=40, t=100, b=80),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.1,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(family='Arial', size=10)
        ),
        dict(
            text=texts.get('total_label', ''),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.87,
            y=0.9,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(family='Arial', size=14)
        )
    ]
)

# Determine output filename and save the image
output_filename = pathlib.Path(json_path).stem + '.png'
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")