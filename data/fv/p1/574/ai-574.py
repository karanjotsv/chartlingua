import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Load data from JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Initialize figure
fig = go.Figure()

# Iterate through each data series in the JSON
for i, series in enumerate(chart_data["chart_data"]):
    color = chart_data["colors"][i]
    series_name = series["name"]

    # Add the main line trace
    fig.add_trace(go.Scatter(
        x=series["x_line"],
        y=series["y_line"],
        mode='lines',
        line=dict(color=color, width=2),
        name=series_name,
        legendgroup=series_name,
        showlegend=False
    ))

    # Add the scatter plot for individual data points
    fig.add_trace(go.Scatter(
        x=series["x_scatter"],
        y=series["y_scatter"],
        mode='markers',
        marker=dict(color=color, size=4),
        name=series_name,
        legendgroup=series_name,
        showlegend=True
    ))

    # Add the large start point
    fig.add_trace(go.Scatter(
        x=series["x_start_point"],
        y=series["y_start_point"],
        mode='markers',
        marker=dict(
            color=color,
            size=10,
            line=dict(width=1, color='black')
        ),
        name=series_name,
        legendgroup=series_name,
        showlegend=False
    ))

# Update layout
texts = chart_data["texts"]
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=50, r=50, t=50, b=50),
    xaxis=dict(
        tickvals=texts["x_axis_labels"],
        ticktext=texts["x_axis_labels"],
        showgrid=True,
        gridwidth=1,
        gridcolor='#D3D3D3',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True
    ),
    yaxis=dict(
        tickvals=texts["y_axis_labels"],
        ticktext=texts["y_axis_labels"],
        range=[min(texts["y_axis_labels"]), max(texts["y_axis_labels"])],
        showgrid=True,
        gridwidth=1,
        gridcolor='#D3D3D3',
        showline=True,
        linewidth=1,
        linecolor='black',
        mirror=True
    ),
    legend=dict(
        x=1.02,
        y=0.8,
        traceorder='normal',
        bgcolor='rgba(0,0,0,0)'
    )
)

# Generate output filename
if '.' in json_path:
    base_name = json_path.rsplit('.', 1)[0]
else:
    base_name = json_path
output_filename = f"{base_name}.png"

# Save the figure
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")