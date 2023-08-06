"""
This module introduce Runner class you can extend creating a new Runner based
on your language or your specification.
"""


from typing import Any


class Runner:
    """
    Extendible class to run a project.
    """

    def can_run(self) -> bool:
        """
        Run all necessary checks to ensure the applicability of this plugin.
        
        :return: True if checks are successful, false otherwise.
        :rtype: bool
        """
        raise NotImplementedError("Plugin.can_run")

    def run(self, inputs: Any = None, **kwargs) -> int:
        """
        Run the project using this Runner.

        :param inputs: Any input your runner could manage.
        :type inputs: Any
        
        :returns: Run result.
        :rtype: int

        .. warning:
            raise NotImplementedError when client didn't implement this function.
        """
        raise NotImplementedError("Plugin.run")
