import customtkinter


# ─────────────────────────────────────────────────────────────────────────────
class CreateGoalModal(customtkinter.CTkToplevel):
    def __init__(self, parent, on_confirm, prefill=None):
        super().__init__(parent)
        self.t = parent.t
        is_edit = prefill is not None
        title_key = "create_goal_title_edit" if is_edit else "create_goal_title"
        self.title(self.t(title_key))
        self.geometry("400x410")
        self.resizable(False, False)
        self.configure(fg_color="#0B0B0C")
        self.transient(parent)
        self.grab_set()
        self.on_confirm = on_confirm

        customtkinter.CTkLabel(
            self, text=self.t(title_key),
            font=("Segoe UI", 16, "bold"), text_color="#FFFFFF",
        ).pack(pady=(20, 15))

        form = customtkinter.CTkFrame(self, fg_color="transparent")
        form.pack(padx=30, fill="x")

        def _field(label, placeholder=""):
            customtkinter.CTkLabel(form, text=label, font=("Segoe UI", 12, "bold"),
                                   text_color="#888888").pack(anchor="w")
            e = customtkinter.CTkEntry(form, placeholder_text=placeholder,
                                      fg_color="#232328", border_color="#2A4D2C",
                                      text_color="#FFFFFF", height=32)
            e.pack(fill="x", pady=(2, 10))
            return e

        self.entry_name   = _field(self.t("create_goal_name"),   self.t("create_goal_name_ph"))
        self.entry_icon   = _field(self.t("create_goal_icon"),   self.t("create_goal_icon_ph"))
        self.entry_target = _field(self.t("create_goal_target"), self.t("create_goal_tgt_ph"))
        self.entry_months = _field(self.t("create_goal_months"), self.t("create_goal_mo_ph"))

        if prefill:
            self.entry_name.insert(0, prefill["name"])
            self.entry_icon.insert(0, prefill.get("icon", ""))
            self.entry_target.insert(0, str(int(prefill["target"])))
            self.entry_months.insert(0, str(int(prefill["months_left"])))

        btn_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(0, 20))

        btn_label = self.t("btn_save") if is_edit else self.t("btn_create")
        customtkinter.CTkButton(
            btn_frame, text=btn_label,
            font=("Segoe UI", 14, "bold"), fg_color="#1E351F",
            hover_color="#2A4D2C", text_color="#FFFFFF", height=35,
            command=self._confirm,
        ).pack(side="left", padx=10)

        customtkinter.CTkButton(
            btn_frame, text=self.t("btn_cancel"),
            font=("Segoe UI", 14, "bold"), fg_color="transparent",
            hover_color="#333333", text_color="#FFFFFF", height=35,
            command=self.destroy,
        ).pack(side="right", padx=10)

    def _confirm(self):
        name = self.entry_name.get().strip()
        icon = self.entry_icon.get().strip() or "🎯"
        ok = True
        try:
            target = float(self.entry_target.get().replace(" ", ""))
            if target <= 0:
                raise ValueError
        except ValueError:
            self.entry_target.configure(border_color="#E05656")
            ok = False
        try:
            months = int(self.entry_months.get().strip())
            if months <= 0:
                raise ValueError
        except ValueError:
            self.entry_months.configure(border_color="#E05656")
            ok = False
        if not name:
            self.entry_name.configure(border_color="#E05656")
            ok = False
        if ok:
            self.on_confirm(name, icon, target, months)
            self.destroy()


