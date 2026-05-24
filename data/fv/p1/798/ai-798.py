import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

# Get JSON file path from command-line argument
json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data for plotting
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Create the figure
fig = go.Figure()

# Add traces to the figure
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=series.get('x', []),
        y=series.get('y', []),
        name=series.get('name', ''),
        marker_color=colors[i % len(colors)] if colors else None
    ))

# Update layout for styling and accuracy
fig.update_layout(
    title=dict(
        text=f"<b>{texts.get('title', '')}</b>",
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top',
        font=dict(size=20)
    ),
    xaxis=dict(
        title=dict(
            text=f"<b>{texts.get('x_axis_title', '')}</b>",
            standoff=15
        ),
        tickangle=-45,
        showgrid=False
    ),
    yaxis=dict(
        title=dict(text=None),  # Title is added via annotation for specific placement
        range=[0, 14],
        dtick=2,
        gridcolor='#D3D3D3',
        showgrid=True,
        zeroline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial"),
    legend=dict(
        orientation='v',
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.01
    ),
    margin=dict(l=60, r=150, b=120, t=80)
)

# Add a custom annotation for the Y-axis title to match the original's horizontal placement
fig.add_annotation(
    text=f"<b>{texts.get('y_axis_title', '')}</b>",
    align='left',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=0,
    y=1,
    yshift=20,
    font=dict(size=12)
)

# Determine output filename from the input JSON path
if '.' in json_path:
    output_base = json_path.rsplit('.', 1)[0]
else:
    output_base = json_path

output_filename = f"{output_base}.png"

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")