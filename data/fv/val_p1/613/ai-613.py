import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data_json = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_data_json.get('chart_data', [])
texts = chart_data_json.get('texts', {})
colors = chart_data_json.get('colors', [])

fig = go.Figure()

for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x', []),
        y=series.get('y', []),
        name=series.get('name', ''),
        mode='lines',
        line=dict(color=colors[i] if i < len(colors) else None, width=1.5)
    ))

# This gnuplot style often has a box around the plot area
fig.update_xaxes(
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True,
    ticks='outside',
    showgrid=True,
    gridwidth=1,
    gridcolor='#D3D3D3' # LightGray
)
fig.update_yaxes(
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True,
    ticks='outside',
    showgrid=True,
    gridwidth=1,
    gridcolor='#D3D3D3' # LightGray
)

fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        range=[0, 450],
        dtick=50
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[-100, -10],
        dtick=10
    ),
    legend=dict(
        x=0.98,
        y=0.98,
        xanchor='right',
        yanchor='top',
        bgcolor='white',
        bordercolor='black',
        borderwidth=1
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=40, t=40, b=40)
)

# Use the base of the JSON filename for the output PNG
if '.' in json_path:
    base_filename = json_path.rsplit('.', 1)[0]
else:
    base_filename = json_path

output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")