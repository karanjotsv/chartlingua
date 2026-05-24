import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data and texts from the JSON structure
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

x_values = [d['year'] for d in chart_data]
y_values = [d['value'] for d in chart_data]

# Initialize the figure
fig = go.Figure()

# Add the main line trace
fig.add_trace(go.Scatter(
    x=x_values,
    y=y_values,
    mode='lines+markers',
    line=dict(color=colors[0], width=2.5),
    marker=dict(color=colors[0], size=7),
    hoverinfo='none'
))

# Add annotations for data point labels
annotations = []
for point in chart_data:
    if point.get('label'):
        annotations.append(
            go.layout.Annotation(
                x=point['year'],
                y=point['value'],
                text=point['label'],
                showarrow=False,
                font=dict(family="Arial", size=12, color="#333333"),
                xanchor='center',
                yanchor='bottom',
                yshift=10
            )
        )

# Add source annotation
if texts.get('source'):
    annotations.append(go.layout.Annotation(
        showarrow=False,
        text=texts['source'],
        xref="paper",
        yref="paper",
        x=1,
        y=-0.15,
        xanchor='right',
        yanchor='top',
        align='right',
        font=dict(family="Arial", size=12, color="#888888")
    ))

# Update layout
fig.update_layout(
    annotations=annotations,
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=80, r=40, t=40, b=100),
    xaxis=dict(
        tickmode='array',
        tickvals=x_values,
        ticktext=[str(year) for year in x_values],
        showgrid=False,
        linecolor='lightgrey'
    ),
    yaxis=dict(
        title=dict(text=texts.get('y_axis_title'), standoff=10),
        range=[2.5, 20],
        dtick=2.5,
        ticksuffix='%',
        gridcolor='#e9e9e9',
        gridwidth=1,
        zeroline=False
    )
)

# Determine output filename and save the image
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")