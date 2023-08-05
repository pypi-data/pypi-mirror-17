==========================================================================
django-unique-uploadto - Ensure no collisions for file uploads
==========================================================================

Use an instantiation of the ``unique_uploadto.UniqueFileName`` class to
prevent uploads from colliding with each other.
Creates a file with a timestamp and uuid in the filename.
Optionally accepts a prefix path and default file extension