# ─────────────────────────────────────────────────────────────────────────────
class AddSavingModal(customtkinter.CTkToplevel):
    def __init__(self, parent, goal_name, on_confirm):
        super().__init__(parent)
        self.t = parent.t
        self.title(self.t("fill_goal_prefix"))
        self.geometry("380x200")
        self.resizable(False, False)
        self.configure(fg_color="#0B0B0C")
        self.transient(parent)
        self.grab_set()
        self.on_confirm = on_confirm

        customtkinter.CTkLabel(
            self, text=f"{self.t('fill_goal_prefix')} {goal_name}",
            font=("Segoe UI", 14, "bold"), text_color="#FFFFFF",
        ).pack(pady=(20, 10))

        self.entry = customtkinter.CTkEntry(
            self, placeholder_text=self.t("fill_goal_amount_ph"),
            fg_color="#232328", border_color="#2A4D2C",
            text_color="#FFFFFF", height=36,
        )
        self.entry.pack(padx=30, fill="x", pady=(0, 15))
        self.entry.focus()

        btn_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        btn_frame.pack()

        customtkinter.CTkButton(
            btn_frame, text=self.t("btn_fill"),
            font=("Segoe UI", 13, "bold"), fg_color="#1E351F",
            hover_color="#2A4D2C", text_color="#FFFFFF", height=33,
            command=self._confirm,
        ).pack(side="left", padx=8)

        customtkinter.CTkButton(
            btn_frame, text=self.t("btn_cancel"),
            font=("Segoe UI", 13, "bold"), fg_color="transparent",
            hover_color="#333333", text_color="#FFFFFF", height=33,
            command=self.destroy,
        ).pack(side="right", padx=8)

    def _confirm(self):
        try:
            val = float(self.entry.get().replace(" ", ""))
            if val <= 0:
                raise ValueError
            self.on_confirm(val)
            self.destroy()
        except ValueError:
            self.entry.configure(border_color="#E05656")


