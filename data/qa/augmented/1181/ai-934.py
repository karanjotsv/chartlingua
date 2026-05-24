import sys
import json
import plotly.graph_objects as go
import pathlib

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]
base_filename = pathlib.Path(json_file_path).stem
output_image_path = f"{base_filename}.png"

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors,
    text=[f"{y}%" for y in y_values],
    textposition='outside',
    cliponaxis=False,
    textfont=dict(family="Arial", size=14, color='black')
))

fig.update_layout(
    font=dict(family="Arial", size=12, color='black'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        ticks='',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 60],
        tickvals=[0, 10, 20, 30, 40, 50, 60],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        showline=False,
        ticks=''
    ),
    margin=dict(l=90, r=40, b=120, t=40),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.25,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=12)
        )
    ]
)

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")