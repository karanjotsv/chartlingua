import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: File not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {json_path}")
    sys.exit(1)

# Extract data and texts from JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

# Create the pie chart trace
pie_trace = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='#FFFFFF', width=1)),
    textinfo='percent',
    textfont=dict(family="Arial", size=14, color='black'),
    textposition='outside',
    hoverinfo='label+percent',
    sort=False,  # Preserve the order from the JSON file
    direction='clockwise'
)

fig = go.Figure(data=[pie_trace])

# Update layout for a clean and accurate presentation
fig.update_layout(
    title=dict(
        text=texts.get('title'),
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(family="Arial", size=26, color='black')
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5
    ),
    font=dict(family="Arial", size=14),
    margin=dict(l=50, r=50, t=120, b=120),
    paper_bgcolor='#EAEAF2',
    plot_bgcolor='#EAEAF2',
    showlegend=True
)

# Derive the output filename from the input JSON path
if json_path.endswith('.json'):
    base_filename = json_path[:-5]
else:
    base_filename = json_path
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to {output_filename}")