import sys
import json
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
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and text from the configuration
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Prepare data for plotting
categories = [d['category'] for d in chart_data]
# The data series are: Cumulative Revenue, Weekly Revenue, Weekly Rank
series1_data = [d['values'][0] for d in chart_data]
series2_data = [d['values'][1] for d in chart_data]
series3_data = [d['values'][2] for d in chart_data]

# Initialize figure
fig = go.Figure()

# Add traces based on the JSON data
# Trace 1: Cumulative Revenue (Grey Bar - not in legend)
if texts['legend_labels'][0]:
    fig.add_trace(go.Bar(
        x=categories,
        y=series1_data,
        name=texts['legend_labels'][0],
        marker_color=colors[0]
    ))
else: # If legend label is null, don't show it in the legend
    fig.add_trace(go.Bar(
        x=categories,
        y=series1_data,
        name=texts['legend_labels'][0],
        marker_color=colors[0],
        showlegend=False
    ))

# Trace 2: Weekly Revenue (Blue Bar - stacked on grey)
fig.add_trace(go.Bar(
    x=categories,
    y=series2_data,
    name=texts['legend_labels'][1],
    marker_color=colors[1]
))

# Trace 3: Weekly Rank (Yellow Line - on secondary y-axis)
fig.add_trace(go.Scatter(
    x=categories,
    y=series3_data,
    name=texts['legend_labels'][2],
    yaxis='y2',
    mode='lines',
    line=dict(color=colors[2], width=2)
))

# Update layout for a professional appearance and accuracy
fig.update_layout(
    barmode='stack',
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        tickmode='linear',
        dtick=1
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 30],
        gridcolor='lightgrey'
    ),
    yaxis2=dict(
        title_text=texts.get('y_axis2_title'),
        overlaying='y',
        side='right',
        showgrid=False,
        range=[10.5, 0.5], # Inverted axis for rank
        tickmode='linear',
        tick0=1,
        dtick=1
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=60, r=60, t=30, b=120),
    title=texts.get('title'),
)

# Determine the output filename from the input JSON path
# e.g., 'path/to/my_chart.json' becomes 'my_chart.png'
base_name = json_path.split('/')[-1].rsplit('.', 1)[0]
output_filename = f"{base_name}.png"


# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")