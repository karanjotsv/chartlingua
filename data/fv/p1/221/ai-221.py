import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

output_path = json_path.with_suffix('.png')

with open(json_path, 'r', encoding='utf-8') as f:
    chart_spec = json.load(f)

chart_data = chart_spec['chart_data']
texts = chart_spec['texts']
colors = chart_spec['colors']

fig = go.Figure()

categories = [item['category'] for item in chart_data]
num_series = len(texts['legend_labels'])

for i in range(num_series):
    series_values = [item['values'][i] for item in chart_data]
    fig.add_trace(go.Bar(
        x=categories,
        y=series_values,
        name=texts['legend_labels'][i],
        marker_color=colors[i]
    ))

# Combine title and subtitle if they exist
title_text = ''
if texts.get('title'):
    title_text += texts['title']
if texts.get('subtitle'):
    title_text += f'<br><sub>{texts["subtitle"]}</sub>'

# Combine source and note if they exist
source_text = ''
if texts.get('source'):
    source_text = texts['source']


fig.update_layout(
    barmode='group',
    title_text=title_text if title_text else None,
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        tickangle=-45,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        range=[0, 70],
        dtick=10,
        gridcolor='#e0e0e0',
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    margin=dict(l=60, r=20, t=40, b=180),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.7,
        xanchor="center",
        x=0.5
    )
)

if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=0, y=-0.75,
        xanchor='left', yanchor='top',
        showarrow=False,
        font=dict(family="Arial", size=10)
    )

fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")