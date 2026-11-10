import csv
import os

FILENAME = "books.csv"

def initialize_file():
    if not os.path.exists(FILENAME):
        try:
            with open(FILENAME, mode='w', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Kitob nomi", "Muallif", "Soni", "Holati"])
                writer.writerow([1, "Python asoslari", "Aliyev", 5, "Mavjud"])
                writer.writerow([2, "HTML va CSS", "Valiyev", 3, "Mavjud"])
        except Exception as e:
            print(f"Faylni yaratishda xatolik yuz berdi: {e}")

def read_books():
    books = []
    try:
        if os.path.exists(FILENAME):
            with open(FILENAME, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    row['ID'] = int(row['ID'])
                    row['Soni'] = int(row['Soni'])
                    books.append(row)
    except Exception as e:
        print(f"Faylni o'qishda xatolik: {e}")
    return books

def write_books(books):
    try:
        with open(FILENAME, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Kitob nomi", "Muallif", "Soni", "Holati"])
            for book in books:
                writer.writerow([book['ID'], book['Kitob nomi'], book['Muallif'], book['Soni'], book['Holati']])
    except Exception as e:
        print(f"Faylga yozishda xatolik: {e}")

def add_book():
    print("\n--- Yangi kitob qo'shish ---")
    books = read_books()
    
    new_id = max([b['ID'] for b in books], default=0) + 1
    
    title = input("Kitob nomini kiriting: ").strip()
    if not title:
        print("Xatolik: Kitob nomi bo'sh bo'lishi mumkin emas!")
        return

    author = input("Muallifni kiriting: ").strip()
    if not author:
        print("Xatolik: Muallif ismi bo'sh bo'lishi mumkin emas!")
        return

    try:
        quantity = int(input("Kitob sonini kiriting: "))
        if quantity < 0:
            print("Xatolik: Kitob soni manfiy bo'lishi mumkin emas!")
            return
    except ValueError:
        print("Xatolik: Iltimos, son kiritishda faqat raqamlardan foydalaning!")
        return

    status = "Mavjud" if quantity > 0 else "Tugagan"
    
    books.append({
        "ID": new_id,
        "Kitob nomi": title,
        "Muallif": author,
        "Soni": quantity,
        "Holati": status
    })
    
    write_books(books)
    print(f"Muvaffaqiyatli: '{title}' kitobi qo'shildi (ID: {new_id})!")

def view_books():
    books = read_books()
    if not books:
        print("\nKutubxonada kitoblar mavjud emas.")
        return

    print("\n--- Barcha kitoblar ro'yxati ---")
    print(f"{'ID':<4} | {'Kitob nomi':<25} | {'Muallif':<15} | {'Soni':<6} | {'Holati':<10}")
    print("-" * 68)
    for b in books:
        print(f"{b['ID']:<4} | {b['Kitob nomi']:<25} | {b['Muallif']:<15} | {b['Soni']:<6} | {b['Holati']:<10}")

def search_by_name():
    keyword = input("\nQidirilayotgan kitob nomini kiriting: ").strip().lower()
    books = read_books()
    results = [b for b in books if keyword in b['Kitob nomi'].lower()]

    if not results:
        print("Bunday nomdagi kitob topilmadi.")
        return

    print("\n--- Qidiruv natijalari ---")
    print(f"{'ID':<4} | {'Kitob nomi':<25} | {'Muallif':<15} | {'Soni':<6} | {'Holati':<10}")
    print("-" * 68)
    for b in results:
        print(f"{b['ID']:<4} | {b['Kitob nomi']:<25} | {b['Muallif']:<15} | {b['Soni']:<6} | {b['Holati']:<10}")

def search_by_author():
    """4. Muallif bo'yicha qidirish"""
    keyword = input("\nQidirilayotgan muallif nomini kiriting: ").strip().lower()
    books = read_books()
    results = [b for b in books if keyword in b['Muallif'].lower()]

    if not results:
        print("Bunday muallifga tegishli kitob topilmadi.")
        return

    print("\n--- Qidiruv natijalari ---")
    print(f"{'ID':<4} | {'Kitob nomi':<25} | {'Muallif':<15} | {'Soni':<6} | {'Holati':<10}")
    print("-" * 68)
    for b in results:
        print(f"{b['ID']:<4} | {b['Kitob nomi']:<25} | {b['Muallif']:<15} | {b['Soni']:<6} | {b['Holati']:<10}")

def issue_book():
    view_books()
    try:
        book_id = int(input("\nBeriladigan kitob ID raqamini kiriting: "))
    except ValueError:
        print("Xatolik: ID raqam bo'lishi kerak!")
        return

    books = read_books()
    found = False
    for b in books:
        if b['ID'] == book_id:
            found = True
            if b['Soni'] > 0:
                b['Soni'] -= 1
                if b['Soni'] == 0:
                    b['Holati'] = "Tugagan"
                write_books(books)
                print(f"Muvaffaqiyatli: '{b['Kitob nomi']}' kitobi berildi. Qolgan soni: {b['Soni']} ta.")
            else:
                print("Xatolik: Bu kitob hozirda mavjud emas (soni 0 ta).")
            break

    if not found:
        print("Xatolik: Bunday ID raqamli kitob topilmadi!")

def return_book():
    view_books()
    try:
        book_id = int(input("\nQaytarilayotgan kitob ID raqamini kiriting: "))
    except ValueError:
        print("Xatolik: ID raqam bo'lishi kerak!")
        return

    books = read_books()
    found = False
    for b in books:
        if b['ID'] == book_id:
            found = True
            b['Soni'] += 1
            b['Holati'] = "Mavjud"
            write_books(books)
            print(f"Muvaffaqiyatli: '{b['Kitob nomi']}' kitobi qaytarib olindi. Hozirgi soni: {b['Soni']} ta.")
            break

    if not found:
        print("Xatolik: Bunday ID raqamli kitob topilmadi!")

def view_available_count():
    """7. Kutubxonada mavjud jami kitoblar sonini ko'rish"""
    books = read_books()
    if not books:
        print("\nKutubxonada kitoblar mavjud emas.")
        return

    total_books = sum(b['Soni'] for b in books)
    available_titles_count = sum(1 for b in books if b['Soni'] > 0)
    
    print("\n--- Kutubxona statistikasi ---")
    print(f"Jami kitob nomlari (pozitsiyalar) soni: {len(books)}")
    print(f"Mavjud kitoblar turlari soni: {available_titles_count}")
    print(f"Kutubxonadagi jami nusxalar (kitoblar) soni: {total_books} ta")

def max_copies_book():
    books = read_books()
    if not books:
        print("\nKutubxonada kitoblar mavjud emas.")
        return

    max_count = max(b['Soni'] for b in books)
    top_books = [b for b in books if b['Soni'] == max_count]

    print(f"\n--- Eng ko'p nusxaga ega kitob(lar) [Nusxalar soni: {max_count} ta] ---")
    for b in top_books:
        print(f"- ID: {b['ID']} | {b['Kitob nomi']} ({b['Muallif']})")

def main():
    initialize_file()
    while True:
        print("\n================ KUTUBXONA TIZIMI ================")
        print("1. Yangi kitob qo'shish")
        print("2. Barcha kitoblarni ko'rish")
        print("3. Kitob nomi bo'yicha qidirish")
        print("4. Muallif bo'yicha qidirish")
        print("5. Kitobni kutubxonadan berish")
        print("6. Qaytarilgan kitobni qayta hisobga olish")
        print("7. Kutubxonada mavjud kitoblar sonini ko'rish")
        print("8. Eng ko'p nusxaga ega kitobni aniqlash")
        print("0. Dasturdan chiqish")
        print("==================================================")
        
        choice = input("Tanlovingizni kiriting (0-8): ").strip()
        
        if choice == '1':
            add_book()
        elif choice == '2':
            view_books()
        elif choice == '3':
            search_by_name()
        elif choice == '4':
            search_by_author()
        elif choice == '5':
            issue_book()
        elif choice == '6':
            return_book()
        elif choice == '7':
            view_available_count()
        elif choice == '8':
            max_copies_book()
        elif choice == '0':
            print("Dastur yakunlandi. Xayr!")
            break
        else:
            print("Xatolik: Noto'g'ri raqam kiritildi! Iltimos, 0 dan 8 gacha bo'lgan raqamlardan birini tanlang.")

if __name__ == "__main__":
    main()