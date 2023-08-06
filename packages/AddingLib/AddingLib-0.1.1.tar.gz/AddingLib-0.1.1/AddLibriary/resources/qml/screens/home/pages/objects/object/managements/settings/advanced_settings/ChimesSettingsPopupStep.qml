import QtQuick 2.13
import QtQuick.Controls 2.12

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import 'qrc:/resources/js/desktop/popups.js' as Popups


DS3Popups.PopupStep {
    id: chimesSettingsPopupStep

    property var chimesItem: null
    property bool isMainSensorChecked: false
    property bool isExternalContactChecked: false

    Connections {
        target: app

        onActionSuccess: {
            changesChecker.changeInitialValues()
        }
    }

    height: maxStepHeight

    sidePadding: 24

    title: tr.chimes_title

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            notifyWithChimeSound.checked,
            ifExternalContactOpened.checked,
            sirenToneCombobox.currentIndex
        ]
    }

    DS3.Spacing {
        height: 24
    }

    Item {
        id: plugItem

        visible: {
            if (device.obj_type == "1d" && device.external_contact_alarm_mode == 2) return true
            if (device.obj_type == "0f" && !chimesItem.isMainSensorChecked && chimesItem.isExternalContactChecked && device.extra_contact_type == 2) return true
            return !chimesItem.isMainSensorChecked && !chimesItem.isExternalContactChecked
        }

        Column {
            width: 452

            DS3.Spacing {
                height: 104
            }

            Image {
                id: plugImage

                width: 136
                height: 136

                anchors.horizontalCenter: parent.horizontalCenter

                source: "qrc:/resources/images/desktop/chimes/ChimesPlug.svg"
            }

            DS3.Spacing {
                height: 24
            }

            DS3.Text {
                id: plugText

                width: parent.width - 40

                anchors.horizontalCenter: parent.horizontalCenter

                text: ["11", "1c", "7c"].includes(device.obj_type) ? // Transmitter, MTR, FMTR
                    tr.no_bistabile_endpoints_for_chimes :
                    tr.no_endpoints_for_chimes
                horizontalAlignment: Text.AlignHCenter
                style: ui.ds3.text.body.MRegular
            }
        }
    }

    Column {
        width: parent.width

        visible: !plugItem.visible

        DS3.TitleSection {
            text: tr.play_chimes_each_time

            isCaps: true
            forceTextToLeft: true
            isBgTransparent: true
        }

        DS3.SettingsContainer {
            width: parent.width

            enabled: devEnable

            DS3.SettingsSwitch {
                id: notifyWithChimeSound

                title: tr.if_opening_detected
                checked: chimesItem.chimeTriggers.includes("CHIME_REED")
                visible: chimesItem.isMainSensorChecked
            }

            DS3.SettingsSwitch {
                id: ifExternalContactOpened

                visible: chimesItem.isExternalContactChecked
                title: ["1d", "11"].includes(device.obj_type) ? tr.if_device_triggered : tr.if_external_contact_opened
                checked: {
                    let extraContact = device.obj_type === "1d" ? "CHIME_EXTRA_CONTACT_S2" : "CHIME_EXTRA_CONTACT"
                    return chimesItem.chimeTriggers.includes(extraContact)
                }
            }
        }

        DS3.Comment {
            width: parent.width

            text: tr.chime_device_settings_info
        }

        DS3.Spacing {
            height: 24
        }

        DS3.TitleSection {
            text: tr.sounds_title

            isCaps: true
            forceTextToLeft: true
            isBgTransparent: true
        }

        DS3.SettingsContainer {
            id: chimeSound

            enabled: devEnable

            DS3.SettingsPickerTitleSecondary {
                id: sirenToneCombobox

                model: [
                    tr.one_beep,
                    tr.two_beeps,
                    tr.three_beeps,
                    tr.four_beeps
                ]
                currentIndex: chimesItem.chimeSignal
                atomTitle.title: tr.ringtone

                onActivated: {
                    app.chimes_module.play(currentIndex)
                }
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            DS3.CommentImportant {
                atomTitle.title: tr.chime_activation
                atomTitle.subtitle: tr.chime_activation_device_info
                imageItem.visible: false
            }
        }
    }

    footer: DS3.ButtonBar {
        buttonText: tr.save
        hasBackground: true
        enabled: changesChecker.hasChanges

        button.onClicked: {
            let triggers = []
            if (notifyWithChimeSound.checked) triggers.push("CHIME_REED")
            if (ifExternalContactOpened.checked) triggers.push(device.obj_type === "1d" ? "CHIME_EXTRA_CONTACT_S2" : "CHIME_EXTRA_CONTACT")
            let settings = {
                "chime_triggers": triggers,
                "chime_signal": sirenToneCombobox.currentIndex,
            }

            Popups.please_wait_popup(app.actionSuccess, goBack)
            app.hub_management_module.apply_update(management, device, settings)
        }
    }
}