# models.py
import math

class Subject:
    def __init__(self, name: str, total_classes_held: int, classes_attended: int, min_required_percentage: float = 75.0):
        self.name = name
        self.total_classes_held = total_classes_held
        self.classes_attended = classes_attended
        self.min_required_percentage = min_required_percentage

    def get_current_percentage(self) -> float:
        if self.total_classes_held == 0:
            return 100.0
        return (self.classes_attended / self.total_classes_held) * 100.0

    def get_remaining_safe_cuts(self) -> int:
        min_req_decimal = self.min_required_percentage / 100.0
        max_total_allowed = self.classes_attended / min_req_decimal
        safe_cuts = math.floor(max_total_allowed - self.total_classes_held)
        return max(0, safe_cuts)
    def calculate_recovery_path(self) -> int:
        if self.get_current_percentage() >= self.min_required_percentage:
            return 0
        
        min_req_decimal = self.min_required_percentage / 100.0
        required_classes = (min_req_decimal * self.total_classes_held - self.classes_attended) / (1.0 - min_req_decimal)
        return math.ceil(required_classes)

class LeaveEvent:
    def __init__(self, event_name: str, missed_classes_count: dict):
        self.event_name = event_name
        self.missed_classes_count = missed_classes_count

class RiskAnalyzer:
    def __init__(self):
        self.subjects = {}
        self.planned_leaves = []

    def add_subject(self, subject: Subject):
        self.subjects[subject.name] = subject

    def add_leave_event(self, leave_event: LeaveEvent):
        self.planned_leaves.append(leave_event)

    def simulate_future_attendance(self) -> dict:
        simulation_results = {}
        for subject_name, subject in self.subjects.items():
            projected_total = subject.total_classes_held
            projected_attended = subject.classes_attended
            for leave in self.planned_leaves:
                if subject_name in leave.missed_classes_count:
                    projected_total += leave.missed_classes_count[subject_name]
            projected_percent = (projected_attended / projected_total) * 100.0 if projected_total > 0 else 100.0
            is_safe = projected_percent >= subject.min_required_percentage
            temp_sub = Subject(subject_name, projected_total, projected_attended, subject.min_required_percentage)
            simulation_results[subject_name] = {
                "current_percent": subject.get_current_percentage(),
                "projected_percent": projected_percent,
                "is_safe": is_safe,
                "safe_cuts_left_now": subject.get_remaining_safe_cuts(),
                "recovery_classes_needed": temp_sub.calculate_recovery_path()
            }
        return simulation_results

    