import sys
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Derive the output filename base from the JSON path
filename_base = json_path.split('/')[-1].split('.')[0]

# Load data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and settings from the JSON object
data_series = chart_data.get('chart_data', [])
colors = chart_data.get('colors', [])

# Create a figure with two subplots stacked vertically
fig = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.03,
    row_heights=[0.7, 0.3]
)

# Add traces to the subplots
for i, series in enumerate(data_series):
    fig.add_trace(
        go.Scatter(
            x=series['x'],
            y=series['y'],
            mode='lines',
            name=series['name'],
            line=dict(color=colors[i], width=1.5),
            showlegend=False
        ),
        row=i + 1,
        col=1
    )

# Add annotations to serve as subplot titles
# Annotation for the top subplot
fig.add_annotation(
    text=f"— {data_series[0]['name']}",
    align='left',
    showarrow=False,
    xref='paper',
    yref='y domain',
    x=0,
    y=1,
    xanchor='left',
    yanchor='bottom',
    font=dict(family="Arial", size=12, color=colors[0])
)

# Annotation for the bottom subplot
fig.add_annotation(
    text=f"— {data_series[1]['name']}",
    align='left',
    showarrow=False,
    xref='paper',
    yref='y2 domain',
    x=0,
    y=1.05,
    xanchor='left',
    yanchor='bottom',
    font=dict(family="Arial", size=12, color=colors[1])
)

# Update layout
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=50, r=20, t=40, b=40),
    font=dict(family="Arial", size=12),
    height=600,
    width=800
)

# Configure axes
fig.update_xaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor='lightgray',
    zeroline=False
)
fig.update_yaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor='lightgray',
    zeroline=False
)

# Specific axis configurations
# Top subplot Y-axis
fig.update_yaxes(
    range=[350, 1700],
    tickvals=[450, 550, 650, 750, 850, 950, 1050, 1150, 1250, 1350, 1450, 1550, 1650],
    row=1, col=1
)

# Bottom subplot Y-axis
fig.update_yaxes(
    range=[-5, 105],
    tickvals=[0, 20, 40, 60, 80, 100],
    row=2, col=1
)

# Bottom subplot X-axis (the only one with labels)
fig.update_xaxes(
    range=[1994.5, 2009.8],
    tickvals=list(range(1995, 2010)),
    tickformat='d',  # Format as integer
    minor=dict(
        ticklen=4,
        tickcolor="black",
        showgrid=False
    ),
    ticks='outside',
    row=2, col=1
)


# Save the figure to a PNG file
output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")