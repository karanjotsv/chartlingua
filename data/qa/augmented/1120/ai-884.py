import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts
data_series = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Create the figure
fig = go.Figure()

# Add a trace for each data series
for i, series in enumerate(data_series):
    fig.add_trace(go.Bar(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        text=series['text'],
        textposition='outside',
        marker_color=colors[i],
        cliponaxis=False 
    ))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    barmode='group',
    bargap=0.2, 
    bargroupgap=0.1,
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        showline=True,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts['y_axis_title'],
        showgrid=True,
        gridcolor='#E0E0E0',
        zeroline=False,
        range=[0, 80],
        tickvals=[0, 20, 40, 60],
        ticksuffix='%'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3, 
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, t=40, b=120),
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
            font=dict(size=12, color='#666666')
        )
    ]
)

fig.update_traces(
    textfont_size=12
)

# Generate output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")