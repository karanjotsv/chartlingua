import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

fig = go.Figure()

# Extract data for plotting
chart_data = data['chart_data'][0]
texts = data['texts']
colors = data['colors']

# Add the line trace
fig.add_trace(go.Scatter(
    x=chart_data['x'],
    y=chart_data['y'],
    mode='lines+markers',
    marker=dict(
        color=colors[0],
        symbol='diamond',
        size=8
    ),
    line=dict(
        color=colors[0],
        width=2
    ),
    showlegend=False
))

# Add annotations
for ann in texts.get('annotations', []):
    fig.add_annotation(
        x=ann['x'],
        y=ann['y'],
        text=ann['text'],
        showarrow=False,
        font=dict(
            family="Arial",
            size=12
        ),
        xanchor='center',
        yanchor='bottom',
        yshift=10
    )

# Configure layout
fig.update_layout(
    font=dict(family="Arial"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        tickmode='array',
        tickvals=[1968, 1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2012],
        ticktext=[str(y) for y in [1968, 1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2012]],
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=False,
        linecolor='black',
        linewidth=1,
        ticks='outside'
    ),
    yaxis=dict(
        tickmode='array',
        tickvals=list(range(len(texts['y_axis_labels']))),
        ticktext=texts['y_axis_labels'],
        showgrid=True,
        gridcolor='lightgrey',
        zeroline=False,
        linecolor='black',
        linewidth=1,
        ticks='',
        range=[-0.5, 8.5]
    ),
    margin=dict(l=180, r=40, t=40, b=40)
)

# Generate output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")