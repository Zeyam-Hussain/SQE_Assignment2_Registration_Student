# SE3002 Assignment 2 — Student Registration Module

An in-memory Python student course-registration system used as the system under test for SE3002 Software Quality Engineering Assignment 2. Develop black-box and white-box tests with `pytest`, assess behavior against the specification, and report suspected defects. The supplied implementation is intentionally not guaranteed to be correct.

## Files
- `registration.py`: Python application to test.
- `REQUIREMENTS.md`: authoritative functional requirements, status strings, and sample scenarios.
- `requirements.txt`: dependencies for test development.

## Getting started
```bash
python -m pip install -r requirements.txt
python -c "from registration import Student, Course, register_course; print(register_course(Student('S001'), Course('CS201', 3, 30)))"
```

## Running tests and coverage
Run these commands from the repository root:
```bash
python -m pytest tests/test_blackbox.py --cov=registration --cov-branch --cov-report=term-missing > coverage_initial.txt 2>&1
python -m pytest tests/ --cov=registration --cov-branch --cov-report=term-missing > coverage_final.txt 2>&1
```

The supplied implementation intentionally has defects, so failing tests are expected evidence and should not be hidden. The GitHub Actions workflow runs both suites, uploads their output as an artifact, and reports a failed check when pytest fails.

## Suggested student workflow
1. Derive ECP/BVA/decision table tests from `REQUIREMENTS.md` **without using implementation behavior as the expected result**.
2. Create `tests/test_blackbox.py`, execute the cases, and log suspected defects as GitHub Issues.
3. Inspect the code and develop `tests/test_whitebox.py` to exercise decisions, branches, conditions, and basis paths.
4. Document CFG and manual MC/DC pairs for a selected function.
5. Record failing tests faithfully. Do not alter expected results to force tests to pass.
6. Make any defect fixes in a separate Pull Request with accompanying regression tests.

Some tests may fail against the supplied source. This is intentional for the exercise.
