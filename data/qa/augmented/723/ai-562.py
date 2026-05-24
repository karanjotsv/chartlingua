import sys
import json
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Load data from the specified JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file {json_path} was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Failed to decode JSON from {json_path}.")
    sys.exit(1)

# Extract data from the loaded JSON
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# Initialize the figure
fig = go.Figure()

# Add traces for each data series
text_positions = ['top center', 'bottom center']
for i, series in enumerate(chart_data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines+markers+text',
        line=dict(color=colors[i]),
        marker=dict(color=colors[i], size=8),
        text=series['y'],
        textposition=text_positions[i % len(text_positions)],
        textfont=dict(
            family="Arial",
            size=12,
            color=colors[i]
        )
    ))

# Create annotations for source and note
annotations = []
if texts.get('note'):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=0, y=-0.25,
        xanchor='left', yanchor='bottom',
        text=f"<span style='color:#4C85E5;'>{texts['note']}</span>",
        showarrow=False,
        font=dict(family="Arial", size=12)
    ))
if texts.get('source'):
    annotations.append(dict(
        xref='paper', yref='paper',
        x=1, y=-0.25,
        xanchor='right', yanchor='bottom',
        text=texts['source'],
        showarrow=False,
        font=dict(family="Arial", size=12, color="#7f7f7f")
    ))

# Update layout
fig.update_layout(
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    xaxis=dict(
        tickvals=chart_data[0]['x'],
        showgrid=False,
        zeroline=False,
        title_text=texts.get('x_axis_title')
    ),
    yaxis=dict(
        range=[15.5, 19],
        gridcolor='#E5E5E5',
        zeroline=False,
        title_text=texts.get('y_axis_title')
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.18,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=60, r=40, t=40, b=120),
    annotations=annotations,
    showlegend=True
)

# Define output filename based on the input JSON filename
if json_path.endswith('.json'):
    output_filename = json_path[:-5] + '.png'
else:
    output_filename = json_path + '.png'

# Save the figure as a high-resolution PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")