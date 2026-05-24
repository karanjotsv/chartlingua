import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Reverse data for correct top-to-bottom display in Plotly horizontal bar chart
categories.reverse()
values.reverse()

# Format text labels for bars with spaces as thousands separators
text_labels = [f'{v:,}'.replace(',', ' ') for v in values]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=text_labels,
    textposition='outside',
    textfont=dict(family='Arial', size=12, color='black'),
    cliponaxis=False
))

fig.update_layout(
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=280, r=80, t=50, b=80),
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#EAEAEA',
        gridwidth=1,
        griddash='dot',
        zeroline=False,
        showline=True,
        linecolor='black',
        mirror=True,
        range=[0, max(values) * 1.3], # Dynamic range to fit labels
        tickvals=[0, 1000000, 2000000, 3000000, 4000000, 5000000, 6000000],
        ticktext=['0', '1 000 000', '2 000 000', '3 000 000', '4 000 000', '5 000 000', '6 00...']
    ),
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False,
        showline=True,
        linecolor='black',
        mirror=True,
        ticks='outside'
    ),
    showlegend=False,
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            align='right',
            font=dict(family="Arial", size=12, color="gray")
        )
    ]
)

# Derive output filename from the input JSON file path
base_name = json_file_path.rsplit('.', 1)[0]
output_filename = f"{base_name}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")