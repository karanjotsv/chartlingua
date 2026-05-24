import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

output_path = json_path.with_suffix(".png")

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info["chart_data"]
texts = chart_info["texts"]
colors = chart_info["colors"]

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines+markers',
        line=dict(color=colors[i % len(colors)], width=2.5),
        marker=dict(symbol='diamond', size=8, color=colors[i % len(colors)])
    ))

fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top',
        font=dict(size=22)
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        range=[1860, 2020],
        tickvals=[1860, 1880, 1900, 1920, 1940, 1960, 1980, 2000, 2020],
        showline=True,
        linewidth=1,
        linecolor='black',
        showgrid=False,
        mirror=False
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 250],
        tickvals=[0, 50, 100, 150, 200, 250],
        showline=False,
        gridcolor='#C0C0C0'
    ),
    legend=dict(
        x=1.02,
        y=0.6,
        xanchor='left',
        yanchor='middle',
        bgcolor='rgba(255,255,255,0)',
        bordercolor='rgba(0,0,0,0)'
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(
        family="Arial",
        size=12
    ),
    margin=dict(l=50, r=150, t=80, b=50)
)

fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")