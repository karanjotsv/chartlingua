import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
output_filename = json_path.rsplit('.', 1)[0] + '.png'

with open(json_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

chart_data_list = config['chart_data']
texts = config['texts']
colors = config['colors']

# Prepare data for Plotly; horizontal bar charts are plotted from bottom to top
categories = [d['category'] for d in chart_data_list]
values = [d['value'] for d in chart_data_list]
labels = [d['label'] for d in chart_data_list]

categories.reverse()
values.reverse()
labels.reverse()
colors.reverse()

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors, line=dict(width=0)),
    text=labels,
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    hoverinfo='none',
    cliponaxis=False
))

# Combine title and subtitle using HTML for styling
full_title = f"{texts['title']}<br><span style='font-size:13px;color:#555555;'>{texts['subtitle']}</span>"

# Combine source and branding for the bottom annotation
source_and_branding = f"{texts['source']}<br>{texts['branding']}"

fig.update_layout(
    title=dict(
        text=full_title,
        y=0.96,
        x=0.01,
        xanchor='left',
        yanchor='top',
        font=dict(family="Arial", size=18, color='black')
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
        range=[0, max(values) * 1.15]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        autorange=False, # Use reversed data order
        range=[-0.5, len(categories) - 0.5],
        tickfont=dict(family="Arial", size=12)
    ),
    margin=dict(l=280, r=40, t=130, b=120),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    font=dict(family="Arial")
)

# Add separator line below the top bar
# There are 9 categories. After reversal, top bar is at index 8. Line is between 8 and 7.
fig.add_shape(
    type="line",
    xref="paper", yref="y",
    x0=0, y0=7.5, x1=1, y1=7.5,
    line=dict(color="lightgrey", width=1)
)

# Add source and branding annotation at the bottom
fig.add_annotation(
    text=source_and_branding,
    xref="paper", yref="paper",
    x=0, y=0,
    xanchor="left", yanchor="top",
    align="left",
    showarrow=False,
    font=dict(family="Arial", size=11, color='#666666'),
    yshift=-35
)

fig.write_image(output_filename, scale=2)

print(f"Chart generated and saved to {output_filename}")