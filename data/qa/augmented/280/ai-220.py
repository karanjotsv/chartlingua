import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [d['category'] for d in chart_data]
values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False,
    textfont=dict(family="Arial", size=12, color='black')
))

annotations = []
if texts.get('note'):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=0, y=-0.18,
        xanchor='left', yanchor='bottom',
        text=f"ⓘ {texts['note']}",
        showarrow=False,
        font=dict(family="Arial", size=12, color="#007bff")
    ))

if texts.get('source'):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=1, y=-0.18,
        xanchor='right', yanchor='bottom',
        text=texts['source'],
        showarrow=False,
        font=dict(family="Arial", size=12, color='#333333')
    ))

fig.update_layout(
    font=dict(family="Arial", size=12, color='#333333'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=20, t=50, b=100),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#f0f0f0',
        linecolor='black',
        ticks='outside',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        title_font=dict(size=14),
        range=[0, 3.1],
        tickmode='array',
        tickvals=[0, 0.5, 1, 1.5, 2, 2.5, 3],
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dash',
        zeroline=False
    ),
    annotations=annotations
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart successfully generated and saved to {output_image_path}")