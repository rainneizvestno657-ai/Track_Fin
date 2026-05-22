import customtkinter
from datetime import datetime


def _is_cancellable(tx: dict) -> bool:
    created_at = tx.get("created_at", "")
    if not created_at:
        return False
    try:
        created = datetime.fromisoformat(created_at)
        return (datetime.now() - created).total_seconds() < 1800
    except (ValueError, TypeError):
        return False


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
        self.geometry("440x400")
        self.resizable(False, False)
        self.configure(fg_color="#0B0B0C")
        self.transient(parent)
        self.grab_set()
        self.on_confirm = on_confirm

        customtkinter.CTkLabel(self, text=self.t("modal_transfer_title"),
                               font=("Segoe UI", 16, "bold"), text_color="#FFFFFF",
                               ).pack(pady=(22, 14))

        form = customtkinter.CTkFrame(self, fg_color="transparent")
        form.pack(padx=28, fill="x")

        def _lbl(text):
            customtkinter.CTkLabel(form, text=text, font=("Segoe UI", 11, "bold"),
                                   text_color="#888888").pack(anchor="w")

        _lbl(self.t("modal_transfer_lbl"))
        self.entry = customtkinter.CTkEntry(
            form, placeholder_text=self.t("modal_transfer_ph"),
            fg_color="#232328", border_color="#2A4D2C",
            text_color="#FFFFFF", font=("Segoe UI", 14), height=38,
        )
        self.entry.pack(fill="x", pady=(2, 12))
        self.entry.focus()

        # Divider with hint
        customtkinter.CTkLabel(
            form, text=self.t("modal_transfer_info_hint"),
            font=("Segoe UI", 10), text_color="#444444",
        ).pack(anchor="w", pady=(0, 6))

        _lbl(self.t("modal_transfer_phone"))
        self.entry_phone = customtkinter.CTkEntry(
            form, placeholder_text=self.t("modal_transfer_phone_ph"),
            fg_color="#232328", border_color="#2A2A2E",
            text_color="#FFFFFF", font=("Segoe UI", 13), height=34,
        )
        self.entry_phone.pack(fill="x", pady=(2, 10))

        _lbl(self.t("modal_transfer_recip_id"))
        self.entry_recip_id = customtkinter.CTkEntry(
            form, placeholder_text=self.t("modal_transfer_recip_id_ph"),
            fg_color="#232328", border_color="#2A2A2E",
            text_color="#FFFFFF", font=("Segoe UI", 13), height=34,
        )
        self.entry_recip_id.pack(fill="x", pady=(2, 0))

        btn_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)

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
            phone     = self.entry_phone.get().strip()
            recip_id  = self.entry_recip_id.get().strip()
            self.on_confirm(val, phone, recip_id)
            self.destroy()
        except ValueError:
            self.entry.configure(border_color="#E05656")


