from file_verification_system.version import get_version

def version(request):
    return {'version': get_version()}