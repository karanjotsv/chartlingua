import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_spec = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_file_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_file_path}' contains invalid JSON.")
    sys.exit(1)

chart_data = chart_spec.get('chart_data', [])
texts = chart_spec.get('texts', {})
colors = chart_spec.get('colors', [])

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x', []),
        y=series.get('y', []),
        name=series.get('name', ''),
        mode='lines+markers+text',
        line=dict(color=colors[i]),
        marker=dict(
            symbol=series.get('marker', 'circle'),
            color=colors[i],
            size=8
        ),
        text=[str(val) for val in series.get('y', [])],
        textposition='middle right',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        )
    ))

fig.update_layout(
    title=dict(
        text=texts.get('title'),
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=16)
    ),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    xaxis=dict(
        showline=True,
        showgrid=True,
        gridcolor='lightgrey',
        linecolor='black',
        tickmode='array',
        tickvals=chart_data[0].get('x', []),
        ticktext=[f"{str(year)[-2:]}" for year in chart_data[0].get('x', [])],
        zeroline=False
    ),
    yaxis=dict(
        showline=True,
        showgrid=True,
        gridcolor='lightgrey',
        linecolor='black',
        range=[0, 70],
        dtick=10,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1
    ),
    legend=dict(
        x=0.05,
        y=0.95,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(255,255,255,0.8)',
        bordercolor='black',
        borderwidth=1
    ),
    margin=dict(l=60, r=60, b=60, t=100),
    autosize=False,
    width=800,
    height=600
)

base_filename = pathlib.Path(json_file_path).stem
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")