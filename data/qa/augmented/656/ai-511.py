import sys
import json
import plotly.graph_objects as go
import pathlib

# Ensure a command-line argument is provided
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Get JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)

# Read and parse the JSON data
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = config.get('chart_data', {})
texts = config.get('texts', {})
colors = config.get('colors', {})

categories = chart_data.get('categories', [])
values = chart_data.get('values', [])

# Create the figure
fig = go.Figure()

# Format text labels for the bars (e.g., "4 505")
text_labels = [f'{v:,}'.replace(',', ' ') for v in values]

# Add the bar trace to the figure
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=text_labels,
    textposition='outside',
    marker_color=colors.get('bars', '#1f77b4'),
    cliponaxis=False  # Allow text labels to appear above the plot area
))

# Update the layout of the figure
fig.update_layout(
    font_family="Arial",
    title_text=texts.get('title'),
    yaxis_title_text=texts.get('y_axis_title'),
    xaxis_title_text=texts.get('x_axis_title'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    bargap=0.3,
    margin=dict(t=50, r=40, b=80, l=90),
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        tickmode='array',
        tickvals=categories,
        ticktext=[str(c) for c in categories]
    ),
    yaxis=dict(
        range=[0, 5000],
        tickvals=[0, 1000, 2000, 3000, 4000, 5000],
        showgrid=True,
        gridcolor=colors.get('grid', '#e0e0e0'),
        gridwidth=1
    ),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper', yref='paper',
            x=0.99, y=-0.15,
            xanchor='right', yanchor='top',
            font=dict(size=12, color='grey')
        )
    ]
)

# Update the font size for the text labels on the bars
fig.update_traces(textfont_size=12)

# Generate the output filename from the input JSON path
output_filename = json_file_path.with_suffix('.png')

# Save the figure to a PNG file with a high resolution
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully saved to {output_filename}")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)