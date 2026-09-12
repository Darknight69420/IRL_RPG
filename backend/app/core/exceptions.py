from fastapi import HTTPException, status

class GameRuleException(HTTPException):
    def __init__(self, error_code: str, message: str, status_code: int = status.HTTP_400_BAD_REQUEST, extra: dict = None):
        detail = {
            "error_code": error_code,
            "message": message
        }
        if extra:
            detail.update(extra)
        super().__init__(status_code=status_code, detail=detail)

class CooldownActiveException(GameRuleException):
    def __init__(self, remaining_seconds: int):
        super().__init__(
            error_code="COOLDOWN_ACTIVE",
            message="This habit was already completed today. Available again tomorrow.",
            status_code=status.HTTP_409_CONFLICT,
            extra={"cooldown_remaining_seconds": remaining_seconds}
        )

class LockedQuestStepException(GameRuleException):
    def __init__(self, required_step_order: int):
        super().__init__(
            error_code="LOCKED_STEP",
            message=f"Prerequisite Step {required_step_order} must be completed first.",
            status_code=status.HTTP_400_BAD_REQUEST,
            extra={"required_step_order": required_step_order}
        )

class ResourceNotFoundException(GameRuleException):
    def __init__(self, resource: str, resource_id: int):
        super().__init__(
            error_code="NOT_FOUND",
            message=f"{resource} with ID {resource_id} does not exist.",
            status_code=status.HTTP_404_NOT_FOUND
        )

class UnauthorizedResourceAccessException(GameRuleException):
    def __init__(self):
        super().__init__(
            error_code="FORBIDDEN",
            message="You do not have permission to access or modify this resource.",
            status_code=status.HTTP_403_FORBIDDEN
        )
