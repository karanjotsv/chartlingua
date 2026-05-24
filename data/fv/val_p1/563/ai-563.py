import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
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

fig = go.Figure()

for i, series in enumerate(chart_info['chart_data']):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers',
        line=dict(color=chart_info['colors'][i]),
        marker=dict(color=chart_info['colors'][i], size=6),
        name=""
    ))

texts = chart_info['texts']
fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=True,
        gridcolor='#D3D3D3',
        tickmode='array',
        tickvals=[2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017],
        tickformat='d'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        showgrid=True,
        gridcolor='#D3D3D3',
        range=[0, 6000],
        dtick=1000
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=50, r=30, t=80, b=50),
    showlegend=False
)

base_name = os.path.splitext(json_path)[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")