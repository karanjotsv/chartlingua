import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' contains invalid JSON.")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_config.get('chart_data', {})
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])
categories = chart_data.get('categories', [])
series = chart_data.get('series', [])

# Create the figure object
fig = go.Figure()

# Add a bar trace for each data series
for i, s in enumerate(series):
    fig.add_trace(go.Bar(
        x=categories,
        y=s.get('data', []),
        name=s.get('name', ''),
        marker_color=colors[i % len(colors)],
        text=[f"{val}%" for val in s.get('data', [])],
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='black', weight='bold'),
        cliponaxis=False
    ))

# Update layout to match the source image
fig.update_layout(
    barmode='group',
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=texts.get('title') if texts.get('title') else '',
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_title'),
        range=[0, 37],
        dtick=5,
        ticksuffix='%',
        showgrid=True,
        gridcolor='#e0e0e0',
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
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=50, b=150),
    annotations=[
        dict(
            text=texts.get('source', ''),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.98,
            y=-0.35,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=12)
        )
    ]
)

# Define output filename from the input JSON path
base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")