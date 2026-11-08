# SE3002 Assignment 2 — Student Registration Module

An in-memory Python student course-registration system used as the system under test for SE3002 Software Quality Engineering Assignment 2. Develop black-box and white-box tests with `pytest`, assess behavior against the specification, and report suspected defects. The supplied implementation is intentionally not guaranteed to be correct.

## Files
- `registration.py`: Python application to test.
- `REQUIREMENTS.md`: authoritative functional requirements, status strings, and sample scenarios.
- `requirements.txt`: dependencies for test development.
- `tests/`: black-box and white-box pytest suites.
- `docs/`: test designs, decision table, control-flow diagram, reports, and original SRS.

## Getting started
```bash
python -m pip install -r requirements.txt
python -c "from registration import Student, Course, register_course; print(register_course(Student('S001'), Course('CS201', 3, 30)))"
```

## Running tests and coverage
Run these commands from the repository root:
```bash
mkdir -p docs
python -m pytest tests/test_blackbox.py --cov=registration --cov-branch --cov-report=term-missing > docs/coverage_initial.txt 2>&1
python -m pytest tests/ --cov=registration --cov-branch --cov-report=term-missing > docs/coverage_final.txt 2>&1
```

The supplied implementation intentionally has defects, so failing tests are expected evidence and should not be hidden. The GitHub Actions workflow runs both suites, writes reports under `docs/`, uploads them as an artifact, and reports a failed check when pytest fails.

## Testing documents
- `docs/blackbox_test_design.xlsx`: equivalence-class and boundary test cases with observed results.
- `docs/decision_table.xlsx`: decision conditions, expected outcomes, and observed outcomes.
- `docs/cfg.png`: control-flow graph for `registration_decision`.
- `docs/testing_report.pdf`: coverage summary and known test failures.
- `docs/Student_Registration_SRS.docx`: supplied source specification.
- `docs/coverage_initial.txt` and `docs/coverage_final.txt`: raw pytest-cov output.

## Suggested student workflow
1. Derive ECP/BVA/decision table tests from `REQUIREMENTS.md` **without using implementation behavior as the expected result**.
2. Create `tests/test_blackbox.py`, execute the cases, and log suspected defects as GitHub Issues.
3. Inspect the code and develop `tests/test_whitebox.py` to exercise decisions, branches, conditions, and basis paths.
4. Document CFG and manual MC/DC pairs for a selected function.
5. Record failing tests faithfully. Do not alter expected results to force tests to pass.
6. Make any defect fixes in a separate Pull Request with accompanying regression tests.

Some tests may fail against the supplied source. This is intentional for the exercise.
