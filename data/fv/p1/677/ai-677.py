import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

json_file_path = pathlib.Path(sys.argv[1])

if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

fig = go.Figure()

data_series = chart_info['chart_data']
colors = chart_info['colors']
texts = chart_info['texts']

for i, series in enumerate(data_series):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers',
        name=series.get('name', ''),
        line=dict(color=colors[i % len(colors)]),
        marker=dict(color=colors[i % len(colors)], size=6)
    ))

title_text = f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br>{texts['subtitle']}"

source_note_parts = []
if texts.get('source'):
    source_note_parts.append(texts['source'])
if texts.get('note'):
    source_note_parts.append(texts['note'])
source_note_text = "<br>".join(source_note_parts)

fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title=texts['x_axis_title'],
    yaxis_title=texts['y_axis_title'],
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=40, t=90, b=80),
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=False,
        dtick=1,
        tickmode='linear',
        range=[0, 30]
    ),
    yaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=True,
        gridcolor='#DDDDDD',
        range=[0, 20],
        dtick=2,
        zeroline=False
    )
)

if source_note_text:
    fig.add_annotation(
        text=source_note_text,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.15,
        xanchor='left',
        yanchor='top'
    )

output_filename = json_file_path.with_suffix(".png").name
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")