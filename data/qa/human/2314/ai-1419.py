import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for the required command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {Path(__file__).name} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = Path(sys.argv[1])
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Load all data and text from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
categories = chart_data['categories']
series = chart_data['series']

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each data series from the JSON
for i, s in enumerate(series):
    fig.add_trace(go.Bar(
        y=categories,
        x=s['data'],
        name=s['name'],
        orientation='h',
        marker=dict(color=colors[i]),
        text=[f'{val}%' for val in s['data']],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white', size=14)
    ))

# Configure the chart layout
fig.update_layout(
    barmode='stack',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='black'),
    margin=dict(l=260, r=40, t=50, b=120),
    xaxis=dict(
        title=texts['x_axis_title'],
        title_font=dict(size=14),
        range=[0, 120],
        tickvals=[0, 20, 40, 60, 80, 100, 120],
        ticktext=[f'{v}%' for v in [0, 20, 40, 60, 80, 100, 120]],
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        autorange='reversed',  # Display categories from top to bottom
        showgrid=False,
        zeroline=False,
        showline=False,
        tickfont=dict(size=13)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5,
        traceorder='normal',
        font=dict(size=13)
    ),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.98,
            y=-0.35,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=12, color='#666666')
        )
    ]
)

# Generate the output filename from the input JSON path
output_filename_base = json_file_path.stem
output_image_path = f"{output_filename_base}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")