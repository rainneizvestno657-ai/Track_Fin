import customtkinter
from core.data_manager import DataManager

from views.transactions_view import TransactionsView
from views.settings_view    import SettingsView
from views.analytics_view   import AnalyticsView
from views.categories_view  import CategoriesView
from views.goals_view       import GoalsView
from views.help_view        import HelpView


class WindowManager(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("FinanceTracker")
        self.geometry("1150x780")
        self.minsize(1000, 700)
        customtkinter.set_appearance_mode("dark")
        self.configure(fg_color="#0B0B0C")

        self.data_manager = DataManager()

        self.history_stack: list[str] = []
        self.current_screen_id: str | None = None

        # ── Sidebar ──────────────────────────────────────────────
        self.sidebar_frame = customtkinter.CTkFrame(
            self, fg_color="#0B0B0C", width=240, corner_radius=0
        )
        self.sidebar_frame.pack(side="left", fill="y", padx=(10, 0), pady=20)
        self.sidebar_frame.pack_propagate(False)

        # ── Main content area ────────────────────────────────────
        self.main_content_frame = customtkinter.CTkFrame(
            self, fg_color="#0B0B0C", corner_radius=0
        )
        self.main_content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # ── Logo ─────────────────────────────────────────────────
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="T R A C K _ F I N",
            font=("Segoe UI", 12, "bold"),
            text_color="#555555",
        )
        self.logo_label.pack(anchor="w", padx=25, pady=(14, 22))

        # ── Nav items — icon + translation key ───────────────────
        self.menu_items = [
            {"id": "settings",     "icon": "⚙",  "key": "nav_settings"},
            {"id": "transactions", "icon": "📋", "key": "nav_transactions"},
            {"id": "analytics",    "icon": "📈", "key": "nav_analytics"},
            {"id": "categories",   "icon": "⊞", "key": "nav_categories"},
            {"id": "goals",        "icon": "🎯", "key": "nav_goals"},
            {"id": "help",         "icon": "🛈", "key": "nav_help"},
        ]

        self.nav_buttons: dict[str, customtkinter.CTkButton] = {}

        for item in self.menu_items:
            btn = customtkinter.CTkButton(
                self.sidebar_frame,
                text=f"{item['icon']}  {self.t(item['key'])}",
                font=("Segoe UI", 13),
                anchor="w",
                height=42,
                corner_radius=8,
                fg_color="transparent",
                border_width=0,
                text_color="#888888",
                hover_color="#1A271A",
                command=lambda s_id=item["id"]: self.switch_screen(s_id),
            )
            btn.pack(fill="x", padx=15, pady=3)
            self.nav_buttons[item["id"]] = btn

        # ── Default screen ────────────────────────────────────────
        self.switch_screen("transactions", add_to_history=False)

    # ─────────────────────────────────────────────────────────────
    # Translation shortcut
    # ─────────────────────────────────────────────────────────────
    def t(self, key: str, **fmt) -> str:
        return self.data_manager.locale.t(key, **fmt)

    # ─────────────────────────────────────────────────────────────
    # Language refresh — update nav labels + re-render current screen
    # ─────────────────────────────────────────────────────────────
    def refresh_language(self) -> None:
        self.data_manager.refresh_category_names()
        for item in self.menu_items:
            btn = self.nav_buttons[item["id"]]
            new_text = f"{item['icon']}  {self.t(item['key'])}"
            btn.configure(text=new_text)
        # Re-apply active styling to keep bold/color correct after text update
        if self.current_screen_id:
            self._apply_nav_styles(self.current_screen_id)
            self._render_active_screen(self.current_screen_id)

    # ─────────────────────────────────────────────────────────────
    def switch_screen(self, screen_id: str, add_to_history: bool = True):
        if self.current_screen_id == screen_id:
            self._render_active_screen(screen_id)
            return

        if self.current_screen_id and add_to_history:
            self.history_stack.append(self.current_screen_id)

        self.current_screen_id = screen_id
        self._apply_nav_styles(screen_id)
        self._render_active_screen(screen_id)

    def _apply_nav_styles(self, active_id: str) -> None:
        for s_id, btn in self.nav_buttons.items():
            if s_id == active_id:
                btn.configure(
                    fg_color="#1E351F",
                    border_width=1,
                    border_color="#56E056",
                    text_color="#FFFFFF",
                    font=("Segoe UI", 13, "bold"),
                    hover_color="#274629",
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    border_width=0,
                    border_color="#0B0B0C",
                    text_color="#888888",
                    font=("Segoe UI", 13),
                    hover_color="#1A271A",
                )

    def _render_active_screen(self, screen_id: str):
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

        _map = {
            "transactions": TransactionsView,
            "settings":     SettingsView,
            "analytics":    AnalyticsView,
            "categories":   CategoriesView,
            "goals":        GoalsView,
            "help":         HelpView,
        }
        cls = _map.get(screen_id)
        if cls:
            view = cls(self.main_content_frame, self)
            view.pack(fill="both", expand=True)
        else:
            lbl = customtkinter.CTkLabel(
                self.main_content_frame,
                text=f"Screen '{screen_id}' not found",
                font=("Segoe UI", 16), text_color="#FFFFFF",
            )
            lbl.place(relx=0.5, rely=0.5, anchor="center")

    # ─────────────────────────────────────────────────────────────
    def navigate_back(self):
        if self.history_stack:
            self.switch_screen(self.history_stack.pop(), add_to_history=False)

    Maps_back = navigate_back   # legacy alias

    def refresh_currency(self) -> None:
        if self.current_screen_id:
            self._render_active_screen(self.current_screen_id)

    def open_fast_add_transaction(self):
        from views.transactions_view import FastAddTransactionModal
        FastAddTransactionModal(self, self.handle_custom_transaction)

    def handle_custom_transaction(self, amount, tx_type, category, vendor, comment):
        self.data_manager.add_custom_transaction(amount, tx_type, category, vendor, comment)
        self._render_active_screen(self.current_screen_id)


if __name__ == "__main__":
    app = WindowManager()
    app.mainloop()
