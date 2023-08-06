import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups


DS3.Popup {
    id: popup

    property var accessCode: null
    property bool duressPassword
    property string passwordFromInput: ""

    width: 500

    header: DS3.NavBarModal {
        headerText: duressPassword ? tr.duress_code_new : tr.access_code_title

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

        text: {
            if (duressPassword) return localDuressPassHashExist ?
                tr.update_duress_code_title :
                tr.enter_duress_code_title
            else return tr.update_access_code_title
        }
    }

    DS3.Text {
        width: 420

        anchors.horizontalCenter: parent.horizontalCenter

        color: ui.ds3.figure.secondary
        horizontalAlignment: Text.AlignHCenter
        style: ui.ds3.text.body.LRegular
        text: duressPassword ? tr.enter_duress_access_code_descr : tr.update_access_code_descr
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
                label: duressPassword ? tr.duress_code_new : tr.access_code_title
                placeholderText: "·····"
                text: passwordFromInput
            }
        }

        DS3.InputPassword {
            id: repeat_password

            validatorError: tr.codes_not_match
            atomInput {
                label: duressPassword ? tr.confirm_duress_code_input_title : tr.access_code_confirmation
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

        visible: localDuressPassHashExist && duressPassword && duressPasswordForSaving != "00000000000000000000"
    }

    DS3.SettingsContainer {
        width: parent.width

        DS3.ButtonRow {
            width: parent.width

            text: tr.delete_duress_code
            isDanger: true
            visible: localDuressPassHashExist && duressPassword && duressPasswordForSaving != "00000000000000000000"

            onClicked: {
                var deletePopup = DesktopPopups.popupByPath("qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                    title: tr.delete_duress_code_title,
                    text: tr.delete_duress_code_descr,
                    firstButtonText: tr.delete,
                    isFirstButtonRed: true,
                    firstButtonCallback: () => {
                        duressPasswordForSaving = "00000000000000000000"
                        localDuressPassHashExist = false
                        popup.close()
                    },
                    secondButtonText: tr.cancel,
                    secondButtonIsOutline: true,
                    isVertical: true,
                })
            }
        }
    }

    DS3.Spacing {
        height: 24
    }

    DS3.ButtonContained {
        width: parent.width

        text: tr.done
        enabled: password.atomInput.text.length >= 4 && repeat_password.atomInput.text.length >= 4

        onClicked: {
            let passwordValid = password.checkValid()
            let repeatPasswordValid = repeat_password.checkValid()

            if (!passwordValid || !repeatPasswordValid) return

            if (duressPassword) {
                duressPasswordForSaving = password.atomInput.text
                localDuressPassHashExist = true
            } else {
                passwordForSaving = password.atomInput.text
            }

            popup.close()
        }
    }
}