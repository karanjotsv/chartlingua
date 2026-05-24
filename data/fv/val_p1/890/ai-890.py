import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Read data from JSON file, ensuring UTF-8 encoding
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' is not a valid JSON file.")
    sys.exit(1)


# Extract data and texts from the configuration
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']
categories = chart_data['categories']
series_data = chart_data['series']

# Initialize the figure
fig = go.Figure()

# Add a trace for each data series
# Iterate through the series and colors to build the stacked bars
for i, series in enumerate(series_data):
    fig.add_trace(go.Bar(
        y=categories,
        x=series['values'],
        name=series['name'],
        orientation='h',
        marker=dict(
            color=colors[i],
            line=dict(color='white', width=0) # No border between segments
        )
    ))

# Update layout to match the original chart
fig.update_layout(
    barmode='stack',
    title=dict(
        text=texts['title'],
        x=0.5,
        xanchor='center',
        font=dict(size=24)
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False
    ),
    legend=dict(
        x=0.98,
        y=0.35,
        xanchor='right',
        yanchor='top',
        bgcolor='rgba(255, 255, 255, 0.7)',
        bordercolor='rgba(0,0,0,0)',
        borderwidth=0,
        font=dict(
           size=14
        )
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    paper_bgcolor='#f0f0f0',
    plot_bgcolor='white',
    margin=dict(l=240, r=20, t=80, b=80)
)

# Determine the output filename from the input JSON path
if json_path.lower().endswith('.json'):
    output_filename = json_path[:-5] + '.png'
else:
    output_filename = json_path + '.png'


# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")