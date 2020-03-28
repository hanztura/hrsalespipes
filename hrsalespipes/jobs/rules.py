def is_allowed_to_edit_close_job(user, job):
    if job.status is None:
        return True

    # check if job is open
    if job.status.is_job_open:
        return True

    # check if user is allowed to bypass
    if user.has_perm('can_edit_closed_job'):
        return True

    return False


def is_associate_or_consultant(user, job_candidate):
    """Check if a user is an assocaite or consulant of a
    pipeline record.
    """
    # if user no employee assigned, then not allowed
    employee = getattr(user, 'as_employee', None)
    if not employee:
        return False

    associate_id = job_candidate.associate_id
    if associate_id:
        print(associate_id, employee.pk)
        if associate_id == employee.pk:
            return True

    consultant_id = job_candidate.consultant_id
    if consultant_id:
        print(consultant_id, employee.pk)
        if consultant_id == employee.pk:
            return True

    return False


def is_allowed_to_view_or_edit(user, job_candidate):
    """Return True if user has permission to view all Pipelines
    OR is an associate or consultant of the Pipeline.
    """
    if user.has_perm('view_all_job_candidates'):
        return True

    return is_associate_or_consultant(user, job_candidate)
