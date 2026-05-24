import sys
import json
import pathlib
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

data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

x_values = [item['x'] for item in data]
y_values = [item['y'] for item in data]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=[f'{y}%' for y in y_values],
    textposition='outside',
    cliponaxis=False,
    hoverinfo='none'
))

fig.update_traces(textfont=dict(family='Arial, bold', size=12, color='black'))

fig.update_layout(
    plot_bgcolor='white',
    font=dict(family="Arial", size=12, color='#000000'),
    margin=dict(l=80, r=40, t=40, b=80),
    showlegend=False,
    xaxis=dict(
        title_text=texts['x_axis_title'],
        tickvals=x_values,
        ticktext=[str(x) for x in x_values],
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='lightgray',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 0.75],
        tickvals=[i * 0.1 for i in range(8)],
        ticktext=['0%'] + [f'{i * 0.1}%' for i in range(1, 8)],
        gridcolor='lightgray',
        showline=False,
        zeroline=False
    ),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=12)
        )
    ]
)

output_base_name = pathlib.Path(json_path).stem
fig.write_image(f"{output_base_name}.png", scale=2, width=800, height=550)