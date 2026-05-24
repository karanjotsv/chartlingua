import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data_json = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data and texts from JSON
chart_data = chart_data_json['chart_data']
texts = chart_data_json['texts']
colors = chart_data_json['colors']

# Prepare data for plotting
y_categories = [item['category'] for item in chart_data]
x_values = [item['value'] for item in chart_data]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=y_categories,
    x=x_values,
    orientation='h',
    marker=dict(color=colors),
    hoverinfo='none'
))

# Combine title and subtitle
title_text = texts['title']
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout
fig.update_layout(
    title=dict(
        text=title_text,
        x=0.05,
        y=0.98,
        xanchor='left',
        yanchor='top',
        font=dict(size=18, family="Arial", color="black")
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False,
        range=[0, 16000]
    ),
    yaxis=dict(
        autorange='reversed',
        showgrid=False,
        tickfont=dict(size=10)
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='#f0f0f0',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=60, r=40, t=80, b=60),
    height=800,
    width=650
)

# Determine output filename from JSON path
if '/' in json_path:
    base_filename = json_path.split('/')[-1].split('.')[0]
elif '\\' in json_path: # Windows path
    base_filename = json_path.split('\\')[-1].split('.')[0]
else:
    base_filename = json_path.split('.')[0]

# Save the figure
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")