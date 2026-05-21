import customtkinter
from core.utils import format_kgs


# ─────────────────────────────────────────────────────────────────────────────
class DepositModal(customtkinter.CTkToplevel):
    def __init__(self, parent, on_confirm):
        super().__init__(parent)
        self.t = parent.t
        self.title(self.t("modal_deposit_title"))
        self.geometry("400x220")
        self.resizable(False, False)
        self.configure(fg_color="#0B0B0C")
        self.transient(parent)
        self.grab_set()
        self.on_confirm = on_confirm

        customtkinter.CTkLabel(self, text=self.t("modal_deposit_lbl"),
                               font=("Segoe UI", 15, "bold"), text_color="#FFFFFF",
                               ).pack(pady=(28, 10))

        self.entry = customtkinter.CTkEntry(
            self, placeholder_text=self.t("modal_deposit_ph"),
            fg_color="#232328", border_color="#2A4D2C",
            text_color="#FFFFFF", font=("Segoe UI", 14), height=40,
        )
        self.entry.pack(pady=0, padx=30, fill="x")
        self.entry.focus()

        btn_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=22)

        customtkinter.CTkButton(
            btn_frame, text=self.t("btn_confirm"),
            font=("Segoe UI", 13, "bold"), fg_color="#1E351F",
            hover_color="#2A4D2C", text_color="#FFFFFF", height=34, corner_radius=20,
            command=self._confirm,
        ).pack(side="left", padx=8)

        customtkinter.CTkButton(
            btn_frame, text=self.t("btn_cancel"),
            font=("Segoe UI", 13, "bold"), fg_color="transparent",
            hover_color="#232328", text_color="#888888", height=34, corner_radius=20,
            command=self.destroy,
        ).pack(side="right", padx=8)

    def _confirm(self):
        try:
            val = float(self.entry.get())
            if val <= 0:
                raise ValueError
            self.on_confirm(val)
            self.destroy()
        except ValueError:
            self.entry.configure(border_color="#E05656")


# ─────────────────────────────────────────────────────────────────────────────
class TransferModal(customtkinter.CTkToplevel):
    def __init__(self, parent, on_confirm):
        super().__init__(parent)
        self.t = parent.t
        self.title(self.t("modal_transfer_title"))
        self.geometry("400x220")
        self.resizable(False, False)
        self.configure(fg_color="#0B0B0C")
        self.transient(parent)
        self.grab_set()
        self.on_confirm = on_confirm

        customtkinter.CTkLabel(self, text=self.t("modal_transfer_lbl"),
                               font=("Segoe UI", 15, "bold"), text_color="#FFFFFF",
                               ).pack(pady=(28, 10))

        self.entry = customtkinter.CTkEntry(
            self, placeholder_text=self.t("modal_transfer_ph"),
            fg_color="#232328", border_color="#2A4D2C",
            text_color="#FFFFFF", font=("Segoe UI", 14), height=40,
        )
        self.entry.pack(pady=0, padx=30, fill="x")
        self.entry.focus()

        btn_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=22)

        customtkinter.CTkButton(
            btn_frame, text=self.t("btn_confirm"),
            font=("Segoe UI", 13, "bold"), fg_color="#1E351F",
            hover_color="#E05656", text_color="#FFFFFF", height=34, corner_radius=20,
            command=self._confirm,
        ).pack(side="left", padx=8)

        customtkinter.CTkButton(
            btn_frame, text=self.t("btn_cancel"),
            font=("Segoe UI", 13, "bold"), fg_color="transparent",
            hover_color="#232328", text_color="#888888", height=34, corner_radius=20,
            command=self.destroy,
        ).pack(side="right", padx=8)

    def _confirm(self):
        try:
            val = float(self.entry.get())
            if val <= 0:
                raise ValueError
            self.on_confirm(val)
            self.destroy()
        except ValueError:
            self.entry.configure(border_color="#E05656")


