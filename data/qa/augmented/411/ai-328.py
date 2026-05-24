import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(sys.argv[0]).name} <json_file_path>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
bar_texts = [f"{v:,}".replace(",", " ") for v in values]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=bar_texts,
    textposition='outside',
    marker_color=colors['bar_color'],
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

annotations = []
if texts.get('note_left'):
    annotations.append(dict(
        text=f"<span style='color:{colors.get('note_color', '#007bff')};'>ⓘ</span> {texts['note_left']}",
        align='left', showarrow=False, xref='paper', yref='paper',
        x=0.0, y=-0.18, xanchor='left', yanchor='bottom',
        font=dict(family="Arial", size=12, color=colors.get('note_color', '#007bff'))
    ))

if texts.get('source_text'):
    annotations.append(dict(
        text=texts['source_text'],
        align='right', showarrow=False, xref='paper', yref='paper',
        x=1.0, y=-0.12, xanchor='right', yanchor='bottom',
        font=dict(family="Arial", size=10, color='#666')
    ))

if texts.get('note_right'):
    annotations.append(dict(
        text=f"{texts['note_right']} <span style='color:{colors.get('note_color', '#007bff')};'>ⓘ</span>",
        align='right', showarrow=False, xref='paper', yref='paper',
        x=1.0, y=-0.18, xanchor='right', yanchor='bottom',
        font=dict(family="Arial", size=12, color=colors.get('note_color', '#007bff'))
    ))

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='#d3d3d3',
        tickfont=dict(size=12, color='#333')
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        title_standoff=15,
        showgrid=True,
        gridcolor='#f0f0f0',
        zeroline=False,
        showline=False,
        range=[0, 25000],
        tickvals=[0, 5000, 10000, 15000, 20000, 25000],
        ticktext=["0", "5 000", "10 000", "15 000", "20 000", "25 000"],
        tickfont=dict(size=12, color='#333')
    ),
    margin=dict(l=80, r=40, t=50, b=120),
    showlegend=False,
    annotations=annotations
)

output_filename = json_file_path.stem + ".png"
fig.write_image(output_filename, scale=2)