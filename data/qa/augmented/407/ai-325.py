import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

chart_data = data.get('chart_data', [])
texts = data.get('texts', {})
colors = data.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Format numbers with spaces for thousands separator
text_labels = [f'{v:,}'.replace(',', ' ') for v in values]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0] if colors else '#367ac1'),
    text=text_labels,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False
))

title_text = texts.get('title')
if title_text:
    subtitle_text = texts.get('subtitle')
    if subtitle_text:
        title_text = f"{title_text}<br><sup>{subtitle_text}</sup>"

fig.update_layout(
    title_text=title_text,
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=120, r=80, t=50, b=80),
    xaxis=dict(
        showgrid=True,
        gridcolor='#E0E0E0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        range=[0, max(values) * 1.15]
    ),
    yaxis=dict(
        autorange='reversed'
    )
)

source_text = texts.get('source')
if source_text:
    fig.add_annotation(
        text=source_text,
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.99,
        y=-0.15,
        xanchor='right',
        yanchor='top'
    )

p = pathlib.Path(json_path)
output_filename = p.with_suffix('.png')

fig.write_image(str(output_filename), scale=2)

print(f"Chart saved to {output_filename.name}")