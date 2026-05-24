import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_filepath = sys.argv[1]

# Ensure the JSON file exists
if not pathlib.Path(json_filepath).is_file():
    print(f"Error: JSON file not found at '{json_filepath}'")
    sys.exit(1)

# Read data from the specified JSON file
try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON in file '{json_filepath}'")
    sys.exit(1)

# Extract data and texts for plotting
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Prepare data labels with suffix
data_labels = [f"{v}{texts.get('data_label_suffix', '')}" for v in values]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=data_labels,
    textposition='outside',
    marker_color=colors[0],
    cliponaxis=False,
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    )
))

# Update layout for a professional look and feel
fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=False,
        tickangle=-45
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 105],
        dtick=20,
        ticksuffix=texts.get('data_label_suffix', ''),
        gridcolor='#EAEAEA',
        gridwidth=1,
        griddash='dot',
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1
    ),
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=120),  # Increased bottom margin for labels and source
    annotations=[
        dict(
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=-0.28,
            xanchor='right',
            yanchor='top',
            text=texts.get('source'),
            font=dict(
                size=12,
                color='grey'
            )
        )
    ]
)

# Derive output filename from the JSON file's base name
output_filename = pathlib.Path(json_filepath).stem + '.png'

# Write the image file
try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully saved to '{output_filename}'")
except Exception as e:
    print(f"Error saving image: {e}")
    sys.exit(1)