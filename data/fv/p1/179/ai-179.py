import sys
import json
from pathlib import Path
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info["chart_data"]
texts = chart_info["texts"]
colors = chart_info["colors"]

fig = go.Figure()

for i, trace_data in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=trace_data['x'],
        y=trace_data['y'],
        mode='lines',
        name=trace_data['name'],
        line=dict(
            color=colors[i],
            dash=trace_data['line_style'],
            width=2 if trace_data['line_style'] != 'dot' else 3
        ),
        showlegend=False
    ))

title_text = f"<b>{texts['title']}</b><br>{texts['subtitle']}"

fig.update_layout(
    font=dict(family="Arial", size=14),
    title=dict(
        text=title_text,
        x=0.05,
        y=0.98,
        xanchor='left',
        yanchor='top'
    ),
    xaxis_title=texts['x_axis_title'],
    yaxis_title=texts['y_axis_title'],
    xaxis=dict(
        range=[0, 100],
        tickmode='linear',
        tick0=0,
        dtick=10,
        showline=True,
        linewidth=1,
        linecolor='black',
        gridcolor='#CCCCCC',
        gridwidth=1,
        mirror=True
    ),
    yaxis=dict(
        range=[0, 100],
        tickmode='linear',
        tick0=0,
        dtick=10,
        showline=True,
        linewidth=1,
        linecolor='black',
        gridcolor='#CCCCCC',
        gridwidth=1,
        mirror=True
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    width=800,
    height=600,
    margin=dict(l=60, r=40, t=120, b=60)
)

output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")