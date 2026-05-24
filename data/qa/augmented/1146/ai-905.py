import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path_str = sys.argv[1]
json_path = pathlib.Path(json_path_str)

if not json_path.is_file():
    print(f"Error: File not found at {json_path_str}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors[0],
    textfont=dict(
        family="Arial",
        size=14,
        color='#333333',
        weight='bold'
    ),
    cliponaxis=False
))

annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            text=texts['source'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.18,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=12, color='grey')
        )
    )

fig.update_layout(
    plot_bgcolor='white',
    font=dict(family="Arial"),
    showlegend=False,
    xaxis=dict(
        showgrid=False,
        linecolor='lightgray',
        ticks='outside'
    ),
    yaxis=dict(
        title=texts.get('ylabel'),
        range=[0, 500],
        showgrid=True,
        gridcolor='#E5E5E5',
        linecolor='lightgray',
        ticks='outside',
        zeroline=False
    ),
    margin=dict(l=80, r=40, t=40, b=120),
    annotations=annotations
)

output_filename_base = json_path.stem
output_png = f"{output_filename_base}.png"

fig.write_image(output_png, scale=2)

print(f"Chart saved to {output_png}")