# ─────────────────────────────────────────────────────────────────────────────
class FastAddTransactionModal(customtkinter.CTkToplevel):
    def __init__(self, parent, on_confirm):
        super().__init__(parent)
        self.t = parent.t
        self.title(self.t("modal_add_title"))
        self.geometry("440x490")
        self.resizable(False, False)
        self.configure(fg_color="#0B0B0C")
        self.transient(parent)
        self.grab_set()
        self.on_confirm = on_confirm
        self.dm  = parent.data_manager
        self.fmt = self.dm.format_amount

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
        cats = [c["name"] for c in parent.data_manager.categories] or ["Другое"]
        self.option_cat = customtkinter.CTkOptionMenu(
            form, values=cats,
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
        # ── Validate amount ───────────────────────────────────────────────────
        try:
            amount = float(self.entry_amount.get().replace(" ", ""))
            if amount <= 0:
                raise ValueError
        except ValueError:
            self.entry_amount.configure(border_color="#E05656")
            return

        tx_type  = "income" if self.option_type.get() == self._income_lbl else "expense"
        category = self.option_cat.get()
        vendor   = self.entry_vendor.get().strip() or "Прочие"
        comment  = self.entry_comment.get().strip() or "—"

        tx_data = {"amount": amount, "type": tx_type,
                   "category": category, "vendor": vendor, "comment": comment}

        def _do_add():
            self.on_confirm(amount, tx_type, category, vendor, comment)
            self.destroy()

        def _show_confirm():
            ConfirmTransactionModal(self, tx_data, _do_add, self.fmt)

        # ── Check category limit (expense only) ───────────────────────────────
        if tx_type == "expense":
            cat_obj = next(
                (c for c in self.dm.categories if c["name"].lower() == category.lower()),
                None,
            )
            if cat_obj and cat_obj["limit"] > 0 and (cat_obj["spent"] + amount) > cat_obj["limit"]:
                LimitWarningModal(
                    self, category, cat_obj["spent"], cat_obj["limit"],
                    self.fmt,
                    on_force=_show_confirm,   # add anyway → go to confirm
                    on_change=lambda: None,   # stay in form to fix
                )
                return

        _show_confirm()


# ─────────────────────────────────────────────────────────────────────────────
class ConfirmTransactionModal(customtkinter.CTkToplevel):
    """Shows a summary of the transaction and asks the user to confirm."""

    def __init__(self, parent, tx_data: dict, on_confirm, fmt):
        super().__init__(parent)
        self.t = parent.t
        self.title(self.t("confirm_tx_title"))
        self.geometry("390x310")
        self.resizable(False, False)
        self.configure(fg_color="#0B0B0C")
        self.transient(parent)
        self.grab_set()
        self.on_confirm = on_confirm

        customtkinter.CTkLabel(
            self, text=self.t("confirm_tx_title"),
            font=("Segoe UI", 16, "bold"), text_color="#FFFFFF",
        ).pack(pady=(22, 14))

        card = customtkinter.CTkFrame(
            self, fg_color="#232328",
            corner_radius=10, border_width=1, border_color="#2A2A2E",
        )
        card.pack(fill="x", padx=24, pady=(0, 16))

        is_income  = tx_data["type"] == "income"
        type_lbl   = self.t("modal_add_income") if is_income else self.t("modal_add_expense")
        type_color = "#56E056" if is_income else "#E05656"
        amt_text   = ("+" if is_income else "−") + fmt(tx_data["amount"])

        def _row(label, value, val_color="#FFFFFF"):
            row = customtkinter.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=16, pady=(7, 0))
            customtkinter.CTkLabel(
                row, text=label, font=("Segoe UI", 11),
                text_color="#666666", width=100, anchor="w",
            ).pack(side="left")
            customtkinter.CTkLabel(
                row, text=value, font=("Segoe UI", 11, "bold"),
                text_color=val_color, anchor="w",
            ).pack(side="left")

        _row(self.t("modal_add_type"),     type_lbl,            type_color)
        _row(self.t("modal_add_amount"),   amt_text,            type_color)
        _row(self.t("modal_add_category"), tx_data["category"])
        _row(self.t("modal_add_vendor"),   tx_data["vendor"])
        _row(self.t("modal_add_comment"),  tx_data["comment"])
        customtkinter.CTkFrame(card, height=8, fg_color="transparent").pack()

        btn_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        btn_frame.pack()

        customtkinter.CTkButton(
            btn_frame, text=self.t("btn_confirm"),
            font=("Segoe UI", 13, "bold"), fg_color="#1E351F",
            hover_color="#2A4D2C", text_color="#FFFFFF",
            height=34, corner_radius=20,
            command=self._do_confirm,
        ).pack(side="left", padx=8)

        customtkinter.CTkButton(
            btn_frame, text=self.t("btn_back"),
            font=("Segoe UI", 13, "bold"), fg_color="transparent",
            hover_color="#232328", text_color="#888888",
            height=34, corner_radius=20,
            command=self.destroy,
        ).pack(side="right", padx=8)

    def _do_confirm(self):
        self.on_confirm()
        self.destroy()


