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
    config = json.load(f)

# Extract data and text from the JSON structure
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
annotations_data = config['annotations_data']

# Initialize the figure
fig = go.Figure()

# Add data series to the figure
for series, color in zip(chart_data, colors):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines',
        line=dict(color=color, width=2.5),
        hoverinfo='none'
    ))

# Add vertical lines and annotations for Km values
km_i = annotations_data['km_inhibited']
km_u = annotations_data['km_uninhibited']

# Vertical lines from x-axis to the curve
fig.add_shape(type="line", x0=km_i['x'], y0=0, x1=km_i['x'], y1=km_i['y'], line=dict(color="black", width=1.5))
fig.add_shape(type="line", x0=km_u['x'], y0=0, x1=km_u['x'], y1=km_u['y'], line=dict(color="black", width=1.5))

# --- Custom X-axis annotations and brackets ---
# Y-coordinates in 'paper' unit for consistent positioning below the plot area
Y_TEXT_PAPER = -0.18
Y_BRACKET_END_PAPER = -0.15
Y_TICK_BOTTOM_PAPER = -0.07

# Annotation for Km (inhibited)
fig.add_annotation(x=km_i['x'], y=Y_TEXT_PAPER, text=km_i['label'], showarrow=False, xref="x", yref="paper", font_size=11)
fig.add_shape(type="line", xref="x", yref="paper", x0=km_i['x'], y0=0, x1=km_i['x'], y1=Y_TICK_BOTTOM_PAPER, line=dict(color="black", width=1))
fig.add_shape(type="line", xref="x", yref="paper", x0=km_i['x'], y0=Y_TICK_BOTTOM_PAPER, x1=km_i['x'] - 0.4, y1=Y_BRACKET_END_PAPER, line=dict(color="black", width=1))
fig.add_shape(type="line", xref="x", yref="paper", x0=km_i['x'], y0=Y_TICK_BOTTOM_PAPER, x1=km_i['x'] + 0.4, y1=Y_BRACKET_END_PAPER, line=dict(color="black", width=1))

# Annotation for Km (uninhibited)
fig.add_annotation(x=km_u['x'], y=Y_TEXT_PAPER, text=km_u['label'], showarrow=False, xref="x", yref="paper", font_size=11)
fig.add_shape(type="line", xref="x", yref="paper", x0=km_u['x'], y0=0, x1=km_u['x'], y1=Y_TICK_BOTTOM_PAPER, line=dict(color="black", width=1))
fig.add_shape(type="line", xref="x", yref="paper", x0=km_u['x'], y0=Y_TICK_BOTTOM_PAPER, x1=km_u['x'] - 0.7, y1=Y_BRACKET_END_PAPER, line=dict(color="black", width=1))
fig.add_shape(type="line", xref="x", yref="paper", x0=km_u['x'], y0=Y_TICK_BOTTOM_PAPER, x1=km_u['x'] + 0.7, y1=Y_BRACKET_END_PAPER, line=dict(color="black", width=1))

# Update layout for axes, titles, legend, and aesthetics
fig.update_layout(
    font=dict(family="Arial", size=12),
    yaxis_title=texts['y_axis_title'],
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        tickmode='array',
        tickvals=[0],
        ticktext=['0'],
        range=[-0.5, 31],
        showticklabels=True
    ),
    yaxis=dict(
        title_standoff=10,
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        range=[0, 1.01],
        tickmode='linear',
        dtick=0.1
    ),
    plot_bgcolor='white',
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.35,
        xanchor='center',
        x=0.5,
        font_size=11
    ),
    margin=dict(l=70, r=30, t=30, b=150)
)

# Add x-axis title as an annotation to position it on the right
fig.add_annotation(
    text=texts['x_axis_title'],
    xref="paper", yref="paper",
    x=1.0, y=-0.1,
    showarrow=False,
    xanchor='right',
    font_size=12
)

# Generate the output image file
output_filename_base = json_path.stem
fig.write_image(f"{output_filename_base}.png", scale=2)
print(f"Chart saved to {output_filename_base}.png")