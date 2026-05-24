import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_details.get('chart_data', [])
texts = chart_details.get('texts', {})
colors = chart_details.get('colors', [])

fig = go.Figure()

fig.add_trace(go.Bar(
    x=[d['category'] for d in chart_data],
    y=[d['value'] for d in chart_data],
    marker_color=colors[0] if colors else None,
    name=''
))

annotations = []
if texts.get('source_left'):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=0, y=-0.15,
            xanchor='left', yanchor='top',
            text=texts['source_left'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="blue")
        )
    )

if texts.get('source_right'):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=1, y=-0.15,
            xanchor='right', yanchor='top',
            align='right',
            text=texts['source_right'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="grey")
        )
    )

fig.update_layout(
    title_text=texts.get('title'),
    yaxis_title_text=texts.get('y_axis_title'),
    xaxis_title_text=texts.get('x_axis_title'),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=120),
    yaxis=dict(
        showgrid=True,
        gridcolor='#e5e5e5',
        range=[0, 5000000],
        tickvals=[0, 1000000, 2000000, 3000000, 4000000, 5000000],
        ticktext=['0', '1 000 000', '2 000 000', '3 000 000', '4 000 000', '5 000 000'],
        zeroline=False
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1
    ),
    annotations=annotations
)

output_path = pathlib.Path(json_path).with_suffix('.png')
fig.write_image(str(output_path), scale=2)

print(f"Chart saved to {output_path}")