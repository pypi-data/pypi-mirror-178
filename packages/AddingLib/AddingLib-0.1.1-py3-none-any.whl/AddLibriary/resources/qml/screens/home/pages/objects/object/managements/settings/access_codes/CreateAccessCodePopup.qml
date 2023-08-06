import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups


DS3.Popup {
    id: popup

    property bool isSaving: false

    Connections {
        target: app

        onActionFailed: isSaving = false
    }

    Connections {
        target: app.rpc.hubAccessCodes

        onAccessCodeAdded: popup.close()

        onAccessCodeNotUnique: {
            isSaving = false
            DesktopPopups.popupByPath("qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                title: tr.failed_save_access_code_title,
                text: tr.failed_save_access_code_descr,
                firstButtonText: tr.ok,
            })
        }

        onAccessCodeLimitExceeded: {
            isSaving = false
            DesktopPopups.popupByPath("qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                title: tr.access_codes_limit_exceeded_title,
                text: tr.access_codes_limit_exceeded_descr,
                firstButtonText: tr.ok,
            })
        }
    }

    width: 500

    header: DS3.NavBarModal {
        headerText: tr.access_code_title

        onClosed: () => {
            popup.close()
        }
    }

    DS3.Spacing {
        height: 24
    }

    DS3.SettingsContainer {
        width: parent.width

        DS3.InputSingleLine {
            id: name

            atomInput {
                label: tr.name
                placeholderText: tr.access_code_name_input

                onTextChanged: {
                    atomInput.text = util.validator(atomInput.text, 24)
                    return
                }
            }
        }
    }

    DS3.Comment {
        width: parent.width

        text: tr.access_code_name_descr
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
                label: tr.access_code_title
                placeholderText: "·····"
            }
        }

        DS3.InputPassword {
            id: repeat_password

            validatorError: tr.codes_not_match
            atomInput {
                label: tr.access_code_confirmation
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

        text: tr.add_code_button
        visible: !isSaving
        enabled: password.atomInput.text.length >= 4 &&
                 repeat_password.atomInput.text.length >= 4 &&
                 name.atomInput.text.length >= 1

        onClicked: {
            let passwordValid = password.checkValid()
            let repeatPasswordValid = repeat_password.checkValid()

            if (!passwordValid || !repeatPasswordValid) return

            isSaving = true
            context.createAccessCode(name.atomInput.text.trim(), password.atomInput.text)
        }
    }

    DS3.ButtonProgress {
        anchors.horizontalCenter: parent.horizontalCenter

        visible: isSaving
        textItem.text: tr.adding_access_code
    }
}