# ─────────────────────────────────────────────────────────────────────────────
class FastAddTransactionModal(customtkinter.CTkToplevel):
    def __init__(self, parent, on_confirm):
        super().__init__(parent)
        self.t = parent.t
        self.title(self.t("modal_add_title"))
        self.geometry("440x430")
        self.resizable(False, False)
        self.configure(fg_color="#0B0B0C")
        self.transient(parent)
        self.grab_set()
        self.on_confirm = on_confirm

        # Store income label for type detection in _confirm
        self._income_lbl = self.t("modal_add_income")

        customtkinter.CTkLabel(self, text=self.t("modal_add_title"),
                               font=("Segoe UI", 16, "bold"), text_color="#FFFFFF",
                               ).pack(pady=(18, 14))

        form = customtkinter.CTkFrame(self, fg_color="transparent")
        form.pack(padx=28, fill="both", expand=True)

        def _lbl(text):
            customtkinter.CTkLabel(form, text=text, font=("Segoe UI", 11, "bold"),
                                   text_color="#888888").pack(anchor="w")

        _lbl(self.t("modal_add_amount"))
        self.entry_amount = customtkinter.CTkEntry(form, fg_color="#232328",
                                                   border_color="#2A4D2C", text_color="#FFFFFF", height=32)
        self.entry_amount.pack(fill="x", pady=(2, 10))

        _lbl(self.t("modal_add_type"))
        self.option_type = customtkinter.CTkOptionMenu(
            form, values=[self.t("modal_add_expense"), self._income_lbl],
            fg_color="#1E351F", button_color="#2A4D2C",
            button_hover_color="#56E056", dropdown_fg_color="#232328",
            dropdown_hover_color="#1E351F",
        )
        self.option_type.pack(fill="x", pady=(2, 10))

        _lbl(self.t("modal_add_category"))
        self.option_cat = customtkinter.CTkOptionMenu(
            form, values=["Еда", "Транспорт", "Интернет", "Развлечения", "Пополнение", "Другое"],
            fg_color="#1E351F", button_color="#2A4D2C",
            button_hover_color="#56E056", dropdown_fg_color="#232328",
            dropdown_hover_color="#1E351F",
        )
        self.option_cat.pack(fill="x", pady=(2, 10))

        _lbl(self.t("modal_add_vendor"))
        self.entry_vendor = customtkinter.CTkEntry(form,
                                                   placeholder_text=self.t("modal_add_vendor_ph"),
                                                   fg_color="#232328", border_color="#2A4D2C",
                                                   text_color="#FFFFFF", height=32)
        self.entry_vendor.pack(fill="x", pady=(2, 10))

        _lbl(self.t("modal_add_comment"))
        self.entry_comment = customtkinter.CTkEntry(form,
                                                    placeholder_text=self.t("modal_add_comment_ph"),
                                                    fg_color="#232328", border_color="#2A4D2C",
                                                    text_color="#FFFFFF", height=32)
        self.entry_comment.pack(fill="x", pady=(2, 14))

        btn_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(0, 18))

        customtkinter.CTkButton(
            btn_frame, text=self.t("btn_add"),
            font=("Segoe UI", 13, "bold"), fg_color="#1E351F",
            hover_color="#2A4D2C", text_color="#FFFFFF", height=34, corner_radius=20,
            command=self._confirm,
        ).pack(side="left", padx=8)

        customtkinter.CTkButton(
            btn_frame, text=self.t("btn_cancel"),
            font=("Segoe UI", 13, "bold"), fg_color="transparent",
            hover_color="#232328", text_color="#888888", height=34, corner_radius=20,
            command=self.destroy,
        ).pack(side="right", padx=8)

    def _confirm(self):
        try:
            amount = float(self.entry_amount.get())
            if amount <= 0:
                raise ValueError
            tx_type = "income" if self.option_type.get() == self._income_lbl else "expense"
            category = self.option_cat.get()
            vendor = self.entry_vendor.get().strip() or "Прочие"
            comment = self.entry_comment.get().strip() or "—"
            self.on_confirm(amount, tx_type, category, vendor, comment)
            self.destroy()
        except ValueError:
            self.entry_amount.configure(border_color="#E05656")


