import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

fig = go.Figure()

for i, series in enumerate(chart_data):
    color = colors[i % len(colors)]
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series.get('name', ''),
        mode='lines+markers',
        line=dict(color=color, width=2.5),
        marker=dict(color=color, size=6)
    ))

title_text = texts.get('title')
if texts.get('subtitle'):
    title_text = f"<b>{title_text}</b><br>{texts.get('subtitle')}"

source_text = texts.get('source', '')
note_text = texts.get('note', '')

annotations = []
if source_text:
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=1.0, y=-0.3,
            xanchor="right", yanchor="top",
            text=source_text,
            showarrow=False,
            font=dict(family="Arial", size=12, color="grey")
        )
    )

fig.update_layout(
    title=dict(text=title_text, x=0.05, xanchor='left'),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridwidth=1,
        gridcolor='#F0F0F0',
        tickangle=-45
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[102, 113],
        tickmode='linear',
        dtick=2,
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        griddash='dash'
    ),
    font=dict(family="Arial"),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=150),
    height=600,
    width=950,
    annotations=annotations
)

base_filename, _ = os.path.splitext(os.path.basename(json_path))
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")