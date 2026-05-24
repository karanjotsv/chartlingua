import sys
import os
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=[f'{v:.2f}' for v in values],
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False
))

fig.update_traces(
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
)

fig.update_layout(
    font=dict(family="Arial", size=12),
    title=texts.get('title'),
    yaxis_title=texts.get('y_axis_title'),
    xaxis_title=texts.get('x_axis_title'),
    plot_bgcolor='white',
    paper_bgcolor='#F8F9FA',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    yaxis=dict(
        range=[0, 70],
        tickmode='linear',
        dtick=10,
        gridcolor='#E0E0E0',
        gridwidth=1,
        griddash='dot',
        zeroline=False
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12)
    )
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=0.99, y=-0.18,
        showarrow=False,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(size=12, color='#7f7f7f')
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")