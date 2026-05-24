import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Load chart configuration from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data and text from the configuration
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for plotting
x_values = [d.get('x') for d in chart_data]
y_values = [d.get('y') for d in chart_data]

# Initialize the figure
fig = go.Figure()

# Add the bar trace with data labels
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    text=y_values,
    textposition='outside',
    marker_color=colors[0] if colors else None,
    cliponaxis=False,
    textfont=dict(family="Arial", size=12, weight='bold')
))

# Configure the chart layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        type='category',
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 30],
        gridcolor='#dddddd',
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    margin=dict(l=80, r=40, t=50, b=80),
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref="paper", yref="paper",
            x=1, y=-0.2,
            xanchor='right', yanchor='top',
            align='right',
            font=dict(size=10, family="Arial")
        )
    ]
)

# Determine the output filename from the input JSON path
if '/' in json_file_path:
    base_name = json_file_path.split('/')[-1]
else:
    base_name = json_file_path

if '\\' in base_name: # Handle Windows paths
    base_name = base_name.split('\\')[-1]

output_filename = base_name.replace('.json', '.png')

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")