# ─────────────────────────────────────────────────────────────────────────────
class LimitWarningModal(customtkinter.CTkToplevel):
    """Warns that a category limit is about to be exceeded."""

    def __init__(self, parent, cat_name: str, spent: float, limit: float,
                 fmt, on_force, on_change):
        super().__init__(parent)
        self.t = parent.t
        self.title(self.t("limit_warn_title"))
        self.geometry("390x260")
        self.resizable(False, False)
        self.configure(fg_color="#0B0B0C")
        self.transient(parent)
        self.grab_set()
        self.on_force  = on_force
        self.on_change = on_change

        customtkinter.CTkLabel(
            self, text="⚠", font=("Segoe UI", 32),
            text_color="#E09030",
        ).pack(pady=(18, 2))

        customtkinter.CTkLabel(
            self, text=self.t("limit_warn_title"),
            font=("Segoe UI", 15, "bold"), text_color="#E05656",
        ).pack()

        customtkinter.CTkLabel(
            self, text=self.t("limit_warn_msg", cat=cat_name),
            font=("Segoe UI", 12), text_color="#AAAAAA",
            justify="center", wraplength=340,
        ).pack(pady=(10, 4), padx=24)

        pct = min(spent / limit * 100, 100) if limit > 0 else 100
        customtkinter.CTkLabel(
            self, text=f"{fmt(spent)} / {fmt(limit)}  ·  {pct:.0f}%",
            font=("Segoe UI", 11, "bold"), text_color="#E05656",
        ).pack(pady=(0, 18))

        btn_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        btn_frame.pack()

        customtkinter.CTkButton(
            btn_frame, text=self.t("limit_warn_force"),
            font=("Segoe UI", 12, "bold"), fg_color="#2A1515",
            hover_color="#4D1515", text_color="#E05656",
            height=34, corner_radius=20,
            command=self._do_force,
        ).pack(side="left", padx=8)

        customtkinter.CTkButton(
            btn_frame, text=self.t("limit_warn_change"),
            font=("Segoe UI", 12, "bold"), fg_color="transparent",
            hover_color="#232328", text_color="#888888",
            height=34, corner_radius=20,
            command=self._do_change,
        ).pack(side="right", padx=8)

    def _do_force(self):
        self.on_force()
        self.destroy()

    def _do_change(self):
        self.on_change()
        self.destroy()


