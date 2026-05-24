import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

data_series = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

# Add vertical background bands for even years
for year in range(1994, 2020, 2):
    fig.add_shape(
        type="rect",
        xref="x",
        yref="paper",
        x0=year - 0.5,
        y0=0,
        x1=year + 0.5,
        y1=1,
        fillcolor="#fafafa",
        layer="below",
        line_width=0,
    )

# Add data trace
series = data_series[0]
fig.add_trace(go.Scatter(
    x=series['x'],
    y=series['y'],
    mode='lines+markers+text',
    line=dict(color=colors[0], width=2.5),
    marker=dict(color=colors[0], size=6),
    text=series['labels'],
    textposition='top center',
    textfont=dict(family="Arial", size=11, color='black'),
    hoverinfo='none',
    name=''
))

fig.update_layout(
    font=dict(family="Arial", size=12, color="#444444"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=False,
        tickmode='array',
        tickvals=[y for y in range(1993, 2020, 2)],
        ticktext=[str(y) for y in range(1993, 2020, 2)],
        zeroline=False,
        ticks='outside'
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        range=[5, 36],
        tickmode='linear',
        tick0=5,
        dtick=5,
        zeroline=False
    ),
    margin=dict(l=90, r=40, t=40, b=120),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.25,
            xanchor='right',
            yanchor='top',
            font=dict(size=12)
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")