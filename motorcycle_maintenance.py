from pymongo import MongoClient
from datetime import datetime
# Simple console application for managing motorcycle maintenance records.
# Uses MongoDB to store motorcycles and their maintenance history.

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["motorcycle_maintenance"]

while True:

    # Display program title
    print("****MOTORCYCLE MAINTENANCE HISTORY****")
    print()

    # Display motorcycles
    motorcycles = list(db.motorcycles.find().sort("motorcycle_brand", 1))
    number = 1
    for motorcycle in motorcycles:
        print(f"{number}.", motorcycle["motorcycle_brand"], motorcycle["motorcycle_model"], motorcycle["year_of_manufacture"])
        number += 1
    print()
    # Display main menu actions
    print("A. Add new motorcycle")
    print("E. Edit motorcycle")
    print("D. Delete motorcycle")
    print("B. Exit")
    print()

    choice_main = input("Select a motorcycle or an action: ")
    print()

    # Add new motorcycle
    if choice_main == "A":
        print("Add new motorcycle")
        brand = input("Motorcycle brand (0 to cancel): ")
        if brand == "0":
            print("Addition cancelled")
            print()
            continue

        model = input("Motorcycle model (0 to cancel): ")
        if model == "0":
            print("Addition cancelled")
            print()
            continue

        year = int(input("Year of manufacture (0 to cancel): "))
        if year == 0:
            print("Addition cancelled")
            print()
            continue

        db.motorcycles.insert_one({
            "motorcycle_brand": brand,
            "motorcycle_model": model,
            "year_of_manufacture": year
        })
        print("New motorcycle saved!")
        print()

    # Edit motorcycle
    elif choice_main == "E":
        edit = int(input("Enter motorcycle number to edit or 0 to cancel: "))
        if edit == 0:
            print("Edit cancelled")

        elif edit >= 1 and edit <= len(motorcycles):
            selected_motorcycle = motorcycles[edit - 1]

            brand = input("Motorcycle brand (0 to cancel): ")
            if brand == "0":
                print("Edit cancelled")
                print()
                continue

            model = input("Motorcycle model (0 to cancel): ")
            if model == "0":
                print("Edit cancelled")
                print()
                continue

            year = int(input("Year of manufacture (0 to cancel): "))
            if year == 0:
                print("Edit cancelled")
                print()
                continue

            db.motorcycles.update_one(
                {"_id": selected_motorcycle["_id"]},
                {"$set": {
                "motorcycle_brand": brand,
                "motorcycle_model": model,
                "year_of_manufacture": year
            }})
            print("Edited motorcycle saved!")
            print()
        else:
            print("!Please check your selection!")
            print()

    # Delete motorcycle
    elif choice_main == "D":
        print("Delete motorcycle")
        delete = int(input("Enter motorcycle number to delete or 0 to cancel: "))

        if delete == 0:
            print("Deletion cancelled")
            print()

        elif delete >= 1 and delete <= len(motorcycles):
            selected_motorcycle = motorcycles[delete - 1]

            confirmation = input(
                f"You are about to DELETE the motorcycle: "
                f"{selected_motorcycle['motorcycle_brand']} "
                f"{selected_motorcycle['motorcycle_model']} "
                f"{selected_motorcycle['year_of_manufacture']}\n"
                f"and its entire maintenance history. Do you want to continue? (Y/N): "
            )
            if confirmation == "Y":
                db.maintenance_records.delete_many({
                    "motorcycle_id": selected_motorcycle["_id"]
                })
                db.motorcycles.delete_one({"_id": selected_motorcycle["_id"]})
                print("Motorcycle deleted!")
                print()
            else:
                print("Deletion cancelled")
                print()
        else:
            print("!Please check your selection!")
            print()

    # Exit program
    elif choice_main == "B":
        print("Goodbye!")
        break

    # Display maintenance history of selected motorcycle
    elif choice_main.isdigit():
        number = int(choice_main)

        if number >= 1 and number <= len(motorcycles):
            selected = motorcycles[number - 1]

            while True:

                print(selected["motorcycle_brand"],selected["motorcycle_model"], selected["year_of_manufacture"], " | Service History |")
                print()
                records = list(db.maintenance_records.find({"motorcycle_id": selected["_id"]}).sort("date", -1))
                number2 =1
                for record in records:
                    print(f"{number2}. {record['date'].date()} | {record['mileage']}km")
                    for service in record["services"]:
                        print(f"   {service['name']}: {service['cost']:.2f}€")
                    number2 += 1
                    print()

                # Display maintenance menu
                print("A. Add new maintenance")
                print("E. Edit maintenance")
                print("D. Delete maintenance")
                print("B. Back to Main menu")
                print()
                choice2 = input("Select an action: ")

                # Add maintenance record
                if choice2 == "A":
                    print("Add new maintanance. Please enter the following details: ")
                    date = input("Maintenance date (YYYY-MM-DD or 0 to cancel): ")

                    if date == "0":
                        print("Addition cancelled")
                        print()
                        continue

                    mileage = int(input("Mileage (km, 0 to cancel): "))
                    if mileage == 0:
                        print("Addition cancelled")
                        print()
                        continue

                    name = input("Service name (0 to cancel): ")
                    if name == "0":
                        print("Addition cancelled")
                        print()
                        continue
                    cost = float(input("Cost (€, 0 to cancel): "))
                    if cost == 0:
                        print("Addition cancelled")
                        print()
                        continue

                    services = [{"name": name, "cost": cost}]
                    print()
                    another_service = input("Add another service task? (Y/N): ")

                    while another_service == "Y":
                        name = input("Service name: ")
                        cost = float(input("Cost (€): "))
                        services.append({"name": name, "cost": cost})
                        print()

                        another_service = input("Add another service task? (Y/N): ")

                    date = datetime.strptime(date, "%Y-%m-%d")

                    db.maintenance_records.insert_one({
                        "motorcycle_id": selected["_id"],
                        "services": services,
                        "mileage": mileage,
                        "date": date
                    })
                    print("New maintenance record saved!")
                    print()

                # Delete maintenance record
                elif choice2 =="D":
                    print("Delete maintenance")
                    delete = int(input("Enter maintenance record number to delete or 0 to cancel: "))

                    if delete == 0:
                        print("Deletion cancelled")

                    elif delete >= 1 and  delete <= len(records):
                        selected_record = records[delete - 1]
                        db.maintenance_records.delete_one({"_id": selected_record["_id"]})
                        print("Maintenance record deleted!")

                # Edit maintanance record
                elif choice2 == "E":
                    print("Edit maintenance")
                    edit = int(input("Enter maintenance record number to edit or 0 to cancel: "))

                    if edit == 0:
                        print("Edit cancelled")

                    elif edit >= 1 and edit <= len(records):
                        selected_record = records[edit - 1]

                        date = input("Maintenance date (YYYY-MM-DD or 0 to cancel): ")

                        if date == "0":
                            print("Edit cancelled")
                            print()
                            continue

                        mileage = int(input("Mileage (km, 0 to cancel): "))
                        if mileage == 0:
                            print("Edit cancelled")
                            print()
                            continue

                        name = input("Service name (0 to cancel): ")
                        if name == "0":
                            print("Edit cancelled")
                            print()
                            continue

                        cost = float(input("Cost (€, 0 to cancel): "))
                        if cost == 0:
                            print("Edit cancelled")
                            continue

                        services = [{"name": name, "cost":  cost}]
                        print()
                        another_service = input("Add another service task? (Y/N): ")
                        while another_service == "Y":
                            name = input("Service name: ")
                            cost = float(input("Cost (€): "))
                            services.append({"name": name, "cost": cost})
                            print()

                            another_service = input("Add another service task? (Y/N): ")
                        date = datetime.strptime(date, "%Y-%m-%d")
                        db.maintenance_records.update_one(
                            {"_id": selected_record["_id"]},
                            {"$set": {
                                "services": services,
                                "mileage": mileage,
                                "date": date
                            }})
                        print("Maintenance updated!")
                        print()

                    else:
                        print("!Please check your selection!")

                # Back to main menu
                elif choice2 == "B":
                    print()
                    break
        else:
            print("!Please check your selection!")

    else:
        print("!Please check your selection!")