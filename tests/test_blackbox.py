"""Black-box tests for the Student Course Registration System.
Expected results are derived from the SRS (FR-01 to FR-15), not from source code.
Test IDs follow the A1 / A2 / A3 tables (TID-n, DT-nn); A4 adds state-change tests.
"""
import copy
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from registration import (  # noqa: E402
    Course,
    Student,
    check_credit_limit,
    prerequisites_satisfied,
    register_course,
    registration_decision,
    withdraw_course,
)


# ---------- baseline fixture ----------
def make_student(**kw):
    base = dict(student_id="S1", completed_courses=set(), current_credits=10,
                outstanding_dues=0, registered_courses=set())
    base.update(kw)
    return Student(**base)


def make_course(**kw):
    base = dict(code="C1", credit_hours=3, capacity=30, enrolled=10,
                prerequisites=set(), waitlist=[])
    base.update(kw)
    return Course(**base)


def snapshot(s, c):
    return copy.deepcopy((vars(s), vars(c)))


# ======================= Consolidated exact duplicates =======================
# One execution, several technique IDs (same function, same input state, same expected output).
@pytest.mark.trace("A1-TID-7", "A2-TID-7", "DT-06")
def test_dup_baseline_dues0_registered():  # FR-04, FR-08
    assert registration_decision(make_student(outstanding_dues=0), make_course()) == "REGISTERED"


@pytest.mark.trace("A2-TID-8", "DT-01")
def test_dup_dues1_dues_block():  # FR-04
    assert registration_decision(make_student(outstanding_dues=1), make_course()) == "DUES_BLOCK"


@pytest.mark.parametrize(
    "outstanding_dues,expected",
    [
        (0, "REGISTERED"),
        (1, "DUES_BLOCK"),
        (999, "DUES_BLOCK"),
        (1000, "DUES_BLOCK"),
        (1001, "DUES_BLOCK"),
    ],
)
def test_issue_3_positive_outstanding_dues_block_registration(
    outstanding_dues, expected
):
    assert registration_decision(
        make_student(outstanding_dues=outstanding_dues), make_course()
    ) == expected


@pytest.mark.trace("A2-TID-9", "DT-05")
def test_dup_full_course_waitlisted():  # FR-08
    assert registration_decision(make_student(), make_course(capacity=30, enrolled=30)) == "WAITLISTED"


# ======================= A1: Equivalence Class Partitioning =======================
@pytest.mark.trace("A1-TID-1")
def test_a1_tid_1():  # FR-01
    assert check_credit_limit(11, 3) is True


@pytest.mark.trace("A1-TID-2")
def test_a1_tid_2():  # FR-01
    assert check_credit_limit(17, 3) is False


@pytest.mark.trace("A1-TID-3")
def test_a1_tid_3():  # FR-02
    with pytest.raises(ValueError, match="Invalid current credits"):
        check_credit_limit(-17, 3)


@pytest.mark.trace("A1-TID-4")
def test_a1_tid_4():  # FR-03
    assert prerequisites_satisfied({"CS101"}, set()) is True


@pytest.mark.trace("A1-TID-5")
def test_a1_tid_5():  # FR-03
    assert prerequisites_satisfied(set(), {"CS101"}) is False


@pytest.mark.trace("A1-TID-6")
def test_a1_tid_6():  # FR-03
    assert prerequisites_satisfied({"CS101"}, {"CS101"}) is True


@pytest.mark.trace("A1-TID-8")
def test_a1_tid_8():  # FR-15
    with pytest.raises(ValueError, match="Invalid dues"):
        registration_decision(make_student(outstanding_dues=-100), make_course())


# ======================= A2: Boundary Value Analysis =======================
@pytest.mark.trace("A2-TID-1")
def test_a2_tid_1():  # FR-01
    assert check_credit_limit(0, 1) is True


@pytest.mark.trace("A2-TID-2")
def test_a2_tid_2():  # FR-01
    assert check_credit_limit(14, 4) is True


@pytest.mark.trace("A2-TID-3")
def test_a2_tid_3():  # FR-01
    assert check_credit_limit(18, 1) is False


@pytest.mark.trace("A2-TID-4")
def test_a2_tid_4():  # FR-02
    with pytest.raises(ValueError, match="Invalid current credits"):
        check_credit_limit(-1, 1)


