import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

fig = go.Figure()

for i, series in enumerate(data):
    fig.add_trace(go.Scatter(
        x=series['x'],
        y=series['y'],
        name=series['name'],
        mode='lines+markers',
        line=dict(color=colors[i], width=2),
        marker=dict(color=colors[i], size=6)
    ))

fig.update_layout(
    font_family="Arial",
    title_text=f"<b style='font-size: 24px'>{texts['title']}</b><br><span style='font-size: 16px; color:#555555'>{texts['subtitle']}</span>",
    title_x=0.03,
    title_y=0.95,
    title_xanchor='left',
    title_yanchor='top',
    showlegend=False,
    plot_bgcolor='#EBF4F8',
    paper_bgcolor='white',
    margin=dict(l=40, r=150, t=120, b=50),
    xaxis=dict(
        tickmode='array',
        tickvals=[1992, 1994, 1996, 1998, 2000, 2002, 2004, 2006],
        ticktext=['1992', '1994', '1996', '1998', '2000', '2002', '2004', '06'],
        showgrid=False,
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='#368CC7',
        range=[1991.5, 2008.5]
    ),
    yaxis=dict(
        range=[0, 100],
        dtick=10,
        gridcolor='#FFFFFF',
        zeroline=False,
        showline=False
    ),
    annotations=[]
)

# Add annotations for series labels
for i, series in enumerate(data):
    fig.add_annotation(
        x=series['x'][-1],
        y=series['y'][-1],
        text=series['name'],
        showarrow=False,
        xanchor='left',
        xshift=10,
        font=dict(
            family="Arial",
            size=12,
            color="black"
        ),
        bgcolor='white',
        borderpad=4
    )

# Add source annotation
fig.add_annotation(
    x=0.99,
    y=1.05,
    xref='paper',
    yref='paper',
    text=texts['source'],
    showarrow=False,
    xanchor='right',
    yanchor='bottom',
    font=dict(
        family="Arial",
        size=12,
        color="#555555"
    )
)

base_filename = json_file_path.rsplit('/', 1)[-1].rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")