import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for the required command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = pathlib.Path(sys.argv[1])

# Verify the JSON file exists
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Read and parse the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data, texts, and colors from the JSON structure
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each series defined in the JSON
# This loop ensures the script works even with multiple data series
for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Bar(
        x=chart_data['categories'],
        y=series['values'],
        name=series.get('name', ''),
        text=series.get('text_values', series['values']), # Use specific text labels if provided
        textposition='outside',
        marker_color=colors[i % len(colors)],
        textfont=dict(family="Arial", size=12, color='black'),
        cliponaxis=False # Prevent data labels at the top from being cut off
    ))

# Prepare annotations list for source text
annotations = []
if texts.get('source'):
    annotations.append(
        dict(
            xref='paper', yref='paper',
            x=1.0, y=-0.15,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=12, color='grey')
        )
    )

# Update the layout of the chart
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    showlegend=False,
    annotations=annotations,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        title_font=dict(size=14),
        range=[0, 40000],
        tickvals=[0, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000],
        ticktext=['0', '5 000', '10 000', '15 000', '20 000', '25 000', '30 000', '35 000', '40 000'],
        gridcolor='#E5E5E5',
        zeroline=True,
        zerolinecolor='#BDBDBD',
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=60, b=80) # Adjust margins for titles and annotations
)

# Generate the output PNG filename from the input JSON filename
output_filename = json_path.stem + ".png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")