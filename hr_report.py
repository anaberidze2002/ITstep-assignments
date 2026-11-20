from pathlib import Path
from datetime import datetime
import csv
from collections import Counter
import json
import os
import time

def folder():
    Path("output").mkdir(exist_ok=True)
    file_path = Path("data/employees.csv")
    if file_path.exists():
        print(file_path.resolve())
        return True
    else:
        print("ფაილი data/employees.csv არ არსებობს.")
        return False
    
def backup_file(src, dst):
    line_count = 0
    with open(src, "r", encoding="utf-8", newline="") as f_src, open(dst, "w", encoding="utf-8", newline="") as f_dst:
        for line in f_src:
            f_dst.write(line)
            line_count += 1
    return line_count

def log(message):
    log_path = Path("output/log.txt")
    timestamp = datetime.now().isoformat()
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} - {message}\n")
        
def lock_txt():
    lock_path = Path("output/lock.txt")
    try:
        with open(lock_path, "x", encoding="utf-8") as f:
            f.write(datetime.now().isoformat())
    except FileExistsError:
        print("ანგარიში უკვე შექმნილია")
        
def csv_reader():
    file_path = Path("data/employees.csv")
    with open(file_path, "r", encoding="utf-8", newline="") as f:
        all_rows = list(csv.reader(f))
    header = all_rows
    rows = all_rows[1:]
    print(header)
    for row in rows[:3]:
        print(row)
    print(len(rows))
    
def  csv_DictReader():
    file_path = Path("data/employees.csv")
    dept_count = {}
    dept_salary = {}
    active_employees = []
    active_count = 0
    inactive_count = 0
    with open(file_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for emp in reader:
            dept = emp["department"]
            salary = int(emp["salary"])
            if dept in dept_count:
                dept_count[dept] += 1
                dept_salary[dept] += salary
            else:
                dept_count[dept] = 1
                dept_salary[dept] = salary
            if emp["is_active"] == "True":
                active_count += 1
                active_employees.append((salary, emp["first_name"], emp["last_name"]))
            else:
                inactive_count += 1
    print("თანამშრომლების რაოდენობა დეპარტამენტების მიხედვით:")
    for dept in dept_count:
        print(dept, dept_count[dept])
    print("საშუალო ხელფასი დეპარტამენტების მიხედვით:")
    for dept in dept_salary:
        avg = round(dept_salary[dept] / dept_count[dept], 2)
        print(dept,avg)
    active_employees.sort(reverse=True)
    print("3 ყველაზე მაღალანაზღაურებადი აქტიური თანამშრომელი:")
    for salary, first_name, last_name in active_employees[:3]:
        print(first_name, last_name, salary)
    print("აქტიური:", active_count)
    print("არააქტიური:", inactive_count)
    return dept_count, dept_salary
def csv_DictWriter(dept_count, dept_salary):
    stats = []
    for dept in dept_count:
        avg = round(dept_salary[dept] / dept_count[dept], 2)
        stats.append((avg, dept, dept_count[dept]))
    stats.sort(reverse=True)
    out_path = Path("output/department_stats.csv")
    fieldnames = ["department", "employee_count", "avg_salary"]
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for avg, dept, count in stats:
            writer.writerow({
                "department":dept,
                "employee_count": count,
                "avg_salary": avg
            })
def csv_writer():
    in_path = Path("data/employees.csv")
    out_path = Path("output/high_earners.csv")
    high_earners = []
    with open(in_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for emp in reader:
            salary = int(emp["salary"])
            if emp["is_active"] == "True" and salary >= 5000:
                full_name = f"{emp['first_name']} {emp['last_name']}"
                high_earners.append([emp["id"], full_name, emp["department"], salary])
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "full_name", "department", "salary"])
        writer.writerows(high_earners)
    
def safe_read(path):
    try:
        with open(path, "r", encoding="utf-8",) as f:
            return f.read()
    except FileNotFoundError:
        log(f"FileNotFoundError: ფაილი {path} ვერ მოიძებნა")
        return ""
    except UnicodeDecodeError:
        log(f"unicodeDecodeError: ფაილში {path} კოდირების შეცდომაა")
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
def missing_txt():
    broken_path = Path("output/broken.txt")
    with open(broken_path, "wb",) as f:
        f.write(bytes([99, 97, 102, 233, 32, 255]))
    missing_text =safe_read(Path("output/missing.txt"))
    print("missing.txt:", repr(missing_text))
    broken_text =safe_read(broken_path)
    print("broken.txt:", broken_text)
    
def cities_txt():
    in_path = Path("data/employees.csv")
    out_path = Path("output/cities.txt")
    cities = Counter()
    with open(in_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for emp in reader:
            cities[emp["city"]] += 1
    top_3 = cities.most_common(3)
    with open(out_path, "w", encoding="utf-8") as f:
        for city, count in top_3:
            print(city, count)
            print(city, count, file=f)
            
def save_json_safe(data, path):
    tmp_path = Path(str(path) + ".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp_path, path)
    
class Timer:
    def __init__(self, name):
        self.name = name
    def __enter__(self):
        print(f"START {self.name}")
        self.start = time.perf_counter()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.perf_counter() - self.start
        if exc_type is None:
            print(f"FINISH {self.name} ({elapsed:.4f} წამი)")
        else:
            print(f"FAILED {self.name}: {exc_type.__name__}")
            return False

def with_timer():
    try:
        with Timer("test"):
            1 / 0
    except ZeroDivisionError:
        print("შეცდომაა, ნულზე გაყოფა")
        
def main():
    if not folder():
        return
    log("პროგრამა დაიწყო")
    
    copied_lines = backup_file(
        Path("data/employees.csv"),
        Path("output/employees.csv")
    )
    print("დაკოპირებული ხაზების რაოდენობა:", copied_lines)
    lock_txt()
    log("ნაწილი 1 დასრულდა")
    
    with Timer("CSV ანალიზი"):
        csv_reader()
        dept_count, dept_salary = csv_DictReader()
        dept_stats = csv_DictWriter(dept_count, dept_salary)
        csv_writer()
    log("ნაწილი 2 დასრულდა")
    
    missing_txt()
    cities_txt()
    save_json_safe(dept_stats, Path("output/summary.json"))
    log("ნაწილი 3 დასრულდა")
    with_timer()
    log("პროგრამა დასრულდა")
    
if __name__ == "__main__":
    main()