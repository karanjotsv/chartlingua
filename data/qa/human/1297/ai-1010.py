import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts
data_series = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Create the figure object
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(data_series):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        mode='lines+markers+text',
        line=dict(color=colors[i], width=3.5),
        marker=dict(
            symbol='circle',
            color='white',
            size=12,
            line=dict(color=colors[i], width=3)
        ),
        text=[str(val) for val in series['y']],
        textposition=['middle left', 'middle right'],
        textfont=dict(
            family="Arial",
            size=14,
            color="#333333"
        ),
        hoverinfo='none',
        showlegend=False
    ))

    # Add annotation for the series label (e.g., "Bad", "Good")
    fig.add_annotation(
        x=0.5,
        y=series['label_y_pos'],
        text=f"<b>{series['label_text']}</b>",
        showarrow=False,
        font=dict(
            family="Arial",
            size=16,
            color=colors[i]
        ),
        xref="x",
        yref="y"
    )

# Combine title and subtitle
title_text = f'<b style="font-size:22px;">{texts["title"]}</b><br><span style="font-size:15px; color:#505050;">{texts["subtitle"]}</span>'

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.97,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    font=dict(family="Arial", color="#333333"),
    xaxis=dict(
        showgrid=False,
        showline=False,
        zeroline=False,
        ticks='',
        tickfont=dict(size=14)
    ),
    yaxis=dict(
        range=[0, 105],
        showgrid=False,
        showline=False,
        zeroline=False,
        tickvals=[0, 100],
        ticktext=['0', '100%'],
        tickfont=dict(size=14)
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=40, r=40, t=160, b=200)
)

# Add a shape for the x-axis baseline
fig.add_shape(
    type="line",
    xref="paper", yref="y",
    x0=0, y0=0, x1=1, y1=0,
    line=dict(color="grey", width=1)
)

# Add annotation for the source text
fig.add_annotation(
    text=texts['source'],
    xref="paper", yref="paper",
    x=0.01, y=-0.3,
    xanchor='left', yanchor='top',
    align='left',
    showarrow=False,
    font=dict(size=12, color='#505050')
)

# Determine output filename and save the image
output_filename = pathlib.Path(json_path).stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")