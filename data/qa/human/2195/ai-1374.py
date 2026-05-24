import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_filepath = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_filepath, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_filepath}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_filepath}'")
    sys.exit(1)

# Extract data and texts from the JSON object
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

# Create the figure
fig = go.Figure()

# Add a trace for each data series
for i, series in enumerate(chart_data['series']):
    fig.add_trace(go.Bar(
        x=chart_data['categories'],
        y=series['y'],
        name=series['name'],
        marker_color=colors[i],
        text=[f"{val}%" for val in series['y']],
        textposition='outside',
        textfont=dict(family="Arial", size=11, color='black'),
        cliponaxis=False
    ))

# Build combined title string
title_text = ""
if texts.get("title"):
    title_text += f"<b>{texts['title']}</b>"
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update the layout for a professional appearance
fig.update_layout(
    barmode='group',
    title=dict(text=title_text, x=0.05, xanchor='left'),
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 70],
        ticksuffix='%',
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=40, b=120, t=50),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1,
            y=-0.35,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=10)
        )
    ]
)

# Derive output filename from the input JSON filename
output_filename = json_filepath.rsplit('.', 1)[0] + '.png'

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")