import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

fig = go.Figure()

for i, series in enumerate(chart_info['chart_data']):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines',
        name=series['name'],
        line=dict(color=chart_info['colors'][i], width=1.5),
        showlegend=False
    ))

fig.update_layout(
    title=dict(
        text=chart_info['texts']['title'],
        x=0.01,
        xanchor='left',
        y=0.95,
        yanchor='top'
    ),
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    width=700,
    height=500,
    margin=dict(l=60, r=40, b=50, t=60),
    xaxis=dict(
        type='log',
        tickvals=[10, 100, 1000, 10000, 50000],
        ticktext=['10', '100', '1k', '10k', '50k'],
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='outside',
        showgrid=True,
        gridcolor='#888888',
        gridwidth=1,
        minor=dict(
            showgrid=True,
            gridcolor='#CCCCCC',
            gridwidth=0.5
        )
    ),
    yaxis=dict(
        type='log',
        tickvals=[0.0005, 0.001, 0.01, 0.05],
        ticktext=['0.0005', '0.001', '0.010', '0.050'],
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='outside',
        showgrid=True,
        gridcolor='#888888',
        gridwidth=1,
        minor=dict(
            showgrid=True,
            gridcolor='#CCCCCC',
            gridwidth=0.5
        )
    ),
    annotations=chart_info['texts'].get('annotations', [])
)

if json_path.endswith('.json'):
    output_filename = json_path[:-5] + '.png'
else:
    output_filename = json_path + '.png'

fig.write_image(output_filename, scale=2)