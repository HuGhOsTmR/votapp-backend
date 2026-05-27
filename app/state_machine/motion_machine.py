from app.enums.system_enums import MotionStatus


ALLOWED_TRANSITIONS = {

    MotionStatus.PROPOSED: [
        MotionStatus.ADMITTED,
        MotionStatus.REJECTED
    ],

    MotionStatus.ADMITTED: [
        MotionStatus.DEBATE
    ],

    MotionStatus.DEBATE: [
        MotionStatus.AMENDMENT,
        MotionStatus.VOTING
    ],

    MotionStatus.AMENDMENT: [
        MotionStatus.DEBATE,
        MotionStatus.VOTING
    ],

    MotionStatus.VOTING: [
        MotionStatus.APPROVED,
        MotionStatus.REJECTED
    ],

    MotionStatus.APPROVED: [
        MotionStatus.ARCHIVED
    ],

    MotionStatus.REJECTED: [
        MotionStatus.ARCHIVED
    ],

    MotionStatus.ARCHIVED: []
}


def can_transition(current, target):

    allowed = ALLOWED_TRANSITIONS.get(
        current,
        []
    )

    return target in allowed