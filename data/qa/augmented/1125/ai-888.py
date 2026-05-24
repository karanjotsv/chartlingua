import sys
import json
import pathlib
import plotly.graph_objects as go

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{json_path}'")
        sys.exit(1)

    chart_data = config['chart_data']
    texts = config['texts']
    colors = config['colors']

    x_values = [d['x'] for d in chart_data]
    y_values = [d['y'] for d in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=x_values,
        y=y_values,
        marker_color=colors[0],
        name=''
    ))

    fig.update_layout(
        font_family="Arial",
        plot_bgcolor='white',
        showlegend=False,
        yaxis_title=texts['y_axis_title'],
        margin=dict(l=80, r=40, t=50, b=120),
        yaxis=dict(
            title_standoff=15,
            showgrid=True,
            gridcolor='#e0e0e0',
            gridwidth=1,
            griddash='dot',
            range=[0, 1050],
            tickformat=" ",
            separatethousands=True,
            zeroline=False
        ),
        xaxis=dict(
            showgrid=False,
            tickmode='array',
            tickvals=x_values,
            ticktext=[str(x) for x in x_values]
        )
    )

    # Add annotations for sources and notes
    if texts.get('source_left'):
        fig.add_annotation(
            text=texts['source_left'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.22,
            xanchor='left',
            yanchor='top',
            font=dict(color="#1f77b4")
        )

    if texts.get('source_right'):
        fig.add_annotation(
            text=texts['source_right'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.22,
            xanchor='right',
            yanchor='top'
        )

    base_filename = pathlib.Path(json_path).stem
    output_filename = f"{base_filename}.png"
    
    fig.write_image(output_filename, scale=2, width=900, height=600)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()