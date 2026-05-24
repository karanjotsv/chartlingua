import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>", file=sys.stderr)
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}", file=sys.stderr)
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=[f'{v}%' for v in values],
    textposition='outside',
    textfont=dict(family='Arial', size=12, color='black'),
    cliponaxis=False,
    hoverinfo='none'
))

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title=texts['x_axis_title'],
        title_font=dict(size=12),
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dot',
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        tickformat='%{value}%',
        range=[0, 42]
    ),
    yaxis=dict(
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    margin=dict(l=400, r=50, t=30, b=80),
    annotations=[
        dict(
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family='Arial', size=12, color='grey')
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")