def is_associate_or_consultant_to_pipeline(user, pipeline):
    """Check if a user is an assocaite or consulant of a
    pipeline record.
    """
    # if user no employee assigned, then not allowed
    employee = getattr(user, 'as_employee', None)
    if not employee:
        return False

    associate_id = pipeline.job_candidate.associate_id
    if associate_id:
        print(associate_id, employee.pk)
        if associate_id == employee.pk:
            return True

    consultant_id = pipeline.job_candidate.consultant_id
    if consultant_id:
        print(consultant_id, employee.pk)
        if consultant_id == employee.pk:
            return True

    return False


def is_allowed_to_view_or_edit_pipeline(user, pipeline):
    """Return True if user has permission to view all Pipelines
    OR is an associate or consultant of the Pipeline.
    """
    if user.has_perm('view_all_pipelines'):
        return True

    return is_associate_or_consultant_to_pipeline(user, pipeline)
