import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_filepath = sys.argv[1]

# Construct the output image path from the JSON filename
output_image_path = json_filepath.rsplit('.', 1)[0] + '.png'

# Read and parse the JSON file
try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_filepath}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_filepath}'")
    sys.exit(1)

# Extract data and texts from the configuration
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
# Format text on bars to match original image (e.g., "4 522")
bar_texts = [f"{v:,}".replace(",", " ") for v in values]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=bar_texts,
    textposition='auto',
    marker_color=colors[0] if colors else '#1f77b4',
    textfont=dict(
        family="Arial",
        size=12
    ),
    hoverinfo='none'
))

# Configure the layout
y_axis_max = 9000
tick_step = 1000
y_tick_vals = list(range(0, y_axis_max + 1, tick_step))
y_tick_texts = [f"{v:,}".replace(",", " ") for v in y_tick_vals]

fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('xaxis_title'),
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont_size=12
    ),
    yaxis=dict(
        title_text=texts.get('yaxis_title'),
        range=[0, y_axis_max],
        tickvals=y_tick_vals,
        ticktext=y_tick_texts,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        tickfont_size=12
    ),
    margin=dict(l=100, r=40, t=40, b=100),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.99,
            y=-0.18,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(
                size=12
            )
        )
    ]
)

# Write the image to a file
fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")