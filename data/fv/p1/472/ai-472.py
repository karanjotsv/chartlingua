import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

labels = [d.get('label', '') for d in chart_data]
values = [d.get('value', 0) for d in chart_data]
custom_text = [f"{d.get('label', '')}<br>{d.get('value', 0)}%" for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    text=custom_text,
    textinfo='text',
    textposition='outside',
    textfont={'size': 11},
    marker_colors=colors,
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    rotation=90
))

title_text = texts.get('title', '')

fig.update_layout(
    title={
        'text': title_text,
        'y': 0.95,
        'x': 0.82,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'family': 'Arial', 'size': 20, 'color': '#333333'}
    },
    title_font_weight="bold",
    font={'family': "Arial", 'size': 12, 'color': "#000000"},
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin={'t': 100, 'b': 40, 'l': 100, 'r': 100}
)

base_filename = json_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")