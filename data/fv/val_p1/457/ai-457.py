import sys
import json
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
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

# Create figure with two subplots
fig = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.1
)

# Extract data for convenience
scatter_series = chart_data['chart_data']['scatter_plot']
step_series = chart_data['chart_data']['step_plot']
colors = chart_data['colors']
texts = chart_data['texts']

# Add scatter plot traces (top subplot)
for i, series in enumerate(scatter_series):
    fig.add_trace(
        go.Scatter(
            x=series['x'],
            y=series['y'],
            mode='markers',
            name=series['name'],
            marker=dict(color=colors[i], size=8),
            legendgroup=series['name'],
            showlegend=True
        ),
        row=1, col=1
    )

# Add step plot traces (bottom subplot)
for i, series in enumerate(step_series):
    fig.add_trace(
        go.Scatter(
            x=series['x'],
            y=series['y'],
            mode='lines',
            name=series['name'],
            line=dict(color=colors[i], shape='hv', width=2),
            legendgroup=series['name'],
            showlegend=False
        ),
        row=2, col=1
    )


# Update layout and styling
fig.update_layout(
    title=dict(
        text=texts['title'],
        x=0.5,
        font=dict(size=14)
    ),
    legend_title_text=texts['legend_title'],
    font_family="Arial",
    plot_bgcolor='#F0F0F0',
    paper_bgcolor='white',
    height=700,
    margin=dict(l=80, r=40, t=100, b=80)
)

# Update axes for top subplot
fig.update_yaxes(
    title_text=texts['y_axis_label_top'],
    row=1, col=1,
    tickvals=[1, 2, 3],
    ticktext=texts['y_axis_tick_labels_top'],
    gridcolor='white',
    zeroline=False,
    range=[0.5, 3.5]
)
fig.update_xaxes(
    row=1, col=1,
    gridcolor='white',
    zeroline=False,
    showticklabels=True
)

# Update axes for bottom subplot
fig.update_yaxes(
    title_text=texts['y_axis_label_bottom'],
    row=2, col=1,
    gridcolor='white',
    zeroline=False,
    range=[-1, 21]
)
fig.update_xaxes(
    title_text=texts['x_axis_label_bottom'],
    row=2, col=1,
    gridcolor='white',
    zeroline=False,
    tickformat='%b %d'
)

# Set common x-axis range
x_min = min(step_series[i]['x'][0] for i in range(len(step_series)))
x_max = max(step_series[i]['x'][-1] for i in range(len(step_series)))
fig.update_xaxes(range=[x_min, x_max])


# Generate output filename from JSON path
filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{filename_base}.png"

# Save the figure
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")