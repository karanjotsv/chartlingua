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
values_series1 = [item['values'][0] for item in chart_data]
values_series2 = [item['values'][1] for item in chart_data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories,
    y=values_series1,
    name=texts['legend_labels'][0],
    marker_color=colors[0],
    text=[f"{v}%" for v in values_series1],
    textposition='outside',
    cliponaxis=False
))

fig.add_trace(go.Bar(
    x=categories,
    y=values_series2,
    name=texts['legend_labels'][1],
    marker_color=colors[1],
    text=[f"{v}%" for v in values_series2],
    textposition='outside',
    cliponaxis=False
))

fig.update_layout(
    barmode='group',
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    xaxis=dict(
        title=dict(
            text=texts['x_axis_title'],
            standoff=15
        ),
        showgrid=False,
        linecolor='black'
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 105],
        tickvals=[0, 20, 40, 60, 80, 100],
        ticktext=[f'{v}%' for v in [0, 20, 40, 60, 80, 100]],
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False
    ),
    legend=dict(
        orientation='h',
        yanchor='top',
        y=-0.3,
        xanchor='center',
        x=0.5,
        font=dict(size=14),
        traceorder='normal'
    ),
    margin=dict(l=60, r=40, b=200, t=40),
    annotations=[
        dict(
            text=texts['source'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.4,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=12)
        )
    ]
)

fig.update_traces(textfont=dict(size=12, family="Arial", color='black'))

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")