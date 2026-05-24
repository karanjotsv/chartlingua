import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
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
    text=values,
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
    font=dict(family="Arial", size=12, color="black"),
    title_text=texts['title'] if texts.get('title') else None,
    yaxis_title=texts.get('y_axis_title'),
    xaxis_title=texts.get('x_axis_title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        showgrid=False,
        showline=False,
        zeroline=False,
        ticks='',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        range=[0, 700],
        gridcolor='#e0e0e0',
        showline=False,
        zeroline=False,
        ticks='',
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=40, b=150)
)

fig.add_annotation(
    text=texts.get('source', ''),
    align='right',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=1,
    y=0,
    xanchor='right',
    yanchor='top',
    yshift=-130, # Position below the x-axis labels
    font=dict(family="Arial", size=12)
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")