import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

x_values = [d['x'] for d in data]
y_values = [d['y'] for d in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=y_values,
    texttemplate='%{y:.1f}',
    textposition='outside',
    cliponaxis=False
))

fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=20, t=50, b=100),
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickmode='array',
        tickvals=x_values,
        title_text=texts['x_axis_title'],
        type='category'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 15.5],
        tickvals=[0, 2.5, 5, 7.5, 10, 12.5, 15],
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False,
        showline=False
    ),
    annotations=[
        dict(
            xref="paper", yref="paper",
            x=0, y=-0.2,
            xanchor='left', yanchor='bottom',
            text=texts['note'],
            showarrow=False,
            align='left'
        ),
        dict(
            xref="paper", yref="paper",
            x=1, y=-0.2,
            xanchor='right', yanchor='bottom',
            text=texts['source'],
            showarrow=False,
            align='right'
        )
    ]
)

fig.update_traces(
    textfont=dict(
        family="Arial",
        size=12,
        color="black"
    )
)

output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")