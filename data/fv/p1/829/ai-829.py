import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

# Read the JSON file
json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data and texts from the JSON structure
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly traces
categories = [item['category'] for item in chart_data]
values_series1 = [item['values'][0] for item in chart_data]
values_series2 = [item['values'][1] for item in chart_data]

# Reverse the order of data to match the visual (top-to-bottom) in Plotly
categories.reverse()
values_series1.reverse()
values_series2.reverse()

# Create the figure object
fig = go.Figure()

# Add the first data series (Female workers)
fig.add_trace(go.Bar(
    y=categories,
    x=values_series1,
    name=texts['legend_labels'][0],
    orientation='h',
    marker=dict(color=colors[0])
))

# Add the second data series (Male workers)
fig.add_trace(go.Bar(
    y=categories,
    x=values_series2,
    name=texts['legend_labels'][1],
    orientation='h',
    marker=dict(color=colors[1])
))

# Update the layout for a clean and accurate representation
fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        xanchor='center'
    ),
    barmode='group',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        range=[0, 250],
        tickmode='linear',
        tick0=0,
        dtick=50,
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12
    ),
    plot_bgcolor='white',
    margin=dict(l=300, r=40, t=80, b=100)
)

# Determine the output filename from the input JSON filename
output_filename = f"{json_path.stem}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")