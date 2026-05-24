import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
categories = chart_data['categories']
series_data = chart_data['series']

fig = go.Figure()

for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series['y'],
        name=series['name'],
        marker_color=colors[i]
    ))

title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sup>{texts['subtitle']}</sup>"

source_note_parts = []
if texts.get('source'):
    source_note_parts.append(texts['source'])
if texts.get('note'):
    source_note_parts.append(texts['note'])
source_note_html = "<br>".join(source_note_parts)

annotations = []
if source_note_html:
    annotations.append(go.layout.Annotation(
        xref='paper', yref='paper',
        x=0, y=-0.35,
        xanchor='left', yanchor='top',
        text=source_note_html,
        showarrow=False,
        align='left',
        font=dict(family="Arial", size=10, color="grey")
    ))

fig.update_layout(
    barmode='stack',
    title=dict(
        text=title_text,
        x=0.01,
        y=0.95,
        xanchor='left',
        yanchor='top',
        font=dict(size=18)
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        linecolor='black',
        ticks=''
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 4500],
        dtick=500,
        showgrid=True,
        gridcolor='lightgray',
        linecolor='black',
        ticks='outside',
        title_font=dict(size=14)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=20, t=80, b=100),
    annotations=annotations
)

base_name = json_path.split('/')[-1].rsplit('.', 1)[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")