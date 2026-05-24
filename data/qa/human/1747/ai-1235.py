import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_data = json.load(f)

# --- 2. Prepare data for Plotly ---
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Data is presented top-to-bottom in the image. Plotly's y-axis is reversed,
# so we reverse our data lists to match the visual order.
data_reversed = data[::-1]
categories = [d['category'] for d in data_reversed]
series_count = len(texts['series_names'])

x_values = [[d['values'][i] for d in data_reversed] for i in range(series_count)]
text_labels = [[d['labels'][i] for d in data_reversed] for i in range(series_count)]
total_labels = [d['total_label'] for d in data_reversed]
totals = [sum(d['values']) for d in data_reversed]

# --- 3. Create the figure ---
fig = go.Figure()

# Add bar traces for each series
for i in range(series_count):
    fig.add_trace(go.Bar(
        y=categories,
        x=x_values[i],
        name=texts['series_names'][i],
        orientation='h',
        marker=dict(
            color=colors['series'][i],
            line=dict(width=0)
        ),
        text=text_labels[i],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family='Arial',
            size=14,
            color=colors['text_on_bar'][i]
        ),
        hoverinfo='none'
    ))

# --- 4. Add annotations and shapes ---
# Add "Total" value annotations to the right of the bars
for i, total in enumerate(totals):
    fig.add_annotation(
        x=total + 2,  # Position slightly to the right of the bar
        y=categories[i],
        text=f"<b>{total_labels[i]}</b>",
        showarrow=False,
        xanchor='left',
        yanchor='middle',
        font=dict(family='Arial', size=14, color='black')
    )

# Add custom headers above the plotting area
y_header_position = 1.05 # Position in paper coordinates above the plot area
fig.add_annotation(
    x=13.5, y=y_header_position, xref='x', yref='paper',
    text=f"<b>{texts['series_names'][0]}</b>",
    showarrow=False, xanchor='center', font=dict(family='Arial', size=14)
)
fig.add_annotation(
    x=50, y=y_header_position, xref='x', yref='paper',
    text=f"<b>{texts['series_names'][1]}</b>",
    showarrow=False, xanchor='center', font=dict(family='Arial', size=14)
)
fig.add_annotation(
    x=totals[0] + 2, y=y_header_position, xref='x', yref='paper',
    text=f"<b>{texts['total_header']}</b>",
    showarrow=False, xanchor='left', font=dict(family='Arial', size=14)
)


# Add horizontal line above the source
fig.add_shape(
    type="line",
    xref="paper", yref="paper",
    x0=0, y0=-0.18, x1=1, y1=-0.18,
    line=dict(color="black", width=1)
)

# Add source text annotation
fig.add_annotation(
    xref="paper", yref="paper",
    x=0, y=-0.21,
    xanchor="left", yanchor="top",
    align="left",
    text=texts['source'],
    showarrow=False,
    font=dict(family='Arial', size=12, color='#666666')
)


# --- 5. Configure layout ---
full_title = f"<b>{texts['title']}</b><br><span style='font-size:16px;color:#555555;'>{texts['subtitle']}</span>"

fig.update_layout(
    barmode='stack',
    title=dict(
        text=full_title,
        font=dict(family='Arial', size=20, color='black'),
        y=0.97,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        visible=False,
        range=[0, max(totals) + 15] # Ensure space for total labels
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        tickfont=dict(family='Arial', size=14)
    ),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=100, r=40, t=160, b=100),
    bargap=0.4
)

# --- 6. Save the output ---
output_filename = json_path.stem + '.png'
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")