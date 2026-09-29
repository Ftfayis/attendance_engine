# models.py
import math

class Subject:
    """
    Represents a single academic course.
    Calculates current attendance and how many future cuts are mathematically safe.
    """
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
        """
        Calculates how many consecutive classes can be skipped without 
        dropping below the minimum required percentage.
        """
        min_req_decimal = self.min_required_percentage / 100.0
        
        # Mathematical derivation to find maximum allowable total classes for current attended count
        max_total_allowed = self.classes_attended / min_req_decimal
        
        # Safe cuts are the difference between max allowed total classes and current total classes
        safe_cuts = math.floor(max_total_allowed - self.total_classes_held)
        
        return max(0, safe_cuts)

# --- Test the Logic ---
if __name__ == "__main__":
    # Example: A student attended 35 out of 40 classes.
    test_subject = Subject("Microcontrollers", 40, 35)
    print(f"Subject: {test_subject.name}")
    print(f"Current Attendance: {test_subject.get_current_percentage():.2f}%")
    print(f"Safe Cuts Remaining: {test_subject.get_remaining_safe_cuts()}")