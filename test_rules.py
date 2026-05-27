from app.rules.parliament_rules import (
    calculate_quorum,
    resolve_tie
)

print(
    calculate_quorum(
        total_members=100,
        connected_members=60,
        required_percent=50
    )
)

print(
    resolve_tie(
        yes_votes=10,
        no_votes=10,
        president_vote="yes"
    )
)