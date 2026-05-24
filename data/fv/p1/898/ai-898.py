import sys
import json
import plotly.graph_objects as go

def create_chart(json_path):
    """
    Generates a chart from a JSON file and saves it as a PNG image.
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{json_path}'")
        sys.exit(1)

    chart_data = chart_config['chart_data']
    texts = chart_config['texts']
    colors = chart_config['colors']

    # Data must be reversed for horizontal bar charts in Plotly to display correctly (top to bottom)
    categories = [item['category'] for item in chart_data][::-1]
    values = [item['value'] for item in chart_data][::-1]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=categories,
        x=values,
        orientation='h',
        marker=dict(color=colors[0]),
        text=values,
        texttemplate='%{x:,.0f}',
        textposition='outside',
        cliponaxis=False
    ))

    # Construct title
    title_text = f"<b>{texts['title']}</b>"
    if texts.get('subtitle'):
        title_text += f"<br><sub>{texts['subtitle']}</sub>"

    # Construct source/note
    source_text = ""
    if texts.get('source'):
        source_text = f"<sub>{texts['source']}</sub>"

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            xanchor='center',
            font=dict(size=18)
        ),
        xaxis=dict(
            title=texts['x_axis_title'],
            showgrid=True,
            gridcolor='#d3d3d3',
            zeroline=False,
            automargin=True
        ),
        yaxis=dict(
            title=texts['y_axis_title'],
            showgrid=False,
            zeroline=False,
            autorange="reversed" # This is another way, but reversing data is safer
        ),
        font=dict(
            family="Arial",
            size=12,
            color="black"
        ),
        plot_bgcolor='#f0f0f0',
        paper_bgcolor='#f0f0f0',
        showlegend=False,
        margin=dict(l=280, r=80, t=100, b=80),
        annotations=[
            dict(
                text=source_text,
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0,
                y=-0.15,  # Adjust this value to position the source text
                xanchor='left',
                yanchor='top',
                align='left'
            )
        ]
    )
    
    # Adjust x-axis range to prevent text from being cut off
    fig.update_xaxes(range=[0, max(values) * 1.15])

    # Derive output filename from JSON path
    if '.' in json_path:
        base_name = json_path.rsplit('.', 1)[0]
    else:
        base_name = json_path

    output_filename = f"{base_name}.png"
    
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)
    
    json_file_path = sys.argv[1]
    create_chart(json_file_path)