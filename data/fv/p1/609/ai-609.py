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
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

fig = go.Figure()

for i, series in enumerate(config.get('chart_data', [])):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines',
        line=dict(color=config.get('colors', [])[i], width=2)
    ))

texts = config.get('texts', {})
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.05,
        xanchor='left',
        font=dict(size=24)
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False,
        range=[1990, 2016],
        tickmode='linear',
        tick0=1990,
        dtick=5
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False,
        range=[0, 1500],
        tickmode='linear',
        tick0=0,
        dtick=500
    ),
    legend=dict(
        x=1,
        y=0.95,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(0,0,0,0)'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=14, color="black"),
    margin=dict(l=60, r=200, t=80, b=50),
    width=800,
    height=500,
    showlegend=True
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")