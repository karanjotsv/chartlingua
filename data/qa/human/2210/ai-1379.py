import sys
import json
import pathlib
import plotly.graph_objects as go

# Check if a file path is provided
if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Read the JSON data from the provided file path
json_file_path = pathlib.Path(sys.argv[1])
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_json = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Prepare data and settings from JSON
chart_data = chart_json['chart_data']
categories = chart_json['categories']
texts = chart_json['texts']
colors = chart_json['colors']

# Create the figure
fig = go.Figure()

# Add a bar trace for each data series
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        name=series['name'],
        x=categories,
        y=series['values'],
        marker_color=colors[i],
        text=[f"{v}%" for v in series['values']],
        textposition='outside',
        textfont=dict(color='black', size=12)
    ))

# Update layout
fig.update_layout(
    barmode='group',
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=50, b=120),
    xaxis=dict(
        title_text=texts['xaxis_title'],
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=11)
    ),
    yaxis=dict(
        title_text=texts['yaxis_title'],
        range=[0, 75],
        tickvals=[i * 10 for i in range(8)],
        ticksuffix='%',
        showgrid=True,
        gridcolor='#E5E5E5',
        zeroline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.4,
        xanchor="center",
        x=0.5
    ),
    annotations=[
        dict(
            text=texts['source'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.5,
            xanchor='right',
            yanchor='bottom'
        )
    ]
)

# Add vertical separator lines between groups
fig.add_vline(x=0.5, line_width=1, line_dash="solid", line_color="#E5E5E5")
fig.add_vline(x=1.5, line_width=1, line_dash="solid", line_color="#E5E5E5")

# Generate the output image file path
output_filename = json_file_path.with_suffix('.png')

# Write the image file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")