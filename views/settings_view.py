import customtkinter
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import os


class SettingsView(customtkinter.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, fg_color="#0B0B0C", **kwargs)
        self.controller = controller
        self.dm = controller.data_manager
        self.t = controller.t

        self._selected_format = customtkinter.StringVar(value="json")
        self._encrypt_var = customtkinter.BooleanVar(value=False)
        self._save_folder = customtkinter.StringVar(value="")

        self._chk_transactions = customtkinter.BooleanVar(value=True)
        self._chk_categories   = customtkinter.BooleanVar(value=True)
        self._chk_goals        = customtkinter.BooleanVar(value=True)
        self._chk_balance      = customtkinter.BooleanVar(value=True)

        scroll = customtkinter.CTkScrollableFrame(
            self, fg_color="transparent",
            scrollbar_fg_color="#0B0B0C",
            scrollbar_button_color="#232328",
            scrollbar_button_hover_color="#1E351F",
        )
        scroll.pack(fill="both", expand=True, padx=5, pady=5)

        self._init_header(scroll)
        self._init_lang_card(scroll)
        self._init_currency_card(scroll)
        self._init_period_stats_card(scroll)
        self._init_main_panels(scroll)
        self._init_extra_options(scroll)
        self._init_folder_row(scroll)
        self._init_export_button(scroll)

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
            frame, text=self.t("settings_title"),
            font=("Segoe UI", 22, "bold"), text_color="#FFFFFF",
        ).pack(side="left")

        customtkinter.CTkLabel(
            parent, text=self.t("settings_subtitle"),
            font=("Segoe UI", 12), text_color="#888888",
        ).pack(anchor="w", padx=15, pady=(0, 12))

    # ──────────────────────────────────────────
    def _init_lang_card(self, parent):
        card = customtkinter.CTkFrame(parent, fg_color="#232328",
                                      corner_radius=12, border_width=1, border_color="#2A4D2C")
        card.pack(fill="x", padx=15, pady=(0, 15))

        customtkinter.CTkLabel(card, text=self.t("settings_lang_title"),
                               font=("Segoe UI", 13, "bold"), text_color="#FFFFFF",
                               ).pack(anchor="w", padx=18, pady=(14, 10))

        btn_row = customtkinter.CTkFrame(card, fg_color="transparent")
        btn_row.pack(fill="x", padx=18, pady=(0, 14))

        current_lang = self.dm.locale.current
        for code, name in self.dm.locale.LANGS.items():
            is_active = (code == current_lang)
            customtkinter.CTkButton(
                btn_row, text=name,
                font=("Segoe UI", 12, "bold"),
                fg_color="#1E351F" if is_active else "transparent",
                border_width=1,
                border_color="#56E056" if is_active else "#2A4D2C",
                hover_color="#1E351F",
                text_color="#FFFFFF" if is_active else "#888888",
                height=34, corner_radius=8, width=110,
                command=lambda c=code: self._switch_lang(c),
            ).pack(side="left", padx=(0, 8))

    def _switch_lang(self, code: str):
        self.dm.set_language(code)
        self.controller.refresh_language()

    # ──────────────────────────────────────────
    def _init_currency_card(self, parent):
        card = customtkinter.CTkFrame(parent, fg_color="#232328",
                                      corner_radius=12, border_width=1, border_color="#2A4D2C")
        card.pack(fill="x", padx=15, pady=(0, 15))

        customtkinter.CTkLabel(card, text=self.t("settings_currency_title"),
                               font=("Segoe UI", 13, "bold"), text_color="#FFFFFF",
                               ).pack(anchor="w", padx=18, pady=(14, 10))

        btn_row = customtkinter.CTkFrame(card, fg_color="transparent")
        btn_row.pack(fill="x", padx=18, pady=(0, 8))

        currencies = [
            ("som", "Сом  (с)"),
            ("usd", "Доллар  ($)"),
            ("rub", "Рубль  (₽)"),
        ]
        current = self.dm.currency
        for code, name in currencies:
            is_active = (code == current)
            customtkinter.CTkButton(
                btn_row, text=name,
                font=("Segoe UI", 12, "bold"),
                fg_color="#1E351F" if is_active else "transparent",
                border_width=1,
                border_color="#56E056" if is_active else "#2A4D2C",
                hover_color="#1E351F",
                text_color="#FFFFFF" if is_active else "#888888",
                height=34, corner_radius=8, width=120,
                command=lambda c=code: self._switch_currency(c),
            ).pack(side="left", padx=(0, 8))

        rates_text = f"1 $ = 87.47 с   ·   1 ₽ = 1.24 с"
        customtkinter.CTkLabel(card, text=f"{self.t('settings_currency_rate')}  {rates_text}",
                               font=("Segoe UI", 11), text_color="#555555",
                               ).pack(anchor="w", padx=18, pady=(0, 12))

    def _switch_currency(self, code: str):
        self.dm.set_currency(code)
        self.controller.refresh_currency()

    # ──────────────────────────────────────────
    def _init_period_stats_card(self, parent):
        card = customtkinter.CTkFrame(parent, fg_color="#232328",
                                      corner_radius=12, border_width=1, border_color="#2A4D2C")
        card.pack(fill="x", padx=15, pady=(0, 15))

        customtkinter.CTkLabel(card, text=self.t("settings_period_title"),
                               font=("Segoe UI", 13, "bold"), text_color="#FFFFFF",
                               ).pack(anchor="w", padx=18, pady=(14, 4))

        customtkinter.CTkLabel(card, text=self.t("settings_period_hint"),
                               font=("Segoe UI", 11), text_color="#555555",
                               ).pack(anchor="w", padx=18, pady=(0, 10))

        btn_row = customtkinter.CTkFrame(card, fg_color="transparent")
        btn_row.pack(fill="x", padx=18, pady=(0, 10))

        self._period_btns = {}
        periods = [
            ("day",   "settings_period_day"),
            ("week",  "settings_period_week"),
            ("month", "settings_period_month"),
            ("year",  "settings_period_year"),
        ]
        for code, key in periods:
            is_active = (code == self.dm.active_period)
            btn = customtkinter.CTkButton(
                btn_row, text=self.t(key),
                font=("Segoe UI", 12, "bold"),
                fg_color="#1E351F" if is_active else "transparent",
                border_width=1,
                border_color="#56E056" if is_active else "#2A4D2C",
                hover_color="#1E351F",
                text_color="#FFFFFF" if is_active else "#888888",
                height=34, corner_radius=8, width=90,
                command=lambda c=code: self._select_period(c),
            )
            btn.pack(side="left", padx=(0, 8))
            self._period_btns[code] = btn

        self._period_result = customtkinter.CTkFrame(
            card, fg_color="#1A2A1B", corner_radius=8,
            border_width=1, border_color="#2A4D2C")
        self._period_result.pack(fill="x", padx=18, pady=(0, 14))

        self._period_income_lbl = customtkinter.CTkLabel(
            self._period_result, text="",
            font=("Segoe UI", 12, "bold"), text_color="#56E056")
        self._period_income_lbl.pack(anchor="w", padx=14, pady=(10, 2))

        self._period_expense_lbl = customtkinter.CTkLabel(
            self._period_result, text="",
            font=("Segoe UI", 12, "bold"), text_color="#E05656")
        self._period_expense_lbl.pack(anchor="w", padx=14, pady=(0, 2))

        self._period_bar = customtkinter.CTkProgressBar(
            self._period_result, height=6, corner_radius=3,
            fg_color="#3D1515", progress_color="#56E056")
        self._period_bar.pack(fill="x", padx=14, pady=(4, 10))
        self._period_bar.set(0)

        # Show stats for the currently saved period immediately
        self._refresh_period_display(self.dm.active_period)

    def _select_period(self, period: str):
        # Save choice to DataManager (persisted to DB)
        self.dm.set_period(period)

        # Update button styles
        for code, btn in self._period_btns.items():
            if code == period:
                btn.configure(fg_color="#1E351F", border_color="#56E056", text_color="#FFFFFF")
            else:
                btn.configure(fg_color="transparent", border_color="#2A4D2C", text_color="#888888")

        self._refresh_period_display(period)

        # Also refresh Transactions screen if it is the currently active screen
        if self.controller.current_screen_id == "transactions":
            self.controller._render_active_screen("transactions")

    def _refresh_period_display(self, period: str):
        stats = self.dm.get_period_stats(period)
        fmt   = self.dm.format_amount

        if stats["income"] == 0 and stats["expenses"] == 0:
            self._period_income_lbl.configure(
                text=self.t("settings_period_no_data"), text_color="#555555")
            self._period_expense_lbl.configure(text="")
            self._period_bar.set(0)
        else:
            self._period_income_lbl.configure(
                text=f"↑ {self.t('settings_period_income_lbl')}  {fmt(stats['income'])}  ({stats['income_pct']:.0f}%)",
                text_color="#56E056")
            self._period_expense_lbl.configure(
                text=f"↓ {self.t('settings_period_expense_lbl')}  {fmt(stats['expenses'])}  ({stats['expense_pct']:.0f}%)")
            self._period_bar.set(stats["income_pct"] / 100)

    # ──────────────────────────────────────────
    def _init_main_panels(self, parent):
        row = customtkinter.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=(0, 15))
        row.grid_columnconfigure(0, weight=1)
        row.grid_columnconfigure(1, weight=1)

        # Left: what to export
        left = customtkinter.CTkFrame(row, fg_color="#232328",
                                      corner_radius=12, border_width=1, border_color="#2A4D2C")
        left.grid(row=0, column=0, padx=(0, 8), sticky="nsew")

        customtkinter.CTkLabel(left, text=self.t("settings_export_what"),
                               font=("Segoe UI", 13, "bold"), text_color="#FFFFFF",
                               ).pack(anchor="w", padx=18, pady=(16, 10))

        export_items = [
            (self._chk_transactions, self.t("settings_chk_tx"),    self.t("settings_chk_tx_desc")),
            (self._chk_categories,   self.t("settings_chk_cat"),   self.t("settings_chk_cat_desc")),
            (self._chk_goals,        self.t("settings_chk_goals"), self.t("settings_chk_goals_desc")),
            (self._chk_balance,      self.t("settings_chk_bal"),   self.t("settings_chk_bal_desc")),
        ]
        for var, label, desc in export_items:
            item = customtkinter.CTkFrame(left, fg_color="#1A2A1B",
                                          corner_radius=8, border_width=1, border_color="#2A4D2C")
            item.pack(fill="x", padx=14, pady=4)

            chk = customtkinter.CTkCheckBox(
                item, text=label, variable=var,
                font=("Segoe UI", 13, "bold"), text_color="#FFFFFF",
                fg_color="#2A4D2C", hover_color="#56E056",
                checkmark_color="#FFFFFF", border_color="#2A4D2C",
            )
            chk.pack(anchor="w", padx=12, pady=(10, 2))
            customtkinter.CTkLabel(item, text=desc, font=("Segoe UI", 11),
                                   text_color="#888888").pack(anchor="w", padx=12, pady=(0, 10))

        # Right: file format
        right = customtkinter.CTkFrame(row, fg_color="#232328",
                                       corner_radius=12, border_width=1, border_color="#2A4D2C")
        right.grid(row=0, column=1, padx=(8, 0), sticky="nsew")

        customtkinter.CTkLabel(right, text=self.t("settings_fmt_title"),
                               font=("Segoe UI", 13, "bold"), text_color="#FFFFFF",
                               ).pack(anchor="w", padx=18, pady=(16, 10))

        formats = [
            ("json",  ".JSON",  self.t("settings_json_desc")),
            ("csv",   ".CSV",   self.t("settings_csv_desc")),
            ("excel", ".EXCEL", self.t("settings_excel_desc")),
        ]
        self._format_cards = {}
        for fmt, label, desc in formats:
            card = customtkinter.CTkFrame(right, fg_color="#1A2A1B",
                                          corner_radius=8, border_width=2,
                                          border_color="#2A4D2C")
            card.pack(fill="x", padx=14, pady=4)
            card.bind("<Button-1>", lambda e, f=fmt: self._select_format(f))

            top = customtkinter.CTkFrame(card, fg_color="transparent")
            top.pack(fill="x", padx=12, pady=(10, 2))
            top.bind("<Button-1>", lambda e, f=fmt: self._select_format(f))

            rb = customtkinter.CTkRadioButton(
                top, text=label, variable=self._selected_format, value=fmt,
                font=("Segoe UI", 13, "bold"), text_color="#FFFFFF",
                fg_color="#56E056", hover_color="#2A4D2C", border_color="#2A4D2C",
            )
            rb.pack(side="left")
            customtkinter.CTkLabel(card, text=desc,
                                   font=("Segoe UI", 11), text_color="#888888",
                                   justify="left").pack(anchor="w", padx=12, pady=(0, 10))
            self._format_cards[fmt] = card

        self._select_format("json")

    def _select_format(self, fmt):
        self._selected_format.set(fmt)
        for f, card in self._format_cards.items():
            card.configure(border_color="#56E056" if f == fmt else "#2A4D2C")

    # ──────────────────────────────────────────
    def _init_extra_options(self, parent):
        card = customtkinter.CTkFrame(parent, fg_color="#232328",
                                      corner_radius=12, border_width=1, border_color="#2A4D2C")
        card.pack(fill="x", padx=15, pady=(0, 12))

        customtkinter.CTkLabel(card, text=self.t("settings_extra_title"),
                               font=("Segoe UI", 13, "bold"), text_color="#FFFFFF",
                               ).pack(anchor="w", padx=18, pady=(14, 8))

        opt_row = customtkinter.CTkFrame(card, fg_color="transparent")
        opt_row.pack(fill="x", padx=18, pady=(0, 14))

        customtkinter.CTkCheckBox(
            opt_row, text=self.t("settings_encrypt_chk"), variable=self._encrypt_var,
            font=("Segoe UI", 12, "bold"), text_color="#FFFFFF",
            fg_color="#2A4D2C", hover_color="#56E056",
            checkmark_color="#FFFFFF", border_color="#2A4D2C",
            command=self._toggle_password,
        ).pack(side="left")

        customtkinter.CTkLabel(opt_row,
                               text=self.t("settings_encrypt_desc"),
                               font=("Segoe UI", 11), text_color="#888888").pack(side="left")

        self.entry_password = customtkinter.CTkEntry(
            card, placeholder_text=self.t("settings_password_ph"),
            fg_color="#1A1A1E", border_color="#2A4D2C",
            text_color="#FFFFFF", height=34, show="*",
            state="disabled",
        )
        self.entry_password.pack(fill="x", padx=18, pady=(0, 14))

    def _toggle_password(self):
        state = "normal" if self._encrypt_var.get() else "disabled"
        self.entry_password.configure(state=state)

    # ──────────────────────────────────────────
    def _init_folder_row(self, parent):
        card = customtkinter.CTkFrame(parent, fg_color="#232328",
                                      corner_radius=12, border_width=1, border_color="#2A4D2C")
        card.pack(fill="x", padx=15, pady=(0, 12))

        customtkinter.CTkLabel(card, text=self.t("settings_folder_title"),
                               font=("Segoe UI", 13, "bold"), text_color="#FFFFFF",
                               ).pack(anchor="w", padx=18, pady=(14, 8))

        row = customtkinter.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=18, pady=(0, 14))
        row.grid_columnconfigure(0, weight=1)
        row.grid_columnconfigure(1, weight=0)

        self.folder_entry = customtkinter.CTkEntry(
            row, textvariable=self._save_folder,
            fg_color="#1A1A1E", border_color="#2A4D2C",
            text_color="#FFFFFF", height=34,
        )
        self.folder_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        customtkinter.CTkButton(
            row, text=self.t("settings_browse"),
            font=("Segoe UI", 12, "bold"), fg_color="#1E351F",
            hover_color="#2A4D2C", text_color="#FFFFFF",
            height=34, width=90, corner_radius=8,
            command=self._browse_folder,
        ).grid(row=0, column=1)

    def _browse_folder(self):
        folder = fd.askdirectory(title=self.t("settings_folder_title"))
        if folder:
            self._save_folder.set(folder)

    # ──────────────────────────────────────────
    def _init_export_button(self, parent):
        customtkinter.CTkButton(
            parent, text=self.t("settings_export_btn"),
            font=("Segoe UI", 15, "bold"), fg_color="#1E351F",
            hover_color="#2A4D2C", text_color="#FFFFFF",
            height=50, corner_radius=10,
            command=self._do_export,
        ).pack(fill="x", padx=15, pady=(0, 20))

    # ──────────────────────────────────────────
    def _do_export(self):
        folder = self._save_folder.get().strip()
        if not folder:
            folder = os.path.expanduser("~")
            self._save_folder.set(folder)

        what = []
        if self._chk_transactions.get():
            what.append("transactions")
        if self._chk_categories.get():
            what.append("categories")
        if self._chk_goals.get():
            what.append("goals")
        if self._chk_balance.get():
            what.append("balance")

        if not what:
            mb.showwarning("", self.t("export_warn"))
            return

        fmt = self._selected_format.get()
        password = self.entry_password.get().strip() if self._encrypt_var.get() else ""

        try:
            path = self.dm.export_data(what, fmt, folder, password=password)
            mb.showinfo("", self.t("export_done", path=path))
        except Exception as exc:
            mb.showerror("", self.t("export_err", error=exc))
