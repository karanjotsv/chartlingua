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
        family="Arial",
        size=10,
        color='black'
    )
))

title_text = texts.get('title') if texts.get('title') else ""
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=title_text,
        automargin=True,
        yref='container',
        y=0.95
    ),
    plot_bgcolor='white',
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 200],
        tickmode='linear',
        tick0=0,
        dtick=25,
        showgrid=True,
        gridcolor='#e0e0e0'
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=False,
        type='category'
    ),
    showlegend=False,
    margin=dict(t=50, b=80, l=80, r=40),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper', yref='paper',
            x=1.0, y=-0.2,
            xanchor='right', yanchor='top',
            align='right',
            font=dict(size=10)
        )
    ]
)

output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")