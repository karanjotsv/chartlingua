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
        chart_config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error loading or parsing JSON file: {e}")
    sys.exit(1)

chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

fig = go.Figure()

for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Bar(
        x=chart_data['categories'],
        y=series['data'],
        name=series['name'],
        marker_color=colors['bars'][i],
        text=series['data'],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family="Arial",
            size=16,
            color=colors['text_on_bar'][i]
        )
    ))

fig.update_layout(
    barmode='stack',
    title_text=texts.get('title'),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 1800],
        tickvals=[0, 250, 500, 750, 1000, 1250, 1500, 1750],
        showgrid=True,
        gridcolor='#e9e9e9',
        zeroline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.1,
        xanchor="center",
        x=0.5,
        traceorder='normal'
    ),
    margin=dict(l=80, r=40, t=40, b=120)
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.95,
        y=-0.2,
        xanchor='right',
        yanchor='top',
        font=dict(family="Arial", size=12)
    )

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)