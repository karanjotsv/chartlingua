import sys
import json
import os
import plotly.graph_objects as go

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print("Usage: python generate_chart.py <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {json_path} was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: The file {json_path} is not a valid JSON.")
        sys.exit(1)

    chart_data = config.get('chart_data', [])
    texts = config.get('texts', {})
    colors = config.get('colors', [])

    categories = [item['category'] for item in chart_data]
    values = [item['value'] for item in chart_data]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color=colors[0] if colors else '#2E75B5',
        text=values,
        texttemplate='%{y}%',
        textposition='inside',
        insidetextanchor='end',
        textfont=dict(
            family="Arial",
            size=14,
            color="black"
        ),
        hoverinfo='none'
    ))

    fig.update_layout(
        title_text=texts.get('title'),
        yaxis=dict(
            title_text=texts.get('y_axis_title'),
            range=[0, 80],
            dtick=10,
            ticksuffix='%',
            showgrid=True,
            gridcolor='lightgray',
            griddash='dot',
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor='black'
        ),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showline=False
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial"),
        showlegend=False,
        margin=dict(l=80, r=40, t=40, b=100),
        annotations=[
            dict(
                text=texts.get('source'),
                showarrow=False,
                xref='paper',
                yref='paper',
                x=0.98,
                y=-0.2,
                xanchor='right',
                yanchor='top',
                align='right',
                font=dict(
                    family="Arial",
                    size=12,
                    color="grey"
                )
            )
        ] if texts.get('source') else []
    )

    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()