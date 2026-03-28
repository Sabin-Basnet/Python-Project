import database

if __name__ == "__main__":
    print("Warning: This will delete ALL 10 years of price history from your database.")
    confirm = input("Type 'yes' to proceed: ")
    
    if confirm.lower() == 'yes':
        database.clear_daily_prices()
        print("✅ Database prices have been successfully wiped.")
    else:
        print("Cancelled. Database was left alone.")
