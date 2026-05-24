import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data from the JSON object
categories = chart_info['categories']
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

fig = go.Figure()

# Add a bar trace for each data series in the specified order
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series['values'],
        name=series['name'],
        marker_color=colors[i]
    ))

# Update layout to create a stacked bar chart and apply styling
fig.update_layout(
    barmode='stack',
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    margin=dict(l=120, r=30, t=30, b=120),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showline=True,
        linecolor='black',
        linewidth=1,
        mirror=True
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 10000000],
        tickformat=',',
        showgrid=True,
        gridcolor='#e0e0e0',
        griddash='dash',
        zeroline=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        mirror=True
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5,
        traceorder='normal'
    )
)

# Determine output filename from the input JSON path
if '.' in json_path:
    output_filename_base = json_path.rsplit('.', 1)[0]
else:
    output_filename_base = json_path

output_filename = f"{output_filename_base}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")