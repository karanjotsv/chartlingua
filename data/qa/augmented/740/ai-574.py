import sys
import json
import os
import plotly.graph_objects as go

def create_chart(json_path):
    """
    Generates a chart from a JSON file and saves it as a PNG image.
    """
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    chart_data = config['chart_data']
    texts = config['texts']
    colors = config['colors']

    # Extract data and reverse it to match the visual top-to-bottom order
    # Plotly's horizontal bar charts plot the first item at the bottom.
    categories = [item['category'] for item in chart_data]
    values = [item['value'] for item in chart_data]
    categories.reverse()
    values.reverse()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=categories,
        x=values,
        orientation='h',
        marker=dict(color=colors[0]),
        text=[f'{v:g}' for v in values], # Format to remove trailing .0
        textposition='outside',
        textfont=dict(family="Arial", size=12, color='black'),
        cliponaxis=False  # Prevents text from being clipped at the chart edge
    ))

    fig.update_layout(
        font=dict(family="Arial", size=12, color="black"),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            title=texts['x_axis_title'],
            showgrid=True,
            gridcolor='#e0e0e0',
            gridwidth=1,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=True
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            ticks='',
            showticklabels=True
        ),
        showlegend=False,
        margin=dict(l=180, r=60, t=40, b=80), # Adjust margins for labels
        annotations=[
            dict(
                text=texts.get('source', ''),
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0.98,
                y=-0.18,
                xanchor='right',
                yanchor='top',
                align="right",
                font=dict(size=12)
            )
        ]
    )

    # Dynamically set x-axis range to give space for outside text labels
    max_value = max(values) if values else 1
    fig.update_xaxes(range=[0, max_value * 1.18])

    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
        sys.exit(1)
    create_chart(sys.argv[1])