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
