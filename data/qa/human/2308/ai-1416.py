import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_filepath = sys.argv[1]

try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_filepath}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_filepath}")
    sys.exit(1)

filename_base = os.path.splitext(os.path.basename(json_filepath))[0]

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Bar(
        x=chart_data['categories'],
        y=series['data'],
        name=series['name'],
        marker_color=colors[i],
        text=[f'{val}%' for val in series['data']],
        textposition='outside',
        textfont=dict(
            family="Arial",
            size=12,
            weight='bold'
        )
    ))

fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(
        family="Arial",
        size=12
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 85],
        tickvals=[0, 20, 40, 60, 80],
        ticksuffix='%',
        showgrid=True,
        gridcolor='lightgray'
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=11)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, b=150, t=50)
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper",
        yref="paper",
        x=1,
        y=-0.35,
        showarrow=False,
        xanchor='right',
        yanchor='bottom',
        font=dict(
            family="Arial",
            size=12,
            color="#808080"
        )
    )

output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")