# Core configuration package
# Cross-cutting infrastructure shared by the API, the Celery workers and the
# ad-hoc scripts: settings loading, DB engine/session, password and JWT helpers,
# anonymous device fingerprinting, and the Celery application.
# The package __init__ imports nothing on purpose: every module is imported
# explicitly where it is needed, so a missing optional dependency in one module
# (e.g. celery) cannot break the import of the others.

