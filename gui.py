import tkinter as tk
from tkinter import ttk, messagebox
from backend import MovieTracker


class MovieTrackerGUI:
  def __init__(self, root):
    self.root = root
    self.tracker = MovieTracker()  # Our backend class
    self.setup_gui()
    self.load_movies()

  def setup_gui(self):
    # Main window configuration
    self.root.title("Movie Watchlist Tracker")
    self.root.geometry("900x600")

    # Configure styles
    self.style = ttk.Style()
    self.style.configure("Treeview", rowheight=25)
    self.style.configure("TButton", padding=5)
