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
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Plotly's y-axis is reversed for horizontal bars, so reverse the data
# to match the visual order (top-to-bottom).
categories.reverse()
values.reverse()

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    texttemplate='<b>%{x}%</b>',
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False,
    hoverinfo='none'
))

fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='#f8f9fa',
    showlegend=False,
    xaxis=dict(
        title=texts.get('x_axis_title'),
        range=[0, 85],
        tickvals=list(range(0, 81, 10)),
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=False,
        title_font=dict(size=14),
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12)
    ),
    margin=dict(l=100, r=40, t=30, b=80),
    title=dict(
        text=texts.get('title'),
        x=0.05,
        xanchor='left'
    )
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper",
        yref="paper",
        x=0.98,
        y=0.03,
        showarrow=False,
        xanchor='right',
        yanchor='bottom',
        font=dict(family="Arial", size=12, color="#6c757d")
    )

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")