import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file {json_file_path} was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file {json_file_path} is not a valid JSON file.")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
categories = chart_data['categories']
series = chart_data['series'][0]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=categories,
    y=series['data'],
    mode='lines+markers+text',
    line=dict(color=colors[0], width=3),
    marker=dict(color=colors[0], size=7),
    text=series['annotations'],
    textposition=series['text_positions'],
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=80),
    xaxis=dict(
        tickmode='array',
        tickvals=categories,
        ticktext=[str(c) for c in categories],
        gridcolor='#f0f0f0',
        showline=False,
        zeroline=False,
        ticks='outside',
        ticklen=5
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[50, 110],
        gridcolor='#e5e5e5',
        showline=False,
        zeroline=False,
        ticks='outside',
        ticklen=5
    ),
    annotations=[
        dict(
            text=texts['source'] if texts['source'] else '',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(
                family="Arial",
                size=12,
                color="#888888"
            )
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")