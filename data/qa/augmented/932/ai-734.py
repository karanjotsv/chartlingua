import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the chart specification from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_spec = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_spec['chart_data']
texts = chart_spec['texts']
colors = chart_spec['colors']

# Prepare data series for Plotly, preserving order
x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

# --- 2. Create and Configure Chart ---
# Initialize the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=[f'{y:.2f}' for y in y_values],
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='#000000'),
    cliponaxis=False, # Ensure text labels are not clipped by the plot area
    hoverinfo='none'
))

# --- 3. Style the Layout ---
fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        tickmode='array',
        tickvals=x_values,
        ticktext=[str(x) for x in x_values]
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 7],
        gridcolor='#E0E0E0',
        zeroline=False
    ),
    # Adjust margins to prevent text clipping
    margin=dict(l=90, r=40, t=50, b=100),
    # Add source annotation at the bottom right
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.22,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(size=12)
        )
    ]
)

# --- 4. Output the Image ---
# Derive the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")