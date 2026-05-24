import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script requires the path to the JSON file as a command-line argument.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and texts from the loaded JSON
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# --- 2. Create the Figure ---
fig = go.Figure()

# Add a trace for each data series from the JSON
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        name=series.get('name'),
        mode='lines',
        line=dict(
            color=colors[i] if i < len(colors) else None,
            width=3,
            shape='hv'  # Create a step-like line (horizontal-then-vertical)
        )
    ))

# --- 3. Configure Layout and Styling ---
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        xanchor='center'
    ),
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='outside',
        range=[0, 300],
        dtick=50
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        ticks='outside',
        range=[0, 125],
        dtick=20
    ),
    legend=dict(
        x=1.02,
        y=0.7,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(0,0,0,0)' # Transparent background
    ),
    margin=dict(l=80, r=200, t=100, b=80) # Adjust margins for titles and legend
)


# --- 4. Output the Image ---
# Derive the output filename from the input JSON filename
filename_base = json_path.stem
output_filename = f"{filename_base}.png"

# Save the figure to a PNG file with a high resolution
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")