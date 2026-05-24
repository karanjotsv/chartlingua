import sys
import json
import plotly.graph_objects as go
import pathlib

# This script must be run from the command line with the JSON file path as an argument.
# Example: python <script_name>.py <path_to_json_file>.json

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
filename_base = pathlib.Path(json_path).stem

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(
        colors=colors,
        line=dict(color='#000000', width=1)
    ),
    sort=False,
    direction='clockwise',
    rotation=105,
    textinfo='none',
    domain=dict(x=[0.02, 0.62], y=[0.1, 0.9])
))

source_text = texts.get('source', '')

fig.update_layout(
    showlegend=True,
    legend=dict(
        x=0.65,
        y=0.95,
        xanchor='left',
        yanchor='top',
        bgcolor='white',
        bordercolor='black',
        borderwidth=1,
        font=dict(size=14)
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    paper_bgcolor='white',
    margin=dict(l=20, r=20, t=20, b=150),
    shapes=[
        dict(
            type="rect",
            xref="paper", yref="paper",
            x0=0, y0=0, x1=0.64, y1=1,
            fillcolor='#D3D3D3',
            layer="below",
            line_width=0
        )
    ],
    annotations=[
        dict(
            text=source_text,
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.01,
            y=0,
            xanchor='left',
            yanchor='bottom',
            align='left',
            font=dict(size=10)
        )
    ]
)

output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2, width=950, height=650)

print(f"Chart saved to {output_filename}")