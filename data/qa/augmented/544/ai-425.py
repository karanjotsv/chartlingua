import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_filepath = sys.argv[1]

try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_filepath}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_filepath}'")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)],
        text=series['y'],
        textposition='outside',
        textfont=dict(family='Arial', size=12, color='black'),
        cliponaxis=False
    ))

fig.update_layout(
    font=dict(family="Arial"),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickvals=chart_data[0]['x'],
        showgrid=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 1800],
        gridcolor='#e0e0e0'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(t=50, b=80, l=80, r=40),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            xref='paper',
            yref='paper',
            x=1,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(size=12)
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_filepath))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")