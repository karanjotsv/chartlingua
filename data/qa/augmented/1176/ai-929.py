import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>", file=sys.stderr)
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}", file=sys.stderr)
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False
))

title_text = texts.get('title') or ''
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    font=dict(family="Arial", size=12),
    title=dict(
        text=title_text,
        x=0.01,
        xanchor='left'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#dddddd',
        gridwidth=1,
        zeroline=False,
        showline=False,
        ticks='outside',
        ticklen=5
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        autorange='reversed',
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='',
        showticklabels=True
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=80, t=60, b=100),
    showlegend=False,
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.18,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(size=10, color='grey')
        )
    ]
)

fig.update_traces(textfont_size=11, textfont_color='black')

output_filename = json_file_path.with_suffix('.png')

fig.write_image(output_filename, scale=2, height=800, width=650)

print(f"Chart saved to {output_filename}")