# ─────────────────────────────────────────────────────────────────────────────
class GoalsView(customtkinter.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, fg_color="#0B0B0C", **kwargs)
        self.controller = controller
        self.dm = controller.data_manager
        self.t = controller.t
        self.fmt = self.dm.format_amount

        scroll = customtkinter.CTkScrollableFrame(
            self, fg_color="transparent",
            scrollbar_fg_color="#0B0B0C",
            scrollbar_button_color="#232328",
            scrollbar_button_hover_color="#1E351F",
        )
        scroll.pack(fill="both", expand=True, padx=5, pady=5)

        self._init_header(scroll)
        self._init_goals_row(scroll)
        self._init_divider(scroll)
        self._init_history(scroll)

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
            frame, text=self.t("goals_title"),
            font=("Segoe UI", 22, "bold"), text_color="#FFFFFF",
        ).pack(side="left")

        customtkinter.CTkButton(
            frame, text=self.t("goals_btn_create"),
            font=("Segoe UI", 13, "bold"), fg_color="#1E351F",
            hover_color="#2A4D2C", text_color="#FFFFFF",
            height=38, corner_radius=8,
            command=self._open_create_modal,
        ).pack(side="right")

    # ──────────────────────────────────────────
    def _init_goals_row(self, parent):
        self.goals_container = customtkinter.CTkFrame(parent, fg_color="transparent")
        self.goals_container.pack(fill="x", padx=15, pady=(0, 10))
        self._render_goal_cards()

    def _render_goal_cards(self):
        for w in self.goals_container.winfo_children():
            w.destroy()

        goals = self.dm.goals

        # Пустое состояние
        if not goals:
            customtkinter.CTkLabel(
                self.goals_container,
                text=self.t("empty_goals"),
                font=("Segoe UI", 12), text_color="#555555",
                justify="center",
            ).pack(pady=30, padx=20)
            return

        for idx, goal in enumerate(goals):
            self.goals_container.grid_columnconfigure(idx, weight=1)

        for idx, goal in enumerate(goals):
            pad = (0, 10) if idx < len(goals) - 1 else (0, 0)
            card = self._build_goal_card(goal, idx)
            card.grid(row=0, column=idx, padx=pad, sticky="nsew")

    def _build_goal_card(self, goal, idx):
        card = customtkinter.CTkFrame(
            self.goals_container, fg_color="#1E351F",
            corner_radius=12, border_width=1, border_color="#2A4D2C",
        )

        top = customtkinter.CTkFrame(card, fg_color="transparent")
        top.pack(fill="x", padx=14, pady=(14, 6))
        customtkinter.CTkLabel(top, text=goal["icon"],
                               font=("Segoe UI", 20), text_color="#FFFFFF").pack(side="left")
        customtkinter.CTkLabel(top, text=f"  {goal['name']}",
                               font=("Segoe UI", 14, "bold"), text_color="#FFFFFF").pack(side="left")

        customtkinter.CTkLabel(
            card,
            text=f"{self.fmt(goal['saved'])} / {self.fmt(goal['target'])}",
            font=("Segoe UI", 14, "bold"), text_color="#FFFFFF",
        ).pack(anchor="w", padx=14, pady=(0, 8))

        ratio = min(goal["saved"] / goal["target"], 1.0) if goal["target"] > 0 else 0.0
        bar = customtkinter.CTkProgressBar(card, height=8, corner_radius=4,
                                           fg_color="#0B0B0C", progress_color="#56E056")
        bar.pack(fill="x", padx=14, pady=(0, 8))
        bar.set(ratio)

        remaining = max(goal["target"] - goal["saved"], 0.0)
        pct_done = ratio * 100
        customtkinter.CTkLabel(
            card,
            text=f"{self.t('goals_remaining_lbl')} {self.fmt(remaining)} · {pct_done:.0f}%",
            font=("Segoe UI", 11), text_color="#AAFFAA",
        ).pack(anchor="w", padx=14, pady=(0, 4))

        # Months left — use locale-aware declension via month_suffix()
        months = goal["months_left"]
        suffix = self.dm.locale.month_suffix(months)
        months_text = self.t("goals_months_fmt", n=months, sfx=suffix)
        customtkinter.CTkLabel(
            card, text=months_text,
            font=("Segoe UI", 11), text_color="#888888",
        ).pack(anchor="w", padx=14, pady=(0, 8))

        # ── Pin hint (shown only when this goal is the active one) ──
        is_pinned = (idx == self.dm.active_goal_index)
        if is_pinned:
            pin_hint = customtkinter.CTkFrame(card, fg_color="#1A3A1A",
                                              corner_radius=6, border_width=1,
                                              border_color="#56E056")
            pin_hint.pack(fill="x", padx=14, pady=(0, 8))
            customtkinter.CTkLabel(pin_hint,
                                   text=f"✓  {self.t('goals_pinned_hint')}",
                                   font=("Segoe UI", 10, "bold"),
                                   text_color="#56E056").pack(pady=4)

        btn_row = customtkinter.CTkFrame(card, fg_color="transparent")
        btn_row.pack(padx=14, pady=(0, 14), fill="x")

        customtkinter.CTkButton(
            btn_row, text=self.t("goals_btn_fill"),
            font=("Segoe UI", 11, "bold"), fg_color="#2A4D2C",
            hover_color="#56E056", text_color="#FFFFFF",
            height=28, corner_radius=6,
            command=lambda i=idx: self._open_add_saving(i),
        ).pack(side="left", fill="x", expand=True, padx=(0, 6))

        # 📌 Pin button — shows goal in Transactions "My Goal" card
        customtkinter.CTkButton(
            btn_row, text="📌", width=34, height=28,
            font=("Segoe UI", 13),
            fg_color="#1E351F" if is_pinned else "transparent",
            hover_color="#1E351F",
            text_color="#56E056" if is_pinned else "#555555",
            corner_radius=6,
            command=lambda i=idx: self._handle_pin_goal(i),
        ).pack(side="right", padx=(0, 4))

        customtkinter.CTkButton(
            btn_row, text="🗑", width=34, height=28,
            font=("Segoe UI", 13), fg_color="#2A1515",
            hover_color="#4D1515", text_color="#E05656",
            corner_radius=6,
            command=lambda i=idx: self._handle_delete_goal(i),
        ).pack(side="right")

        customtkinter.CTkButton(
            btn_row, text="✏", width=34, height=28,
            font=("Segoe UI", 13), fg_color="#1A2A1A",
            hover_color="#2A4D2C", text_color="#AAFFAA",
            corner_radius=6,
            command=lambda i=idx: self._open_edit_goal_modal(i),
        ).pack(side="right", padx=(0, 4))

        return card

    # ──────────────────────────────────────────
    def _init_divider(self, parent):
        customtkinter.CTkFrame(parent, height=1, fg_color="#2E2E34").pack(
            fill="x", padx=15, pady=10)

    # ──────────────────────────────────────────
    def _init_history(self, parent):
        card = customtkinter.CTkFrame(
            parent, fg_color="#232328",
            corner_radius=12, border_width=1, border_color="#2A4D2C",
        )
        card.pack(fill="x", padx=15, pady=(0, 20))

        customtkinter.CTkLabel(
            card, text=self.t("goals_history_title"),
            font=("Segoe UI", 14, "bold"), text_color="#FFFFFF",
        ).pack(anchor="w", padx=20, pady=(15, 10))

        table = customtkinter.CTkFrame(card, fg_color="transparent")
        table.pack(fill="x", padx=20, pady=(0, 15))
        for i, w in enumerate([1, 2, 2, 1]):
            table.grid_columnconfigure(i, weight=w)

        headers = [
            self.t("goals_col_date"),
            self.t("goals_col_amount"),
            self.t("goals_col_goal"),
            self.t("goals_col_type"),
        ]
        for col, hdr in enumerate(headers):
            customtkinter.CTkLabel(table, text=hdr, font=("Segoe UI", 11, "bold"),
                                   text_color="#888888", anchor="w",
                                   ).grid(row=0, column=col, sticky="ew", pady=(0, 5), padx=(0, 8))

        customtkinter.CTkFrame(table, height=1, fg_color="#3A3A40").grid(
            row=1, column=0, columnspan=4, sticky="ew", pady=(0, 8))

        if not self.dm.savings_history:
            customtkinter.CTkLabel(
                card, text=self.t("empty_savings"),
                font=("Segoe UI", 12), text_color="#555555",
                justify="center",
            ).pack(pady=20, padx=20)
            return

        r = 2
        for entry in self.dm.savings_history:
            customtkinter.CTkLabel(table, text=entry["date"],
                                   font=("Segoe UI", 11), text_color="#FFFFFF", anchor="w",
                                   ).grid(row=r, column=0, sticky="ew", pady=5, padx=(0, 8))
            customtkinter.CTkLabel(table, text=f"+{self.fmt(entry['amount'])}",
                                   font=("Segoe UI", 11, "bold"), text_color="#56E056", anchor="w",
                                   ).grid(row=r, column=1, sticky="ew", pady=5, padx=(0, 8))
            customtkinter.CTkLabel(table, text=entry["goal"],
                                   font=("Segoe UI", 11), text_color="#FFFFFF", anchor="w",
                                   ).grid(row=r, column=2, sticky="ew", pady=5, padx=(0, 8))
            customtkinter.CTkLabel(table, text=entry["type"],
                                   font=("Segoe UI", 11), text_color="#888888", anchor="w",
                                   ).grid(row=r, column=3, sticky="ew", pady=5)
            r += 1
            customtkinter.CTkFrame(table, height=1, fg_color="#2E2E34").grid(
                row=r, column=0, columnspan=4, sticky="ew", pady=2)
            r += 1

        if len(self.dm.savings_history) > 4:
            customtkinter.CTkButton(
                card, text=self.t("goals_show_all"),
                font=("Segoe UI", 12), fg_color="transparent",
                hover_color="#1E351F", text_color="#56E056",
                height=30, anchor="e",
                command=lambda: None,
            ).pack(anchor="e", padx=20, pady=(0, 10))

    # ──────────────────────────────────────────
    def _open_create_modal(self):
        CreateGoalModal(self.winfo_toplevel(), self._handle_create)

    def _handle_create(self, name, icon, target, months):
        self.dm.add_goal(name, icon, target, months)
        self._render_goal_cards()

    def _open_edit_goal_modal(self, idx):
        prefill = self.dm.goals[idx]
        CreateGoalModal(self.winfo_toplevel(),
                        lambda n, ic, t, m: self._handle_edit_goal(idx, n, ic, t, m),
                        prefill=prefill)

    def _handle_edit_goal(self, idx, name, icon, target, months):
        self.dm.edit_goal(idx, name, icon, target, months)
        self.controller.switch_screen("goals", add_to_history=False)

    def _open_add_saving(self, idx):
        goal_name = self.dm.goals[idx]["name"]
        AddSavingModal(self.winfo_toplevel(), goal_name,
                       lambda amt: self._handle_saving(idx, amt))

    def _handle_saving(self, idx, amount):
        self.dm.add_saving_to_goal(idx, amount)
        self.controller.switch_screen("goals", add_to_history=False)

    def _handle_delete_goal(self, idx):
        self.dm.delete_goal(idx)
        self.controller.switch_screen("goals", add_to_history=False)

    def _handle_pin_goal(self, idx):
        # Toggle: click on already-pinned goal → unpin; otherwise pin
        if idx == self.dm.active_goal_index:
            self.dm.set_active_goal(-1)
        else:
            self.dm.set_active_goal(idx)
        self._render_goal_cards()
