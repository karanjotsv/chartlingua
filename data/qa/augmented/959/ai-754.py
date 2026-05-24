import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read the chart configuration from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_file_path}")
    sys.exit(1)

# Extract data and text from the configuration
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each data series in the JSON
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)] if colors else None
    ))

# Prepare annotations, including the source text
annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            text=texts.get('source'),
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.15,
            xanchor='right',
            yanchor='top'
        )
    )

# Format y-axis ticks to match the original image (e.g., "40 000")
y_tick_values = list(range(0, 40001, 5000))
y_tick_text = [f"{v:,}".replace(",", " ") for v in y_tick_values]

# Update the layout of the chart
fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickmode='array',
        tickvals=chart_data[0]['x'] if chart_data and 'x' in chart_data[0] else None,
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 41000],
        gridcolor='#EAEAEA',
        griddash='dot',
        zeroline=False,
        tickvals=y_tick_values,
        ticktext=y_tick_text
    ),
    margin=dict(l=80, r=40, t=40, b=100),
    annotations=annotations
)

# Derive the output PNG filename from the input JSON filename
if json_file_path.lower().endswith('.json'):
    output_filename = json_file_path[:-5] + '.png'
else:
    output_filename = json_file_path + '.png'

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")