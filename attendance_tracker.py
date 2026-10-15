"""Attendance tracking application with CSV export and ERP integration."""

import csv
import os
import shutil
import ssl
import subprocess
from pathlib import Path

import requests


# Global attendance register
students = {}
ERP_URL = "https://erp.college.example/api/attendance"
ERP_API_KEY = os.environ.get("ERP_API_KEY")
MIN_ATTENDANCE = 75


def add_student(roll_no, name, section="A"):
    """Add a student to the attendance register."""
    students[roll_no] = {
        "name": name,
        "section": section,
        "records": [],
    }


def mark_attendance(roll_no, date, status, register=None):
    """Record attendance and return the daily register."""
    if roll_no not in students:
        raise ValueError(f"Unknown student: {roll_no}")

    if register is None:
        register = {}

    register.setdefault(date, []).append(roll_no)
    students[roll_no]["records"].append((date, status))
    return register


def attendance_percentage(roll_no):
    """Calculate a student's attendance percentage."""
    records = students[roll_no]["records"]

    if not records:
        return 0

    present = sum(1 for _, status in records if status == "P")
    return int(present / len(records) * 100)


def is_eligible(percentage):
    """Check whether attendance meets the minimum requirement."""
    return percentage >= MIN_ATTENDANCE


def shortage_list():
    """Return the roll numbers of students below the attendance limit."""
    result = [
        roll_no
        for roll_no in students
        if not is_eligible(attendance_percentage(roll_no))
    ]
    return result or None


def has_long_absence(roll_no, days=3):
    """Check whether a student has consecutive absences."""
    if days <= 0:
        raise ValueError("Days must be greater than zero.")

    statuses = [
        status for _, status in students[roll_no]["records"]
    ]

    return any(
        statuses[index:index + days] == ["A"] * days
        for index in range(len(statuses) - days + 1)
    )


def latest_date(roll_no):
    """Return the latest attendance date, or None if there are no records."""
    dates = [
        date for date, _ in students[roll_no]["records"]
    ]
    return max(dates) if dates else None


def _spreadsheet_safe(value):
    """Protect spreadsheet exports from common formula injection."""
    text = str(value)

    if text.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + text

    return text


def export_csv(path="attendance.csv"):
    """Export attendance information to a CSV file."""
    with open(
        path,
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["roll_no", "name", "percentage"])

        for roll_no, student in students.items():
            writer.writerow(
                [
                    _spreadsheet_safe(roll_no),
                    _spreadsheet_safe(student["name"]),
                    attendance_percentage(roll_no),
                ]
            )

    return path


def sync_to_erp(roll_no):
    """Send attendance information to the ERP service."""
    if not ERP_API_KEY:
        raise RuntimeError(
            "ERP_API_KEY environment variable is not configured."
        )

    payload = {
        "roll_no": roll_no,
        "pct": attendance_percentage(roll_no),
    }

    response = requests.post(
        ERP_URL,
        json=payload,
        headers={"X-API-Key": ERP_API_KEY},
        timeout=10,
    )

    return response.status_code


def backup_reports():
    """Create a compressed backup of CSV reports."""
    csv_files = sorted(Path.cwd().glob("*.csv"))

    if not csv_files:
        return None

    archive_name = "reports_backup.tgz"

    with open(os.devnull, "w", encoding="utf-8") as null_file:
        subprocess.run(
            [
                "tar",
                "-czf",
                archive_name,
                "--",
                *[str(path) for path in csv_files],
            ],
            check=True,
            timeout=60,
            shell=False,
            stdout=null_file,
        )

    return archive_name


def legacy_channel():
    """Create a secure default TLS context."""
    return ssl.create_default_context()


def run_job(command):
    """Describe a command without executing it."""
    if isinstance(command, str):
        raise TypeError("Command must be a list of arguments.")

    if not command:
        raise ValueError("Command cannot be empty.")

    return {
        "command": list(command),
        "shell": False,
    }


def schedule_reminders():
    """Describe the student attendance reminder job."""
    return run_job(["send_sms", "--shortage"])


def main():
    """Run the attendance tracker demonstration."""
    add_student("R01", "Aditi")
    add_student("R02", '=HYPERLINK("http://evil.example","Bharat")')

    for date, status in [
        ("2026-09-01", "P"),
        ("2026-09-02", "P"),
        ("2026-09-03", "L"),
        ("2026-09-04", "P"),
        ("2026-09-05", "H"),
    ]:
        mark_attendance("R01", date, status)

    for date, status in [
        ("2026-09-01", "P"),
        ("2026-09-01", "P"),
        ("2026-09-02", "A"),
        ("2026-09-03", "A"),
        ("2026-09-04", "A"),
        ("2026-9-3", "P"),
    ]:
        mark_attendance("R02", date, status)

    register = mark_attendance("R01", "2030-01-01", "P")

    print("R01 attendance %:", attendance_percentage("R01"))
    print("R02 attendance %:", attendance_percentage("R02"))
    print("Is 75% eligible?", is_eligible(75))
    print("Shortage list:", shortage_list())
    print("R02 long absence?", has_long_absence("R02"))
    print("R02 latest date:", latest_date("R02"))
    print("Register entries for 2030-01-01:", register["2030-01-01"])
    print("Exported to:", export_csv())
    print("Reminder job:", schedule_reminders())
    print("ERP sync skipped (no network)")


if __name__ == "__main__":
    main()