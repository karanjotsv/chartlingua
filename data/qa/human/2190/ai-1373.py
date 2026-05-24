import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
# The script expects the JSON file path as the sole command-line argument.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Ensure the file exists before proceeding.
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

# Load the chart configuration from the specified JSON file, using UTF-8 for multilingual support.
with open(json_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# Extract data and text elements from the loaded configuration.
chart_data = chart_config.get('chart_data', {})
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])
categories = chart_data.get('categories', [])
series_data = chart_data.get('series', [])

# --- 2. Create the Plotly figure ---
fig = go.Figure()

# Iterate through each data series in the JSON to create a corresponding bar trace.
for i, series in enumerate(series_data):
    # Format data labels as bold percentages to be displayed inside the bars.
    text_labels = [f"<b>{val}%</b>" for val in series['data']]
    
    fig.add_trace(go.Bar(
        x=categories,
        y=series['data'],
        name=series['name'],
        marker_color=colors[i % len(colors)],  # Use modulo for color safety.
        text=text_labels,
        textposition='inside',
        textfont=dict(color='white', size=12),
        hoverinfo='skip'
    ))

# --- 3. Configure the chart layout ---
# Build annotations list, starting with the source text.
annotations = []
if texts.get('source'):
    annotations.append(
        go.layout.Annotation(
            xref="paper", yref="paper",
            x=1, y=-0.28,
            xanchor='right', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=10, color="#666666")
        )
    )

fig.update_layout(
    barmode='stack',
    # Set global font properties.
    font=dict(family="Arial", size=12),
    # Set background colors.
    plot_bgcolor='white',
    paper_bgcolor='white',
    # Define margins to prevent element clipping.
    margin=dict(l=90, r=40, t=50, b=140),
    # Configure the legend to appear below the chart.
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.15,
        xanchor="center",
        x=0.5
    ),
    # Configure the X-axis.
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linecolor='black',
        linewidth=1,
        ticks='outside',
        tickfont=dict(size=12)
    ),
    # Configure the Y-axis.
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 125],
        tickvals=[0, 25, 50, 75, 100, 125],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1
    ),
    # Apply annotations.
    annotations=annotations
)

# --- 4. Output the chart as a PNG image ---
# Derive the output filename from the input JSON filename.
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file.
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")