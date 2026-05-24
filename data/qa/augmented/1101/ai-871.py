import sys
import os
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=values,
    textposition='outside',
    marker_color=colors[0],
    hoverinfo='none',
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
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=80),
    xaxis=dict(
        title_text=texts['x_axis_title'] if texts.get('x_axis_title') else None,
        showgrid=True,
        gridcolor='#F0F0F0',
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'] if texts.get('y_axis_title') else None,
        range=[0, 45],
        tickvals=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45],
        showgrid=True,
        gridcolor='#EAEAEA',
        tickfont=dict(size=12),
        title_standoff=15
    )
)

annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            xref="paper", yref="paper",
            x=1.0, y=-0.15,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(size=12, color='#666666')
        )
    )

if annotations:
    fig.update_layout(annotations=annotations)


base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")