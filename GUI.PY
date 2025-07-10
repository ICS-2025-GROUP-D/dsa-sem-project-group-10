import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from movie_tracker import MovieTracker  # your backend module

class MovieWatchlistGUI:
    def _init_(self, root):
        self.root = root
        self.root.title("Movie Watchlist Tracker")
        self.tracker = MovieTracker()

        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        # Controls
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=5)

        self.search_var = tk.StringVar()
        tk.Entry(top_frame, textvariable=self.search_var, width=30).pack(side=tk.LEFT)
        tk.Button(top_frame, text="Search", command=self.search_movie).pack(side=tk.LEFT, padx=2)
        tk.Button(top_frame, text="Add Movie", command=self.add_movie).pack(side=tk.LEFT, padx=2)
        tk.Button(top_frame, text="Refresh", command=self.refresh_table).pack(side=tk.LEFT, padx=2)

        # Treeview with Title included in columns
        columns = ("Title", "Genre", "Rating", "Year", "Watched")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100 if col != "Title" else 150)
        self.tree.pack(pady=10)

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack()

        tk.Button(button_frame, text="Mark Watched", command=self.mark_watched).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Delete", command=self.delete_movie).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="View Details", command=self.view_details).pack(side=tk.LEFT, padx=5)

        # Status label
        self.status_label = tk.Label(self.root, text="")
        self.status_label.pack()

        # Console log
        self.console = tk.Text(self.root, height=5, bg="#000", fg="#0f0")
        self.console.pack(fill=tk.BOTH, expand=True)

    def log(self, message):
        self.console.insert(tk.END, f"- {message}\n")
        self.console.see(tk.END)

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for movie in self.tracker.get_sorted_movies():
            self.tree.insert('', tk.END, iid=movie['title'], values=(
                movie['title'], movie['genre'], "★" * movie['rating'], movie['year'], "✓" if movie['watched'] else "✗"
            ))

        self.update_status()

    def add_movie(self):
        title = simpledialog.askstring("Movie Title", "Enter title:")
        if not title:
            return
        genre = simpledialog.askstring("Genre", "Enter genre:")
        rating = simpledialog.askinteger("Rating", "Enter rating (1-5):")
        year = simpledialog.askinteger("Year", "Enter year:")

        success = self.tracker.add_movie(title, genre, rating, year)
        if success:
            self.log(f'Added "{title}" to watchlist')
            self.refresh_table()
        else:
            messagebox.showwarning("Add Failed", f'Movie "{title}" may already exist.')

    def search_movie(self):
        title = self.search_var.get()
        movie = self.tracker.search_movie(title)
        if movie:
            self.tree.selection_set(movie['title'])
            self.tree.focus(movie['title'])
            self.tree.see(movie['title'])
        else:
            messagebox.showinfo("Not Found", f'No movie found with title "{title}".')

    def mark_watched(self):
        selected = self.tree.focus()
        if not selected:
            return
        success = self.tracker.mark_as_watched(selected)
        if success:
            self.log(f'Marked "{selected}" as watched')
            self.refresh_table()
        else:
            self.log(f'Failed to mark "{selected}"')

    def view_details(self):
        selected = self.tree.focus()
        if selected:
            movie = self.tracker.search_movie(selected)
            details = f'''
Title: {movie['title']}
Genre: {movie['genre']}
Rating: {"★" * movie['rating']}
Year: {movie['year']}
Watched: {'Yes' if movie['watched'] else 'No'}
'''
            messagebox.showinfo("Movie Details", details)

    def delete_movie(self):
        messagebox.showinfo("Not implemented", "Delete feature not implemented in DB yet.")

    def update_status(self):
        queue_len = len(self.tracker.watchlist)
        stack_len = len(self.tracker.watched_history)
        self.status_label.config(
            text=f"WATCHLIST (Queue): {queue_len} | RECENTLY WATCHED (Stack): {stack_len}"
        )

    def on_close(self):
        self.tracker.close()
        self.root.destroy()

if _name_ == "_main_":
    root = tk.Tk()
    app = MovieWatchlistGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
