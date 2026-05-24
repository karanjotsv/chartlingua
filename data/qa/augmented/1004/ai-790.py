import sys
import json
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Prepare data for Plotly
categories = [d['category'] for d in chart_config['chart_data']]
values = [d['value'] for d in chart_config['chart_data']]
texts_data = chart_config['texts']
bar_color = chart_config['colors'][0]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=[f'{v:g}' for v in values],
    textposition='inside',
    insidetextanchor='end',
    marker_color=bar_color,
    hoverinfo='none',
    insidetextfont=dict(family='Arial', size=12, color='black')
))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    showlegend=False,
    yaxis_title=texts_data['y_axis_title'],
    margin=dict(l=90, r=40, t=50, b=100),
    xaxis=dict(
        showgrid=False,
        linecolor='#d3d3d3',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#e9e9e9',
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1,
        range=[-3000, 1000],
        tickvals=[-3000, -2500, -2000, -1500, -1000, -500, 0, 500, 1000],
        ticktext=["-3 000", "-2 500", "-2 000", "-1 500", "-1 000", "-500", "0", "500", "1 000"],
        linecolor='#d3d3d3',
        tickfont=dict(size=12)
    ),
    annotations=[
        dict(
            text=texts_data.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=10, color='#666666')
        )
    ]
)

# Determine the output filename from the input JSON path
output_filename = json_path.rsplit('.', 1)[0] + '.png'

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")