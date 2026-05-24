import sys
import json
from pathlib import Path
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path_str = sys.argv[1]
json_path = Path(json_path_str)
output_path = json_path.with_suffix('.png')

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

years = [d['year'] for d in data]
patents = [d['patents_granted'] for d in data]

fig = go.Figure()

# Add the area trace
fig.add_trace(go.Scatter(
    x=years,
    y=patents,
    mode='lines',
    fill='tozeroy',
    fillcolor=colors['area_fill'],
    line=dict(color=colors['line'], width=1.5),
    showlegend=False
))

# Update layout
fig.update_layout(
    plot_bgcolor=colors['plot_background'],
    paper_bgcolor=colors['paper_background'],
    font=dict(family="Arial", size=12, color=colors['main_font']),
    margin=dict(t=100, l=80, r=40, b=80),
    xaxis=dict(
        title=texts['x_axis_title'],
        range=[1870, 2010],
        tickmode='linear',
        tick0=1870,
        dtick=20,
        gridcolor=colors['grid'],
        gridwidth=0.5,
        zeroline=False
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        type='log',
        range=[4, 6], # Corresponds to 10,000 to 1,000,000
        tickvals=[10000, 100000, 1000000],
        ticktext=['10,000', '100,000', '1,000,000'],
        gridcolor=colors['grid'],
        gridwidth=1,
        zeroline=False
    )
)

# Add annotations
fig.add_annotation(
    text=f"<b>{texts['title']}</b>",
    xref="paper", yref="paper",
    x=0.04, y=0.9,
    showarrow=False,
    xanchor='left',
    font=dict(color=colors['title_font'], size=20, family="Arial")
)

fig.add_annotation(
    text=texts['log_plot_annotation'],
    xref="paper", yref="paper",
    x=0.5, y=0.9,
    showarrow=False,
    bgcolor=colors['log_plot_background'],
    borderpad=4,
    font=dict(color=colors['log_plot_text'], size=14, family="Arial")
)

# Header annotations (top right)
fig.add_annotation(
    text=texts['header_patent'],
    xref="paper", yref="paper",
    x=0.73, y=0.98,
    showarrow=False,
    font=dict(size=10)
)
fig.add_annotation(
    text=texts['header_date'],
    xref="paper", yref="paper",
    x=0.8, y=0.98,
    showarrow=False,
    font=dict(size=10)
)
fig.add_annotation(
    text=texts['header_sheet'],
    xref="paper", yref="paper",
    x=0.88, y=0.98,
    showarrow=False,
    font=dict(size=10)
)
fig.add_annotation(
    text=texts['header_number'],
    xref="paper", yref="paper",
    x=0.96, y=0.98,
    showarrow=False,
    font=dict(size=10)
)
fig.add_annotation(
    text=texts['header_fig'],
    xref="paper", yref="paper",
    x=0.86, y=0.90,
    showarrow=False,
    font=dict(size=10)
)

fig.write_image(output_path, scale=2)
print(f"Chart saved to {output_path}")