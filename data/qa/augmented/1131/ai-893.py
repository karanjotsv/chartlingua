import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error: Could not read or parse the JSON file at {json_path}. Details: {e}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
categories = chart_data['categories']
series = chart_data['series']

fig = go.Figure()

for i, s in enumerate(series):
    fig.add_trace(go.Bar(
        x=categories,
        y=s['data'],
        name=s['name'],
        marker_color=colors[i],
        text=[f'<b>{val}%</b>' for val in s['data']],
        textposition='outside',
        texttemplate='%{text}',
        textfont=dict(family="Arial", size=12)
    ))

fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    barmode='group',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='lightgray',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[-25, 45],
        tickvals=[-20, -10, 0, 10, 20, 30, 40],
        ticktext=['-20%', '-10%', '0%', '10%', '20%', '30%', '40%'],
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1,
        griddash='dot',
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='black',
        tickfont=dict(size=12)
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.2,
        xanchor="center",
        x=0.5,
        traceorder='normal'
    ),
    margin=dict(l=80, r=40, t=40, b=150)
)

if texts.get('source'):
    fig.add_annotation(
        xref="paper", yref="paper",
        x=1, y=-0.3,
        text=texts['source'],
        showarrow=False,
        xanchor='right',
        yanchor='bottom',
        font=dict(size=12)
    )

base_name = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_name}.png"

try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)