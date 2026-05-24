import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    chart_data = chart_config.get('chart_data', [])
    texts = chart_config.get('texts', {})
    colors = chart_config.get('colors', [])

    categories = [item['category'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color=colors[0] if colors else None,
        text=values,
        textposition='outside',
        texttemplate='%{text:.2f}',
        cliponaxis=False 
    ))

    fig.update_layout(
        font_family="Arial",
        font_size=12,
        plot_bgcolor='white',
        showlegend=False,
        margin=dict(l=80, r=40, t=50, b=100),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showgrid=False,
            showline=True,
            linecolor='lightgrey',
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            title_standoff=15,
            showgrid=True,
            gridcolor='lightgrey',
            griddash='dot',
            showline=False,
            zeroline=False,
            range=[0, 5],
            tickvals=[0, 1, 2, 3, 4, 5],
            tickfont=dict(size=12)
        ),
        annotations=[
            dict(
                text=texts.get('source', ''),
                align='right',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=1.0,
                y=-0.22,
                xanchor='right',
                yanchor='bottom',
                font=dict(size=12)
            )
        ]
    )

    output_filename_base = pathlib.Path(json_path).stem
    output_png_path = f"{output_filename_base}.png"
    
    fig.write_image(output_png_path, scale=2)
    print(f"Chart saved to {output_png_path}")

if __name__ == "__main__":
    main()