import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path and define the output image path
json_path = pathlib.Path(sys.argv[1])
output_path = json_path.with_suffix(".png")

# Read the chart data and configuration from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data and settings from the loaded JSON
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])
background_colors = config.get('background_colors', {})

# Initialize the figure
fig = go.Figure()

# Add a trace for each data series specified in the JSON
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines+markers',
        line=dict(
            color=colors[i],
            width=2,
            dash=series.get('line_style')
        ),
        marker=dict(
            color=colors[i],
            symbol=series.get('marker_symbol'),
            size=6
        )
    ))

# Add text annotations to the chart
annotations_list = []
for ann in texts.get('annotations', []):
    annotations_list.append(go.layout.Annotation(
        x=ann.get('x'),
        y=ann.get('y'),
        text=ann.get('text'),
        showarrow=ann.get('showarrow', False),
        font=dict(
            family="Arial",
            size=12,
            color=ann.get('color')
        ),
        align=ann.get('align', 'center'),
        ax=ann.get('ax', 0),
        ay=ann.get('ay', 0),
        arrowhead=ann.get('arrowhead', 0),
        arrowcolor=ann.get('arrowcolor')
    ))

# Add source text as a separate annotation, positioned relative to the paper
if texts.get('source'):
    annotations_list.append(go.layout.Annotation(
        text=texts['source'],
        xref="paper", yref="paper",
        x=0, y=-0.22,
        xanchor='left', yanchor='top',
        showarrow=False,
        align="left",
        font=dict(family="Arial", size=10, color="grey")
    ))

# Configure the chart layout
fig.update_layout(
    annotations=annotations_list,
    font=dict(family="Arial", size=12, color="black"),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        title_font=dict(size=14),
        tickvals=[1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016],
        range=[1978, 2018.5],
        showgrid=False,
        zeroline=False,
        linecolor='black',
        linewidth=1
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        title_font=dict(size=14),
        tickvals=[0, 25, 50, 75, 100],
        range=[-5, 105],
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False,
        linecolor='black',
        linewidth=1
    ),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=80, t=50, b=120),
    shapes=[
        # Horizontal dashed line for 'Neutral feeling'
        dict(
            type="line", xref="paper", x0=0, x1=1,
            yref="y", y0=50, y1=50,
            line=dict(color="grey", width=1, dash="dash")
        ),
        # Background rectangle for the 'Favorable' region
        dict(
            type="rect", xref="paper", x0=0, x1=1,
            yref="y", y0=50, y1=105,
            fillcolor=background_colors.get('favorable'),
            layer="below", line_width=0
        ),
        # Background rectangle for the 'Unfavorable' region
        dict(
            type="rect", xref="paper", x0=0, x1=1,
            yref="y", y0=-5, y1=50,
            fillcolor=background_colors.get('unfavorable'),
            layer="below", line_width=0
        )
    ]
)

# Save the figure as a high-resolution PNG image
fig.write_image(output_path, scale=2)

print(f"Chart saved to {output_path}")