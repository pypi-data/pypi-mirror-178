import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.Popup {
    id: addHubPopup

//  Registration in progress
    property bool registrationInProgress: false

    width: 500

    hasCrossButton: !registrationInProgress
    title: tr.hub_registration
    defaultHeaderBackgroundColor: ui.ds3.bg.high
    closePolicy: registrationInProgress ? Popup.NoAutoClose : addHubPopup.defaultPolicy

    /* -------------------------------------------- */
    /* desktop tests */
    accessibleHeaderIcoName: "add-hub_close_button"
    accessibleHeaderTextName: "add-hub_header_text"
    accessibleHeaderAreaName: "add-hub_header"
    accessibleHeaderAreaDescription: "add-hub popup header grouping"
    /* -------------------------------------------- */

    Connections {
        target: app.hub_management_module

        onBindHubToUserFailed: {
            registrationInProgress = false
        }

        onBindHubToUserSuccess: {
            addHubPopup.close()
        }
    }

    DS3.Spacing {
        height: 24
    }

    DS3.SettingsContainer {
        DS3.InputSingleLine {
            id: nameField

            atomInput {
                label: tr.name
                placeholderText: tr.hub_name_tip_desktop
                maxByteLength: 24

                /* -------------------------------------------- */
                /* desktop tests */
                accessibleLabelName: "add-hub_name_text"
                accessibleFieldName: "add-hub_name_field"
                /* -------------------------------------------- */
            }
        }
    }

    DS3.Comment {
        text: tr.hub_name_registration_descr_desktop

        /* ------------------------------------------------ */
        /* desktop tests */
        Accessible.name: "add-hub_name_comment"
        Accessible.description: text
        Accessible.role: Accessible.Paragraph
        /* ------------------------------------------------ */
    }

    DS3.Spacing {
        height: 24
    }

    DS3.SettingsContainer {
        DS3.InputSingleLine {
            id: qrField

            signal reDashInsertResult(string new_text, int pos)

            onReDashInsertResult: {
                qrField.atomInput.text = new_text
                qrField.atomInput.cursorPosition = pos
            }

            Component.onCompleted: util.dashInsertResult.connect(reDashInsertResult)

            atomInput {
                label: tr.registration_key
                placeholderText: tr.twenty_symbols_hub_input
                maxByteLength: 23

                onTextEdited: {
                    util.dash_insert(qrField.atomInput.text, qrField.atomInput.cursorPosition)
                }

                /* -------------------------------------------- */
                /* desktop tests */
                accessibleLabelName: "add-hub_id_text"
                accessibleFieldName: "add-hub_id_field"
                /* -------------------------------------------- */
            }
            regex: ui.regexes.hub_qr
        }
    }

    DS3.Comment {
        text: tr.hub_qr_registration_descr_desktop

        /* ------------------------------------------------ */
        /* desktop tests */
        Accessible.name: "add-hub_id_comment"
        Accessible.description: text
        Accessible.role: Accessible.Paragraph
        /* ------------------------------------------------ */
    }

    DS3.Spacing {
        height: 24
    }

    footer: DS3.ButtonBar {
        id: addHubFooter

        enabled: qrField.atomInput.text.length == 23 && !!nameField.atomInput.text.trim()
        button {
            text: tr.next
            visible: !registrationInProgress
            onClicked: {
                registrationInProgress = true

                var settings = {}
                settings["hub_name"] = nameField.atomInput.text.trim()
                settings["hub_qr_code"] = qrField.atomInput.text
                app.hub_management_module.bind_hub_to_user(settings)
            }

            /* -------------------------------------------- */
            /* desktop tests */
            accessibleAreaName: "add-hub_next_button"
            /* -------------------------------------------- */
        }

        buttons: [
            DS3.ButtonProgress {
                width: parent.width

                visible: registrationInProgress
                textItem.text: tr.registering
            }
        ]
    }
}
