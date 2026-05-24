import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)

# Define the output image path
output_image_path = json_file_path.with_suffix('.png')

# Load data from the JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data for plotting
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Create the figure
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines+markers',
        line=dict(
            color=colors[i % len(colors)] if colors else None,
            shape='spline',
            width=2
        ),
        marker=dict(
            color=colors[i % len(colors)] if colors else None,
            symbol='cross',
            size=10,
            line=dict(width=2)
        ),
        name=series.get('name', ''),
        showlegend=False
    ))

# Define ranges and ticks for axes
xaxis_range = [-0.2, 3.3]
yaxis_range = [-8.5, 6.5]

# Update the layout of the figure
fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='#F0F4F8',
    margin=dict(l=50, r=40, t=40, b=50),
    xaxis=dict(
        range=xaxis_range,
        tickvals=[0, 1, 2, 3],
        showline=True,
        linewidth=1.5,
        linecolor='black',
        showgrid=True,
        gridcolor='#CCCCCC',
        gridwidth=1,
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='black',
        minor=dict(
            tickmode='linear',
            dtick=0.2,
            showgrid=True,
            gridcolor='#EAEAEA',
            gridwidth=1
        )
    ),
    yaxis=dict(
        range=yaxis_range,
        tickvals=[-5, 0, 5],
        showline=True,
        linewidth=1.5,
        linecolor='black',
        showgrid=True,
        gridcolor='#CCCCCC',
        gridwidth=1,
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='black',
        minor=dict(
            tickmode='linear',
            dtick=1,
            showgrid=True,
            gridcolor='#EAEAEA',
            gridwidth=1
        )
    ),
    annotations=[
        # X-axis arrow
        dict(
            x=xaxis_range[1], y=0,
            ax=-12, ay=0,
            xref='x', yref='y', axref='pixel', ayref='pixel',
            showarrow=True, arrowhead=3, arrowwidth=1.5, arrowcolor='black'
        ),
        # Y-axis arrow
        dict(
            x=0, y=yaxis_range[1],
            ax=0, ay=12,
            xref='x', yref='y', axref='pixel', ayref='pixel',
            showarrow=True, arrowhead=3, arrowwidth=1.5, arrowcolor='black'
        ),
        # X-axis title
        dict(
            x=xaxis_range[1], y=-0.2,
            xref='x', yref='y',
            text=texts.get('x_axis_title', ''),
            showarrow=False,
            xanchor='right',
            yanchor='top'
        ),
        # Y-axis title
        dict(
            x=-0.05, y=yaxis_range[1],
            xref='x', yref='y',
            text=texts.get('y_axis_title', ''),
            showarrow=False,
            xanchor='right',
            yanchor='middle'
        )
    ]
)

# Save the figure to a PNG file
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to '{output_image_path}'")