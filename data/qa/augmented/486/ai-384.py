import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Check if the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in '{json_path}'")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker=dict(color=colors[0]),
    text=[f'<b>{v}%</b>' for v in values],
    textposition='outside',
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Update layout
fig.update_layout(
    font=dict(
        family="Arial"
    ),
    title=dict(
        text=texts.get('title'),
        x=0.05,
        xanchor='left'
    ),
    plot_bgcolor='white',
    paper_bgcolor='#F8F9FA',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 50],
        showgrid=True,
        gridcolor='#E5E5E5',
        ticksuffix='%',
        zeroline=False
    ),
    margin=dict(l=80, r=40, t=50, b=120),
    showlegend=False,
    annotations=[
        dict(
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.25,
            xanchor='right',
            yanchor='top',
            text=texts.get('source_note'),
            showarrow=False,
            font=dict(
                family="Arial",
                size=12,
                color='#666666'
            )
        )
    ]
)

# Define output filename
output_filename = os.path.splitext(json_path)[0] + '.png'

# Save the figure as a PNG image
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)