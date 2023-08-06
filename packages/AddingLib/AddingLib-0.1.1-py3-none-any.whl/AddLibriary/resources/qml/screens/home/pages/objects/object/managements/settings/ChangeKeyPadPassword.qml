import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups


DS3.Popup {
    id: popup

    property var device: null
    property bool force: false
    property bool isSaving: false

    Connections {
        target: app

        onActionFailed: isSaving = false
    }

    Connections {
        target: app.hub_management_module

        onPasswordChangeSuccess: popup.close()
        onKeypadCodeNotUnique: {
            isSaving = false
            DesktopPopups.popupByPath("qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                title: force ? tr.failed_save_duress_code_title : tr.failed_save_keypad_code_title,
                text: tr.failed_save_keypad_code_descr,
                firstButtonText: tr.i_will_check,
                isSecondButtonRed: true,
                secondButtonText: tr.rollback_changes,
                secondButtonIsOutline: true,
                secondButtonCallback: () => {
                    popup.close()
                },
                isVertical: true
            })
        }
        onKeypadPasswordTheSameAsDuress: {
            isSaving = false
            DesktopPopups.popupByPath("qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                title: force ? tr.failed_save_duress_code_title : tr.failed_save_keypad_code_title,
                text: tr.passcode_and_duress_code_should_not_match,
                firstButtonText: tr.i_will_check,
                isSecondButtonRed: true,
                secondButtonText: tr.rollback_changes,
                secondButtonIsOutline: true,
                secondButtonCallback: () => {
                    popup.close()
                },
                isVertical: true
            })
        }
    }

    width: 500

    header: DS3.NavBarModal {
        headerText: force ? tr.duress_code_new : tr.keypad_code_title

        onClosed: () => {
            popup.close()
        }
    }

    DS3.Spacing {
        height: 24
    }

    DS3.TitleUniversal {
        width: 420

        anchors.horizontalCenter: parent.horizontalCenter

        text: force ? tr.create_new_duress_code_title : tr.create_new_keypad_code_title
    }

    DS3.Text {
        width: 420

        anchors.horizontalCenter: parent.horizontalCenter

        color: ui.ds3.figure.secondary
        horizontalAlignment: Text.AlignHCenter
        style: ui.ds3.text.body.LRegular
        text: force ? tr.create_new_duress_code_descr : tr.create_new_keypad_code_descr
    }

    DS3.Spacing {
        height: 24
    }

    DS3.SettingsContainer {
        width: parent.width

        DS3.InputPassword {
            id: password

            validatorError: tr.try_again_the_passcode_must_be_4_to_6
            regex: ui.regexes.user_passcode
            atomInput {
                label: force ? tr.duress_code_new : tr.keypad_code_title
                placeholderText: "·····"
            }
        }

        DS3.InputPassword {
            id: repeat_password

            validatorError: tr.codes_not_match
            atomInput {
                label: force ? tr.confirm_duress_code_input_title : tr.keypad_code_confirmation
                placeholderText: "·····"

                onActiveFocusChanged: {
                    if (!atomInput.activeFocus) {
                        regex = Qt.binding(() => RegExp(password.atomInput.text))
                        checkValid()
                    }
                    else regex = ui.regexes.user_passcode
                }
            }
        }
    }

    DS3.Comment {
        width: parent.width

        text: tr.code_input_value_descr
    }

    DS3.Spacing {
        height: 24
    }

    DS3.ButtonContained {
        width: parent.width

        text: tr.save
        visible: !isSaving
        enabled: password.atomInput.text.length >= 4 && repeat_password.atomInput.text.length >= 4

        onClicked: {
            let passwordValid = password.checkValid()
            let repeatPasswordValid = repeat_password.checkValid()
            if (!passwordValid || !repeatPasswordValid) return

            isSaving = true
            app.hub_management_module.save_keypad_password(device, force, password.atomInput.text)
        }
    }

    DS3.ButtonProgress {
        anchors.horizontalCenter: parent.horizontalCenter

        visible: isSaving
        textItem.text: tr.saving
    }
}