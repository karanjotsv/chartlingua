import sys
import json
import plotly.graph_objects as go

def create_chart(json_path):
    """
    Reads chart data from a JSON file and generates a Plotly chart.
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_info = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    chart_data = chart_info.get('chart_data', [])
    texts = chart_info.get('texts', {})
    colors = chart_info.get('colors', [])

    categories = [d.get('category') for d in chart_data]
    values = [d.get('value') for d in chart_data]

    # Create text labels, displaying only the one explicitly shown in the original image.
    # The original shows the label for the maximum value.
    max_value = max(values) if values else 0
    text_labels = [str(v) if v == max_value else '' for v in values]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color=colors,
        text=text_labels,
        textposition='outside',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        cliponaxis=False
    ))

    title_text = texts.get('title', '')
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts['subtitle']}</sub>"

    fig.update_layout(
        title_text=title_text,
        title_x=0.5,
        title_font=dict(
            family="Arial",
            size=18,
            color='black'
        ),
        xaxis_title=texts.get('x_axis_title', ''),
        yaxis_title=texts.get('y_axis_title', ''),
        font=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        yaxis=dict(
            range=[0, 45],
            tickmode='linear',
            dtick=5,
            gridcolor='#EAEAEA',
            zeroline=False,
            showline=True,
            linewidth=1,
            linecolor='grey'
        ),
        xaxis=dict(
            showline=True,
            linewidth=1,
            linecolor='grey'
        ),
        margin=dict(l=80, r=40, b=80, t=100)
    )

    # Derive output filename from the input JSON path
    base_filename = json_path.rsplit('.', 1)[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create_chart.py <path_to_json_file>")
        sys.exit(1)
    
    json_file_path = sys.argv[1]
    create_chart(json_file_path)