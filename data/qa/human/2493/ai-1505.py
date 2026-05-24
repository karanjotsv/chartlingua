import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

data = chart_info['chart_data'][0]
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

fig.add_trace(go.Bar(
    x=data['x'],
    y=data['y'],
    orientation='h',
    marker=dict(color=colors[0]),
    text=data['x'],
    textposition='outside',
    texttemplate='%{text:.2f}',
    cliponaxis=False
))

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=100, r=40, t=40, b=80),
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False,
        showline=False,
        range=[0, max(data['x']) * 1.18]
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor='black',
        linewidth=1
    ),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10, color='grey')
        )
    ]
)

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")