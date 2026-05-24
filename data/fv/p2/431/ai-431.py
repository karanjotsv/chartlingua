import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Load all data and configuration from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' is not a valid JSON file.")
    sys.exit(1)


# Extract data, texts, and colors from the loaded configuration
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']

categories = chart_data['categories']
series = chart_data['series']
right_data = series[0]['data']
left_data = series[2]['data']

# Initialize the figure
fig = go.Figure()

# Add the horizontal bars that connect the 'right' and 'left' points
fig.add_trace(go.Bar(
    y=categories,
    x=[l - r for r, l in zip(right_data, left_data)],
    base=right_data,
    orientation='h',
    marker=dict(
        color=colors['range_bar'],
        line_width=0
    ),
    showlegend=False,
    hoverinfo='none'
))

# Add the scatter points for 'right', 'center', and 'left'
marker_size = 18
for i, s in enumerate(series):
    fig.add_trace(go.Scatter(
        x=s['data'],
        y=categories,
        mode='markers',
        marker=dict(
            color=colors['series'][i],
            size=marker_size,
            line=dict(width=1.5, color='white')
        ),
        name=s['name'],
        showlegend=False,
        hoverinfo='x'
    ))

# --- Create a custom legend at the bottom of the chart ---
# Define positions and dimensions for legend elements in paper coordinates
legend_y_base = -0.22
legend_y_text = -0.3
legend_x_positions = [0.25, 0.5, 0.75]
plot_width, plot_height = 900, 750
circle_x_radius = 0.015
circle_y_radius = circle_x_radius * (plot_width / plot_height)

# Add a gray bar as a backdrop for the legend markers
fig.add_shape(
    type="rect",
    xref="paper", yref="paper",
    x0=legend_x_positions[0], y0=legend_y_base - 0.005,
    x1=legend_x_positions[2], y1=legend_y_base + 0.005,
    fillcolor=colors['range_bar'],
    layer="below",
    line_width=0
)

# Add colored circles and text labels for each legend item
for i, text in enumerate(texts['legend_items']):
    # Add a circle shape for the marker
    fig.add_shape(
        type="circle",
        xref="paper", yref="paper",
        x0=legend_x_positions[i] - circle_x_radius,
        y0=legend_y_base - circle_y_radius,
        x1=legend_x_positions[i] + circle_x_radius,
        y1=legend_y_base + circle_y_radius,
        fillcolor=colors['series'][i],
        line=dict(color='white', width=1.5)
    )
    # Add the text annotation
    fig.add_annotation(
        xref="paper", yref="paper",
        x=legend_x_positions[i], y=legend_y_text,
        text=text,
        showarrow=False,
        font=dict(family="Arial", size=14),
        xanchor='center',
        yanchor='top'
    )

# --- Update layout for final presentation ---
fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        xanchor='center',
        font=dict(family="Arial", size=24, color='black')
    ),
    yaxis=dict(
        title=dict(
            text=texts['y_axis_title'],
            font=dict(family="Arial", size=18, color='black')
        ),
        showgrid=True,
        gridcolor='#E5E5E5',
        tickfont=dict(family="Arial", size=14, color='black'),
        autorange="reversed" # Ensures categories are displayed top-to-bottom
    ),
    xaxis=dict(
        range=[0, 100],
        tickmode='linear',
        tick0=0,
        dtick=10,
        ticksuffix='%',
        showgrid=True,
        gridcolor='#E5E5E5',
        zeroline=False,
        tickfont=dict(family="Arial", size=16, color='black')
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=120, r=40, t=100, b=220), # Increase bottom margin for legend
    showlegend=False,
    height=plot_height,
    width=plot_width
)

# Generate the output filename from the input JSON filename
# e.g., "path/to/my_chart.json" -> "my_chart.png"
base_filename = json_path.split('/')[-1].rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")