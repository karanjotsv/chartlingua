import sys
import json
import pathlib
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the chart data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from the JSON structure
data_series = chart_data.get('chart_data', [])
texts = chart_data.get('texts', {})
colors = chart_data.get('colors', [])

# Prepare data for Plotly: extract categories and values
# The data is read in the visual order (top to bottom)
categories = [item['category'] for item in data_series]
values = [item['value'] for item in data_series]

# Reverse the lists because Plotly plots horizontal bars from bottom to top by default
categories.reverse()
values.reverse()

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(
        color=colors[0] if colors else '#EA3323',
        line_width=0
    ),
    text=values,
    textposition='inside',
    insidetextanchor='end',
    textfont=dict(
        family='Arial',
        size=16,
        color='white',
        weight='bold'
    ),
    hoverinfo='none'
))

# Update layout for a clean, accurate representation
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        y=0.9,
        xanchor='center',
        yanchor='middle',
        font=dict(
            family='Arial',
            size=28,
            color='black',
            weight='bold'
        )
    ),
    xaxis=dict(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        showline=False,
        domain=[0.3, 1] # Provide space for y-axis labels
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='',
        tickfont=dict(
            family='Arial',
            size=20,
            color='black'
        ),
        automargin=False # Manual domain for precise control
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    width=800,
    height=600,
    margin=dict(l=10, r=10, t=120, b=40)
)

# Generate the output filename from the input JSON path
output_filename_base = pathlib.Path(json_path).stem
output_png_path = f"{output_filename_base}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_png_path, scale=2)

print(f"Chart saved to {output_png_path}")