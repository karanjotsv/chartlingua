import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
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

categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors),
    texttemplate='%{x:.2f}%',
    textposition='outside',
    cliponaxis=False
))

title_text = f"<b>{texts['title']}</b><br><span style='font-size: 0.8em; color: #555555;'>{texts['subtitle']}</span>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.01,
        y=0.97,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dash',
        zeroline=False,
        showline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        autorange='reversed',
        ticks='outside',
        ticklen=8
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=100, r=80, t=140, b=80),
    annotations=[
        dict(
            text=texts['source_note'],
            showarrow=False,
            xref='paper', yref='paper',
            x=0, y=-0.15,
            xanchor='left', yanchor='top',
            font=dict(size=12, color='#666666')
        )
    ]
)

output_filename = json_path.with_suffix('.png').name
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")