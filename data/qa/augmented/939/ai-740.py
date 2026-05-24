import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python recreate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0],
    text=values,
    textposition='outside',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    hoverinfo='skip',
    cliponaxis=False
))

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    bargap=0.35,
    margin=dict(l=80, r=40, t=50, b=120),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 50],
        tickvals=[0, 10, 20, 30, 40, 50],
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        showline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12),
        showgrid=True,
        gridcolor='#f5f5f5'
    )
)

# Add source and note annotations at the bottom
if texts.get("note"):
    fig.add_annotation(
        text=texts["note"],
        align='left',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0,
        y=-0.2,
        xanchor='left',
        yanchor='top',
        font=dict(color="#0073B2")
    )

if texts.get("source"):
    fig.add_annotation(
        text=texts["source"],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.2,
        xanchor='right',
        yanchor='top'
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")