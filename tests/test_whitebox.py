
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
)


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


@pytest.mark.trace("WB-01", "BP-03", "MC-2")
def test_wb_01_capacity_below_one_alone():
    with pytest.raises(ValueError, match="Invalid capacity or enrollment"):
        registration_decision(make_student(), make_course(capacity=0, enrolled=0))


@pytest.mark.trace("WB-02", "BP-04", "MC-3")
def test_wb_02_enrolled_below_zero_alone():
   
    with pytest.raises(ValueError, match="Invalid capacity or enrollment"):
        registration_decision(make_student(), make_course(capacity=30, enrolled=-1))


@pytest.mark.trace("WB-03")
def test_wb_03_current_credits_above_18():
    with pytest.raises(ValueError, match="Invalid current credits"):
        check_credit_limit(19, 1)


@pytest.mark.trace("WB-04")
def test_wb_04_current_credits_checked_before_course_credits():
    with pytest.raises(ValueError, match="Invalid current credits"):
        check_credit_limit(19, 0)


@pytest.mark.trace("WB-05")
def test_wb_05_dues_validated_before_capacity():
    with pytest.raises(ValueError, match="Invalid dues"):
        registration_decision(make_student(outstanding_dues=-1),
                              make_course(capacity=0, enrolled=0))


@pytest.mark.trace("WB-06")
def test_wb_06_waitlist_branch_student_already_listed():
    s, c = make_student(), make_course(capacity=30, enrolled=30, waitlist=["S1"])
    assert registration_decision(s, c) == "WAITLISTED"
    register_course(s, c)
    assert c.waitlist == ["S1"]
    assert c.enrolled == 30
    assert s.current_credits == 10
    assert s.registered_courses == set()

@pytest.mark.trace("WB-07")
def test_wb_07_dues_block_branch():
    s, c = make_student(outstanding_dues=5000), make_course()
    assert registration_decision(s, c) == "DUES_BLOCK"


@pytest.mark.trace("WB-08")
def test_wb_08_prerequisites_partially_completed():
    assert prerequisites_satisfied({"CS101"}, {"CS101", "MATH101"}) is False