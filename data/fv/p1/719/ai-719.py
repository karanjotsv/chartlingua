import sys
import json
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON object
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add traces to the figure by iterating through the chart_data
for i, series in enumerate(chart_data):
    color = colors[i] if i < len(colors) else None
    
    trace_params = {
        'x': series.get('x'),
        'y': series.get('y'),
        'name': series.get('name'),
        'mode': series.get('mode')
    }

    if series.get('type') == 'scatter':
        trace_params['marker'] = dict(
            color=color,
            symbol=series.get('marker_symbol', 'circle'),
            size=series.get('marker_size', 10),
            line=dict(color='black', width=1)
        )
        fig.add_trace(go.Scatter(**trace_params))
    elif series.get('type') == 'line':
        trace_params['line'] = dict(
            color=color,
            width=series.get('line_width', 2)
        )
        fig.add_trace(go.Scatter(**trace_params))

# Update layout
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        x=0.5,
        xanchor='center',
        font=dict(size=16)
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        type='log',
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1,
        showline=True,
        linewidth=2,
        linecolor='black',
        mirror=True,
        tickvals=[30, 100, 1000, 7000],
        ticktext=['30', '100', '1000', '7000'],
        zeroline=False
    ),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='lightgray',
        gridwidth=1,
        showline=True,
        linewidth=2,
        linecolor='black',
        mirror=True,
        tickformat='%H:%M<br>%b %d<br>%Y',
        dtick=12*60*60*1000 # 12 hours
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.5, # Position legend below the x-axis labels
        xanchor="center",
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    margin=dict(l=80, r=40, t=80, b=180) # Adjust margins for labels and legend
)

# Derive output filename from JSON path
if json_file_path.endswith('.json'):
    output_filename = json_file_path[:-5] + '.png'
else:
    output_filename = json_file_path + '.png'

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")