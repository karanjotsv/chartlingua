import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for the required command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <path_to_json_file>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from the file '{json_path}'.")
    sys.exit(1)

# Extract data and texts from the loaded JSON
data_series = chart_data['chart_data']
categories = chart_data['categories']
texts = chart_data['texts']
colors = chart_data['colors']

# Initialize the figure
fig = go.Figure()

# Add traces for each data series
for i, series in enumerate(data_series):
    # Format text labels to show '.0' as an integer, and others with one decimal place
    text_labels = [f'{v:.1f}'.replace('.0', '') for v in series['values']]
    
    fig.add_trace(go.Bar(
        x=categories,
        y=series['values'],
        name=series['name'],
        marker_color=colors[i],
        text=text_labels,
        textposition='outside',
        textfont=dict(
            family="Arial",
            size=12,
            color='#333333'
        ),
        cliponaxis=False # Ensures text labels are not clipped by the plot area
    ))

# Configure the layout
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    xaxis=dict(
        title_text=None,
        showgrid=True,
        gridcolor='#f0f0f0',
        linecolor='black',
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 35],
        showgrid=True,
        gridcolor='#e0e0e0',
        linecolor='black',
        zeroline=False
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5
    ),
    margin=dict(l=80, r=40, t=50, b=120),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.99,
            y=-0.3,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(
                size=12,
                color='#7f7f7f'
            )
        )
    ]
)

# Derive the output filename from the input JSON path
output_filename = pathlib.Path(json_path).stem + ".png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")