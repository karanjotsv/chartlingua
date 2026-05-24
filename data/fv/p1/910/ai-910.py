import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

fig = go.Figure()

# Add traces
for i, series in enumerate(chart_data['chart_data']):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines',
        line=dict(color=chart_data['colors'][i])
    ))

# Update layout
texts = chart_data['texts']
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        title=texts['x_axis_title'],
        showline=True,
        linewidth=1,
        linecolor='black',
        gridcolor='#E5E5E5',
        tickvals=['Oct 02', 'Oct 04', 'Oct 06', 'Oct 08', 'Oct 10']
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 75000],
        showline=False,
        gridcolor='#E5E5E5'
    ),
    legend=dict(
        x=1.02,
        y=0.95,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(255,255,255,0)',
        bordercolor='black',
        borderwidth=1
    ),
    margin=dict(l=80, r=280, t=50, b=80),
)

# Generate output filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the chart as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")