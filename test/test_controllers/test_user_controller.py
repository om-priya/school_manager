from src.controllers.user_controller import AuthenticationController

# test authentication controller -- is logged in
# wrong cred, pending, deactive, ok


class TestUserController:
    def test_is_logged_in_valid_cred(self, monkeypatch):
        monkeypatch.setattr(
            "src.controllers.user_controller.validate.pattern_validator",
            lambda *args: "anbcde",
        )
        monkeypatch.setattr(
            "src.controllers.user_controller.validate.password_validator",
            lambda *args: "password",
        )
        monkeypatch.setattr(
            "src.controllers.user_controller.hash_password",
            lambda *args: "hashed_password",
        )
        monkeypatch.setattr(
            "src.controllers.user_controller.DatabaseAccess.execute_returning_query",
            lambda *args: [("dummy", "dummy", "active")],
        )
        actual_result = AuthenticationController.is_logged_in()

        assert actual_result == [True, "dummy", "dummy"]

    def test_is_logged_in_invalid_cred(self, monkeypatch):
        monkeypatch.setattr(
            "src.controllers.user_controller.validate.pattern_validator",
            lambda *args: "anbcde",
        )
        monkeypatch.setattr(
            "src.controllers.user_controller.validate.password_validator",
            lambda *args: "password",
        )
        monkeypatch.setattr(
            "src.controllers.user_controller.hash_password",
            lambda *args: "hashed_password",
        )
        monkeypatch.setattr(
            "src.controllers.user_controller.DatabaseAccess.execute_returning_query",
            lambda *args: [],
        )
        actual_result = AuthenticationController.is_logged_in()

        assert actual_result == [False, "", ""]

    def test_is_logged_in_pending_user(self, monkeypatch):
        monkeypatch.setattr(
            "src.controllers.user_controller.validate.pattern_validator",
            lambda *args: "anbcde",
        )
        monkeypatch.setattr(
            "src.controllers.user_controller.validate.password_validator",
            lambda *args: "password",
        )
        monkeypatch.setattr(
            "src.controllers.user_controller.hash_password",
            lambda *args: "hashed_password",
        )
        monkeypatch.setattr(
            "src.controllers.user_controller.DatabaseAccess.execute_returning_query",
            lambda *args: [("dummy", "dummy", "pending")],
        )
        actual_result = AuthenticationController.is_logged_in()

        assert actual_result == [False, "", ""]

    def test_is_logged_in_deactivated_user(self, monkeypatch):
        monkeypatch.setattr(
            "src.controllers.user_controller.validate.pattern_validator",
            lambda *args: "anbcde",
        )
        monkeypatch.setattr(
            "src.controllers.user_controller.validate.password_validator",
            lambda *args: "password",
        )
        monkeypatch.setattr(
            "src.controllers.user_controller.hash_password",
            lambda *args: "hashed_password",
        )
        monkeypatch.setattr(
            "src.controllers.user_controller.DatabaseAccess.execute_returning_query",
            lambda *args: [("dummy", "dummy", "deactivate")],
        )
        actual_result = AuthenticationController.is_logged_in()

        assert actual_result == [False, "", ""]

    def test_sign_up_principal(self, monkeypatch, mocker):
        options_pattern = [
            "dummy",
            "dummy",
            "dummy",
            "dummy",
            "dummy",
            "principal",
            "dummy",
        ]
        options_password = ["Ompriya@123"]
        monkeypatch.setattr(
            "src.controllers.user_controller.validate.pattern_validator",
            lambda *args: options_pattern.pop(0),
        )
        monkeypatch.setattr(
            "src.controllers.user_controller.validate.password_validator",
            lambda *args: options_password.pop(0),
        )
        mock_principal_obj = mocker.Mock()
        mocker.patch(
            "src.controllers.user_controller.Principal", return_value=mock_principal_obj
        )
        AuthenticationController.sign_up()

        mock_principal_obj.save_principal.assert_called_once()

    def test_sign_up_teacher(self, monkeypatch, mocker):
        options_pattern = [
            "dummy",
            "dummy",
            "dummy",
            "dummy",
            "dummy",
            "teacher",
            "dummy",
            "dummy",
        ]
        options_password = ["Ompriya@123"]
        monkeypatch.setattr(
            "src.controllers.user_controller.validate.pattern_validator",
            lambda *args: options_pattern.pop(0),
        )
        monkeypatch.setattr(
            "src.controllers.user_controller.validate.password_validator",
            lambda *args: options_password.pop(0),
        )
        mock_teacher_obj = mocker.Mock()
        mocker.patch(
            "src.controllers.user_controller.Teacher", return_value=mock_teacher_obj
        )
        AuthenticationController.sign_up()

        mock_teacher_obj.save_teacher.assert_called_once()
