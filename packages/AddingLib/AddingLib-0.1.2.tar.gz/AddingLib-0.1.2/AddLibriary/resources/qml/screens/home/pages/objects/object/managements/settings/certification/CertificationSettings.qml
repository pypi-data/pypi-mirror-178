import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3

Item {
    id: certificationSettings

    Connections {
        target: app.hub_management_module

        onCertificationCommandSuccess: Popups.popupByPath(
            "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                title: tr.information,
                text: "Request sent."
            }
        )
    }

    DS3.NavBarModal {
        id: navBar

        headerText: "Certification"
        showCloseIcon: false
        isRound: false
    }

    DS3.ScrollView {
        id: userSettings

        anchors {
            fill: undefined
            top: navBar.bottom
            bottom: parent.bottom
            left: parent.left
            right: parent.right
        }

        padding: 24

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.InputSingleLine {
                id: masterKey

                width: parent.width

                atomInput {
                    label: "Master key"
                    required: true
                }
                regex: ui.regexes.certification_master_key
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            DS3.SettingsPickerTitleSecondary {
                id: certificationTypeCombobox

                model: [0, 1, 2, 3, 4]
                atomTitle.title: "Certification Name"
            }

            DS3.SettingsPickerTitleSecondary {
                id: certificationStepCombobox

                model: [0, 1, 2, 3, 4]
                atomTitle.title: "Certification Step"
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.ButtonContained {
            width: parent.width

            text: "Start"

            onClicked: app.hub_management_module.send_certification_step({
                "master_key": masterKey.atomInput.text,
                "certification_type": certificationTypeCombobox.currentIndex,
                "certification_step": certificationStepCombobox.currentIndex
            }, hub.id)
        }

        DS3.Spacing {
            height: 24
        }

        DS3.ButtonContained {
            width: parent.width

            text: "Stop"
            isAttention: true

            onClicked: app.hub_management_module.send_certification_step({
                "master_key": masterKey.atomInput.text,
                "certification_type": 0,
                "certification_step": 0
            }, hub.id)
        }
    }
}
