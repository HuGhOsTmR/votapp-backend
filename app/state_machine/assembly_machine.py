from app.enums.system_enums import AssemblyStatus


ALLOWED_TRANSITIONS = {
    AssemblyStatus.DRAFT: [
        AssemblyStatus.SCHEDULED
    ],

    AssemblyStatus.SCHEDULED: [
        AssemblyStatus.OPEN
    ],

    AssemblyStatus.OPEN: [
        AssemblyStatus.DEBATE,
        AssemblyStatus.CLOSED
    ],

    AssemblyStatus.DEBATE: [
        AssemblyStatus.VOTING,
        AssemblyStatus.CLOSED
    ],

    AssemblyStatus.VOTING: [
        AssemblyStatus.DEBATE,
        AssemblyStatus.CLOSED
    ],

    AssemblyStatus.CLOSED: [
        AssemblyStatus.ARCHIVED
    ],

    AssemblyStatus.ARCHIVED: []
}


def can_transition(current, target):

    allowed = ALLOWED_TRANSITIONS.get(
        current,
        []
    )

    return target in allowed