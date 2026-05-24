import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

data_series = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

for i, series in enumerate(data_series):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=series['x'],
        y=series['y'],
        marker_color=colors[i],
        text=[f'{val}%' for val in series['y']],
        textposition='outside',
        textfont=dict(family='Arial', size=12, color='black'),
        cliponaxis=False
    ))

fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(family='Arial', size=12, color='black'),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=False
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        showgrid=True,
        gridcolor='#e5e5e5',
        range=[0, 75],
        dtick=10,
        ticksuffix='%'
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5
    ),
    margin=dict(l=60, r=40, t=40, b=150),
    annotations=[]
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1,
        y=-0.3,
        xanchor='right',
        yanchor='bottom'
    )

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")