import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
x_axis_config = config['x_axis_config']

fig = go.Figure()

for i, series in enumerate(chart_data['series']):
    text_positions = 'top center' if series['name'] == 'Approve' else 'bottom center'
    fig.add_trace(go.Scatter(
        x=chart_data['categories'],
        y=series['y'],
        mode='lines+markers+text',
        name=series['name'],
        line=dict(color=colors[i], width=3),
        marker=dict(
            symbol='circle',
            color='white',
            size=9,
            line=dict(color=colors[i], width=2.5)
        ),
        text=series['y'],
        textposition=text_positions,
        textfont=dict(
            family='Arial',
            size=12,
            color='#444444'
        )
    ))

annotations = [
    dict(
        xref='paper', yref='paper',
        x=0, y=1.1,
        xanchor='left', yanchor='bottom',
        text=f"{texts['title']}<br><span style='font-size:13px;color:#333333'>{texts['subtitle']}</span>",
        showarrow=False,
        align='left'
    ),
    dict(
        xref='paper', yref='paper',
        x=0, y=-0.35,
        xanchor='left', yanchor='top',
        text=f"<span style='font-size:11px;color:#555555'>{texts['source']}</span>",
        showarrow=False,
        align='left'
    ),
    dict(
        x=chart_data['categories'][3],
        y=chart_data['series'][0]['y'][3] + 6,
        text=chart_data['series'][0]['name'],
        showarrow=False,
        font=dict(family='Arial', size=14, color=colors[0]),
        xanchor='center'
    ),
    dict(
        x=chart_data['categories'][3],
        y=chart_data['series'][1]['y'][3] - 7,
        text=chart_data['series'][1]['name'],
        showarrow=False,
        font=dict(family='Arial', size=14, color=colors[1]),
        xanchor='center',
        yanchor='top'
    )
]

fig.update_layout(
    annotations=annotations,
    font=dict(family="Arial"),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=20, r=20, t=140, b=220),
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=False,
        tickvals=x_axis_config['tickvals'],
        ticktext=x_axis_config['ticktext'],
        tickfont=dict(size=12, color='black'),
    ),
    yaxis=dict(
        visible=False,
        range=[0, 85]
    ),
    width=450,
    height=550
)

output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")