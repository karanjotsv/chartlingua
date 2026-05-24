import sys
import json
import pathlib
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

# Load data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = data.get('chart_data', [])
categories = data.get('categories', [])
texts = data.get('texts', {})
colors = data.get('colors', [])

# Initialize figure
fig = go.Figure()

# Add traces for each data series, preserving order
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series['values'],
        name=series['name'],
        marker_color=colors[i % len(colors)],
        text=[f'{val:,}'.replace(',', ' ') for val in series['values']],
        textposition='inside',
        insidetextanchor='middle'
    ))

# Update layout to match the original chart
fig.update_layout(
    barmode='stack',
    font=dict(
        family="Arial",
        size=12
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        range=[0, 200000],
        tickvals=[0, 50000, 100000, 150000, 200000],
        ticktext=['0', '50 000', '100 000', '150 000', '200 000'],
        showgrid=True,
        gridcolor='lightgrey'
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=False # Vertical grid lines are very faint, omitting for clarity
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, t=40, b=100),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=True,
    annotations=[
        dict(
            text=texts.get('source'),
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.25,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=12)
        )
    ]
)

fig.update_traces(
    insidetextfont=dict(color='white', size=12, family='Arial')
)


# Generate the output filename from the input JSON path
base_filename = pathlib.Path(json_path).stem
output_filename = f"{base_filename}.png"

# Save the figure to a file
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")