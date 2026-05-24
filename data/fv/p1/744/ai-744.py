import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    sys.exit(1)

json_file_path = sys.argv[1]
output_filename = json_file_path.rsplit('.', 1)[0] + '.png'

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines',
        line=dict(color=colors[i] if i < len(colors) else None)
    ))

fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        xanchor='center'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#D3D3D3',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        range=[0, 0.3],
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        type='log',
        range=[-1, 4], # Corresponds to 10^-1 (0.1) to 10^4 (10000)
        tickvals=[10, 100, 1000, 10000],
        ticktext=['10.0', '100.0', '1000.0', '10000.0'],
        showgrid=True,
        gridcolor='#D3D3D3',
        gridwidth=1,
        griddash='dot',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True
    ),
    font=dict(
        family="Arial"
    ),
    legend=dict(
        x=0.05,
        y=0.95,
        xanchor='left',
        yanchor='top',
        borderwidth=1,
        bordercolor='grey'
    ),
    plot_bgcolor='white',
    margin=dict(l=80, r=40, t=80, b=80)
)

fig.write_image(output_filename, scale=2)