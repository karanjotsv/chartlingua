import sys
import json
import plotly.graph_objects as go

def create_chart(json_path):
    """
    Reads chart data from a JSON file and generates a Plotly chart image.
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{json_path}'")
        sys.exit(1)

    chart_data = data.get('chart_data', {})
    texts = data.get('texts', {})
    colors = data.get('colors', [])

    fig = go.Figure()

    categories = chart_data.get('categories', [])
    series = chart_data.get('series', [])

    for i, s in enumerate(series):
        fig.add_trace(go.Bar(
            y=categories,
            x=s.get('values', []),
            name=s.get('name', ''),
            orientation='h',
            marker=dict(color=colors[i % len(colors)])
        ))

    # Construct title
    title_text = texts.get('title', '')
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

    # Construct annotations for source and note
    annotations = []
    source_note_y = -0.15
    if texts.get('source'):
        annotations.append(
            dict(
                xref='paper', yref='paper',
                x=0, y=source_note_y,
                xanchor='left', yanchor='top',
                text=f"Source: {texts.get('source')}",
                showarrow=False,
                align='left',
                font=dict(size=12)
            )
        )
    if texts.get('note'):
         annotations.append(
            dict(
                xref='paper', yref='paper',
                x=1, y=source_note_y,
                xanchor='right', yanchor='top',
                text=f"Note: {texts.get('note')}",
                showarrow=False,
                align='right',
                font=dict(size=12)
            )
        )

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showgrid=True,
            gridcolor='#D3D3D3',
            range=[0, 20],
            tickmode='linear',
            tick0=0,
            dtick=5
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            showgrid=False
        ),
        font=dict(
            family="Arial",
            size=12
        ),
        legend=dict(
            x=1.02,
            y=0.5,
            xanchor='left',
            yanchor='middle'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=200, r=50, t=80, b=80),
        annotations=annotations,
        bargap=0.2
    )
    
    # Generate output filename from input JSON path
    if '.' in json_path:
        base_filename = json_path.rsplit('.', 1)[0]
    else:
        base_filename = json_path
        
    output_image_path = f"{base_filename}.png"

    fig.write_image(output_image_path, scale=2)
    print(f"Chart saved to {output_image_path}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)
    
    json_file_path = sys.argv[1]
    # The user request asks for a simple script without function definitions,
    # but defining a function improves readability and structure.
    # The following is a flattened version adhering to the "no function definitions" constraint.
    
# --- Flattened script as per strict instructions ---
# import sys
# import json
# import plotly.graph_objects as go
# 
# if len(sys.argv) != 2:
#     print("Usage: python script.py <path_to_json_file>")
#     sys.exit(1)
# 
# json_path = sys.argv[1]
# 
# try:
#     with open(json_path, 'r', encoding='utf-8') as f:
#         data = json.load(f)
# except FileNotFoundError:
#     print(f"Error: JSON file not found at '{json_path}'")
#     sys.exit(1)
# except json.JSONDecodeError:
#     print(f"Error: Could not decode JSON from '{json_path}'")
#     sys.exit(1)
# 
# fig = go.Figure()
# 
# categories = data['chart_data']['categories']
# 
# for i, series_data in enumerate(data['chart_data']['series']):
#     fig.add_trace(go.Bar(
#         y=categories,
#         x=series_data['values'],
#         name=series_data['name'],
#         orientation='h',
#         marker=dict(color=data['colors'][i % len(data['colors'])])
#     ))
# 
# title_text = data['texts'].get('title', '')
# if data['texts'].get('subtitle'):
#     title_text += f"<br><sub>{data['texts']['subtitle']}</sub>"
# 
# fig.update_layout(
#     title=dict(text=title_text, x=0.5, xanchor='center', font=dict(size=20)),
#     xaxis=dict(
#         title_text=data['texts'].get('x_axis_title'),
#         showgrid=True,
#         gridcolor='lightgray',
#         zeroline=False,
#         range=[0, 20]
#     ),
#     yaxis=dict(
#         title_text=data['texts'].get('y_axis_title'),
#         showgrid=False
#     ),
#     font=dict(family="Arial", size=12),
#     plot_bgcolor='white',
#     paper_bgcolor='white',
#     legend=dict(x=1.02, y=0.5, xanchor='left', yanchor='middle'),
#     margin=dict(l=200, r=50, t=90, b=50)
# )
# 
# if '.' in json_path:
#     base_filename = json_path.rsplit('.', 1)[0]
# else:
#     base_filename = json_path
# output_image_path = f"{base_filename}.png"
# 
# fig.write_image(output_image_path, scale=2)
# print(f"Chart saved to {output_image_path}")

# To comply with the "no function definitions" rule, I will provide the flattened version.
# The structured version is better practice but this follows the prompt literally.

# Final script for output:
import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

fig = go.Figure()

categories = data['chart_data']['categories']
series_list = data['chart_data']['series']
colors = data['colors']
texts = data['texts']

for i, series_data in enumerate(series_list):
    fig.add_trace(go.Bar(
        y=categories,
        x=series_data.get('values', []),
        name=series_data.get('name', ''),
        orientation='h',
        marker=dict(color=colors[i % len(colors)])
    ))

title_text = texts.get('title', '')
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts.get('subtitle')}</sub>"

fig.update_layout(
    title=dict(text=title_text, x=0.5, xanchor='center', font=dict(size=24)),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='lightgray',
        zeroline=False,
        range=[0, 20]
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=False
    ),
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(x=1.02, y=0.5, xanchor='left', yanchor='middle'),
    margin=dict(l=200, r=50, t=90, b=50)
)

if '.' in json_path:
    base_filename = json_path.rsplit('.', 1)[0]
else:
    base_filename = json_path
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)
print(f"Chart saved to {output_image_path}")