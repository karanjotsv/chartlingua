import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]
output_image_path = os.path.splitext(json_file_path)[0] + ".png"

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#ffffff', width=2)),
    texttemplate='%{label} %{value}%',
    textposition='outside',
    sort=False,
    direction='clockwise'
)])

fig.update_layout(
    showlegend=False,
    font=dict(family="Arial", size=14, color="black"),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=80, r=80, t=50, b=50),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            xref="paper",
            yref="paper",
            x=0.98,
            y=0.01,
            xanchor='right',
            yanchor='bottom',
            font=dict(family="Arial", size=12, color="grey")
        )
    ]
)

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")