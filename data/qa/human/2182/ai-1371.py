import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Initialize figure
fig = go.Figure()

# Add traces by iterating through the chart data
for i, series in enumerate(chart_data['chart_data']):
    fig.add_trace(go.Bar(
        x=chart_data['categories'],
        y=series['values'],
        name=series['name'],
        marker_color=chart_data['colors']['traces'][i],
        text=[f'{v}%' for v in series['values']],
        textposition='inside',
        textfont=dict(
            family='Arial',
            color=chart_data['colors']['text'][i]
        ),
        insidetextanchor='middle'
    ))

# Update layout
fig.update_layout(
    barmode='stack',
    xaxis=dict(
        title_text=chart_data['texts']['x_axis_title'],
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=chart_data['texts']['y_axis_title'],
        range=[0, 100],
        tickvals=[0, 25, 50, 75, 100],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e9e9e9',
        zeroline=False,
        title_font=dict(size=14),
        tickfont=dict(size=12)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12),
    margin=dict(l=80, r=40, t=50, b=140),
    annotations=[
        dict(
            text=chart_data['texts']['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.25,
            xanchor='right',
            yanchor='top',
            font=dict(size=10)
        )
    ]
)

# Generate output filename from JSON path
output_filename = f"{Path(json_path).stem}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")