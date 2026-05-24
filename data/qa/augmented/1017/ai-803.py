import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read the chart data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' is not a valid JSON.")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add traces to the figure by iterating through the chart data
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series.get('x'),
        y=series.get('y'),
        mode='lines+markers',
        name=series.get('name', ''),
        line=dict(color=colors[i % len(colors)], width=3),
        marker=dict(color=colors[i % len(colors)], size=8),
        hoverinfo='skip'
    ))

# Combine source and note for the footer right annotation
footer_right_text = f"{texts.get('source', '')}&nbsp;&nbsp;&nbsp;&nbsp;{texts.get('note', '')}"

# Update the layout of the figure for a professional and clean look
fig.update_layout(
    font=dict(family="Arial", size=14),
    plot_bgcolor='white',
    showlegend=False,
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#f0f0f0',
        gridwidth=1.5,
        zeroline=False
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dash',
        zeroline=False,
        tickprefix=' ',
        ticksuffix=' '
    ),
    margin=dict(l=100, r=40, t=40, b=120),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('footer_left', ''),
            xref='paper',
            yref='paper',
            x=0,
            y=-0.25,
            xanchor='left',
            yanchor='top',
            font=dict(size=12, color='#0073e5')
        ),
        dict(
            showarrow=False,
            text=footer_right_text,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.25,
            xanchor='right',
            yanchor='top',
            font=dict(size=12, color='#666666')
        )
    ]
)

# Derive the output filename from the input JSON file path
base_filename = json_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")