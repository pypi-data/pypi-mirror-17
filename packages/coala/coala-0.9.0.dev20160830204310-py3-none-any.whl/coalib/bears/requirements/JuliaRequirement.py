from coalib.bears.requirements.PackageRequirement import PackageRequirement


class JuliaRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``, and helps specifying
    requirements from ``julia``, without using the manager name.
    """

    def __init__(self, package, version=""):
        """
        Constructs a new ``JuliaRequirement``, using the ``PackageRequirement``
        constructor.

        >>> pr = JuliaRequirement('Lint', '19.2')
        >>> pr.manager
        'julia'
        >>> pr.package
        'Lint'
        >>> pr.version
        '19.2'

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        """
        PackageRequirement.__init__(self, 'julia', package, version)
