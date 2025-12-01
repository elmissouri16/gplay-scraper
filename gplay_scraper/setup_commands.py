from setuptools.command.install import install


class InstallCommand(install):
    """Install command that provides install_layout to satisfy install_lib expectations."""

    user_options = install.user_options + [
        ("install-layout=", None, "Installation layout (unused; for compatibility)"),
        ("prefix-option=", None, "Prefix option (unused; for compatibility)"),
    ]

    def initialize_options(self) -> None:
        super().initialize_options()
        self.install_layout = None
        self.prefix_option = None

    def finalize_options(self) -> None:
        # Ensure attribute exists for install_lib finalize_options.
        if not hasattr(self, "install_layout"):
            self.install_layout = None
        if not hasattr(self, "prefix_option"):
            self.prefix_option = None
        super().finalize_options()
