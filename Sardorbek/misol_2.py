import csv
from datetime import datetime
from pathlib import Path


CSV_FILE = Path(__file__).with_name("expenses.csv")
FIELDS = ["ID", "Sana", "Kategoriya", "Izoh", "Summa"]


def load_expenses():
	if not CSV_FILE.exists():
		return []

	with CSV_FILE.open("r", newline="", encoding="utf-8-sig") as file:
		return list(csv.DictReader(file))


def add_expense():
	date_text = input("Sana (kk.oo.yyyy): ").strip()
	try:
		datetime.strptime(date_text, "%d.%m.%Y")
	except ValueError:
		print("Xatolik: sanani kk.oo.yyyy formatida kiriting.")
		return

	category = input("Kategoriya: ").strip()
	note = input("Izoh: ").strip()
	if not category:
		print("Xatolik: kategoriya bo'sh bo'lmasligi kerak.")
		return

	amount_text = input("Summa: ").strip()
	try:
		amount = int(amount_text)
		if amount <= 0:
			raise ValueError
	except ValueError:
		print("Xatolik: summa musbat butun son bo'lishi kerak.")
		return

	expenses = load_expenses()
	expense_id = max((int(row["ID"]) for row in expenses), default=0) + 1
	write_header = not CSV_FILE.exists() or CSV_FILE.stat().st_size == 0

	with CSV_FILE.open("a", newline="", encoding="utf-8-sig") as file:
		writer = csv.DictWriter(file, fieldnames=FIELDS)
		if write_header:
			writer.writeheader()
		writer.writerow({
			"ID": expense_id,
			"Sana": date_text,
			"Kategoriya": category,
			"Izoh": note,
			"Summa": amount,
		})
	print("Xarajat saqlandi.")


def show_expenses(expenses):
	if not expenses:
		print("Hozircha xarajatlar mavjud emas.")
		return

	print(f"{'ID':<5} {'Sana':<12} {'Kategoriya':<18} {'Izoh':<24} {'Summa':>12}")
	print("-" * 75)
	for row in expenses:
		print(
			f"{row['ID']:<5} {row['Sana']:<12} {row['Kategoriya']:<18} "
			f"{row['Izoh']:<24} {row['Summa']:>12}"
		)


def main():
	while True:
		print("\nShaxsiy xarajatlar hisobi")
		print("1. Yangi xarajat qo'shish")
		print("2. Barcha xarajatlarni ko'rish")
		print("3. Kategoriya bo'yicha saralash")
		print("4. Umumiy xarajatni hisoblash")
		print("5. Eng katta xarajatni aniqlash")
		print("6. Sana bo'yicha qidirish")
		print("7. Kategoriya bo'yicha jami xarajat")
		print("0. Chiqish")
		choice = input("Tanlov: ").strip()
		expenses = load_expenses()

		if choice == "1":
			add_expense()
		elif choice == "2":
			show_expenses(expenses)
		elif choice == "3":
			show_expenses(sorted(expenses, key=lambda row: row["Kategoriya"].casefold()))
		elif choice == "4":
			total = sum(int(row["Summa"]) for row in expenses)
			print(f"Umumiy xarajat: {total}")
		elif choice == "5":
			if expenses:
				largest = max(expenses, key=lambda row: int(row["Summa"]))
				print("Eng katta xarajat:")
				show_expenses([largest])
			else:
				print("Hozircha xarajatlar mavjud emas.")
		elif choice == "6":
			date_text = input("Qidiriladigan sana (kk.oo.yyyy): ").strip()
			try:
				datetime.strptime(date_text, "%d.%m.%Y")
			except ValueError:
				print("Xatolik: sanani kk.oo.yyyy formatida kiriting.")
				continue
			matches = [row for row in expenses if row["Sana"] == date_text]
			show_expenses(matches)
		elif choice == "7":
			totals = {}
			for row in expenses:
				category = row["Kategoriya"]
				totals[category] = totals.get(category, 0) + int(row["Summa"])
			if totals:
				for category, total in sorted(totals.items(), key=lambda item: item[0].casefold()):
					print(f"{category}: {total}")
			else:
				print("Hozircha xarajatlar mavjud emas.")
		elif choice == "0":
			print("Dastur yakunlandi.")
			break
		else:
			print("Noto'g'ri tanlov. Qaytadan urinib ko'ring.")


if __name__ == "__main__":
	main()
