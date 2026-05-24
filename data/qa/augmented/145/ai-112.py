import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False,
    textfont=dict(
        family='Arial',
        size=12
    )
))

annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(
                family='Arial',
                size=12,
                color='grey'
            )
        )
    )

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='#f8f9fa',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 800],
        tickmode='linear',
        dtick=100,
        gridcolor='#e0e0e0',
        zerolinecolor='#e0e0e0',
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=40, b=100),
    showlegend=False,
    annotations=annotations
)

output_filename = json_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")