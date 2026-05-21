import json
import csv
import os
from datetime import datetime

from core.locale_manager import LocaleManager


class DataManager:
    def __init__(self):
        # Locale / i18n
        self.locale = LocaleManager(default="ru")

        self.monthly_income   = 0.0
        self.monthly_expenses = 0.0
        self.balance          = 0.0

        # Single goal card shown on transactions dashboard (empty = no active goal)
        self.goal_name  = ""
        self.goal_total = 0.0
        self.goal_saved = 0.0

        # Category expenses used on transactions dashboard
        self.category_expenses: list[dict] = []

        # Full categories with spending limits (Categories screen)
        self.categories = [
            {"name": "Еда",         "icon": "🍔", "limit": 0.0, "spent": 0.0},
            {"name": "Транспорт",   "icon": "🚗", "limit": 0.0, "spent": 0.0},
            {"name": "Развлечения", "icon": "🎮", "limit": 0.0, "spent": 0.0},
            {"name": "Подписки",    "icon": "💳", "limit": 0.0, "spent": 0.0},
            {"name": "Мобильные",   "icon": "📱", "limit": 0.0, "spent": 0.0},
            {"name": "Другое",      "icon": "📦", "limit": 0.0, "spent": 0.0},
        ]

        # Goals (Goals screen)
        self.goals: list[dict] = []

        # Savings history shown on Goals screen
        self.savings_history: list[dict] = []

        # Analytics: previous month totals
        self.prev_monthly_income   = 0.0
        self.prev_monthly_expenses = 0.0

        # Analytics: per-category comparison (previous month vs this month)
        self.analytics_comparison: list[dict] = []

        # Transaction history
        self.transactions: list[dict] = []

    # ──────────────────────────────────────────
    # Computed helpers
    # ──────────────────────────────────────────

    def _recalculate_balance(self):
        self.balance = self.monthly_income - self.monthly_expenses

    def get_largest_expense_category(self) -> str:
        if not self.category_expenses:
            return ""
        return max(self.category_expenses, key=lambda c: c["amount"])["category"]

    def get_expense_change_percent(self) -> float:
        if self.prev_monthly_expenses == 0:
            return 0.0
        return (self.monthly_expenses - self.prev_monthly_expenses) / self.prev_monthly_expenses * 100

    def get_largest_category_change_percent(self) -> tuple:
        largest = self.get_largest_expense_category()
        for comp in self.analytics_comparison:
            if comp["category"] == largest and comp["prev"] > 0:
                pct = (comp["curr"] - comp["prev"]) / comp["prev"] * 100
                return largest, pct
        return largest, 0.0

    # ──────────────────────────────────────────
    # Transactions
    # ──────────────────────────────────────────

    def add_deposit(self, amount: float):
        if amount <= 0:
            return
        self.monthly_income += amount
        self._recalculate_balance()
        self.transactions.insert(0, {
            "date": "Сегодня", "vendor": "Банкомат",
            "category": "Пополнение", "comment": "Быстрое пополнение",
            "amount": amount, "type": "income",
        })

    def add_transfer(self, amount: float):
        if amount <= 0:
            return
        self.monthly_expenses += amount
        self._recalculate_balance()
        for cat in self.category_expenses:
            if cat["category"] == "Другое":
                cat["amount"] += amount
                break
        self.transactions.insert(0, {
            "date": "Сегодня", "vendor": "Перевод",
            "category": "Другое", "comment": "Быстрый перевод",
            "amount": amount, "type": "expense",
        })

    def add_custom_transaction(self, amount: float, tx_type: str, category: str, vendor: str, comment: str):
        if amount <= 0:
            return
        if tx_type == "income":
            self.monthly_income += amount
        else:
            self.monthly_expenses += amount
            found = False
            for cat in self.category_expenses:
                if cat["category"].lower() == category.lower():
                    cat["amount"] += amount
                    found = True
                    break
            if not found:
                self.category_expenses.append({"category": category, "amount": amount})
        self._recalculate_balance()
        self.transactions.insert(0, {
            "date": "Сегодня", "vendor": vendor,
            "category": category, "comment": comment,
            "amount": amount, "type": tx_type,
        })

    # ──────────────────────────────────────────
    # Categories
    # ──────────────────────────────────────────

    def add_category(self, name: str, icon: str, limit: float):
        self.categories.append({"name": name, "icon": icon, "limit": limit, "spent": 0.0})

    def edit_category(self, index: int, name: str, icon: str, limit: float):
        if 0 <= index < len(self.categories):
            self.categories[index].update({"name": name, "icon": icon, "limit": limit})

    # ──────────────────────────────────────────
    # Goals
    # ──────────────────────────────────────────

    def add_goal(self, name: str, icon: str, target: float, months_left: int):
        self.goals.append({"name": name, "icon": icon, "target": target, "saved": 0.0, "months_left": months_left})

    def add_saving_to_goal(self, goal_index: int, amount: float):
        if 0 <= goal_index < len(self.goals) and amount > 0:
            self.goals[goal_index]["saved"] += amount
            self.savings_history.insert(0, {
                "date": "Сегодня",
                "amount": amount,
                "goal": self.goals[goal_index]["name"],
                "type": "Перевод",
            })

    # ──────────────────────────────────────────
    # Export
    # ──────────────────────────────────────────

    def export_data(self, what: list, fmt: str, folder: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data = {}
        if "transactions" in what:
            data["transactions"] = self.transactions
        if "categories" in what:
            data["categories"] = self.categories
        if "goals" in what:
            data["goals"] = self.goals
        if "balance" in what:
            data["balance"] = {
                "current": self.balance,
                "monthly_income": self.monthly_income,
                "monthly_expenses": self.monthly_expenses,
            }

        if fmt == "json":
            path = os.path.join(folder, f"finance_export_{timestamp}.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        elif fmt == "csv":
            path = os.path.join(folder, f"finance_export_{timestamp}.csv")
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                w = csv.writer(f)
                if "transactions" in data:
                    w.writerow(["=== ТРАНЗАКЦИИ ==="])
                    w.writerow(["Дата", "Контрагент", "Категория", "Комментарий", "Сумма", "Тип"])
                    for tx in data["transactions"]:
                        w.writerow([tx["date"], tx["vendor"], tx["category"],
                                    tx["comment"], tx["amount"], tx["type"]])
                if "categories" in data:
                    w.writerow([])
                    w.writerow(["=== КАТЕГОРИИ ==="])
                    w.writerow(["Название", "Иконка", "Лимит", "Потрачено"])
                    for cat in data["categories"]:
                        w.writerow([cat["name"], cat["icon"], cat["limit"], cat["spent"]])
                if "goals" in data:
                    w.writerow([])
                    w.writerow(["=== ЦЕЛИ ==="])
                    w.writerow(["Название", "Цель (с)", "Накоплено (с)", "Осталось месяцев"])
                    for g in data["goals"]:
                        w.writerow([g["name"], g["target"], g["saved"], g["months_left"]])
                if "balance" in data:
                    w.writerow([])
                    w.writerow(["=== БАЛАНС ==="])
                    b = data["balance"]
                    w.writerow(["Текущий баланс", "Доходы за месяц", "Расходы за месяц"])
                    w.writerow([b["current"], b["monthly_income"], b["monthly_expenses"]])

        elif fmt == "excel":
            try:
                import openpyxl
                from openpyxl.styles import Font, PatternFill, Alignment
                path = os.path.join(folder, f"finance_export_{timestamp}.xlsx")
                wb = openpyxl.Workbook()
                header_font = Font(bold=True, color="FFFFFF")
                header_fill = PatternFill("solid", fgColor="1E351F")

                def _write_sheet(ws, headers, rows):
                    ws.append(headers)
                    for cell in ws[1]:
                        cell.font = header_font
                        cell.fill = header_fill
                        cell.alignment = Alignment(horizontal="center")
                    for row in rows:
                        ws.append(row)
                    for col in ws.columns:
                        ws.column_dimensions[col[0].column_letter].width = 20

                if "transactions" in data:
                    ws = wb.active
                    ws.title = "Транзакции"
                    _write_sheet(ws,
                        ["Дата", "Контрагент", "Категория", "Комментарий", "Сумма", "Тип"],
                        [[t["date"], t["vendor"], t["category"], t["comment"], t["amount"], t["type"]]
                         for t in data["transactions"]])
                if "categories" in data:
                    ws2 = wb.create_sheet("Категории")
                    _write_sheet(ws2,
                        ["Название", "Иконка", "Лимит (с)", "Потрачено (с)"],
                        [[c["name"], c["icon"], c["limit"], c["spent"]] for c in data["categories"]])
                if "goals" in data:
                    ws3 = wb.create_sheet("Цели")
                    _write_sheet(ws3,
                        ["Название", "Цель (с)", "Накоплено (с)", "Осталось месяцев"],
                        [[g["name"], g["target"], g["saved"], g["months_left"]] for g in data["goals"]])
                if "balance" in data:
                    ws4 = wb.create_sheet("Баланс")
                    b = data["balance"]
                    _write_sheet(ws4,
                        ["Текущий баланс (с)", "Доходы за месяц (с)", "Расходы за месяц (с)"],
                        [[b["current"], b["monthly_income"], b["monthly_expenses"]]])
                wb.save(path)
            except ImportError:
                # fallback to CSV
                path = os.path.join(folder, f"finance_export_{timestamp}_excel.csv")
                with open(path, "w", newline="", encoding="utf-8-sig") as f:
                    w = csv.writer(f)
                    w.writerow(["openpyxl не установлен. Экспортировано в CSV формате."])

        return path
