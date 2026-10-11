import datetime
import os
import sqlite3

DB_NAME = "poultry_management_system.db"


def init_db():
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE,
            live_count INTEGER,
            mortality INTEGER,
            weight REAL,
            feed REAL,
            water REAL,
            temp REAL,
            humidity REAL,
            meds REAL,
            expenses REAL,
            sales REAL,
            notes TEXT
        )
    """)
  conn.commit()
  conn.close()


def main():
  init_db()
  while True:
    print("\n" + "=" * 65)
    print("   POULTRY FARM FINANCIAL & OPERATIONAL MANAGEMENT SYSTEM")
    print("=" * 65)
    print("1. Enter New Daily Record (12 Indicators)")
    print("2. View Summary Reports")
    print("3. Exit")

    choice = input("\nSelect an option (1-3): ").strip()

    if choice == "1":
      print("\n--- Daily Data Entry ---")
      default_date = datetime.date.today().strftime("%Y-%m-%d")
      record_date = (
          input(f"Date (YYYY-MM-DD) [Press Enter for {default_date}]: ").strip()
          or default_date
      )

      try:
        live_count = int(input("1. Live Birds Count: "))
        mortality = int(input("2. Daily Mortality Count: "))
        weight = float(input("3. Average Weight (kg): "))
        feed = float(input("4. Daily Feed Consumed (kg): "))
        water = float(input("5. Daily Water Consumed (liters): "))
        temp = float(input("6. Temperature (°C): "))
        humidity = float(input("7. Relative Humidity (%): "))
        meds = float(input("8. Medication Cost: "))
        expenses = float(input("9. Operational Expenses: "))
        sales = float(input("10. Daily Sales Revenue: "))
        notes = input("11. Administrative Notes: ").strip()

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            """
                    INSERT OR REPLACE INTO records (
                        date, live_count, mortality, weight, feed, water, temp, humidity, meds, expenses, sales, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
            (
                record_date,
                live_count,
                mortality,
                weight,
                feed,
                water,
                temp,
                humidity,
                meds,
                expenses,
                sales,
                notes,
            ),
        )
        conn.commit()
        conn.close()
        print("✅ Record successfully saved to database!")
      except ValueError:
        print("❌ Error: Please enter valid numbers.")

    elif choice == "2":
      conn = sqlite3.connect(DB_NAME)
      cursor = conn.cursor()
      cursor.execute("SELECT * FROM records ORDER BY date ASC")
      rows = cursor.fetchall()
      conn.close()

      if not rows:
        print("\n📭 No records found yet.")
      else:
        print(f"\n--- Total Records ({len(rows)} Days) ---")
        total_feed = sum(r[5] for r in rows)
        total_mortality = sum(r[3] for r in rows)
        total_sales = sum(r[11] for r in rows)
        total_costs = sum(r[9] + r[10] for r in rows)
        print(f"• Total Feed Used: {total_feed:,.2f} kg")
        print(f"• Total Mortality: {total_mortality} birds")
        print(f"• Total Sales: {total_sales:,.2f}")
        print(f"• Total Costs: {total_costs:,.2f}")

    elif choice == "3":
      print("\nExiting system. Good luck!")
      break
    else:
      print("❌ Invalid choice. Please choose 1, 2, or 3.")

    input("\n[Press Enter to continue...]")


if __name__ == "__main__":
  main()