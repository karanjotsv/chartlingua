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

data_series = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(data_series):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines',
        line=dict(
            color=colors[i],
            width=2.5,
            shape='spline',
            smoothing=1.3
        ),
        showlegend=False,
        hoverinfo='none'
    ))

    # Add custom legend items using a short line segment and an annotation
    anno_y = series['y'][-1]
    
    # Adjust position for the top label to match the original
    if "H<sub>2</sub>" in series['name']:
        anno_y -= 0.05
    
    fig.add_trace(go.Scatter(
        x=[series['x'][-1] + 0.05, series['x'][-1] + 0.25],
        y=[anno_y, anno_y],
        mode='lines',
        line=dict(color=colors[i], width=2.5),
        showlegend=False,
        hoverinfo='none'
    ))

    fig.add_annotation(
        x=series['x'][-1] + 0.3,
        y=anno_y,
        text=series['name'],
        showarrow=False,
        xanchor='left',
        yanchor='middle',
        font=dict(family="Arial", size=14, color='black')
    )

fig.update_layout(
    xaxis_title=texts['x_axis_title'],
    yaxis_title=texts['y_axis_title'],
    font=dict(
        family="Arial",
        size=14,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=220, t=40, b=80),
    xaxis=dict(
        range=[0, 6],
        tickmode='array',
        tickvals=[0, 1, 2, 3, 4, 5, 6],
        showline=True,
        linewidth=1.5,
        linecolor='black',
        ticks='outside',
        tickfont=dict(size=14),
        showgrid=False
    ),
    yaxis=dict(
        range=[0, 6.2],
        tickmode='array',
        tickvals=[0, 1, 2, 3, 4, 5, 6],
        showline=True,
        linewidth=1.5,
        linecolor='black',
        ticks='outside',
        tickfont=dict(size=14),
        gridcolor='lightgrey',
        showgrid=True
    ),
    showlegend=False
)

filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")