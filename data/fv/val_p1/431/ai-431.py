import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

data_series = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(data_series):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines',
        line=dict(
            color=colors[i],
            width=2.5,
            dash=series['line_style']
        ),
        yaxis=series['yaxis']
    ))

fig.update_layout(
    font=dict(family="Arial", size=14),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=100, r=100, t=60, b=80),
    xaxis=dict(
        title=texts['x_axis_title'],
        tickvals=[1965, 1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010],
        showgrid=False,
        zeroline=False,
        linecolor='black',
        linewidth=1,
        ticks='outside',
        range=[1960, 2013]
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        side='left',
        range=[0, 180000000],
        showgrid=False,
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor='black',
        linecolor='black',
        linewidth=1,
        ticks='outside'
    ),
    yaxis2=dict(
        title=texts['y2_axis_title'],
        overlaying='y',
        side='right',
        range=[0, 6000000],
        showgrid=False,
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor='black',
        linecolor='black',
        linewidth=1,
        ticks='outside'
    )
)

for anno in texts.get('annotations', []):
    fig.add_annotation(anno)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart image saved to {output_filename}")