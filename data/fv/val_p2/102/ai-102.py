import sys
import json
from pathlib import Path
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <json_file_path>")
    sys.exit(1)

# Create a Path object for the JSON file
json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

# Load the chart data from the JSON file
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract data components from the loaded JSON
chart_data = data['chart_data']
texts = data['texts']
colors = data['colors']
series_order = data['series_order']

# Initialize a Plotly Figure
fig = go.Figure()

# Add a bar trace for each data series, following the specified order
for series_name in series_order:
    if series_name in chart_data:
        series = chart_data[series_name]
        fig.add_trace(go.Bar(
            x=series['x'],
            y=series['y'],
            name=texts['legend_items'].get(series_name, series_name),
            marker=dict(
                color=colors.get(series_name),
                line=dict(
                    color=colors['outline'],
                    width=2
                )
            ),
            showlegend=True
        ))

# Determine the maximum y-value to set the axis range dynamically
max_y = 0
for series in chart_data.values():
    if series['y']:
        current_max = max(series['y'])
        if current_max > max_y:
            max_y = current_max

# Configure the figure's layout
fig.update_layout(
    font=dict(family="Arial", size=16, color=colors['text']),
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    showlegend=True,
    legend=dict(
        x=1,
        y=1.02,
        xanchor='right',
        yanchor='top',
        bgcolor=colors['background'],
        bordercolor=colors['outline'],
        borderwidth=2,
        traceorder='normal'
    ),
    xaxis=dict(
        showgrid=False,
        showline=False,
        zeroline=False,
        tickmode='array',
        tickvals=list(range(10)),
        ticktext=[str(i) for i in range(10)],
        tickfont=dict(size=14),
        ticks='outside',
        tickcolor=colors['outline'],
        tickwidth=2,
        ticklen=8,
        range=[-0.5, 9.5]
    ),
    yaxis=dict(
        visible=False,
        range=[0, max_y * 1.1] # Add 10% padding to the top
    ),
    margin=dict(l=10, r=10, t=10, b=40),
    bargap=0, # No gap between bars at the same x-coordinate
    bargroupgap=0 # No gap between bar groups
)

# Add the annotation box if its text is defined in the JSON
if texts.get('annotation_text'):
    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=0.98,
        y=0.15,
        xanchor='right',
        yanchor='bottom',
        text=texts['annotation_text'],
        showarrow=False,
        font=dict(family="Arial", size=16, color=colors['text']),
        align='left',
        bgcolor=colors['background'],
        bordercolor=colors['outline'],
        borderwidth=2
    )

# Generate the output PNG image
output_filename = json_path.stem + '.png'
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")