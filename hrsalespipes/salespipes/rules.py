def is_associate_or_consultant_to_pipeline(user, pipeline):
    """Check if a user is an assocaite or consulant of a
    pipeline record.
    """
    # if user no employee assigned, then not allowed
    employee = getattr(object, 'as_employee', None)
    if not employee:
        return False

    if pipeline.job_candidate.associate_id:
        if pipeline.associate_id == employee.pk:
            return True

    if pipeline.job_candidate.consultant_id:
        if pipeline.consultant_id == employee.pk:
            return True

    return False


def is_allowed_to_view_or_edit_pipeline(user, pipeline):
    """Return True if user has permission to view all Pipelines
    OR is an associate or consultant of the Pipeline.
    """
    if user.has_perm('view_all_pipelines'):
        return True

    return is_associate_or_consultant_to_pipeline(user, pipeline)
