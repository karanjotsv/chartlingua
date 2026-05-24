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

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=chart_data['x_values'],
    y=chart_data['y_values'],
    mode='lines+markers+text',
    line=dict(color=colors['trace'][0], width=2.5),
    marker=dict(color=colors['trace'][0], size=7),
    text=chart_data['text_labels'],
    textposition=chart_data['text_positions'],
    textfont=dict(
        family="Arial",
        size=11,
        color=colors['text']
    ),
    hoverinfo='none'
))

fig.update_layout(
    font=dict(family="Arial", size=12, color=colors['text']),
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    showlegend=False,
    margin=dict(l=90, r=40, t=40, b=80),
    xaxis=dict(
        tickmode='array',
        tickvals=[chart_data['x_values'][i] for i in range(0, len(chart_data['x_values']), 2)],
        ticktext=[chart_data['x_values'][i] for i in range(0, len(chart_data['x_values']), 2)],
        showgrid=False,
        zeroline=False,
        ticks="outside",
        tickangle=0
    ),
    yaxis=dict(
        title=dict(text=texts['y_axis_title'], standoff=15),
        range=[150, 560],
        showgrid=True,
        gridcolor=colors['grid'],
        gridwidth=1,
        zeroline=False
    ),
    annotations=[
        dict(
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.18,
            xanchor='right',
            yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(
                family="Arial",
                size=12,
                color=colors['text']
            )
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2, width=1000, height=600)

print(f"Chart saved to {output_filename}")