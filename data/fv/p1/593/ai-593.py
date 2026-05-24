import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', {})
layout_options = chart_info.get('layout_options', {})

fig = go.Figure()

series_colors = colors.get('series_colors', [])
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='markers',
        name=series.get('name', ''),
        marker=dict(
            color=series_colors[i % len(series_colors)] if series_colors else None,
            size=8
        )
    ))

title_parts = []
if texts.get('title'):
    title_parts.append(f"<b>{texts['title']}</b>")
if texts.get('subtitle'):
    title_parts.append(f"<sub>{texts['subtitle']}</sub>")
full_title_text = "<br>".join(title_parts)

source_parts = []
if texts.get('source'):
    source_parts.append(texts['source'])
if texts.get('note'):
    source_parts.append(texts['note'])
caption_text = "<br>".join(source_parts)

fig.update_layout(
    plot_bgcolor=colors.get('plot_background', '#FFFFFF'),
    paper_bgcolor=colors.get('paper_background', '#FFFFFF'),
    font=dict(family="Arial"),
    title=dict(
        text=full_title_text,
        x=0.05,
        xanchor='left',
        y=0.95,
        yanchor='top'
    ),
    xaxis=dict(
        visible=layout_options.get('show_axes', True),
        title_text=texts.get('x_axis_title')
    ),
    yaxis=dict(
        visible=layout_options.get('show_axes', True),
        title_text=texts.get('y_axis_title')
    ),
    showlegend=layout_options.get('show_legend', True),
    margin=dict(l=5, r=5, t=5, b=5) if layout_options.get('show_axes') else dict(l=0, r=0, t=0, b=0),
    annotations=[
        dict(
            text=caption_text,
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.0,
            y=-0.01,
            xanchor='left',
            yanchor='top',
            align='left'
        )
    ] if caption_text else []
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")