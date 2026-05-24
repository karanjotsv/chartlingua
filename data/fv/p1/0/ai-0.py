import sys
import json
import pathlib
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

fig = go.Figure()

# Main Donut Chart
main_chart_data = data['chart_data']['main_chart']
main_chart_domain = {'x': [0, 1], 'y': [0.4, 1.0]}
fig.add_trace(go.Pie(
    labels=main_chart_data['labels'],
    values=main_chart_data['values'],
    hole=0.65,
    marker_colors=data['colors'],
    domain=main_chart_domain,
    textinfo='none',
    showlegend=False,
    sort=False,
    direction='clockwise',
    rotation=110 # Adjust rotation to place the "Yes" slice correctly
))

# Sub-charts (Donut Multiples)
sub_charts_data = data['chart_data']['sub_charts']
num_charts = len(sub_charts_data)
chart_width = 0.12
spacing = 0.04
total_width = num_charts * chart_width + (num_charts - 1) * spacing
start_x = (1 - total_width) / 2
y_domain = [0.15, 0.35]
annotations = []

for i, chart in enumerate(sub_charts_data):
    x0 = start_x + i * (chart_width + spacing)
    x1 = x0 + chart_width
    values = [chart['value'], 100 - chart['value']]
    
    fig.add_trace(go.Pie(
        values=values,
        hole=0.7,
        marker_colors=data['colors'],
        domain={'x': [x0, x1], 'y': y_domain},
        textinfo='none',
        showlegend=False,
        sort=False,
        direction='clockwise',
        rotation=90 + (chart['value']/100 * 360 / 2) # Center the smaller slice at the top
    ))

    center_x = x0 + chart_width / 2
    center_y = y_domain[0] + (y_domain[1] - y_domain[0]) / 2

    # Percentage annotation above sub-chart
    annotations.append(dict(
        x=center_x, y=y_domain[1] + 0.03,
        xref='paper', yref='paper',
        text=f"<b>{chart['value']}%</b>",
        showarrow=False,
        font=dict(family="Arial", size=14, color='black'),
        xanchor='center', yanchor='bottom'
    ))

    # Category annotation inside sub-chart
    annotations.append(dict(
        x=center_x, y=center_y,
        xref='paper', yref='paper',
        text=f"<b>{chart['label']}</b>",
        showarrow=False,
        font=dict(family="Arial", size=14, color='black'),
        xanchor='center', yanchor='center'
    ))

# Annotations for Main Chart
main_center_x = main_chart_domain['x'][0] + (main_chart_domain['x'][1] - main_chart_domain['x'][0]) / 2
main_center_y = main_chart_domain['y'][0] + (main_chart_domain['y'][1] - main_chart_domain['y'][0]) / 2

# Center Text
annotations.append(dict(
    x=main_center_x, y=main_center_y,
    xref='paper', yref='paper',
    text=f"<b>{data['texts']['main_chart_center_text']}</b>",
    showarrow=False,
    font=dict(family="Arial", size=20, color='black'),
    xanchor='center', yanchor='center'
))

# "Yes" Label
annotations.append(dict(
    x=0.5, y=0.88,
    xref='paper', yref='paper',
    text=f"<b><span style='font-size: 32px;'>{main_chart_data['labels'][0]}</span></b><br>{main_chart_data['values'][0]}%",
    showarrow=False,
    font=dict(family="Arial", size=16, color='white'),
    xanchor='center', yanchor='middle',
    bgcolor=data['colors'][0],
    borderpad=4
))

# "No" Label
annotations.append(dict(
    x=0.8, y=0.55,
    xref='paper', yref='paper',
    text=f"<b><span style='font-size: 32px;'>{main_chart_data['labels'][1]}</span></b><br>{main_chart_data['values'][1]}%",
    showarrow=False,
    font=dict(family="Arial", size=16, color='black'),
    xanchor='center', yanchor='middle'
))

# Source Text Annotation
annotations.append(dict(
    x=0, y=0.01,
    xref='paper', yref='paper',
    text=data['texts']['source'],
    showarrow=False,
    align='left',
    xanchor='left',
    yanchor='top',
    font=dict(family="Arial", size=12)
))

fig.update_layout(
    title_text=f"<b>&#9632; {data['texts']['title']}</b>",
    title_x=0.02,
    title_y=0.98,
    title_xanchor='left',
    title_yanchor='top',
    title_font=dict(family="Arial", size=24),
    paper_bgcolor='white',
    plot_bgcolor='white',
    font_family="Arial",
    margin=dict(t=140, b=280, l=40, r=40),
    annotations=annotations,
    showlegend=False
)

# Generate output filename from JSON path
filename_base = pathlib.Path(json_path).stem
output_filename = f"{filename_base}.png"

# Save the figure
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")