# ─────────────────────────────────────────────────────────────────────────────
class TransactionsView(customtkinter.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, fg_color="#0B0B0C", **kwargs)
        self.controller = controller
        self.data_manager = controller.data_manager
        self.t = controller.t

        self.scroll_container = customtkinter.CTkScrollableFrame(
            self, fg_color="transparent",
            scrollbar_fg_color="#0B0B0C",
            scrollbar_button_color="#232328",
            scrollbar_button_hover_color="#1E351F",
        )
        self.scroll_container.pack(fill="both", expand=True, padx=5, pady=5)

        self._init_header()
        self._init_summary_row()
        self._init_dashboard_grid()

    # ──────────────────────────────────────────
    def _init_header(self):
        header_frame = customtkinter.CTkFrame(self.scroll_container, fg_color="transparent")
        header_frame.pack(fill="x", padx=18, pady=(14, 14))

        customtkinter.CTkLabel(
            header_frame,
            text=self.t("tx_title"),
            font=("Segoe UI", 22, "bold"),
            text_color="#FFFFFF",
        ).pack(side="left")

        right = customtkinter.CTkFrame(header_frame, fg_color="transparent")
        right.pack(side="right")

        customtkinter.CTkButton(
            right, text=self.t("tx_btn_deposit"),
            font=("Segoe UI", 12),
            fg_color="#1E351F", hover_color="#2A4D2C",
            text_color="#56E056",
            height=28, corner_radius=20,
            command=self.open_deposit_modal,
        ).pack(side="left", padx=(0, 8))

        customtkinter.CTkButton(
            right, text=self.t("tx_btn_transfer"),
            font=("Segoe UI", 12),
            fg_color="#1E351F", hover_color="#3D1515",
            text_color="#E05656",
            height=28, corner_radius=20,
            command=self.open_transfer_modal,
        ).pack(side="left")

    # ──────────────────────────────────────────
    def _init_summary_row(self):
        row_frame = customtkinter.CTkFrame(self.scroll_container, fg_color="transparent")
        row_frame.pack(fill="x", padx=18, pady=(0, 14))
        for i in range(3):
            row_frame.grid_columnconfigure(i, weight=1)

        self._summary_card(row_frame, 0, self.t("tx_card_balance"),
                           format_kgs(self.data_manager.balance), "#FFFFFF")
        self._summary_card(row_frame, 1, self.t("tx_card_income"),
                           "+" + format_kgs(self.data_manager.monthly_income), "#56E056")
        self._summary_card(row_frame, 2, self.t("tx_card_expenses"),
                           "−" + format_kgs(self.data_manager.monthly_expenses), "#E05656")

    def _summary_card(self, parent, col, title, value, color):
        pad = (0, 8) if col == 0 else ((8, 0) if col == 2 else (4, 4))
        card = customtkinter.CTkFrame(parent, fg_color="#232328",
                                      border_width=1, border_color="#2A2A2E", corner_radius=12)
        card.grid(row=0, column=col, padx=pad, sticky="nsew")
        customtkinter.CTkLabel(card, text=title, font=("Segoe UI", 11),
                               text_color="#666666").pack(pady=(12, 3), padx=16, anchor="w")
        customtkinter.CTkLabel(card, text=value, font=("Segoe UI", 19, "bold"),
                               text_color=color).pack(pady=(0, 12), padx=16, anchor="w")

    # ──────────────────────────────────────────
    def _init_dashboard_grid(self):
        grid_frame = customtkinter.CTkFrame(self.scroll_container, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        grid_frame.grid_columnconfigure(0, weight=6)
        grid_frame.grid_columnconfigure(1, weight=4)
        grid_frame.grid_rowconfigure(0, weight=1)

        self.left_column = customtkinter.CTkFrame(grid_frame, fg_color="transparent")
        self.left_column.grid(row=0, column=0, padx=(0, 10), sticky="nsew")

        self.right_column = customtkinter.CTkFrame(grid_frame, fg_color="transparent")
        self.right_column.grid(row=0, column=1, padx=(10, 0), sticky="nsew")

        self._render_category_expenses()
        self._render_operation_history()
        self._render_goal_tracker()
        self._render_monthly_ratio()

    # ──────────────────────────────────────────
    def _render_category_expenses(self):
        card = customtkinter.CTkFrame(self.left_column, fg_color="#232328",
                                      border_width=1, border_color="#2A2A2E", corner_radius=12)
        card.pack(fill="x", pady=(0, 12))

        customtkinter.CTkLabel(card, text=self.t("tx_section_cat"),
                               font=("Segoe UI", 13, "bold"), text_color="#FFFFFF",
                               ).pack(anchor="w", padx=20, pady=(15, 10))

        expenses = self.data_manager.category_expenses
        max_amount = max(c["amount"] for c in expenses) if expenses else 1.0

        for cat_data in expenses:
            cat_name = cat_data["category"]
            cat_amt  = cat_data["amount"]
            ratio    = cat_amt / max_amount if max_amount > 0 else 0.0

            row = customtkinter.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=(6, 1))

            customtkinter.CTkLabel(row, text=cat_name,
                                   font=("Segoe UI", 12), text_color="#CCCCCC").pack(side="left")
            customtkinter.CTkLabel(row, text=format_kgs(cat_amt),
                                   font=("Segoe UI", 12, "bold"), text_color="#FFFFFF").pack(side="right")

            bar = customtkinter.CTkProgressBar(card, height=3, corner_radius=2,
                                               fg_color="#1E2A1E", progress_color="#56E056")
            bar.pack(fill="x", padx=20, pady=(0, 4))
            bar.set(ratio)

        customtkinter.CTkFrame(card, fg_color="transparent", height=4).pack()

    # ──────────────────────────────────────────
    def _render_operation_history(self):
        card = customtkinter.CTkFrame(self.left_column, fg_color="#232328",
                                      border_width=1, border_color="#2A2A2E", corner_radius=12)
        card.pack(fill="both", expand=True)

        hdr = customtkinter.CTkFrame(card, fg_color="transparent")
        hdr.pack(fill="x", padx=20, pady=(15, 10))

        customtkinter.CTkLabel(hdr, text=self.t("tx_section_history"),
                               font=("Segoe UI", 13, "bold"), text_color="#FFFFFF").pack(side="left")

        customtkinter.CTkButton(
            hdr, text=self.t("tx_btn_add"),
            font=("Segoe UI", 11),
            fg_color="#1E351F", hover_color="#2A4D2C",
            text_color="#56E056",
            height=24, corner_radius=20, width=90,
            command=self.controller.open_fast_add_transaction,
        ).pack(side="right")

        table = customtkinter.CTkFrame(card, fg_color="transparent")
        table.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        table.grid_columnconfigure(0, weight=30)
        table.grid_columnconfigure(1, weight=20)
        table.grid_columnconfigure(2, weight=20)
        table.grid_columnconfigure(3, weight=30)

        HEADER_PAD = {"pady": (0, 5), "padx": (0, 12)}
        DATA_PAD   = {"pady": 5,      "padx": (0, 12)}

        for col, (txt, anch) in enumerate([
            (self.t("tx_col_date"),    "w"),
            (self.t("tx_col_amount"),  "e"),
            (self.t("tx_col_category"),"w"),
            (self.t("tx_col_comment"), "w"),
        ]):
            customtkinter.CTkLabel(table, text=txt,
                                   font=("Segoe UI", 11, "bold"), text_color="#555555",
                                   anchor=anch,
                                   ).grid(row=0, column=col, sticky="ew",
                                          **{k: v for k, v in HEADER_PAD.items()})

        customtkinter.CTkFrame(table, height=1, fg_color="#2A2A2E").grid(
            row=1, column=0, columnspan=4, sticky="ew", pady=(0, 6))

        r = 2
        for tx in self.data_manager.transactions:
            date_vendor = f"{tx['date']}  {tx['vendor']}"

            if tx["type"] == "income":
                amt_text  = f"+{format_kgs(tx['amount'])}"
                amt_color = "#56E056"
            else:
                amt_text  = f"−{format_kgs(tx['amount'])}"
                amt_color = "#E05656"

            customtkinter.CTkLabel(table, text=date_vendor,
                                   font=("Segoe UI", 11), text_color="#FFFFFF", anchor="w",
                                   ).grid(row=r, column=0, sticky="ew", **DATA_PAD)

            customtkinter.CTkLabel(table, text=amt_text,
                                   font=("Segoe UI", 11, "bold"), text_color=amt_color, anchor="e",
                                   ).grid(row=r, column=1, sticky="ew", **DATA_PAD)

            customtkinter.CTkLabel(table, text=tx["category"],
                                   font=("Segoe UI", 11), text_color="#CCCCCC", anchor="w",
                                   ).grid(row=r, column=2, sticky="ew", **DATA_PAD)

            customtkinter.CTkLabel(table, text=tx["comment"],
                                   font=("Segoe UI", 11), text_color="#555555", anchor="w",
                                   ).grid(row=r, column=3, sticky="ew", pady=5)

            r += 1
            customtkinter.CTkFrame(table, height=1, fg_color="#1E1E22").grid(
                row=r, column=0, columnspan=4, sticky="ew", pady=3)
            r += 1

    # ──────────────────────────────────────────
    def _render_goal_tracker(self):
        card = customtkinter.CTkFrame(self.right_column, fg_color="#232328",
                                      border_width=1, border_color="#2A2A2E", corner_radius=12)
        card.pack(fill="both", expand=True, pady=(0, 12))

        customtkinter.CTkLabel(card, text=self.t("tx_card_goal"),
                               font=("Segoe UI", 13, "bold"), text_color="#FFFFFF",
                               ).pack(anchor="w", padx=18, pady=(15, 8))

        total = self.data_manager.goal_total
        saved = self.data_manager.goal_saved
        name  = self.data_manager.goal_name

        # ── Пустое состояние: цель не задана ──────────────────────
        if not name or total <= 0:
            customtkinter.CTkLabel(
                card, text="—",
                font=("Segoe UI", 22, "bold"), text_color="#444444",
            ).pack(expand=True, pady=(10, 18))
            return

        # ── Цель задана ───────────────────────────────────────────
        remain = max(0.0, total - saved)
        ratio  = saved / total

        customtkinter.CTkLabel(card, text=format_kgs(total),
                               font=("Segoe UI", 11), text_color="#555555",
                               ).pack(anchor="e", padx=18, pady=(0, 2))
        customtkinter.CTkLabel(card, text=name,
                               font=("Segoe UI", 15, "bold"), text_color="#FFFFFF",
                               ).pack(anchor="w", padx=18, pady=(0, 4))

        sub = customtkinter.CTkFrame(card, fg_color="transparent")
        sub.pack(fill="x", padx=18, pady=(0, 8))
        customtkinter.CTkLabel(sub, text=format_kgs(saved),
                               font=("Segoe UI", 12, "bold"), text_color="#56E056").pack(side="left")
        customtkinter.CTkLabel(sub, text=f"  /  {format_kgs(remain)} {self.t('tx_goal_remaining')}",
                               font=("Segoe UI", 11), text_color="#555555").pack(side="left")

        bar = customtkinter.CTkProgressBar(card, height=8, corner_radius=4,
                                           fg_color="#1E2A1E", progress_color="#56E056")
        bar.pack(fill="x", padx=18, pady=(0, 8))
        bar.set(ratio)

        customtkinter.CTkLabel(card, text=f"{ratio * 100:.1f}{self.t('tx_goal_done_fmt')}",
                               font=("Segoe UI", 11, "bold"), text_color="#56E056",
                               ).pack(anchor="e", padx=18, pady=(0, 14))

    # ──────────────────────────────────────────
    def _render_monthly_ratio(self):
        card = customtkinter.CTkFrame(self.right_column, fg_color="#232328",
                                      border_width=1, border_color="#2A2A2E", corner_radius=12)
        card.pack(fill="both", expand=True)

        customtkinter.CTkLabel(card, text=self.t("tx_card_ratio"),
                               font=("Segoe UI", 13, "bold"), text_color="#FFFFFF",
                               ).pack(anchor="w", padx=18, pady=(15, 10))

        income   = self.data_manager.monthly_income
        expenses = self.data_manager.monthly_expenses

        labels = customtkinter.CTkFrame(card, fg_color="transparent")
        labels.pack(fill="x", padx=18, pady=(0, 6))

        customtkinter.CTkLabel(labels,
                               text=f"{self.t('tx_income_lbl')}  +{format_kgs(income)}",
                               font=("Segoe UI", 11, "bold"), text_color="#56E056").pack(side="left")
        customtkinter.CTkLabel(labels,
                               text=f"{self.t('tx_expenses_lbl')}  −{format_kgs(expenses)}",
                               font=("Segoe UI", 11, "bold"), text_color="#E05656").pack(side="right")

        ratio = income / (income + expenses) if (income + expenses) > 0 else 0.5
        bar = customtkinter.CTkProgressBar(card, height=8, corner_radius=4,
                                           fg_color="#E05656", progress_color="#56E056")
        bar.pack(fill="x", padx=18, pady=(0, 16))
        bar.set(ratio)

    # ──────────────────────────────────────────
    def open_deposit_modal(self):
        DepositModal(self.winfo_toplevel(), self._handle_deposit)

    def _handle_deposit(self, amount: float):
        self.data_manager.add_deposit(amount)
        self.controller.switch_screen("transactions", add_to_history=False)

    def open_transfer_modal(self):
        TransferModal(self.winfo_toplevel(), self._handle_transfer)

    def _handle_transfer(self, amount: float):
        self.data_manager.add_transfer(amount)
        self.controller.switch_screen("transactions", add_to_history=False)
