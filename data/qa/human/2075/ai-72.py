import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]
if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
    
output_filename_base = os.path.splitext(os.path.basename(json_path))[0]
output_image_path = f"{output_filename_base}.png"

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON file at {json_path}")
    sys.exit(1)

chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

labels = [d['label'] for d in chart_data]
values = [d['value'] for d in chart_data]

fig = go.Figure()

fig.add_trace(go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='white', width=1)),
    hoverinfo='label+percent',
    textinfo='none', # Text will be handled by annotations
    sort=False,
    direction='clockwise',
    pull=[0] * len(values)
))

annotations = []
for i, data_point in enumerate(chart_data):
    # This part for creating external labels manually is more complex
    # Plotly's default 'outside' textposition is usually sufficient.
    # The original image seems to have a custom connector/label style
    # that is hard to replicate perfectly without more complex logic.
    # For robustness, we will rely on Plotly's standard outside labeling.
    pass # Reverting to standard labeling for simplicity and robustness

# Add source annotation
if texts.get('source'):
    annotations.append(
        dict(
            text=texts['source'],
            showarrow=False,
            xref="paper",
            yref="paper",
            x=1,
            y=0,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=12, color="grey"),
            align="right"
        )
    )

fig.update_traces(
    texttemplate='%{label} %{value}%',
    textposition='outside',
    textfont=dict(family="Arial", size=14)
)

fig.update_layout(
    title_text=texts.get('title'),
    showlegend=False,
    font=dict(family="Arial"),
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=80, r=80, t=80, b=80),
    annotations=annotations,
    width=800,
    height=600
)


try:
    fig.write_image(output_image_path, scale=2)
    print(f"Chart saved to {output_image_path}")
except ValueError as e:
     if "requires the kaleido package" in str(e):
        print("Error: The 'kaleido' package is required for image export. Please install it using 'pip install kaleido'")
        sys.exit(1)
     else:
        raise e