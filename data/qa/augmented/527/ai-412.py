import sys
import json
import plotly.graph_objects as go
import pathlib

if len(sys.argv) != 2:
    print(f"Usage: {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])

if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

x_values = [d['x'] for d in chart_data]
y_values = [d['y'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    textposition='outside',
    marker_color=colors[0],
    texttemplate='%{text:.2f}',
    hoverinfo='none',
    cliponaxis=False
))

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=100),
    xaxis=dict(
        title_text=texts.get('xaxis_title'),
        showgrid=False,
        linecolor='black',
        ticks='outside'
    ),
    yaxis=dict(
        title_text=texts.get('yaxis_title'),
        range=[0, 7],
        tickmode='array',
        tickvals=[i for i in range(8)],
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False
    ),
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=0.98, y=-0.15,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(size=12, color='#666666')
    )

output_filename = json_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")