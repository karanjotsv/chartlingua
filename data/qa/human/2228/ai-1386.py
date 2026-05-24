import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_filepath = sys.argv[1]

try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_filepath}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_filepath}")
    sys.exit(1)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

if not chart_data:
    print("Error: 'chart_data' is missing or empty in the JSON file.")
    sys.exit(1)

fig = go.Figure()

categories = [item['category'] for item in chart_data]
series_names = list(chart_data[0]['values'].keys())

for i, series_name in enumerate(series_names):
    values = [item['values'].get(series_name) for item in chart_data]
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        name=series_name,
        marker_color=colors[i % len(colors)],
        text=[f'{v:.2f}' if isinstance(v, float) and v % 1 != 0 else str(v) for v in values],
        textposition='outside',
        cliponaxis=False
    ))

y_max = 0
for item in chart_data:
    y_max = max(y_max, *item['values'].values())

y_axis_range = [0, y_max * 1.35]

fig.update_layout(
    barmode='group',
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        linecolor='black',
        linewidth=1,
        ticks='outside'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=y_axis_range,
        gridcolor='#e0e0e0',
        zeroline=False,
        showline=False,
        ticksuffix=' '
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5
    ),
    margin=dict(l=80, r=40, t=40, b=150),
    hovermode=False
)

fig.update_traces(
    textfont=dict(size=11, family="Arial", color='black')
)

annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            xref='paper',
            yref='paper',
            x=1,
            y=-0.3,
            xanchor='right',
            yanchor='bottom',
            text=texts['source'],
            showarrow=False,
            font=dict(size=11, color='#666666')
        )
    )

fig.update_layout(annotations=annotations)

base_name = os.path.splitext(os.path.basename(json_filepath))[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2, width=800, height=550)

print(f"Chart saved to {output_filename}")