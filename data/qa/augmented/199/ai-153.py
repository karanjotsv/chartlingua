import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)],
        text=series['y'],
        textposition='outside',
        texttemplate='%{text:.2f}',
        cliponaxis=False,
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        )
    ))

annotations = []
if texts.get('source_left'):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=0, y=-0.18,
            xanchor='left', yanchor='top',
            text=texts['source_left'],
            showarrow=False,
            font=dict(family="Arial", size=11, color="#555555")
        )
    )

if texts.get('source_right'):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=1, y=-0.18,
            xanchor='right', yanchor='top',
            text=texts['source_right'],
            showarrow=False,
            align='right',
            font=dict(family="Arial", size=11, color="#555555")
        )
    )

fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='black'),
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='lightgrey'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 21],
        tickvals=[0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20],
        gridcolor='#EAEAEA',
        zeroline=False,
        showline=False
    ),
    margin=dict(l=90, r=40, t=40, b=120),
    annotations=annotations
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")