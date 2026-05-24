import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

bar_labels = [f"{v}%" if i == len(values) - 1 else str(v) for i, v in enumerate(values)]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=colors,
    text=bar_labels,
    textposition='outside',
    textfont=dict(family='Arial', size=14, color='#333333'),
    cliponaxis=False
))

fig.update_layout(
    title_text=f"{texts['title']}<br><span style='font-size:14px;color:#555555'>{texts['subtitle']}</span>",
    title_x=0.01,
    title_y=0.98,
    title_xanchor='left',
    title_yanchor='top',
    font=dict(family="Arial", size=14),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=160, r=40, t=100, b=120),
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
        range=[0, max(values) * 1.15]
    ),
    yaxis=dict(
        showline=False,
        showgrid=False,
        ticks='',
        tickfont=dict(size=14)
    ),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.2,
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(size=12, color='#555555')
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")