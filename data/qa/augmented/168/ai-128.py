import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
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
    texttemplate='%{y}%',
    textposition='outside',
    hoverinfo='none',
    cliponaxis=False
))

fig.update_traces(
    textfont=dict(
        family="Arial",
        size=14,
        color='black'
    )
)

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=120),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 50],
        tickvals=[0, 10, 20, 30, 40, 50],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        zeroline=False,
        linecolor='black',
        linewidth=1
    ),
    xaxis=dict(
        showline=True,
        linecolor='black',
        linewidth=1,
        automargin=True
    ),
    annotations=[
        dict(
            text=texts['source'] if texts['source'] else '',
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.25,
            xanchor='right',
            yanchor='top',
            font=dict(size=12, color='#666666')
        )
    ]
)

output_filename = json_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")