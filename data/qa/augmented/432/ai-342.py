import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get file path from command-line argument
json_path = pathlib.Path(sys.argv[1])

# Read the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data from the JSON object
chart_data = chart_info.get('chart_data', {})
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])
categories = chart_data.get('categories', [])
series = chart_data.get('series', [])

# Initialize the figure
fig = go.Figure()

# Add a trace for each data series
for i, s in enumerate(series):
    fig.add_trace(go.Bar(
        x=categories,
        y=s['data'],
        name=s['name'],
        marker_color=colors[i],
        text=s['data'],
        textposition='outside',
        textfont=dict(family='Arial', size=12, color='#000000'),
        cliponaxis=False
    ))

# Update the layout of the chart
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(family="Arial", size=14, color="black"),
    margin=dict(l=80, r=40, t=50, b=150),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 600],
        gridcolor='#E5E5E5',
        showgrid=True,
        zeroline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=False
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    annotations=[
        dict(
            text=texts.get('note'),
            showarrow=False,
            xref="paper", yref="paper",
            x=0, y=-0.3,
            xanchor='left', yanchor='top',
            align='left'
        ),
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref="paper", yref="paper",
            x=1, y=-0.3,
            xanchor='right', yanchor='top',
            align='right'
        )
    ]
)

# Define output filename and save the image
output_filename = json_path.with_suffix('.png')
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")