import sys
import os
import json
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script expects the JSON file path as the first and only command-line argument.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)

# Extract data and texts from the loaded JSON
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
x_values = [item['x'] for item in chart_data]
y_values = [item['y'] for item in chart_data]

# --- 2. Create the Plotly Figure ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0] if colors else '#1f77b4',
    text=y_values,
    textposition='outside',
    texttemplate='%{text:.2f}',
    cliponaxis=False  # Allow text to be drawn outside the plot area
))

# --- 3. Configure Layout ---
fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 1850],
        tickvals=[0, 250, 500, 750, 1000, 1250, 1500, 1750],
        gridcolor='#e9e9e9',
        showgrid=True,
        linecolor='black'
    ),
    # Adjust margins to prevent titles/labels from being clipped
    margin=dict(l=80, r=40, t=50, b=100),
    # Add source text as an annotation
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.18,
            xanchor='right',
            yanchor='top',
            font=dict(size=12)
        )
    ]
)

# Update text font for the bar labels
fig.update_traces(textfont_size=12)

# --- 4. Output the Image ---
# Derive the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")