import tkinter as tk
from tkinter import font as tkfont
import random

# ─────────────────────────────────────────────
#  GAME CONSTANTS
# ─────────────────────────────────────────────
WIN_SCORE   = 10
BG_COLOR    = "#0D0D1A"
ACCENT      = "#00F5FF"
GOLD        = "#FFD700"
RED_COLOR   = "#FF3366"
GREEN_COLOR = "#00FF88"
CARD_BG     = "#1A1A2E"
TEXT_WHITE  = "#E8E8FF"
TEXT_DIM    = "#6B6B8E"

CHOICES = ["Rock", "Paper", "Scissors"]

SYMBOL = {
    "Rock":     "✊",
    "Paper":    "✋",
    "Scissors": "✌",
}

RULES = {
    ("Rock",     "Scissors"): "Rock crushes Scissors",
    ("Scissors", "Paper"):    "Scissors cuts Paper",
    ("Paper",    "Rock"):     "Paper covers Rock",
}

def get_winner(player, ai):
    if player == ai:
        return "draw", "It's a Tie!"
    if (player, ai) in RULES:
        return "player", RULES[(player, ai)]
    return "ai", RULES[(ai, player)]


# ─────────────────────────────────────────────
#  ANIMATED PARTICLE BACKGROUND
# ─────────────────────────────────────────────
class ParticleBackground:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.w = width
        self.h = height
        self.particles = []
        for _ in range(50):
            self.particles.append({
                "x":  random.uniform(0, width),
                "y":  random.uniform(0, height),
                "r":  random.uniform(1, 3),
                "vx": random.uniform(-0.3, 0.3),
                "vy": random.uniform(-0.3, 0.3),
                "a":  random.randint(40, 120),
                "id": None,
            })
        self._draw()

    def _draw(self):
        for p in self.particles:
            if p["id"]:
                self.canvas.delete(p["id"])
            a = p["a"]
            color = "#{:02x}{:02x}{:02x}".format(a, a // 2, min(255, a + 80))
            p["id"] = self.canvas.create_oval(
                p["x"] - p["r"], p["y"] - p["r"],
                p["x"] + p["r"], p["y"] + p["r"],
                fill=color, outline="")
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            if p["x"] < 0:       p["x"] = self.w
            if p["x"] > self.w:  p["x"] = 0
            if p["y"] < 0:       p["y"] = self.h
            if p["y"] > self.h:  p["y"] = 0
        self.canvas.after(30, self._draw)


# ─────────────────────────────────────────────
#  MAIN GAME WINDOW
# ─────────────────────────────────────────────
class RPSGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rock  Paper  Scissors  -  First to 10")
        self.resizable(False, False)
        self.configure(bg=BG_COLOR)

        self.W, self.H = 820, 680
        self.geometry("{}x{}".format(self.W, self.H))

        self.player_score = tk.IntVar(value=0)
        self.ai_score     = tk.IntVar(value=0)
        self.round_num    = tk.IntVar(value=1)
        self.game_active  = True

        self._load_fonts()
        self._build_ui()

    # ── Fonts ──────────────────────────────────
    def _load_fonts(self):
        self.font_title = tkfont.Font(family="Courier", size=20, weight="bold")
        self.font_big   = tkfont.Font(family="Courier", size=42, weight="bold")
        self.font_med   = tkfont.Font(family="Courier", size=15, weight="bold")
        self.font_small = tkfont.Font(family="Courier", size=12)
        self.font_tiny  = tkfont.Font(family="Courier", size=10)
        self.font_score = tkfont.Font(family="Courier", size=34, weight="bold")
        self.font_btn   = tkfont.Font(family="Courier", size=14, weight="bold")

    # ── UI Layout ──────────────────────────────
    def _build_ui(self):

        # Particle background canvas
        self.bg_canvas = tk.Canvas(self, width=self.W, height=self.H,
                                   bg=BG_COLOR, highlightthickness=0)
        self.bg_canvas.place(x=0, y=0)
        self.particles = ParticleBackground(self.bg_canvas, self.W, self.H)

        # Header
        header = tk.Frame(self, bg="#0A0A15")
        header.place(x=0, y=0, width=self.W, height=62)
        tk.Label(header, text="  ROCK  *  PAPER  *  SCISSORS  ",
                 font=self.font_title, bg="#0A0A15", fg=ACCENT).pack(pady=6)
        tk.Label(header, text="First to {} wins the match".format(WIN_SCORE),
                 font=self.font_tiny, bg="#0A0A15", fg=TEXT_DIM).pack()

        # Score board
        score_frame = tk.Frame(self, bg=CARD_BG)
        score_frame.place(x=30, y=72, width=self.W - 60, height=110)

        tk.Label(score_frame, text="YOU", font=self.font_small,
                 bg=CARD_BG, fg=GREEN_COLOR).grid(row=0, column=0, padx=60, pady=8)
        tk.Label(score_frame, textvariable=self.player_score, font=self.font_score,
                 bg=CARD_BG, fg=GREEN_COLOR).grid(row=1, column=0, padx=60)

        vs_sub = tk.Frame(score_frame, bg=CARD_BG)
        vs_sub.grid(row=0, column=1, rowspan=2, padx=40)
        tk.Label(vs_sub, text="VS", font=self.font_big,
                 bg=CARD_BG, fg=TEXT_DIM).pack()
        rnd_row = tk.Frame(vs_sub, bg=CARD_BG)
        rnd_row.pack()
        tk.Label(rnd_row, text="Round ", font=self.font_tiny,
                 bg=CARD_BG, fg=TEXT_DIM).pack(side="left")
        tk.Label(rnd_row, textvariable=self.round_num, font=self.font_tiny,
                 bg=CARD_BG, fg=ACCENT).pack(side="left")

        tk.Label(score_frame, text="AI", font=self.font_small,
                 bg=CARD_BG, fg=RED_COLOR).grid(row=0, column=2, padx=60, pady=8)
        tk.Label(score_frame, textvariable=self.ai_score, font=self.font_score,
                 bg=CARD_BG, fg=RED_COLOR).grid(row=1, column=2, padx=60)

        score_frame.grid_columnconfigure(0, weight=1)
        score_frame.grid_columnconfigure(1, weight=1)
        score_frame.grid_columnconfigure(2, weight=1)

        # Battle display
        battle = tk.Frame(self, bg=BG_COLOR)
        battle.place(x=0, y=192, width=self.W, height=130)

        self.player_display = tk.Label(battle, text="?", font=self.font_big,
                                       bg=BG_COLOR, fg=TEXT_WHITE, width=4)
        self.player_display.grid(row=0, column=0, padx=30)

        tk.Label(battle, text="VS", font=self.font_med,
                 bg=BG_COLOR, fg=TEXT_DIM).grid(row=0, column=1, padx=30)

        self.ai_display = tk.Label(battle, text="?", font=self.font_big,
                                   bg=BG_COLOR, fg=TEXT_WHITE, width=4)
        self.ai_display.grid(row=0, column=2, padx=30)

        tk.Label(battle, text="YOU", font=self.font_tiny,
                 bg=BG_COLOR, fg=GREEN_COLOR).grid(row=1, column=0)
        tk.Label(battle, text="", bg=BG_COLOR).grid(row=1, column=1)
        tk.Label(battle, text="AI", font=self.font_tiny,
                 bg=BG_COLOR, fg=RED_COLOR).grid(row=1, column=2)

        battle.grid_columnconfigure(0, weight=1)
        battle.grid_columnconfigure(1, weight=1)
        battle.grid_columnconfigure(2, weight=1)

        # Result labels
        self.result_label = tk.Label(self, text="Choose your weapon!",
                                     font=self.font_med, bg=BG_COLOR, fg=GOLD)
        self.result_label.place(x=0, y=335, width=self.W)

        self.detail_label = tk.Label(self, text="",
                                     font=self.font_small, bg=BG_COLOR, fg=TEXT_DIM)
        self.detail_label.place(x=0, y=362, width=self.W)

        # Choice buttons
        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.place(x=0, y=395, width=self.W)

        self.choice_buttons = []
        btn_data = [
            ("Rock",     "✊",  "#1E3A5F", "#2E5A8F", ACCENT),
            ("Paper",    "✋",  "#1F3D2A", "#2E6040", GREEN_COLOR),
            ("Scissors", "✌",  "#3D1F1F", "#6B2B2B", RED_COLOR),
        ]
        for i, (name, sym, bg_n, bg_h, border) in enumerate(btn_data):
            btn = self._make_btn(btn_frame, name, sym, bg_n, bg_h, border)
            btn.grid(row=0, column=i, padx=20, pady=10)
            self.choice_buttons.append(btn)

        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)

        # History strip
        self.history_frame = tk.Frame(self, bg=BG_COLOR)
        self.history_frame.place(x=0, y=590, width=self.W, height=30)
        tk.Label(self.history_frame, text="History: ",
                 font=self.font_tiny, bg=BG_COLOR, fg=TEXT_DIM).pack(side="left", padx=30)
        self.history_dots = []

        # Restart button (hidden until game over)
        self.restart_btn = tk.Button(self, text="  PLAY AGAIN  ",
                                     font=self.font_btn,
                                     bg=ACCENT, fg="#000000",
                                     activebackground=GOLD,
                                     relief="flat", bd=0,
                                     cursor="hand2",
                                     command=self._restart)

    # ── Button factory ─────────────────────────
    def _make_btn(self, parent, name, symbol, bg_n, bg_h, border_color):
        outer = tk.Frame(parent, bg=border_color, padx=2, pady=2)
        inner = tk.Frame(outer, bg=bg_n, cursor="hand2")
        inner.pack()

        lbl_sym  = tk.Label(inner, text=symbol, font=self.font_big,
                            bg=bg_n, fg=TEXT_WHITE)
        lbl_sym.pack(padx=30, pady=10)

        lbl_name = tk.Label(inner, text=name.upper(), font=self.font_btn,
                            bg=bg_n, fg=TEXT_WHITE)
        lbl_name.pack(padx=30, pady=8)

        def on_enter(e):
            inner.config(bg=bg_h)
            lbl_sym.config(bg=bg_h)
            lbl_name.config(bg=bg_h)

        def on_leave(e):
            inner.config(bg=bg_n)
            lbl_sym.config(bg=bg_n)
            lbl_name.config(bg=bg_n)

        def on_click(e):
            if self.game_active:
                self._play_round(name)

        for w in [inner, lbl_sym, lbl_name]:
            w.bind("<Enter>",    on_enter)
            w.bind("<Leave>",    on_leave)
            w.bind("<Button-1>", on_click)

        return outer

    # ── Game logic ─────────────────────────────
    def _play_round(self, player_choice):
        self.game_active = False
        ai_choice = random.choice(CHOICES)
        self.player_display.config(text=SYMBOL[player_choice], fg=ACCENT)
        self._animate_ai(ai_choice, player_choice, step=0)

    def _animate_ai(self, final_ai, player_choice, step=0):
        if step < 12:
            self.ai_display.config(text=SYMBOL[random.choice(CHOICES)], fg=TEXT_DIM)
            delay = 50 + step * 18
            self.after(delay, lambda: self._animate_ai(final_ai, player_choice, step + 1))
        else:
            self.ai_display.config(text=SYMBOL[final_ai], fg=RED_COLOR)
            self._resolve(player_choice, final_ai)

    def _resolve(self, player_choice, ai_choice):
        outcome, detail = get_winner(player_choice, ai_choice)

        if outcome == "player":
            self.player_score.set(self.player_score.get() + 1)
            self.result_label.config(text="  YOU WIN THIS ROUND!", fg=GREEN_COLOR)
        elif outcome == "ai":
            self.ai_score.set(self.ai_score.get() + 1)
            self.result_label.config(text="  AI WINS THIS ROUND!", fg=RED_COLOR)
        else:
            self.result_label.config(text="  DRAW!", fg=GOLD)

        self.detail_label.config(text=detail)
        self.round_num.set(self.round_num.get() + 1)
        self._add_dot(outcome)

        ps = self.player_score.get()
        ai = self.ai_score.get()
        if ps >= WIN_SCORE:
            self.after(600, lambda: self._game_over("player"))
        elif ai >= WIN_SCORE:
            self.after(600, lambda: self._game_over("ai"))
        else:
            self.game_active = True

    def _add_dot(self, outcome):
        colors  = {"player": GREEN_COLOR, "ai": RED_COLOR, "draw": GOLD}
        symbols = {"player": "W", "ai": "L", "draw": "-"}
        dot = tk.Label(self.history_frame,
                       text=" {} ".format(symbols[outcome]),
                       font=self.font_tiny,
                       bg=BG_COLOR, fg=colors[outcome])
        dot.pack(side="left")
        self.history_dots.append(dot)

    # ── Game over ──────────────────────────────
    def _game_over(self, winner):
        self.game_active = False
        if winner == "player":
            msg = "  YOU ARE THE CHAMPION!"
            sub = "You reached {} points first. Well played!".format(WIN_SCORE)
            col = GOLD
        else:
            msg = "  AI WINS THE MATCH!"
            sub = "The AI reached {} points. Try again!".format(WIN_SCORE)
            col = RED_COLOR

        self.result_label.config(
            text=msg, fg=col,
            font=tkfont.Font(family="Courier", size=16, weight="bold"))
        self.detail_label.config(text=sub)
        self.restart_btn.place(x=self.W // 2 - 90, y=540, width=180, height=44)

    # ── Restart ────────────────────────────────
    def _restart(self):
        self.player_score.set(0)
        self.ai_score.set(0)
        self.round_num.set(1)
        self.game_active = True
        self.result_label.config(text="Choose your weapon!", fg=GOLD,
                                 font=self.font_med)
        self.detail_label.config(text="")
        self.player_display.config(text="?", fg=TEXT_WHITE)
        self.ai_display.config(text="?", fg=TEXT_WHITE)
        self.restart_btn.place_forget()
        for dot in self.history_dots:
            dot.destroy()
        self.history_dots.clear()


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = RPSGame()
    app.mainloop()
    