import sys
import json
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract subplot titles from the JSON data
subplot_titles = [chart.get('texts', {}).get('title', '') for chart in chart_info['charts']]

# Create a figure with subplots
fig = make_subplots(
    rows=len(chart_info['charts']),
    cols=1,
    subplot_titles=subplot_titles,
    vertical_spacing=0.15 
)

# Iterate through each chart defined in the JSON
for i, chart in enumerate(chart_info['charts']):
    row_num = i + 1
    chart_data = chart.get('chart_data', [])
    colors = chart.get('colors', [])
    texts = chart.get('texts', {})

    # Iterate through each data series in the chart
    for j, series in enumerate(chart_data):
        # Add trace to the corresponding subplot
        fig.add_trace(
            go.Scatter(
                x=series.get('x'),
                y=series.get('y'),
                name=series.get('name'),
                mode='lines',
                line=dict(color=colors[j % len(colors)]),
                showlegend=(i == 0) # Show legend only for the first subplot's traces
            ),
            row=row_num,
            col=1
        )
    
    # Update axes for the current subplot
    fig.update_xaxes(
        title_text=texts.get('x_axis_title'),
        range=[10, 16],
        tickmode='linear',
        dtick=1.0,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        gridcolor='lightgray',
        row=row_num,
        col=1
    )
    fig.update_yaxes(
        title_text=texts.get('y_axis_title'),
        range=[0, 18],
        tickmode='linear',
        dtick=2.0,
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True,
        gridcolor='lightgray',
        row=row_num,
        col=1
    )

# Update the overall layout of the figure
fig.update_layout(
    font_family="Arial",
    width=700,
    height=800,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=50, t=80, b=80),
    legend=dict(
        x=0.95,
        y=0.95,
        xanchor='right',
        yanchor='top',
        bgcolor='white',
        bordercolor='black',
        borderwidth=1
    )
)

# Determine output filename from JSON path
filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")