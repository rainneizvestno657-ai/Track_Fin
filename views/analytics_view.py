import customtkinter
from core.utils import format_kgs


class AnalyticsView(customtkinter.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, fg_color="#0B0B0C", **kwargs)
        self.controller = controller
        self.dm = controller.data_manager
        self.t = controller.t

        scroll = customtkinter.CTkScrollableFrame(
            self, fg_color="transparent",
            scrollbar_fg_color="#0B0B0C",
            scrollbar_button_color="#232328",
            scrollbar_button_hover_color="#1E351F",
        )
        scroll.pack(fill="both", expand=True, padx=5, pady=5)

        self._init_header(scroll)
        self._init_banner(scroll)
        self._init_summary_cards(scroll)
        self._init_top_expense(scroll)
        self._init_comparison_table(scroll)

    # ──────────────────────────────────────────
    def _init_header(self, parent):
        frame = customtkinter.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=(10, 15))

        customtkinter.CTkButton(
            frame, text="←", width=36, height=36,
            font=("Segoe UI", 20, "bold"), fg_color="transparent",
            text_color="#FFFFFF", hover_color="#1E351F", corner_radius=6,
            command=self.controller.navigate_back,
        ).pack(side="left", padx=(0, 10))

        customtkinter.CTkLabel(
            frame, text=self.t("an_title"),
            font=("Segoe UI", 22, "bold"), text_color="#FFFFFF",
        ).pack(side="left")

    # ──────────────────────────────────────────
    def _init_banner(self, parent):
        pct = self.dm.get_expense_change_percent()
        pct_color = "#E05656" if pct >= 0 else "#56E056"
        pct_str = f"{abs(pct):.0f}%"

        # Prefix and suffix depend on direction; word order differs per language
        if pct >= 0:
            prefix = self.t("an_banner_prefix_up")
            suffix = self.t("an_banner_suffix_up")
        else:
            prefix = self.t("an_banner_prefix_dn")
            suffix = self.t("an_banner_suffix_dn")

        card = customtkinter.CTkFrame(
            parent, fg_color="#232328", corner_radius=12,
            border_width=1, border_color="#2A4D2C",
        )
        card.pack(fill="x", padx=15, pady=(0, 15))

        row = customtkinter.CTkFrame(card, fg_color="transparent")
        row.pack(pady=22)

        customtkinter.CTkLabel(
            row, text=prefix,
            font=("Segoe UI", 20, "bold"), text_color="#FFFFFF",
        ).pack(side="left")

        customtkinter.CTkLabel(
            row, text=pct_str,
            font=("Segoe UI", 20, "bold"), text_color=pct_color,
        ).pack(side="left")

        customtkinter.CTkLabel(
            row, text=suffix,
            font=("Segoe UI", 20, "bold"), text_color="#FFFFFF",
        ).pack(side="left")

    # ──────────────────────────────────────────
    def _init_summary_cards(self, parent):
        row = customtkinter.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=(0, 15))
        for i in range(3):
            row.grid_columnconfigure(i, weight=1)

        self._summary_card(row, 0, self.t("an_card_balance"),
                           format_kgs(self.dm.balance), "#FFFFFF")

        inc_delta = self.dm.monthly_income - self.dm.prev_monthly_income
        inc_sign = "↑+" if inc_delta >= 0 else "↓-"
        self._summary_card(row, 1, self.t("an_card_income"),
                           f"{inc_sign}{format_kgs(abs(inc_delta))}", "#56E056")

        self._summary_card(row, 2, self.t("an_card_expenses"),
                           f"→-{format_kgs(self.dm.monthly_expenses)}", "#E05656")

    def _summary_card(self, parent, col, title, value, color):
        pad = (0, 8) if col == 0 else ((8, 0) if col == 2 else (4, 4))
        card = customtkinter.CTkFrame(
            parent, fg_color="#232328",
            border_width=1, border_color="#2A4D2C", corner_radius=12,
        )
        card.grid(row=0, column=col, padx=pad, sticky="nsew")
        customtkinter.CTkLabel(card, text=title, font=("Segoe UI", 12, "bold"),
                               text_color="#888888").pack(pady=(12, 4), padx=15, anchor="w")
        customtkinter.CTkLabel(card, text=value, font=("Segoe UI", 20, "bold"),
                               text_color=color).pack(pady=(0, 12), padx=15, anchor="w")

    # ──────────────────────────────────────────
    def _init_top_expense(self, parent):
        card = customtkinter.CTkFrame(
            parent, fg_color="#232328", corner_radius=12,
            border_width=1, border_color="#2A4D2C",
        )
        card.pack(fill="x", padx=15, pady=(0, 15))

        # Пустое состояние
        if not self.dm.category_expenses:
            customtkinter.CTkLabel(card, text=self.t("an_top_title"),
                                   font=("Segoe UI", 12), text_color="#888888",
                                   ).pack(anchor="w", padx=20, pady=(15, 4))
            customtkinter.CTkLabel(card, text="—",
                                   font=("Segoe UI", 22, "bold"), text_color="#444444",
                                   ).pack(anchor="w", padx=20, pady=(0, 15))
            return

        cat_name, change_pct = self.dm.get_largest_category_change_percent()
        cat_amount = next(
            (c["amount"] for c in self.dm.category_expenses if c["category"] == cat_name),
            0.0,
        )

        inner = customtkinter.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=15)
        inner.grid_columnconfigure(0, weight=1)
        inner.grid_columnconfigure(1, weight=0)

        left = customtkinter.CTkFrame(inner, fg_color="transparent")
        left.grid(row=0, column=0, sticky="w")

        customtkinter.CTkLabel(left, text=self.t("an_top_title"),
                               font=("Segoe UI", 12), text_color="#888888").pack(anchor="w")
        customtkinter.CTkLabel(left, text=format_kgs(cat_amount),
                               font=("Segoe UI", 22, "bold"), text_color="#E05656").pack(anchor="w")
        customtkinter.CTkLabel(left, text=f"{self.t('an_top_category')} {cat_name}",
                               font=("Segoe UI", 12), text_color="#888888").pack(anchor="w")
        customtkinter.CTkLabel(left, text=self.t("an_top_more", pct=f"{abs(change_pct):.0f}"),
                               font=("Segoe UI", 12), text_color="#888888").pack(anchor="w")

        arrow_color = "#E05656" if change_pct >= 0 else "#56E056"
        arrow_text = "↑" if change_pct >= 0 else "↓"
        customtkinter.CTkLabel(inner, text=arrow_text,
                               font=("Segoe UI", 40, "bold"), text_color=arrow_color,
                               ).grid(row=0, column=1, sticky="e", padx=(20, 0))

    # ──────────────────────────────────────────
    def _init_comparison_table(self, parent):
        card = customtkinter.CTkFrame(
            parent, fg_color="#232328", corner_radius=12,
            border_width=1, border_color="#2A4D2C",
        )
        card.pack(fill="x", padx=15, pady=(0, 20))

        customtkinter.CTkLabel(
            card, text=self.t("an_comparison_title"),
            font=("Segoe UI", 16, "bold"), text_color="#FFFFFF",
        ).pack(anchor="w", padx=20, pady=(15, 10))

        table = customtkinter.CTkFrame(card, fg_color="transparent")
        table.pack(fill="x", padx=20, pady=(0, 15))
        for i in range(4):
            table.grid_columnconfigure(i, weight=1)

        headers = [
            self.t("an_col_category"),
            self.t("an_col_prev"),
            self.t("an_col_curr"),
            self.t("an_col_change"),
        ]
        for col, hdr in enumerate(headers):
            customtkinter.CTkLabel(
                table, text=hdr, font=("Segoe UI", 11, "bold"),
                text_color="#888888", anchor="w",
            ).grid(row=0, column=col, sticky="ew", pady=(0, 5), padx=(0, 8))

        customtkinter.CTkFrame(table, height=1, fg_color="#3A3A40").grid(
            row=1, column=0, columnspan=4, sticky="ew", pady=(0, 8))

        r = 2
        for comp in self.dm.analytics_comparison:
            change = comp["curr"] - comp["prev"]
            sign = "+" if change > 0 else ""
            clr = "#E05656" if change > 0 else "#56E056"

            customtkinter.CTkLabel(table, text=comp["category"],
                                   font=("Segoe UI", 12), text_color="#FFFFFF", anchor="w",
                                   ).grid(row=r, column=0, sticky="ew", pady=6, padx=(0, 8))
            customtkinter.CTkLabel(table, text=format_kgs(comp["prev"]),
                                   font=("Segoe UI", 12, "bold"), text_color="#FFFFFF", anchor="w",
                                   ).grid(row=r, column=1, sticky="ew", pady=6, padx=(0, 8))
            customtkinter.CTkLabel(table, text=format_kgs(comp["curr"]),
                                   font=("Segoe UI", 12, "bold"), text_color="#FFFFFF", anchor="w",
                                   ).grid(row=r, column=2, sticky="ew", pady=6, padx=(0, 8))
            customtkinter.CTkLabel(table, text=f"{sign}{format_kgs(abs(change))}",
                                   font=("Segoe UI", 12, "bold"), text_color=clr, anchor="w",
                                   ).grid(row=r, column=3, sticky="ew", pady=6)
            r += 1
            customtkinter.CTkFrame(table, height=1, fg_color="#2E2E34").grid(
                row=r, column=0, columnspan=4, sticky="ew", pady=2)
            r += 1
