"""Demo ticket routing system using fictional employees and tickets."""
import csv
from pathlib import Path

TEAM = [
    {"name": "Anita", "skills": {"Salesforce", "Data"}, "workload": 2},
    {"name": "Rahul", "skills": {"ETL", "Data"}, "workload": 1},
    {"name": "Priya", "skills": {"Salesforce", "ETL"}, "workload": 0},
]

TICKETS = [
    {"id": "T001", "category": "Salesforce", "priority": "High"},
    {"id": "T002", "category": "ETL", "priority": "Medium"},
    {"id": "T003", "category": "Data", "priority": "Low"},
    {"id": "T004", "category": "Network", "priority": "High"},
    {"id": "T005", "category": "Salesforce", "priority": "Low"},
]

PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}


def assign_tickets(tickets, team):
    results = []
    for ticket in sorted(tickets, key=lambda t: (PRIORITY_ORDER.get(t["priority"], 99), t["id"])):
        eligible = [person for person in team if ticket["category"] in person["skills"]]
        if eligible:
            assignee = min(eligible, key=lambda person: (person["workload"], person["name"]))
            assignee["workload"] += 1
            assigned_to = assignee["name"]
            status = "Assigned"
        else:
            assigned_to = "Unassigned"
            status = "Manual review"
        results.append({**ticket, "assigned_to": assigned_to, "status": status})
    return results


def main():
    results = assign_tickets(TICKETS, TEAM)
    for ticket in results:
        print(f'{ticket["id"]} | {ticket["priority"]:6} | {ticket["category"]:10} | {ticket["assigned_to"]:10} | {ticket["status"]}')
    output = Path(__file__).with_name("assigned_tickets.csv")
    with output.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "category", "priority", "assigned_to", "status"])
        writer.writeheader()
        writer.writerows(results)
    print(f"\nSaved results to: {output}")


if __name__ == "__main__":
    main()
