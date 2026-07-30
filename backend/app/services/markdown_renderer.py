import markdown


def markdown_to_html(markdown_text: str) -> str:
    """
    Convert Markdown into styled HTML.
    """

    html = markdown.markdown(
        markdown_text,
        extensions=[
            "tables",
            "fenced_code",
        ],
    )

    return f"""
<!DOCTYPE html>
<html>

<head>

<style>

body {{

    font-family: Arial, sans-serif;

    margin: 40px;

    line-height: 1.7;

}}

h1 {{

    color: #1E3A8A;

}}

h2 {{

    color: #2563EB;

}}

table {{

    border-collapse: collapse;

    width:100%;

}}

table, th, td {{

    border:1px solid #ccc;

}}

th, td {{

    padding:10px;

}}

code {{

    background:#f4f4f4;

    padding:2px 5px;

}}

pre {{

    background:#f4f4f4;

    padding:15px;

}}

</style>

</head>

<body>

{html}

</body>

</html>
"""