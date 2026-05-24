import sys
import os
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    text=[f"{v}{texts.get('data_labels_suffix', '')}" for v in values],
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False
))

title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

annotations = []
if texts.get("source"):
    annotations.append(
        dict(
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            text=texts["source"],
            showarrow=False,
            font=dict(family="Arial", size=12)
        )
    )

fig.update_layout(
    title_text=title_text,
    yaxis_title=texts.get('y_axis_title'),
    xaxis_title=texts.get('x_axis_title'),
    font=dict(family="Arial", size=14),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=40, t=50, b=100),
    yaxis=dict(
        range=[0, 50],
        ticksuffix='%',
        showgrid=True,
        gridwidth=1,
        gridcolor='#E0E0E0',
        griddash='dot',
        zeroline=False,
        showline=False
    ),
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    annotations=annotations
)

base_filename = os.path.splitext(json_path)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")