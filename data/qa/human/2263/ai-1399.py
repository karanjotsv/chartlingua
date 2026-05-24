import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error loading JSON file: {e}")
    sys.exit(1)

fig = go.Figure()

for i, series in enumerate(config.get('chart_data', [])):
    fig.add_trace(go.Bar(
        x=config.get('categories', []),
        y=series.get('data', []),
        name=series.get('name', ''),
        marker_color=config.get('colors', [])[i % len(config.get('colors', [None]))],
        text=series.get('data', []),
        textposition='outside',
        texttemplate='<b>%{text}</b>',
        cliponaxis=False,
        textfont=dict(family='Arial', size=12, color='black')
    ))

texts = config.get('texts', {})
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
full_title = ''
if title_text:
    full_title += f"<b>{title_text}</b>"
    if subtitle_text:
        full_title += f"<br><sub>{subtitle_text}</sub>"
elif subtitle_text:
    full_title = f"<sub>{subtitle_text}</sub>"

source_text = texts.get('source', '')

fig.update_layout(
    barmode='group',
    font=dict(family="Arial", size=12),
    title=dict(
        text=full_title,
        x=0.05,
        y=0.95,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 5000],
        dtick=1000,
        gridcolor='#EAEAEA',
        griddash='dot',
        zeroline=False,
        tickfont=dict(size=12)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(t=60, b=120, l=80, r=40)
)

if source_text:
    fig.add_annotation(
        text=source_text,
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.35,
        xanchor='right',
        yanchor='bottom',
        align='right',
        font=dict(size=10, color='grey')
    )

output_path = json_file_path.rsplit('.', 1)[0] + '.png'
fig.write_image(output_path, scale=2)
print(f"Image saved to {output_path}")