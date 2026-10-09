import csv, os, re
from datetime import datetime

IN_FILE="stock_in.csv"
OUT_FILE="stock_out.csv"

if not os.path.exists(IN_FILE):
    with open(IN_FILE,'w',newline='') as f: csv.writer(f).writerow(["Date_Arrived","Item","Supplier_From","Qty","Buy_Price","Total_Cost"])
if not os.path.exists(OUT_FILE):
    with open(OUT_FILE,'w',newline='') as f: csv.writer(f).writerow(["Date_Sold","Item","Qty_Sold","Sell_Price_Each","Total_For","Customer"])

def must_input(prompt):
    while True:
        s=input(prompt).strip()
        if s: return s
        print("! Must enter value, cannot be empty")

def get_number(prompt):
    while True:
        s=input(prompt).strip()
        if not s:
            print("! Must enter number")
            continue
        m=re.findall(r"[\d.]+",s)
        if m:
            try:
                v=float(m[0])
                if v>0: return int(v) if v.is_integer() else v
            except: pass
        print("! Invalid, enter number e.g. 5")

def add_stock():
    date=input("Date arrived [Enter=today]: ").strip() or datetime.now().strftime("%Y-%m-%d")
    item=must_input("Item name: ").lower()
    supplier=must_input("From where: ")
    qty=get_number("Qty bought: ")
    buy=get_number("Buying price each: ")
    with open(IN_FILE,'a',newline='') as f: csv.writer(f).writerow([date,item,supplier,qty,buy,qty*buy])
    print(f"✓ Saved {qty} {item} from {supplier}")

def sell_stock():
    date=input("Date sold [Enter=today]: ").strip() or datetime.now().strftime("%Y-%m-%d")
    item=must_input("Item name: ").lower()
    qty=get_number("Qty sold: ")
    sell=get_number("Sold for each: ")
    cust=must_input("Customer: ")
    with open(OUT_FILE,'a',newline='') as f: csv.writer(f).writerow([date,item,qty,sell,qty*sell,cust])
    print(f"✓ Sold {qty} {item} to {cust} for {qty*sell}")

def delete_last():
    print("\nWhat to delete?")
    print("1=Last Stock IN 2=Last Sale OUT")
    c=input("Choose: ").strip()
    file=IN_FILE if c=="1" else OUT_FILE if c=="2" else None
    if not file: return
    with open(file,'r') as f: rows=list(csv.reader(f))
    if len(rows)<=1:
        print("No data to delete")
        return
    print(f"Deleting: {rows[-1]}")
    confirm=input("Type YES to confirm: ").strip()
    if confirm.upper()=="YES":
        with open(file,'w',newline='') as f:
            csv.writer(f).writerows(rows[:-1])
        print("✓ Deleted last entry")
    else:
        print("Cancelled")

def dashboard():
    bought,sold,buy_p,sell_p={},{},{},{}
    try:
        with open(IN_FILE) as f:
            for r in csv.DictReader(f):
                k=r['Item'].lower()
                bought[k]=bought.get(k,0)+float(r['Qty'])
                buy_p[k]=float(r['Buy_Price'])
    except: pass
    try:
        with open(OUT_FILE) as f:
            for r in csv.DictReader(f):
                k=r['Item'].lower()
                sold[k]=sold.get(k,0)+float(r['Qty_Sold'])
                sell_p[k]=float(r['Sell_Price_Each'])
    except: pass
    print("\n--- STOCK | PROFIT / LOSS ---")
    if not bought:
        print("No stock yet")
        return
    for it,b in bought.items():
        s=sold.get(it,0)
        rem=b-s
        bp=buy_p.get(it,0)
        sp=sell_p.get(it,0)
        profit=(sp-bp)*s if s>0 and sp>0 else 0
        status="PROFIT" if profit>0 else "LOSS" if profit<0 else "NO SALE YET"
        print(f"{it.upper()}: Bought {b} | Sold {s} | REMAIN {rem}")
        print(f" Buy@{bp} Sell@{sp} -> {status} {profit} KES")
        if rem<5 and rem>0: print(f" ⚠ LOW STOCK! Only {rem} left")
        print("")
    print("-----------------------------")

while True:
    print("\n1=Add Stock 2=Sell 3=Show Remaining+Profit/Loss 4=Delete Last Entry 5=Exit")
    c=input("Choose: ").strip()
    if c=="1": add_stock()
    elif c=="2": sell_stock()
    elif c=="3": dashboard()
    elif c=="4": delete_last()
    elif c=="5": break
    else: print("Choose 1-5 only")