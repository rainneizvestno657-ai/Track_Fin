import customtkinter


class AnalyticsView(customtkinter.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, fg_color="#0B0B0C", **kwargs)
        self.controller = controller
        self.dm  = controller.data_manager
        self.t   = controller.t
        self.fmt = self.dm.format_amount
        self.period = self.dm.active_period          # "day"|"week"|"month"|"year"

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
        frame.pack(fill="x", padx=15, pady=(10, 4))

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

        # Period badge
        period_name = self.t(f"settings_period_{self.period}")
        badge = customtkinter.CTkFrame(frame, fg_color="#1E351F",
                                       corner_radius=8, border_width=1,
                                       border_color="#56E056")
        badge.pack(side="right")
        customtkinter.CTkLabel(badge, text=period_name,
                               font=("Segoe UI", 11, "bold"),
                               text_color="#56E056").pack(padx=10, pady=4)

        customtkinter.CTkLabel(
            parent, text=self.t("an_period_hint"),
            font=("Segoe UI", 11), text_color="#444444",
        ).pack(anchor="w", padx=15, pady=(0, 12))

    # ──────────────────────────────────────────
    def _init_banner(self, parent):
        curr = self.dm.get_period_stats(self.period)
        prev = self.dm.get_prev_period_stats(self.period)

        no_data = (
            curr["income"] == 0 and curr["expenses"] == 0
            and prev["income"] == 0 and prev["expenses"] == 0
        )
        if no_data:
            card = customtkinter.CTkFrame(
                parent, fg_color="#232328", corner_radius=12,
                border_width=1, border_color="#2A4D2C",
            )
            card.pack(fill="x", padx=15, pady=(0, 15))
            customtkinter.CTkLabel(
                card, text=self.t("empty_analytics"),
                font=("Segoe UI", 16, "bold"), text_color="#555555",
                justify="center",
            ).pack(pady=26, padx=20)
            return

        def _pct(curr_val, prev_val):
            if prev_val == 0:
                return 100.0 if curr_val > 0 else 0.0
            return (curr_val - prev_val) / prev_val * 100

        exp_pct = _pct(curr["expenses"], prev["expenses"])
        inc_pct = _pct(curr["income"],   prev["income"])

        vs_label = self.t(f"an_vs_prev_{self.period}")

        row = customtkinter.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=(0, 15))
        row.grid_columnconfigure(0, weight=1)
        row.grid_columnconfigure(1, weight=1)

        self._banner_card(row, col=0, padx=(0, 6),
                          label=self.t(f"tx_card_expenses_{self.period}"),
                          amount=curr["expenses"], pct=exp_pct,
                          positive_is_bad=True, vs_label=vs_label)
        self._banner_card(row, col=1, padx=(6, 0),
                          label=self.t(f"tx_card_income_{self.period}"),
                          amount=curr["income"], pct=inc_pct,
                          positive_is_bad=False, vs_label=vs_label)

    def _banner_card(self, parent, col, padx, label, amount, pct, positive_is_bad, vs_label):
        card = customtkinter.CTkFrame(
            parent, fg_color="#232328", corner_radius=12,
            border_width=1, border_color="#2A4D2C",
        )
        card.grid(row=0, column=col, padx=padx, sticky="nsew")

        customtkinter.CTkLabel(
            card, text=label,
            font=("Segoe UI", 11), text_color="#888888",
        ).pack(anchor="w", padx=16, pady=(14, 2))

        customtkinter.CTkLabel(
            card, text=self.fmt(amount),
            font=("Segoe UI", 18, "bold"),
            text_color="#E05656" if positive_is_bad else "#56E056",
        ).pack(anchor="w", padx=16, pady=(0, 4))

        if positive_is_bad:
            pct_color = "#E05656" if pct >= 0 else "#56E056"
        else:
            pct_color = "#56E056" if pct >= 0 else "#E05656"

        arrow = "↑" if pct >= 0 else "↓"
        sign  = "+" if pct > 0 else ""

        customtkinter.CTkLabel(
            card, text=f"{arrow}  {sign}{abs(pct):.0f}%",
            font=("Segoe UI", 22, "bold"), text_color=pct_color,
        ).pack(anchor="w", padx=16, pady=(0, 4))

        customtkinter.CTkLabel(
            card, text=vs_label,
            font=("Segoe UI", 11), text_color="#555555",
        ).pack(anchor="w", padx=16, pady=(0, 14))

    # ──────────────────────────────────────────
    def _init_summary_cards(self, parent):
        curr = self.dm.get_period_stats(self.period)
        prev = self.dm.get_prev_period_stats(self.period)

        row = customtkinter.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=(0, 15))
        for i in range(3):
            row.grid_columnconfigure(i, weight=1)

        self._summary_card(row, 0, self.t("an_card_balance"),
                           self.fmt(self.dm.balance), "#FFFFFF")

        inc_delta = curr["income"] - prev["income"]
        inc_arrow = "↑+" if inc_delta >= 0 else "↓"
        self._summary_card(row, 1, self.t(f"tx_card_income_{self.period}"),
                           f"{inc_arrow}{self.fmt(abs(inc_delta))}", "#56E056")

        self._summary_card(row, 2, self.t(f"tx_card_expenses_{self.period}"),
                           f"−{self.fmt(curr['expenses'])}", "#E05656")

    def _summary_card(self, parent, col, title, value, color):
        pad = (0, 8) if col == 0 else ((8, 0) if col == 2 else (4, 4))
        card = customtkinter.CTkFrame(
            parent, fg_color="#232328",
            border_width=1, border_color="#2A4D2C", corner_radius=12,
        )
        card.grid(row=0, column=col, padx=pad, sticky="nsew")
        customtkinter.CTkLabel(card, text=title, font=("Segoe UI", 11),
                               text_color="#888888").pack(pady=(12, 4), padx=15, anchor="w")
        customtkinter.CTkLabel(card, text=value, font=("Segoe UI", 18, "bold"),
                               text_color=color).pack(pady=(0, 12), padx=15, anchor="w")

    # ──────────────────────────────────────────
    def _init_top_expense(self, parent):
        card = customtkinter.CTkFrame(
            parent, fg_color="#232328", corner_radius=12,
            border_width=1, border_color="#2A4D2C",
        )
        card.pack(fill="x", padx=15, pady=(0, 15))

        period_cat = self.dm.get_period_category_expenses(self.period)

        if not period_cat:
            customtkinter.CTkLabel(card, text=self.t("an_top_title"),
                                   font=("Segoe UI", 12), text_color="#888888",
                                   ).pack(anchor="w", padx=20, pady=(15, 4))
            customtkinter.CTkLabel(card, text="—",
                                   font=("Segoe UI", 22, "bold"), text_color="#444444",
                                   ).pack(anchor="w", padx=20, pady=(0, 15))
            return

        top_cat    = period_cat[0]["category"]
        top_amount = period_cat[0]["amount"]

        # Change vs previous period for this category
        comparison = self.dm.get_period_comparison(self.period)
        change_pct = 0.0
        for row in comparison:
            if row["category"] == top_cat and row["prev"] > 0:
                change_pct = (row["curr"] - row["prev"]) / row["prev"] * 100
                break

        inner = customtkinter.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=15)
        inner.grid_columnconfigure(0, weight=1)
        inner.grid_columnconfigure(1, weight=0)

        left = customtkinter.CTkFrame(inner, fg_color="transparent")
        left.grid(row=0, column=0, sticky="w")

        customtkinter.CTkLabel(left, text=self.t("an_top_title"),
                               font=("Segoe UI", 12), text_color="#888888").pack(anchor="w")
        customtkinter.CTkLabel(left, text=self.fmt(top_amount),
                               font=("Segoe UI", 22, "bold"), text_color="#E05656").pack(anchor="w")
        customtkinter.CTkLabel(left, text=f"{self.t('an_top_category')} {top_cat}",
                               font=("Segoe UI", 12), text_color="#888888").pack(anchor="w")
        customtkinter.CTkLabel(left, text=self.t("an_top_more", pct=f"{abs(change_pct):.0f}"),
                               font=("Segoe UI", 12), text_color="#888888").pack(anchor="w")

        arrow_color = "#E05656" if change_pct >= 0 else "#56E056"
        arrow_text  = "↑" if change_pct >= 0 else "↓"
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
            self.t(f"an_col_prev_{self.period}"),
            self.t(f"an_col_curr_{self.period}"),
            self.t("an_col_change"),
        ]
        for col, hdr in enumerate(headers):
            customtkinter.CTkLabel(
                table, text=hdr, font=("Segoe UI", 11, "bold"),
                text_color="#888888", anchor="w",
            ).grid(row=0, column=col, sticky="ew", pady=(0, 5), padx=(0, 8))

        customtkinter.CTkFrame(table, height=1, fg_color="#3A3A40").grid(
            row=1, column=0, columnspan=4, sticky="ew", pady=(0, 8))

        comparison = self.dm.get_period_comparison(self.period)

        if not comparison:
            customtkinter.CTkLabel(
                card, text=self.t("empty_comparison"),
                font=("Segoe UI", 12), text_color="#555555",
                justify="center",
            ).pack(pady=20, padx=20)
            return

        r = 2
        for comp in comparison:
            change = comp["curr"] - comp["prev"]
            sign   = "+" if change > 0 else ""
            clr    = "#E05656" if change > 0 else "#56E056"

            customtkinter.CTkLabel(table, text=comp["category"],
                                   font=("Segoe UI", 12), text_color="#FFFFFF", anchor="w",
                                   ).grid(row=r, column=0, sticky="ew", pady=6, padx=(0, 8))
            customtkinter.CTkLabel(table, text=self.fmt(comp["prev"]),
                                   font=("Segoe UI", 12, "bold"), text_color="#CCCCCC", anchor="w",
                                   ).grid(row=r, column=1, sticky="ew", pady=6, padx=(0, 8))
            customtkinter.CTkLabel(table, text=self.fmt(comp["curr"]),
                                   font=("Segoe UI", 12, "bold"), text_color="#FFFFFF", anchor="w",
                                   ).grid(row=r, column=2, sticky="ew", pady=6, padx=(0, 8))
            customtkinter.CTkLabel(table, text=f"{sign}{self.fmt(abs(change))}",
                                   font=("Segoe UI", 12, "bold"), text_color=clr, anchor="w",
                                   ).grid(row=r, column=3, sticky="ew", pady=6)
            r += 1
            customtkinter.CTkFrame(table, height=1, fg_color="#2E2E34").grid(
                row=r, column=0, columnspan=4, sticky="ew", pady=2)
            r += 1
