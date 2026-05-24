import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

fig = go.Figure()

annotations = []
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers',
        name=series['name'],
        line=dict(color=colors[i], width=2),
        marker=dict(symbol='circle', size=6),
        connectgaps=False
    ))

    last_x, last_y = None, None
    for x_val, y_val in reversed(list(zip(series['x'], series['y']))):
        if y_val is not None:
            last_x = x_val
            last_y = y_val
            break
            
    if last_x is not None and last_y is not None:
        annotations.append(
            dict(
                x=last_x,
                y=last_y,
                text=series['name'],
                showarrow=False,
                xanchor='left',
                yanchor='middle',
                xshift=10,
                font=dict(
                    family="Arial",
                    size=12,
                    color="black"
                ),
                bgcolor="rgba(255, 255, 255, 0.8)",
                bordercolor=colors[i],
                borderwidth=1,
                borderpad=4
            )
        )

title_text = f"<span style='font-size: 24px;'>{texts['title']}</span>  <span style='font-size: 16px; color: #555555;'>{texts['subtitle']}</span>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.97,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        showline=False,
        showgrid=False,
        tickmode='array',
        tickvals=list(range(1976, 2005, 2)),
        tickfont=dict(size=12, family="Arial")
    ),
    yaxis=dict(
        showline=False,
        showgrid=True,
        gridcolor='#d3d3d3',
        gridwidth=1,
        range=[-0.5, 14],
        tickmode='array',
        tickvals=list(range(0, 13, 2)),
        tickfont=dict(size=12, family="Arial")
    ),
    font=dict(
        family="Arial"
    ),
    plot_bgcolor='#e9f1f8',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=40, r=120, t=100, b=40),
    annotations=annotations + [
        dict(
            text=texts['source'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1.0,
            y=1.02,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=12, color="#555555", family="Arial")
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")