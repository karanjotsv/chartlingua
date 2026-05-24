import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = pathlib.Path(sys.argv[1])

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data and texts from the JSON object
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
categories = chart_data['categories']
series = chart_data['series']

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each data series, ensuring original order is preserved
for i, s in enumerate(series):
    fig.add_trace(go.Bar(
        x=categories,
        y=s['data'],
        name=s['name'],
        marker_color=colors[i],
        text=[f'<b>{val}</b>' for val in s['data']],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family='Arial',
            size=12,
            color='white'
        )
    ))

# Combine title and subtitle using HTML for proper formatting
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Configure the layout of the chart
fig.update_layout(
    barmode='stack',
    title=dict(
        text=title_text if title_text else None,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickfont=dict(family='Arial', size=12),
        showgrid=True,
        gridcolor='#f0f0f0'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        tickfont=dict(family='Arial', size=12),
        gridcolor='#e0e0e0',
        range=[0, 2500],
        dtick=500
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5,
        font=dict(family='Arial', size=12)
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family='Arial'),
    margin=dict(l=80, r=40, t=50, b=120)
)

# Add source text as an annotation at the bottom right
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper",
        yref="paper",
        x=0.98,
        y=-0.28,
        showarrow=False,
        xanchor='right',
        yanchor='bottom',
        font=dict(family='Arial', size=10, color='grey')
    )

# Determine the output filename from the input JSON path
base_filename = json_path.stem
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved as {output_filename}")