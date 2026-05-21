import customtkinter


class HelpView(customtkinter.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, fg_color="#0B0B0C", **kwargs)
        self.controller = controller
        self.t = controller.t
        self._open_items: dict[int, bool] = {}

        scroll = customtkinter.CTkScrollableFrame(
            self, fg_color="transparent",
            scrollbar_fg_color="#0B0B0C",
            scrollbar_button_color="#232328",
            scrollbar_button_hover_color="#1E351F",
        )
        scroll.pack(fill="both", expand=True, padx=5, pady=5)

        self._init_header(scroll)
        self._init_faq(scroll)
        self._init_about(scroll)

    # ──────────────────────────────────────────
    def _init_header(self, parent):
        frame = customtkinter.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=(10, 5))

        customtkinter.CTkButton(
            frame, text="←", width=36, height=36,
            font=("Segoe UI", 20, "bold"), fg_color="transparent",
            text_color="#FFFFFF", hover_color="#1E351F", corner_radius=6,
            command=self.controller.navigate_back,
        ).pack(side="left", padx=(0, 10))

        customtkinter.CTkLabel(
            frame, text=self.t("help_title"),
            font=("Segoe UI", 22, "bold"), text_color="#FFFFFF",
        ).pack(side="left")

        customtkinter.CTkLabel(
            parent, text=self.t("help_subtitle"),
            font=("Segoe UI", 12), text_color="#888888",
        ).pack(anchor="w", padx=15, pady=(0, 15))

    # ──────────────────────────────────────────
    def _init_faq(self, parent):
        # Load FAQ items dynamically from locale keys
        faq = [(self.t(f"faq_q{i}"), self.t(f"faq_a{i}")) for i in range(1, 9)]

        faq_card = customtkinter.CTkFrame(
            parent, fg_color="#232328",
            corner_radius=12, border_width=1, border_color="#2A4D2C",
        )
        faq_card.pack(fill="x", padx=15, pady=(0, 15))

        customtkinter.CTkLabel(
            faq_card, text=self.t("help_faq_title"),
            font=("Segoe UI", 14, "bold"), text_color="#FFFFFF",
        ).pack(anchor="w", padx=20, pady=(15, 10))

        for idx, (question, answer) in enumerate(faq):
            self._open_items[idx] = False
            self._build_faq_item(faq_card, idx, question, answer)

    def _build_faq_item(self, parent, idx: int, question: str, answer: str):
        item_frame = customtkinter.CTkFrame(parent, fg_color="#1A2A1B",
                                            corner_radius=8, border_width=1,
                                            border_color="#2A4D2C")
        item_frame.pack(fill="x", padx=14, pady=4)

        q_row = customtkinter.CTkFrame(item_frame, fg_color="transparent")
        q_row.pack(fill="x", padx=12, pady=10)
        q_row.grid_columnconfigure(0, weight=1)
        q_row.grid_columnconfigure(1, weight=0)

        q_lbl = customtkinter.CTkLabel(
            q_row, text=question,
            font=("Segoe UI", 12, "bold"), text_color="#FFFFFF",
            anchor="w", justify="left",
        )
        q_lbl.grid(row=0, column=0, sticky="ew")

        self._arrows = getattr(self, "_arrows", {})
        arrow_lbl = customtkinter.CTkLabel(
            q_row, text="▸", font=("Segoe UI", 14), text_color="#56E056",
        )
        arrow_lbl.grid(row=0, column=1, padx=(10, 0))
        self._arrows[idx] = arrow_lbl

        ans_lbl = customtkinter.CTkLabel(
            item_frame, text=answer,
            font=("Segoe UI", 11), text_color="#CCCCCC",
            anchor="w", justify="left", wraplength=800,
        )
        self._faq_answers = getattr(self, "_faq_answers", {})
        self._faq_answers[idx] = ans_lbl

        def _toggle(e=None, i=idx):
            self._toggle_faq(i)

        for widget in [q_row, q_lbl, arrow_lbl]:
            widget.bind("<Button-1>", _toggle)

    def _toggle_faq(self, idx: int):
        is_open = self._open_items[idx]
        ans_lbl = self._faq_answers[idx]
        if is_open:
            ans_lbl.pack_forget()
            self._arrows[idx].configure(text="▸")
            self._open_items[idx] = False
        else:
            ans_lbl.pack(anchor="w", padx=12, pady=(0, 12), fill="x")
            self._arrows[idx].configure(text="▾")
            self._open_items[idx] = True

    # ──────────────────────────────────────────
    def _init_about(self, parent):
        card = customtkinter.CTkFrame(
            parent, fg_color="#232328",
            corner_radius=12, border_width=1, border_color="#2A4D2C",
        )
        card.pack(fill="x", padx=15, pady=(0, 20))

        customtkinter.CTkLabel(
            card, text=self.t("help_about_title"),
            font=("Segoe UI", 14, "bold"), text_color="#FFFFFF",
        ).pack(anchor="w", padx=20, pady=(15, 8))

        info_lines = [
            (self.t("help_version_lbl"),  "1.0.0"),
            (self.t("help_tech_lbl"),     "Python 3 · CustomTkinter"),
            (self.t("help_currency_lbl"), "Кыргызский сом (с)"),
            (self.t("help_theme_lbl"),    "Nordic Dark Minimalist"),
        ]
        for label, value in info_lines:
            row = customtkinter.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=2)
            customtkinter.CTkLabel(row, text=label, font=("Segoe UI", 12, "bold"),
                                   text_color="#888888", width=120, anchor="w").pack(side="left")
            customtkinter.CTkLabel(row, text=value, font=("Segoe UI", 12),
                                   text_color="#FFFFFF", anchor="w").pack(side="left")

        customtkinter.CTkFrame(card, height=1, fg_color="#2E2E34").pack(fill="x", padx=20, pady=10)

        customtkinter.CTkLabel(
            card, text=self.t("help_desc"),
            font=("Segoe UI", 11), text_color="#888888",
            justify="left",
        ).pack(anchor="w", padx=20, pady=(0, 15))
