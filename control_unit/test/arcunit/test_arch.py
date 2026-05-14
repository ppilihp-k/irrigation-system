# ---------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from archunitpython import project_files

# ---------------------------------------------------------------------------------------------------------------------


class VerifyArchitecture(TestCase):
    def test_core_does_not_include_components(self) -> None:
        """Core does not import anything from components/."""
        self.assertEqual(
            0,
            len(
                project_files("control_unit/")
                .in_folder("**/core/**")
                .should_not()
                .depend_on_files()
                .in_folder("**/components/**")
                .check()
            ),
        )
        pass

    def test_components_do_not_include_core(self) -> None:
        """Components can import from control/interfaces/,
        but other than that are not allowed to import from control/.
        """
        self.assertEqual(
            0,
            len(
                project_files("control_unit/")
                .in_folder("**/components/**")
                .should_not()
                .depend_on_files()
                .in_folder("**/control/core.py")
                .check()
            ),
        )
        self.assertEqual(
            0,
            len(
                project_files("control_unit/")
                .in_folder("**/components/**")
                .should_not()
                .depend_on_files()
                .in_folder("**/control/handler/**")
                .check()
            ),
        )
        self.assertEqual(
            0,
            len(
                project_files("control_unit/")
                .in_folder("**/components/**")
                .should_not()
                .depend_on_files()
                .in_folder("**/control/logger/**")
                .check()
            ),
        )
        pass

    def test_queue_does_not_include(self) -> None:
        """Queue must not import anything from control/ or components/."""
        self.assertEqual(
            0,
            len(
                project_files("control_unit/")
                .in_folder("**/queue/**")
                .should_not()
                .depend_on_files()
                .in_folder("**/components/**")
                .check()
            ),
        )
        self.assertEqual(
            0,
            len(
                project_files("control_unit/")
                .in_folder("**/queue/**")
                .should_not()
                .depend_on_files()
                .in_folder("**/control/**")
                .check()
            ),
        )
        pass

    def test_config_does_not_include(self) -> None:
        """Config must not import any Modules."""
        self.assertEqual(
            0,
            len(
                project_files("control_unit/")
                .in_folder("**/config/**")
                .should_not()
                .depend_on_files()
                .in_folder("**/components/**")
                .check()
            ),
        )
        self.assertEqual(
            0,
            len(
                project_files("control_unit/")
                .in_folder("**/config/**")
                .should_not()
                .depend_on_files()
                .in_folder("**/control/**")
                .check()
            ),
        )
        self.assertEqual(
            0,
            len(
                project_files("control_unit/")
                .in_folder("**/config/**")
                .should_not()
                .depend_on_files()
                .in_folder("**/queue/**")
                .check()
            ),
        )
        pass

    pass


# ---------------------------------------------------------------------------------------------------------------------
