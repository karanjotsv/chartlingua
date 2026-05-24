import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script.py> <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

base_filename = os.path.splitext(json_path)[0]
output_image_path = f"{base_filename}.png"

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=[f'{v:.1f}' if isinstance(v, float) and v != int(v) else str(int(v)) for v in values],
    textposition='outside',
    textfont=dict(family='Arial', size=12, color='black', weight='bold'),
    cliponaxis=False
))

annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=1.0, y=-0.2,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family='Arial', size=12, color='grey')
        )
    )
if texts.get('note'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=0.0, y=-0.2,
            xanchor='left', yanchor='top',
            text=texts['note'],
            showarrow=False,
            font=dict(family='Arial', size=12, color='grey')
        )
    )

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='#F8F9FA',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=False,
        tickfont=dict(family='Arial', size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        title_font=dict(family='Arial', size=14),
        range=[0, 120],
        tickmode='array',
        tickvals=[0, 20, 40, 60, 80, 100, 120],
        showgrid=True,
        gridcolor='#E0E0E0',
        zeroline=False,
        tickfont=dict(family='Arial', size=12)
    ),
    showlegend=False,
    margin=dict(l=90, r=40, t=50, b=100),
    annotations=annotations
)

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")