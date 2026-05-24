import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' is not a valid JSON file.")
    sys.exit(1)

# Extract data and settings from the JSON object
chart_data = config.get('chart_data', [])
categories = config.get('categories', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Create the figure
fig = go.Figure()

# Add a bar trace for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        y=categories,
        x=series.get('values', []),
        name=series.get('name', ''),
        orientation='h',
        marker_color=colors[i % len(colors)],
        text=[f"{v}%" for v in series.get('values', [])],
        textposition='outside',
        textfont=dict(family="Arial", color='black'),
        cliponaxis=False,
        hovertemplate='%{y}: %{x}%<extra></extra>'
    ))

# Update layout for a professional appearance
fig.update_layout(
    barmode='group',
    font=dict(family="Arial", size=12),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False,
        ticksuffix='%',
        range=[0, 85]
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        autorange='reversed' # Reverses order to match image (top to bottom)
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5,
        traceorder='normal'
    ),
    margin=dict(l=300, r=40, t=50, b=120),
    plot_bgcolor='white',
    paper_bgcolor='white',
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.22,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=12, color='#666666')
        )
    ]
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the chart as a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")