import QtQuick 2.13
import QtQuick.Controls 2.12

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import 'qrc:/resources/js/desktop/popups.js' as Popups


DS3Popups.PopupStep {
    id: chimesSettingsPopupStep

    property var chimeTriggers: device.chime_triggers
    property var chimesItem: null

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
            sensorOneTriggered.checked,
            sensorTwoTriggered.checked,
            sensorThreeTriggered.checked,
            sirenToneCombobox.currentIndex
        ]
    }

    DS3.Spacing {
        height: 24
    }

    DS3.TitleSection {
        text: tr.play_chimes_each_time
        visible: wizardSection.visible
        isCaps: true
        forceTextToLeft: true
        isBgTransparent: true
    }

    DS3.SettingsContainer {
        id: chimeSettings

        width: parent.width

        enabled: devEnable

        DS3.SettingsSwitch {
            id: sensorOneTriggered

            visible: sensor1.visible
            checked: device.chime_triggers.includes("CHIME_EXTRA_CONTACT_S1")
            title: tr.if_sensor_one_triggered

            onSwitched: () => {
                checked = !checked

                if (checked) chimeTriggers.push("CHIME_EXTRA_CONTACT_S1")
                else {
                    let index = chimeTriggers.indexOf("CHIME_EXTRA_CONTACT_S1")
                    chimeTriggers.splice(index, 1)
                }
            }
        }

        DS3.SettingsSwitch {
            id: sensorTwoTriggered

            visible: sensor2.visible
            checked: device.chime_triggers.includes("CHIME_EXTRA_CONTACT_S2")
            title: chimesItem.sensorType === 0 || chimesItem.sensorType === 1 ? tr.if_device_triggered : tr.if_device_triggered

            onSwitched: () => {
                checked = !checked

                if (checked) chimeTriggers.push("CHIME_EXTRA_CONTACT_S2")
                else {
                    let index = chimeTriggers.indexOf("CHIME_EXTRA_CONTACT_S2")
                    chimeTriggers.splice(index, 1)
                }
            }
        }

        DS3.SettingsSwitch {
            id: sensorThreeTriggered

            visible: sensor3.visible
            checked: device.chime_triggers.includes("CHIME_EXTRA_CONTACT_S3")
            title: tr.if_sensor_three_triggered

            onSwitched: () => {
                checked = !checked

                if (checked) chimeTriggers.push("CHIME_EXTRA_CONTACT_S3")
                else {
                    let index = chimeTriggers.indexOf("CHIME_EXTRA_CONTACT_S3")
                    chimeTriggers.splice(index, 1)
                }
            }
        }
    }

    DS3.Comment {
        width: parent.width

        text: tr.chime_descr_eol_devices
    }

    DS3.Spacing {
        height: 24
        visible: siren_bits.visible
    }

    DS3.TitleSection {
        text: tr.sounds_title
        visible: wizardSection.visible

        isCaps: true
        forceTextToLeft: true
        isBgTransparent: true
    }

    DS3.SettingsContainer {
        id: chimeSound

        width: parent.width

        enabled: devEnable

        DS3.SettingsPickerTitleSecondary {
            id: sirenToneCombobox

            model: [
                tr.one_beep,
                tr.two_beeps,
                tr.three_beeps,
                tr.four_beeps
            ]
            currentIndex: device.chime_signal
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
            width: parent.width

            atomTitle.title: tr.chime_activation
            atomTitle.subtitle: tr.chime_activation_device_info
            imageItem.visible: false
        }
    }

    footer: DS3.ButtonBar {
        id: saveButton

        width: parent.width

        button.text: tr.save
        enabled: changesChecker.hasChanges
        hasBackground: true

        button.onClicked: {
            if ([2].includes(chimesItem.sensorType)) {
                chimeTriggers = chimeTriggers.filter(sensor => sensor !== 'CHIME_EXTRA_CONTACT_S3')
            }

            if ([0, 1].includes(chimesItem.sensorType)) {
                chimeTriggers = chimeTriggers.filter(
                    (sensor) => !['CHIME_EXTRA_CONTACT_S1', 'CHIME_EXTRA_CONTACT_S3'].includes(sensor)
                );
            }

            var settings = {
                "chime_triggers": chimeTriggers,
                "chime_signal": sirenToneCombobox.currentIndex,
            }

            Popups.please_wait_popup()
            app.hub_management_module.apply_update(management, device, settings)
        }
    }
}