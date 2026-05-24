import sys
import json
import os
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    fig = go.Figure()

    chart_data = data.get('chart_data', {})
    categories = chart_data.get('categories', [])
    series = chart_data.get('series', [])
    colors = data.get('colors', [])
    texts = data.get('texts', {})

    for i, s in enumerate(series):
        fig.add_trace(go.Bar(
            x=categories,
            y=s.get('y', []),
            name=s.get('name', ''),
            marker_color=colors[i] if i < len(colors) else None,
            text=[f"{val}%" for val in s.get('y', [])],
            textposition='outside',
            textfont=dict(family='Arial', size=12, color='#000000'),
            cliponaxis=False
        ))

    annotations = []
    source_text = texts.get('source')
    if source_text:
        annotations.append(dict(
            xref='paper', yref='paper',
            x=0.99, y=-0.28,
            xanchor='right', yanchor='top',
            text=source_text,
            showarrow=False,
            font=dict(family='Arial', size=12, color='grey')
        ))
        
    fig.update_layout(
        barmode='group',
        plot_bgcolor='white',
        font=dict(family='Arial', size=12, color='black'),
        margin=dict(l=60, r=20, t=50, b=150),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showgrid=False,
            zeroline=True,
            zerolinecolor='#333333',
            zerolinewidth=1,
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            range=[0, 26],
            tickvals=[0, 5, 10, 15, 20, 25],
            gridcolor='#e0e0e0',
            griddash='dot',
            zeroline=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        annotations=annotations
    )

    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == '__main__':
    main()