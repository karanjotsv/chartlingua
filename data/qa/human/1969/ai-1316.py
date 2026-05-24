import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = config.get('chart_data', {})
texts = config.get('texts', {})
colors = config.get('colors', [])

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=chart_data.get('labels', []),
    values=chart_data.get('values', []),
    marker=dict(
        colors=colors,
        line=dict(color='#ffffff', width=2)
    ),
    textinfo='label',
    textposition='outside',
    sort=False,
    direction='clockwise',
    automargin=True
))

fig.update_layout(
    showlegend=False,
    font=dict(family="Arial"),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=80, r=80, t=40, b=40),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=0.02,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=12, color='#808080')
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")