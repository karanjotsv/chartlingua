import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

labels = [d['label'] for d in chart_data['chart_data']]
values = [d['value'] for d in chart_data['chart_data']]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=chart_data['colors']),
    sort=False,
    direction='clockwise',
    textinfo='none',
    hole=0
))

title_text = chart_data['texts']['title']
if chart_data['texts']['subtitle']:
    title_text += f"<br><sub>{chart_data['texts']['subtitle']}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.5,
        font=dict(size=18)
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    showlegend=True,
    legend=dict(
        x=0.85,
        y=0.7,
        xanchor='left',
        yanchor='middle'
    ),
    margin=dict(l=40, r=40, t=100, b=180),
    annotations=[
        dict(
            text=chart_data['texts']['source'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.25,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(size=10)
        )
    ]
)

filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")