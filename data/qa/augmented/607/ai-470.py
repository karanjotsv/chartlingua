import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file provided as a command-line argument ---
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data_json = json.load(f)
except FileNotFoundError:
    print(f"Error: The file {json_path} was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file {json_path} is not a valid JSON.")
    sys.exit(1)

# --- 2. Extract data and text from the JSON structure ---
data = chart_data_json['chart_data']
texts = chart_data_json['texts']
colors = chart_data_json['colors']

y_categories = [item['category'] for item in data]
x_values = [item['value'] for item in data]
text_labels = [item['label'] for item in data]

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=y_categories,
    x=x_values,
    text=text_labels,
    textposition='outside',
    texttemplate='%{text}',
    marker_color=colors[0],
    orientation='h',
    hoverinfo='none',
    cliponaxis=False
))

# --- 4. Configure the layout and styling ---

# Combine title and subtitle
title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    title=dict(text=title_text, x=0.05, xanchor='left'),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='lightgray',
        griddash='dot',
        zeroline=False,
        showline=False,
        ticks='',
        range=[0, max(x_values) * 1.25]  # Extend range to fit labels
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        autorange="reversed",  # To display categories from top to bottom
        showgrid=False,
        ticks='',
        showline=False
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=260, r=80, t=50, b=80),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0.99, y=-0.15,
            xanchor='right', yanchor='top',
            text=texts.get('source'),
            showarrow=False,
            font=dict(size=12)
        )
    ]
)

# --- 5. Output the chart as a PNG file ---
base_name = pathlib.Path(json_path).stem
output_filename = f"{base_name}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")