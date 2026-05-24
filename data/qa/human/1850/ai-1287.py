import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Load data from JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Initialize figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines+markers',
        line=dict(color=colors[i], width=2.5),
        marker=dict(color=colors[i], size=6, symbol='circle')
    ))

# Add annotations for each series at the end of the line
for series in chart_data:
    # Special handling for overlapping labels at the bottom
    yshift = 0
    if series['name'] == 'Turkey':
        yshift = -15
    elif series['name'] == 'Iceland':
        yshift = 15

    fig.add_annotation(
        x=series['x'][-1],
        y=series['y'][-1],
        text=series['name'],
        showarrow=False,
        xshift=10,
        yshift=yshift,
        xanchor='left',
        yanchor='middle',
        font=dict(family="Arial", size=12, color="black"),
        bgcolor="rgba(255, 255, 255, 0.75)",
        borderpad=4
    )

# Configure layout
fig.update_layout(
    font_family="Arial",
    title=dict(
        text=f"<b>{texts['title']}</b><br><span style='font-size: 16px; color: #555;'>{texts['subtitle']}</span>",
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    plot_bgcolor='#e5eff5',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        tickvals=list(range(1988, 2004, 2)),
        showgrid=False,
        zeroline=False,
        linecolor='lightgrey',
        showline=False
    ),
    yaxis=dict(
        range=[-30, 500],
        tickvals=list(range(0, 500, 50)),
        gridcolor='white',
        gridwidth=1.5,
        zeroline=False
    ),
    margin=dict(l=40, r=150, t=100, b=40),
    height=600
)

# Add source text as an annotation
fig.add_annotation(
    text=texts['source'],
    showarrow=False,
    xref='paper',
    yref='paper',
    x=1,
    y=0.96,
    xanchor='right',
    yanchor='top',
    align='right',
    font=dict(size=12, color="#555")
)

# Add decorative line below the title
fig.add_shape(
    type="line",
    xref="paper", yref="paper",
    x0=0, y0=0.88, x1=1, y1=0.88,
    line=dict(color="#2d8fd5", width=2)
)

# Generate and save the output image
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")