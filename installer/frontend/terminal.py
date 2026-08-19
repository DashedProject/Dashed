import socket

import qrcode
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

PORT = 8001

console = Console()

def get_local_ip():
    connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        connection.connect(("8.8.8.8", 80))
        return connection.getsockname()[0]
    finally:
        connection.close()


def render_qr(url):
    qr = qrcode.QRCode(border=1)
    qr.add_data(url)
    qr.make(fit=True)

    matrix = qr.get_matrix()
    lines = []

    for y in range(0, len(matrix), 2):
        line = ""

        for x in range(len(matrix[0])):
            top = matrix[y][x]
            bottom = y + 1 < len(matrix) and matrix[y + 1][x]

            if top and bottom:
                line += "█"
            elif top:
                line += "▀"
            elif bottom:
                line += "▄"
            else:
                line += " "

        lines.append(line)

    return "\n".join(lines)


def terminal_ui():
    url = f"http://{get_local_ip()}:{PORT}"
    qr = render_qr(url)

    content = Text()
    content.append("Dashed Installer\n", style="bold cyan")
    content.append("Ready to be used\n\n", style="bold green")
    content.append("Open the following link in your browser:\n\n", style="dim")
    content.append(f"{url}\n\n", style="bold white")
    content.append(qr, style="white")
    content.append("\n\nOr scan the QR code to open the installer.", style="dim")

    console.print(
        Panel(
            content,
            border_style="cyan",
            padding=(1, 4),
            expand=False,
        )
    )