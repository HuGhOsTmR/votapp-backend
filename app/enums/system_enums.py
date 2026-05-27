from enum import Enum


class AssemblyStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    OPEN = "open"
    DEBATE = "debate"
    VOTING = "voting"
    CLOSED = "closed"
    ARCHIVED = "archived"


class MotionStatus(str, Enum):
    PROPOSED = "proposed"
    ADMITTED = "admitted"
    DEBATE = "debate"
    AMENDMENT = "amendment"
    VOTING = "voting"
    APPROVED = "approved"
    REJECTED = "rejected"
    ARCHIVED = "archived"


class AttendanceStatus(str, Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    GRACE_PERIOD = "grace_period"
    REMOVED = "removed"


class VoteValue(str, Enum):
    YES = "yes"
    NO = "no"
    ABSTAIN = "abstain"
    BLANK = "blank"
    NULL = "null"

class UserRole(str, Enum):

    SUPER_ADMIN = "super_admin"

    ADMIN = "admin"

    PRESIDENT = "president"

    SECRETARY = "secretary"

    ASSEMBLY_MEMBER = "assembly_member"

    GUEST = "guest"