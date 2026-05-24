import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' is not a valid JSON file.")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines',
        line=dict(color=colors[i % len(colors)] if colors else '#0000FF', width=1.5),
        name=series.get('name', '')
    ))

title_text = texts.get('title')
if title_text:
    title_text = f'<b>{title_text}</b>'

x_axis_tick_vals = list(range(1993, 2018))
x_axis_tick_text = [f"'{str(y)[2:]}" for y in x_axis_tick_vals]

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=16)
    ),
    font=dict(
        family="Arial",
        color='white'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='rgba(255, 255, 255, 0.4)',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='white',
        tickvals=x_axis_tick_vals,
        ticktext=x_axis_tick_text,
        range=[1992.8, 2017.7]
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='rgba(255, 255, 255, 0.4)',
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='white',
        range=[20, 105],
        dtick=10
    ),
    plot_bgcolor='black',
    paper_bgcolor='black',
    showlegend=False,
    margin=dict(l=50, r=20, t=60, b=50)
)

base_filename = json_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")