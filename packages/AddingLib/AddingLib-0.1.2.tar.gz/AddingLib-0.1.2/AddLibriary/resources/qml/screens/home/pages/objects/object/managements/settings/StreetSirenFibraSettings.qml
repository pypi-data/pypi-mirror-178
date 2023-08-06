import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/components/911/DS3" as DS3


Parts.DeviceSettings {
    Parts.CommonSettings {
        settingsForChangesChecker: [
            groupAssociatedCombobox.currentIndex,
            alarmVolumeCombobox.currentIndex,
            alarmVolumeDurationSlider.value,
            blinkWhileArmed.checked,
            lightIndicationSiren.currentIndex,
            ifLidOpen.checked,
            ifPowerNotSufficient.checked
        ]
        generateSettings: () => {
            var volume_associated = {0: 32, 1: 29, 2: 18, 3: 1}

            var settings = {
                "common_part": {
                    "name": {"name": deviceName.atomInput.text.trim()},
                },
                "alarm_duration": alarmVolumeDurationSlider.value,
                "siren_volume_level": volume_associated[
                    device.mute_available ? alarmVolumeCombobox.currentIndex : alarmVolumeCombobox.currentIndex + 1
                ],
            }

            if (roomsCombobox.currentIndex >= 0) {
                var room = rooms.get_room(roomsCombobox.currentIndex)
                settings["common_part"]["room_id"] = room.id
            }

            if (hub.firmware_version_dec >= 206000 && hub.groups_enabled) {
                if (groupAssociatedCombobox.currentIndex == 0) {
                    settings["associated_group_id"] = "00000000"
                } else {
                    var group = groups.get(groupAssociatedCombobox.currentIndex - 1)
                    if (group) {
                        settings["associated_group_id"] = group.group_id
                    }
                }
            }

            if (lightIndicationSiren.visible) {
                settings["blink_while_armed"] = lightIndicationSiren.currentIndex + 1
            } else {
                settings["blink_while_armed"] = blinkWhileArmed.checked ? 2 : 1
            }

            settings["tamper_aware"] = ifLidOpen.checked ?
                "TAMPER_AWARE_ENABLED" :
                "TAMPER_AWARE_DISABLED"
            settings["lost_external_power_aware"] = ifPowerNotSufficient.checked ?
                "LOST_EXTERNAL_POWER_AWARE_ENABLED" :
                "LOST_EXTERNAL_POWER_AWARE_DISABLED"

            // Temporary solution for backward compatibility
            settings["_refactored"] = true

            return settings
        }

        Column {
            width: parent.width

            enabled: devEnable

            DS3.SettingsContainer {
                Settings.GroupAssociatedComboboxSirens { id: groupAssociatedCombobox }
                Settings.AlarmVolumeCombobox { id: alarmVolumeCombobox }
                Settings.AlarmVolumeDurationSlider { id: alarmVolumeDurationSlider }
                Settings.BlinkWhileArmed { id: blinkWhileArmed }
                Settings.LightIndicationSiren { id: lightIndicationSiren }
                Parts.SirenBeepsButtonNav { id: beepsButton }
            }

            DS3.Spacing {
                height: 24
            }

            DS3.TitleSection {
                isCaps: true
                forceTextToLeft: true
                isBgTransparent: true
                text: tr.activate_buzzer_fibra_siren_title
            }

            DS3.SettingsContainer {
                Settings.IfLidOpen { id: ifLidOpen }
                Settings.IfPowerNotSufficient { id: ifPowerNotSufficient }
            }

            DS3.Comment {
                text: tr.activate_buzzer_fibra_siren_descr
            }

            DS3.Spacing {
                height: 24
            }
        }

        DS3.SettingsContainer {
            Column {
                width: parent.width

                enabled: devEnable
                spacing: 1

                Parts.TestSignalLevelNav {
                    title: tr.fibra_signal_strength_test
                    icon: "qrc:resources/images/Athena/settings_icons/FibraSettings-L.svg"
                }
                Parts.TestVolumeNav {}
            }
            Parts.ManualNav {}
            Parts.BypassButtonNav {}
        }
    }
}
