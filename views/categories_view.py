import customtkinter


# ─────────────────────────────────────────────────────────────────────────────
class AddCategoryModal(customtkinter.CTkToplevel):
    def __init__(self, parent, on_confirm, prefill=None):
        super().__init__(parent)
        self.t = parent.t
        is_edit = prefill is not None
        title_key = "add_cat_title_edit" if is_edit else "add_cat_title_new"
        self.title(self.t(title_key))
        self.geometry("400x320")
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

        # Name
        customtkinter.CTkLabel(form, text=self.t("add_cat_name"),
                               font=("Segoe UI", 12, "bold"), text_color="#888888").pack(anchor="w")
        self.entry_name = customtkinter.CTkEntry(
            form, fg_color="#232328", border_color="#2A4D2C",
            text_color="#FFFFFF", height=32,
        )
        self.entry_name.pack(fill="x", pady=(2, 10))

        # Icon
        customtkinter.CTkLabel(form, text=self.t("add_cat_icon"),
                               font=("Segoe UI", 12, "bold"), text_color="#888888").pack(anchor="w")
        self.entry_icon = customtkinter.CTkEntry(
            form, placeholder_text=self.t("add_cat_icon_ph"),
            fg_color="#232328", border_color="#2A4D2C",
            text_color="#FFFFFF", height=32,
        )
        self.entry_icon.pack(fill="x", pady=(2, 10))

        # Limit
        customtkinter.CTkLabel(form, text=self.t("add_cat_limit"),
                               font=("Segoe UI", 12, "bold"), text_color="#888888").pack(anchor="w")
        self.entry_limit = customtkinter.CTkEntry(
            form, placeholder_text=self.t("add_cat_limit_ph"),
            fg_color="#232328", border_color="#2A4D2C",
            text_color="#FFFFFF", height=32,
        )
        self.entry_limit.pack(fill="x", pady=(2, 15))

        if prefill:
            self.entry_name.insert(0, prefill["name"])
            self.entry_icon.insert(0, prefill["icon"])
            if prefill["limit"] > 0:
                self.entry_limit.insert(0, str(int(prefill["limit"])))

        btn_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(0, 20))

        customtkinter.CTkButton(
            btn_frame, text=self.t("btn_save"),
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
        icon = self.entry_icon.get().strip() or "📦"
        try:
            limit = float(self.entry_limit.get().replace(" ", "")) if self.entry_limit.get().strip() else 0.0
        except ValueError:
            self.entry_limit.configure(border_color="#E05656")
            return
        if not name:
            self.entry_name.configure(border_color="#E05656")
            return
        self.on_confirm(name, icon, limit)
        self.destroy()


# ─────────────────────────────────────────────────────────────────────────────
class CategoriesView(customtkinter.CTkFrame):
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
        self._init_grid(scroll)

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
            frame, text=self.t("cat_title"),
            font=("Segoe UI", 22, "bold"), text_color="#FFFFFF",
        ).pack(side="left")

        customtkinter.CTkButton(
            frame, text=self.t("cat_btn_add"),
            font=("Segoe UI", 13, "bold"), fg_color="#1E351F",
            hover_color="#2A4D2C", text_color="#FFFFFF",
            height=38, corner_radius=8,
            command=self._open_add_modal,
        ).pack(side="right")

    # ──────────────────────────────────────────
    def _init_grid(self, parent):
        self.grid_frame = customtkinter.CTkFrame(parent, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True, padx=15, pady=(0, 20))
        self.grid_frame.grid_columnconfigure(0, weight=1)
        self.grid_frame.grid_columnconfigure(1, weight=1)
        self._render_cards()

    def _render_cards(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()

        categories = self.dm.categories
        row, col = 0, 0
        for idx, cat in enumerate(categories):
            card = self._build_category_card(cat, idx)
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            col += 1
            if col > 1:
                col = 0
                row += 1

    # ──────────────────────────────────────────
    def _build_category_card(self, cat, idx):
        card = customtkinter.CTkFrame(
            self.grid_frame, fg_color="#1E351F",
            corner_radius=12, border_width=1, border_color="#2A4D2C",
        )

        top = customtkinter.CTkFrame(card, fg_color="transparent")
        top.pack(fill="x", padx=15, pady=(14, 0))

        customtkinter.CTkLabel(
            top, text=f"{cat['icon']}  {cat['name']}",
            font=("Segoe UI", 16, "bold"), text_color="#FFFFFF",
        ).pack(side="left")

        customtkinter.CTkButton(
            top, text="🗑", width=28, height=28,
            font=("Segoe UI", 13), fg_color="transparent",
            hover_color="#4D1515", text_color="#E05656",
            command=lambda i=idx: self._handle_delete_category(i),
        ).pack(side="right", padx=(4, 0))

        customtkinter.CTkButton(
            top, text="✏", width=28, height=28,
            font=("Segoe UI", 14), fg_color="transparent",
            hover_color="#2A4D2C", text_color="#FFFFFF",
            command=lambda i=idx: self._open_edit_modal(i),
        ).pack(side="right")

        customtkinter.CTkLabel(
            card, text=f"{self.t('cat_limit_lbl')} {self.fmt(cat['limit'])}",
            font=("Segoe UI", 12), text_color="#AAFFAA",
        ).pack(anchor="w", padx=15, pady=(4, 6))

        ratio = min(cat["spent"] / cat["limit"], 1.0) if cat["limit"] > 0 else 0.0
        bar_color = "#E05656" if ratio > 0.9 else "#56E056"
        bar = customtkinter.CTkProgressBar(
            card, height=6, corner_radius=3,
            fg_color="#0B0B0C", progress_color=bar_color,
        )
        bar.pack(fill="x", padx=15, pady=(0, 6))
        bar.set(ratio)

        pct = ratio * 100
        bottom = customtkinter.CTkFrame(card, fg_color="transparent")
        bottom.pack(fill="x", padx=15, pady=(0, 14))

        customtkinter.CTkLabel(
            bottom, text=f"{self.t('cat_spent_lbl')} {self.fmt(cat['spent'])} · {pct:.0f}%",
            font=("Segoe UI", 11), text_color="#CCCCCC",
        ).pack(side="left")

        pct_badge_color = "#E05656" if ratio > 0.9 else "#56E056"
        customtkinter.CTkLabel(
            bottom, text=f"{pct:.0f}%",
            font=("Segoe UI", 13, "bold"), text_color=pct_badge_color,
        ).pack(side="right")

        return card

    # ──────────────────────────────────────────
    def _open_add_modal(self):
        AddCategoryModal(self.winfo_toplevel(), self._handle_add)

    def _handle_add(self, name, icon, limit):
        self.dm.add_category(name, icon, limit)
        self._render_cards()

    def _open_edit_modal(self, idx):
        prefill = self.dm.categories[idx]
        AddCategoryModal(self.winfo_toplevel(),
                         lambda n, ic, lm: self._handle_edit(idx, n, ic, lm),
                         prefill=prefill)

    def _handle_edit(self, idx, name, icon, limit):
        self.dm.edit_category(idx, name, icon, limit)
        self._render_cards()

    def _handle_delete_category(self, idx):
        self.dm.delete_category(idx)
        self._render_cards()
