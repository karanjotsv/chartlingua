import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
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
    marker=dict(color=colors[0]),
    text=[f'{v}%' for v in values],
    textposition='outside',
    cliponaxis=False,
    hoverinfo='none'
))

title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    title=dict(text=title_text, x=0.05),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        title_font_size=12,
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        range=[0, max(values) * 1.15]
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        autorange="reversed",
        showgrid=False,
        zeroline=False,
    ),
    margin=dict(l=130, r=40, t=50, b=80),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.99,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(size=10, color="grey")
        )
    ]
)

fig.update_traces(textfont_size=12, textfont_color='black')

output_path = json_path.with_suffix(".png")
fig.write_image(output_path, scale=2)
print(f"Chart saved to {output_path}")