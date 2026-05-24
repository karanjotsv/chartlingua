import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

if not os.path.exists(json_file_path):
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=series['x'],
        y=series['y'],
        marker_color=colors[i % len(colors)],
        text=[f'{val:,}'.replace(',', ' ') for val in series['y']],
        textposition='inside',
        textfont=dict(color='white', family='Arial', size=14),
        insidetextanchor='middle'
    ))

fig.update_layout(
    barmode='stack',
    title_text=texts.get('title'),
    yaxis_title_text=texts['y_axis_title'],
    xaxis_title_text=texts.get('x_axis_title'),
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        orientation='h',
        yanchor='top',
        y=-0.15,
        xanchor='center',
        x=0.5
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#e9e9e9',
        gridwidth=1,
        range=[0, 1800],
        dtick=250,
        zeroline=False,
        linecolor='black',
        ticks='outside'
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        linecolor='black',
        ticks='outside'
    ),
    margin=dict(l=60, r=40, t=50, b=120)
)

if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        align='right',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.25,
        xanchor='right',
        yanchor='top',
        font=dict(size=10, family="Arial")
    )

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")