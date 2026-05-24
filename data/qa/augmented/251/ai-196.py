import sys
import json
import plotly.graph_objects as go
import pathlib

if len(sys.argv) != 2:
    print("Usage: python script.name.py <path_to_json_file>")
    sys.exit(1)

json_path_str = sys.argv[1]
json_path = pathlib.Path(json_path_str)

if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
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
    marker_color=colors[0],
    texttemplate='<b>%{y}%</b>',
    textposition='outside',
    textfont=dict(family="Arial", size=14, color='black'),
    cliponaxis=False
))

fig.update_layout(
    font=dict(family="Arial", size=12, color='black'),
    title_text=None,
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 70],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#E5E5E5',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=True,
        linecolor='black'
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showline=True,
        linecolor='black'
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=120),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            align='right'
        )
    ]
)

output_filename = json_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")