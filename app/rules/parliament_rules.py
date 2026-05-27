from app.enums.system_enums import AttendanceStatus


def calculate_quorum(
    total_members,
    connected_members,
    required_percent
):

    if total_members == 0:
        return False

    percent = (
        connected_members / total_members
    ) * 100

    return percent >= required_percent


def can_user_vote(
    attendance_status,
    assembly_status
):

    if attendance_status != AttendanceStatus.CONNECTED:
        return False

    if assembly_status != "voting":
        return False

    return True


def can_change_vote(
    voting_open,
    allow_vote_change
):

    if not voting_open:
        return False

    return allow_vote_change


def resolve_tie(
    yes_votes,
    no_votes,
    president_vote
):

    if yes_votes != no_votes:
        return None

    return president_vote