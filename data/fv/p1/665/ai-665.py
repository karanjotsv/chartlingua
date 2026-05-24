import sys
import json
import pathlib
import plotly.graph_objects as go

# This script requires a command-line argument for the JSON file path.
if len(sys.argv) != 2:
    print(f"Usage: python {pathlib.Path(__file__).name} <json_file_path>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load data from the specified JSON file.
with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the loaded JSON.
data_series = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Initialize the Plotly figure.
fig = go.Figure()

# Add bar traces to the figure by iterating through the data series.
for i, series in enumerate(data_series):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series.get('name', ''),
        marker=dict(
            color=colors[i % len(colors)],
            line=dict(
                color='#660000',  # Darker border to mimic 3D effect
                width=1.5
            )
        ),
        width=0.5  # Set a fixed bar width
    ))

# Configure the figure layout for aesthetics and accuracy.
fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        xanchor='center',
        font=dict(size=20)
    ),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        showline=True,
        linecolor='#C00000',
        linewidth=3,
        mirror=True # To create the full border
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[12500, 16000],
        dtick=500,
        showgrid=True,
        gridcolor='lightgrey',
        showline=True,
        linecolor='#C00000',
        linewidth=3,
        mirror=True # To create the full border
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    width=650,
    height=450,
    margin=dict(l=80, r=40, t=100, b=50) # Adjust margins to prevent clipping
)

# Derive the output filename from the input JSON filename.
output_filename = json_path.stem + ".png"

# Save the figure as a high-resolution PNG file.
fig.write_image(output_filename, scale=2)

print(f"Chart saved to '{output_filename}'")