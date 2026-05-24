import sys
import json
import plotly.graph_objects as go
import os

# Check for the correct number of command-line arguments
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' is not a valid JSON file.")
    sys.exit(1)

# Extract data, texts, and colors from the JSON object
data = chart_info.get('chart_data', {})
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', {})
settings = chart_info.get('settings', {})

# Assign data to variables
x_vals = data.get('x', [])
y_outer_upper = data.get('y_outer_upper', [])
y_fill_upper = data.get('y_fill_upper', [])
y_fill_lower = data.get('y_fill_lower', [])
y_inner_lower = data.get('y_inner_lower', [])

# Initialize the figure
fig = go.Figure()

# Add the filled area trace first for correct layering
if x_vals and y_fill_upper and y_fill_lower:
    fig.add_trace(go.Scatter(
        x=x_vals + x_vals[::-1],
        y=y_fill_upper + y_fill_lower[::-1],
        fill='toself',
        fillcolor=colors.get('fill', '#FFFF00'),
        line_color='rgba(0,0,0,0)',
        hoverinfo='none',
        showlegend=False
    ))

# Define the common style for the magenta lines
line_style = dict(color=colors.get('lines', '#FF00FF'), width=3, dash='dot')

# Add the four line traces
for y_series in [y_outer_upper, y_fill_upper, y_fill_lower, y_inner_lower]:
    if x_vals and y_series:
        fig.add_trace(go.Scatter(
            x=x_vals, y=y_series,
            mode='lines', line=line_style,
            hoverinfo='none', showlegend=False
        ))

# Add the horizontal line across the plot
horizontal_line_y = settings.get('horizontal_line_y')
if horizontal_line_y is not None and x_vals:
    fig.add_shape(type="line",
        x0=min(x_vals), y0=horizontal_line_y,
        x1=max(x_vals), y1=horizontal_line_y,
        line=dict(color=colors.get('horizontal_line', '#C0C0C0'), width=2)
    )
    
# Add arrowheads using scatter markers, a robust method
if x_vals and y_outer_upper:
    fig.add_trace(go.Scatter(
        x=[max(x_vals)], y=[0],
        mode='markers', marker_symbol='triangle-right',
        marker_color=colors.get('axes', '#000000'), marker_size=15,
        hoverinfo='none', showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=[0], y=[max(y_outer_upper)],
        mode='markers', marker_symbol='triangle-up',
        marker_color=colors.get('axes', '#000000'), marker_size=15,
        hoverinfo='none', showlegend=False
    ))

# Update the layout of the chart
fig.update_layout(
    plot_bgcolor=colors.get('background', '#808080'),
    paper_bgcolor=colors.get('background', '#808080'),
    font=dict(family="Arial"),
    margin=dict(l=80, r=40, t=40, b=80),
    xaxis=dict(
        title=dict(text=f"<b>{texts.get('x_axis_title', '')}</b>", font=dict(size=22, color=colors.get('axes', '#000000'))),
        showgrid=False, zeroline=False, showline=True,
        linewidth=3, linecolor=colors.get('axes', '#000000'),
        showticklabels=False, range=[min(x_vals) if x_vals else 0, max(x_vals) if x_vals else 1]
    ),
    yaxis=dict(
        title=dict(text=f"<b>{texts.get('y_axis_title', '')}</b>", font=dict(size=22, color=colors.get('axes', '#000000'))),
        showgrid=False, zeroline=False, showline=True,
        linewidth=3, linecolor=colors.get('axes', '#000000'),
        showticklabels=False, range=[0, max(y_outer_upper) * 1.05 if y_outer_upper else 1]
    ),
    showlegend=False
)

# Determine the output filename and save the chart
output_filename_base = os.path.splitext(json_path)[0]
output_filename = f"{output_filename_base}.png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")