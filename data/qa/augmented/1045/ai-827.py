import sys
import json
import os
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    # This is the only print statement, for user guidance on correct usage.
    print(f"Usage: python {os.path.basename(__file__)} <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the chart configuration and data from the specified JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Initialize a Plotly graph objects figure
fig = go.Figure()

# Iterate through the data series in the JSON and add them as traces to the figure
# The order from the JSON is preserved.
for i, series in enumerate(config['chart_data']):
    fig.add_trace(go.Bar(
        x=config['categories'],
        y=series['y'],
        name=series['name'],
        marker_color=config['colors'][i],
        text=series['y'],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white', size=12),
        texttemplate='%{text}'
    ))

# Configure the overall layout of the chart for a clean, professional appearance
fig.update_layout(
    barmode='stack',
    font=dict(family="Arial"),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=config['texts'].get('x_axis_title'),
        showgrid=False,
        type='category',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=config['texts'].get('y_axis_title'),
        gridcolor='#e9e9e9',
        griddash='dash',
        zeroline=False,
        tickfont=dict(size=12)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, t=40, b=150) # Adjust margins to prevent element clipping
)

# Add annotations for source and note text, positioned at the bottom of the chart
if config['texts'].get('note'):
    fig.add_annotation(
        text=config['texts']['note'],
        xref="paper", yref="paper",
        x=0, y=-0.4,
        showarrow=False,
        align="left",
        xanchor="left",
        font=dict(color="#297acc", size=12)
    )

if config['texts'].get('source'):
    fig.add_annotation(
        text=config['texts']['source'],
        xref="paper", yref="paper",
        x=1, y=-0.4,
        showarrow=False,
        align="right",
        xanchor="right",
        font=dict(color="grey", size=12)
    )

# Derive the output filename from the input JSON path's base name
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the generated chart as a high-resolution PNG file
fig.write_image(output_filename, scale=2)