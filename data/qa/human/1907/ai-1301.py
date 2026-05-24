import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# The script must accept the JSON path as a required command-line argument.
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Derive output filename from the input JSON path.
output_path = json_path.with_suffix(".png")

# Read the JSON file, which is the only source for data and styling.
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Initialize the Plotly figure object.
fig = go.Figure()

# Iterate through the data series from the JSON to create traces.
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers',
        name=series.get('name', ''),
        line=dict(color=colors[i % len(colors)], width=2.5),
        marker=dict(color=colors[i % len(colors)], size=8),
        hoverinfo='none'
    ))

    # Add data labels as annotations, preserving order and placement.
    if 'labels' in series:
        for j, label_info in enumerate(series['labels']):
            if label_info:
                y_anchor = label_info.get('anchor', 'bottom')
                y_shift = 10 if y_anchor == 'bottom' else -10

                fig.add_annotation(
                    x=series['x'][j],
                    y=series['y'][j],
                    text=label_info['text'],
                    showarrow=False,
                    font=dict(family="Arial", size=12, color="black"),
                    xanchor='center',
                    yanchor=y_anchor,
                    yshift=y_shift
                )

# Configure the layout, ensuring no text is clipped.
fig.update_layout(
    font=dict(family="Arial", size=12, color="#333"),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        showline=False,
        tickmode='array',
        tickvals=list(range(2000, 2020)),
        ticktext=[str(y) for y in range(2000, 2020)],
        tickangle=0
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#E9E9E9',
        zeroline=False,
        showline=False,
        range=[5, 85],
        tickvals=[10, 20, 30, 40, 50, 60, 70, 80],
        ticktext=[f"{v}%" for v in [10, 20, 30, 40, 50, 60, 70, 80]]
    ),
    margin=dict(l=80, r=40, t=40, b=80),
)

# Add source annotation at the bottom right.
if texts.get('source'):
    fig.add_annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=0.98, y=-0.15,
        showarrow=False,
        align="right",
        xanchor="right",
        yanchor="top",
        font=dict(family="Arial", size=12, color="#555")
    )

# Output the chart to a PNG file with a high-resolution scale.
fig.write_image(output_path, scale=2)

print(f"Chart successfully generated and saved to {output_path}")