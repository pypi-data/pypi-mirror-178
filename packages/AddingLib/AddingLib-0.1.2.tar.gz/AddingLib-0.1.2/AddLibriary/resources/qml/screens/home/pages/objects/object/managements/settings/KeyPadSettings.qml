import QtQuick 2.12

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/components/911/DS3" as DS3


Parts.DeviceSettings {
    Parts.CommonSettings {
        settingsForChangesChecker: [
            groupAssociatedCombobox.currentIndex,
            accessProfileCombobox.currentIndex,
            functionCombobox.currentIndex,
            fastArm.checked,
            blocking.checked,
            blockTimeCombobox.currentText,
            brightness.value,
            volume.value,
            ifSecurityButton.checked
        ]
        generateSettings: () => {
            var settings = {
                "common_part": {
                    "name": {"name": deviceName.atomInput.text.trim()},
                },
                "star_button_function": parseInt(functionCombobox.currentIndex) + 1,
                "allow_fast_arming": fastArm.checked,
                "block_on_multiple_password_failures": blocking.checked,
                "time_to_block_on_multiple_password_failures_minutes": parseInt(blockTimeCombobox.currentText),
                "brightness_level": parseInt(brightness.value),
                "volume_level": parseInt(volume.value),
                "siren_triggers": ifSecurityButton.checked ? [1] : [],
            }

            if (roomsCombobox.currentIndex >= 0) {
                var room = rooms.get_room(roomsCombobox.currentIndex)
                settings["common_part"]["room_id"] = room.id
            }

            if (hub.firmware_version_dec >= 206000) {
                if (hub.groups_enabled) {
                    if (groupAssociatedCombobox.currentIndex == 0) {
                        settings["associated_group_id"] = "00000000"
                    } else {
                        var group = groups.get(groupAssociatedCombobox.currentIndex - 1)
                        if (group) {
                            settings["associated_group_id"] = group.group_id
                        }
                    }
                }
                if (accessProfileCombobox.currentIndex == 2) {
                    settings["access_profiles"] = [1, 2]
                } else if (accessProfileCombobox.currentIndex == 1) {
                    settings["access_profiles"] = [2]
                } else if (accessProfileCombobox.currentIndex == 0) {
                    settings["access_profiles"] = [1]
                }
            }

            // Temporary solution for backward compatibility
            settings["_refactored"] = true

            return settings
        }

        Column {
            width: parent.width

            enabled: devEnable

            DS3.SettingsContainer {
                Settings.GroupAssociatedCombobox { id: groupAssociatedCombobox }
                Settings.AccessProfileCombobox { id: accessProfileCombobox }
                Settings.Password { id: password }
                Settings.DuressPassword { id: duress_password }
                Settings.StarButtonFunctionCombobox { id: functionCombobox }
                Settings.FastArm { id: fastArm }
                Settings.Blocking { id: blocking }
                Settings.BlockTimeCombobox { id: blockTimeCombobox }
                Settings.Brightness { id: brightness }
                Settings.Volume {
                    id: volume

                    title: tr.volume_keypad_buttons
                }
            }

            DS3.Spacing {
                height: 24

                visible: ifSecurityButton.visible
            }

            DS3.TitleSection {
                visible: ifSecurityButton.visible
                isCaps: true
                forceTextToLeft: true
                isBgTransparent: true
                text: tr.alert_with_a_siren
            }

            DS3.SettingsContainer {
                Settings.IfSecurityButton { id: ifSecurityButton }
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

                Parts.TestSignalLevelNav {}
                Parts.TestSignalLostNav {}
            }
            Parts.ManualNav {}
            Parts.BypassButtonNav {}
        }
    }
}