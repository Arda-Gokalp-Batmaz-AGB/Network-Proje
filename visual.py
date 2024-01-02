import threading
import tkinter as tk
from tkinter import ttk
import udp_server
import udp_client
from tkinter import Canvas

class CommunicationVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("UDP Communication Visualizer")
        self.geometry("800x400")

        # Create a Canvas widget
        self.canvas = Canvas(self, width=800, height=400)
        self.canvas.pack()

        # Draw labels for Host and Client
        self.canvas.create_text(200, 30, text="Host (Server)", font=("Arial", 16))
        self.canvas.create_text(600, 30, text="Client (Computer)", font=("Arial", 16))

        # Draw vertical lines to represent Host and Client
        self.canvas.create_line(200, 50, 200, 350, arrow=tk.LAST)
        self.canvas.create_line(600, 50, 600, 350, arrow=tk.LAST)

        self.next_event_y = 60

    def add_event(self, source, destination, seq, ack, length, status="normal"):
        colors = {"normal": "green", "lost": "red", "corrupted": "orange"}
        color = colors.get(status, "black")

        x0, y0, x1, y1 = (600, self.next_event_y, 200, self.next_event_y) if source == "client" else (200, self.next_event_y, 600, self.next_event_y)
        self.canvas.create_line(x0, y0, x1, y1, arrow=tk.LAST, fill=color)
        self.canvas.create_text((x0 + x1) / 2, y0 + 10, text=f"Seq: {seq}, Ack: {ack}, Length: {length}", fill=color)

        self.next_event_y += 40
        if self.next_event_y > 350:
            self.next_event_y = 60
    def _draw_red_cross(self, x, y):
        cross_size = 10
        self.canvas.create_line(x - cross_size, y - cross_size, x + cross_size, y + cross_size, fill="red", width=2)
        self.canvas.create_line(x + cross_size, y - cross_size, x - cross_size, y + cross_size, fill="red", width=2)
def run_client(visualizer):
    udp_client.udp_client('auto',app)

def run_server(visualizer):
  udp_server.udp_server('auto',app)
if __name__ == "__main__":
    app = CommunicationVisualizer()

    # Create threads for client and server
    client_thread = threading.Thread(target=run_client, args=(app,))
    server_thread = threading.Thread(target=run_server, args=(app,))

    client_thread.start()
    server_thread.start()
    # app.add_event("client", "host", 1, 2, 10, "normal")
    # app.add_event("host", "client", 2, 3, 10, "corrupted")
    # Run the Tkinter main loop in the main thread
    app.mainloop()

    # Optionally, join the threads when the main loop ends
    client_thread.join()
    server_thread.join()
