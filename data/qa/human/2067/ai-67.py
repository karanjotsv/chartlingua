import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
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

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series.get('name', ''),
        mode='lines+markers+text',
        text=series.get('text', None),
        textposition='top center',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        line=dict(color=colors[i], width=2.5),
        marker=dict(color=colors[i], size=7)
    ))

title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    if title_text:
        title_text += "<br>"
    title_text += f"<span style='font-size:0.8em;color:grey;'>{texts['subtitle']}</span>"

source_text = ""
if texts.get('source'):
    source_text = texts['source']
if texts.get('note'):
    if source_text:
        source_text += "<br>"
    source_text += texts['note']

fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color="#333333"),
    showlegend=False,
    title=dict(
        text=title_text,
        x=0.01,
        xanchor='left',
        y=0.95,
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        tickmode='linear',
        tick0=2000,
        dtick=1,
        showgrid=True,
        gridcolor='#f0f0f0',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[20, 55],
        tickmode='linear',
        tick0=25,
        dtick=5,
        gridcolor='lightgray',
        zeroline=False
    ),
    margin=dict(l=90, r=40, t=60, b=80)
)

if source_text:
    fig.add_annotation(
        text=source_text,
        xref="paper", yref="paper",
        x=1.0, y=-0.15,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(size=10, color='grey')
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2, width=800, height=600)

print(f"Chart saved to {output_filename}")