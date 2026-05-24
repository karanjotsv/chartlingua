import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series.get('x'),
        y=series.get('y'),
        text=[f'{val:.2f}' if isinstance(val, float) and val % 1 != 0 else str(val) for val in series.get('y', [])],
        textposition='outside',
        marker_color=colors[i % len(colors)] if colors else None,
        name=series.get('name', ''),
        cliponaxis=False
    ))

title_text = texts.get('title', '') or ''
subtitle_text = texts.get('subtitle', '') or ''
full_title = ""
if title_text:
    full_title += f"<b>{title_text}</b>"
if subtitle_text:
    full_title += f"<br><sub>{subtitle_text}</sub>"

fig.update_layout(
    font=dict(family="Arial"),
    title=dict(
        text=full_title,
        x=0.05,
        xanchor='left',
        y=0.95,
        yanchor='top'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 18],
        dtick=2.5,
        gridcolor='#E5E5E5',
        showline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=60, b=80),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            xref="paper",
            yref="paper",
            x=1,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10, color='#808080')
        )
    ]
)

fig.update_traces(
    textfont_size=12,
    textfont_color='black'
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")