@pytest.mark.trace("A2-TID-5")
def test_a2_tid_5():  # FR-02
    with pytest.raises(ValueError, match="Invalid course credits"):
        check_credit_limit(10, 0)


@pytest.mark.trace("A2-TID-6")
def test_a2_tid_6():  # FR-02
    with pytest.raises(ValueError, match="Invalid course credits"):
        check_credit_limit(10, 5)


@pytest.mark.trace("A2-TID-10")
def test_a2_tid_10():  # FR-15
    with pytest.raises(ValueError, match="Invalid capacity or enrollment"):
        registration_decision(make_student(), make_course(capacity=30, enrolled=31))


# ======================= A3: Decision Table =======================
# DT-01, DT-05, DT-06 are executed by the consolidated tests above.
def dt_case(dues=False, already=False, prereq=False, credit=False, full=False):
    s, c = make_student(), make_course()
    if dues:
        s.outstanding_dues = 1
    if already:
        s.registered_courses = {"C1"}
    if prereq:
        c.prerequisites = {"CS101"}
        s.completed_courses = set()
    if credit:
        s.current_credits = 16
    if full:
        c.enrolled = 30
    return s, c


DT_CASES = [
    ("DT-02", dict(already=True), "ALREADY_REGISTERED"),
    ("DT-03", dict(prereq=True), "PREREQUISITES_MISSING"),
    ("DT-04", dict(credit=True), "CREDIT_LIMIT"),
    ("DT-07", dict(dues=True, already=True, prereq=True, credit=True, full=True), "DUES_BLOCK"),
    ("DT-08", dict(dues=True, full=True), "DUES_BLOCK"),
    ("DT-09", dict(already=True, prereq=True, credit=True, full=True), "ALREADY_REGISTERED"),
    ("DT-10", dict(prereq=True, credit=True, full=True), "PREREQUISITES_MISSING"),
    ("DT-11", dict(credit=True, full=True), "CREDIT_LIMIT"),
]


@pytest.mark.parametrize(
    "flags,expected",
    [pytest.param(f, e, id=i, marks=pytest.mark.trace(i)) for i, f, e in DT_CASES],
)
def test_a3_decision_table(flags, expected):
    s, c = dt_case(**flags)
    assert registration_decision(s, c) == expected


# ======================= A4: State changes =======================
def test_a4_decision_does_not_mutate():  # FR-10
    s, c = make_student(), make_course()
    before = snapshot(s, c)
    registration_decision(s, c)
    assert snapshot(s, c) == before


def test_a4_register_success_updates_state():  # FR-11
    s, c = make_student(current_credits=10), make_course(credit_hours=3, enrolled=10)
    register_course(s, c)
    assert "C1" in s.registered_courses
    assert s.current_credits == 13
    assert c.enrolled == 11
    assert c.waitlist == []


def test_a4_register_waitlisted_appends_only():  # FR-12
    s, c = make_student(), make_course(enrolled=30)
    before_s = copy.deepcopy(vars(s))
    register_course(s, c)
    assert c.waitlist == ["S1"]
    assert c.enrolled == 30
    assert vars(s) == before_s


def test_a4_waitlist_no_duplicate():  # FR-12
    s, c = make_student(), make_course(enrolled=30, waitlist=["S1"])
    register_course(s, c)
    assert c.waitlist == ["S1"]


@pytest.mark.parametrize("flags", [
    dict(dues=True), dict(already=True), dict(prereq=True), dict(credit=True),
], ids=["DUES_BLOCK", "ALREADY_REGISTERED", "PREREQUISITES_MISSING", "CREDIT_LIMIT"])
def test_a4_failed_registration_no_state_change(flags):  # FR-12
    s, c = dt_case(**flags)
    before = snapshot(s, c)
    register_course(s, c)
    assert snapshot(s, c) == before


def test_a4_withdraw_enrolled():  # FR-13
    s = make_student(current_credits=13, registered_courses={"C1"})
    c = make_course(credit_hours=3, enrolled=11)
    assert withdraw_course(s, c) is True
    assert "C1" not in s.registered_courses
    assert s.current_credits == 10
    assert c.enrolled == 10


def test_a4_withdraw_not_registered_no_change():  # FR-14
    s, c = make_student(), make_course()
    before = snapshot(s, c)
    assert withdraw_course(s, c) is False
    assert snapshot(s, c) == before