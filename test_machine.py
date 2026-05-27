from app.state_machine.motion_machine import can_transition

from app.enums.system_enums import MotionStatus


print(
    can_transition(
        MotionStatus.PROPOSED,
        MotionStatus.ADMITTED
    )
)

print(
    can_transition(
        MotionStatus.PROPOSED,
        MotionStatus.VOTING
    )
)