# ─────────────────────────────────────────────────────────────────────────────
class TransactionsView(customtkinter.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, fg_color="#0B0B0C", **kwargs)
        self.controller = controller
        self.data_manager = controller.data_manager
        self.t = controller.t
        self.fmt = self.data_manager.format_amount

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

        period = self.data_manager.active_period
        stats  = self.data_manager.get_period_stats(period)

        income_lbl   = self.t(f"tx_card_income_{period}")
        expenses_lbl = self.t(f"tx_card_expenses_{period}")

        self._summary_card(row_frame, 0, self.t("tx_card_balance"),
                           self.fmt(self.data_manager.balance), "#FFFFFF")
        self._summary_card(row_frame, 1, income_lbl,
                           "+" + self.fmt(stats["income"]), "#56E056")
        self._summary_card(row_frame, 2, expenses_lbl,
                           "−" + self.fmt(stats["expenses"]), "#E05656")

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
        self._render_draft()

    # ──────────────────────────────────────────
    def _render_category_expenses(self):
        card = customtkinter.CTkFrame(self.left_column, fg_color="#232328",
                                      border_width=1, border_color="#2A2A2E", corner_radius=12)
        card.pack(fill="x", pady=(0, 12))

        customtkinter.CTkLabel(card, text=self.t("tx_section_cat"),
                               font=("Segoe UI", 13, "bold"), text_color="#FFFFFF",
                               ).pack(anchor="w", padx=20, pady=(15, 10))

        active_names = {c["name"].lower() for c in self.data_manager.categories}
        expenses = [e for e in self.data_manager.category_expenses
                    if e["category"].lower() in active_names]
        max_amount = max((c["amount"] for c in expenses), default=1.0)

        if not expenses:
            customtkinter.CTkLabel(
                card, text=self.t("empty_tx_cat"),
                font=("Segoe UI", 12), text_color="#555555",
                justify="center",
            ).pack(pady=20, padx=20)
        else:
            for cat_data in expenses:
                cat_name = cat_data["category"]
                cat_amt  = cat_data["amount"]
                ratio    = cat_amt / max_amount if max_amount > 0 else 0.0

                row = customtkinter.CTkFrame(card, fg_color="transparent")
                row.pack(fill="x", padx=20, pady=(6, 1))

                customtkinter.CTkLabel(row, text=cat_name,
                                       font=("Segoe UI", 12), text_color="#CCCCCC").pack(side="left")
                customtkinter.CTkLabel(row, text=self.fmt(cat_amt),
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

        table.grid_columnconfigure(0, weight=28)
        table.grid_columnconfigure(1, weight=20)
        table.grid_columnconfigure(2, weight=18)
        table.grid_columnconfigure(3, weight=26)
        table.grid_columnconfigure(4, weight=8)

        HEADER_PAD = {"pady": (0, 5), "padx": (0, 12)}
        DATA_PAD   = {"pady": 5,      "padx": (0, 12)}

        for col, (txt, anch) in enumerate([
            (self.t("tx_col_date"),    "w"),
            (self.t("tx_col_amount"),  "e"),
            (self.t("tx_col_category"),"w"),
            (self.t("tx_col_comment"), "w"),
            ("", "w"),
        ]):
            customtkinter.CTkLabel(table, text=txt,
                                   font=("Segoe UI", 11, "bold"), text_color="#555555",
                                   anchor=anch,
                                   ).grid(row=0, column=col, sticky="ew",
                                          **{k: v for k, v in HEADER_PAD.items()})

        customtkinter.CTkFrame(table, height=1, fg_color="#2A2A2E").grid(
            row=1, column=0, columnspan=5, sticky="ew", pady=(0, 6))

        if not self.data_manager.transactions:
            customtkinter.CTkLabel(
                table, text=self.t("empty_tx_history"),
                font=("Segoe UI", 12), text_color="#555555",
                justify="center",
            ).grid(row=2, column=0, columnspan=5, pady=24)
            return

        r = 2
        for tx in self.data_manager.transactions:
            date_vendor = f"{tx['date']}  {tx['vendor']}"

            if tx["type"] == "income":
                amt_text  = f"+{self.fmt(tx['amount'])}"
                amt_color = "#56E056"
            else:
                amt_text  = f"−{self.fmt(tx['amount'])}"
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

            if _is_cancellable(tx):
                ca = tx["created_at"]
                customtkinter.CTkButton(
                    table, text=self.t("tx_cancel_btn"),
                    font=("Segoe UI", 11, "bold"),
                    fg_color="transparent", hover_color="#3D1515",
                    text_color="#E05656", width=26, height=26, corner_radius=13,
                    command=lambda c=ca: self._handle_cancel_tx(c),
                ).grid(row=r, column=4, pady=3)
            else:
                customtkinter.CTkLabel(table, text="", width=26).grid(row=r, column=4)

            r += 1
            customtkinter.CTkFrame(table, height=1, fg_color="#1E1E22").grid(
                row=r, column=0, columnspan=5, sticky="ew", pady=3)
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
                card, text=self.t("empty_goal_card"),
                font=("Segoe UI", 12), text_color="#555555",
                justify="center",
            ).pack(expand=True, pady=(10, 18), padx=18)
            return

        # ── Цель задана ───────────────────────────────────────────
        remain = max(0.0, total - saved)
        ratio  = saved / total

        customtkinter.CTkLabel(card, text=self.fmt(total),
                               font=("Segoe UI", 11), text_color="#555555",
                               ).pack(anchor="e", padx=18, pady=(0, 2))
        customtkinter.CTkLabel(card, text=name,
                               font=("Segoe UI", 15, "bold"), text_color="#FFFFFF",
                               ).pack(anchor="w", padx=18, pady=(0, 4))

        sub = customtkinter.CTkFrame(card, fg_color="transparent")
        sub.pack(fill="x", padx=18, pady=(0, 8))
        customtkinter.CTkLabel(sub, text=self.fmt(saved),
                               font=("Segoe UI", 12, "bold"), text_color="#56E056").pack(side="left")
        customtkinter.CTkLabel(sub, text=f"  /  {self.fmt(remain)} {self.t('tx_goal_remaining')}",
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

        period_lbl = self.t(f"settings_period_{self.data_manager.active_period}")
        customtkinter.CTkLabel(card, text=f"{self.t('tx_card_ratio')} · {period_lbl}",
                               font=("Segoe UI", 13, "bold"), text_color="#FFFFFF",
                               ).pack(anchor="w", padx=18, pady=(15, 10))

        _stats   = self.data_manager.get_period_stats(self.data_manager.active_period)
        income   = _stats["income"]
        expenses = _stats["expenses"]

        labels = customtkinter.CTkFrame(card, fg_color="transparent")
        labels.pack(fill="x", padx=18, pady=(0, 6))

        customtkinter.CTkLabel(labels,
                               text=f"{self.t('tx_income_lbl')}  +{self.fmt(income)}",
                               font=("Segoe UI", 11, "bold"), text_color="#56E056").pack(side="left")
        customtkinter.CTkLabel(labels,
                               text=f"{self.t('tx_expenses_lbl')}  −{self.fmt(expenses)}",
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

    def _handle_transfer(self, amount: float, phone: str = "", recipient_id: str = ""):
        self.data_manager.add_transfer(amount)
        if phone or recipient_id:
            self.data_manager.save_draft(phone, recipient_id, amount)
        self.controller.switch_screen("transactions", add_to_history=False)

    def _handle_cancel_tx(self, created_at: str):
        self.data_manager.cancel_transaction(created_at)
        self.controller.switch_screen("transactions", add_to_history=False)

    def _handle_delete_draft(self, index: int):
        self.data_manager.delete_draft(index)
        self.controller.switch_screen("transactions", add_to_history=False)

    # ──────────────────────────────────────────
    def _render_draft(self):
        card = customtkinter.CTkFrame(self.right_column, fg_color="#232328",
                                      border_width=1, border_color="#2A2A2E", corner_radius=12)
        card.pack(fill="x", pady=(12, 0))

        hdr = customtkinter.CTkFrame(card, fg_color="transparent")
        hdr.pack(fill="x", padx=18, pady=(12, 6))
        customtkinter.CTkLabel(hdr, text=self.t("draft_title"),
                               font=("Segoe UI", 13, "bold"), text_color="#FFFFFF").pack(side="left")

        drafts = self.data_manager.drafts
        if not drafts:
            customtkinter.CTkLabel(card, text=self.t("draft_empty"),
                                   font=("Segoe UI", 11), text_color="#444444",
                                   ).pack(pady=(0, 12), padx=18, anchor="w")
            return

        for i, draft in enumerate(drafts[:3]):
            item = customtkinter.CTkFrame(card, fg_color="#1A1A1E", corner_radius=8)
            item.pack(fill="x", padx=14, pady=(0, 6))

            info = customtkinter.CTkFrame(item, fg_color="transparent")
            info.pack(side="left", fill="x", expand=True, padx=10, pady=6)

            line1 = f"📱 {draft['phone'] or '—'}  ·  🆔 {draft['recipient_id'] or '—'}"
            line2 = f"{self.t('draft_amount_lbl')} {self.fmt(draft['amount'])}  ·  {draft['date']}"
            customtkinter.CTkLabel(info, text=line1,
                                   font=("Segoe UI", 11), text_color="#CCCCCC").pack(anchor="w")
            customtkinter.CTkLabel(info, text=line2,
                                   font=("Segoe UI", 10), text_color="#555555").pack(anchor="w")

            customtkinter.CTkButton(
                item, text="✕", width=26, height=26,
                font=("Segoe UI", 11, "bold"), fg_color="transparent",
                hover_color="#3D1515", text_color="#E05656", corner_radius=13,
                command=lambda idx=i: self._handle_delete_draft(idx),
            ).pack(side="right", padx=6, pady=6)

        customtkinter.CTkFrame(card, fg_color="transparent", height=4).pack()
