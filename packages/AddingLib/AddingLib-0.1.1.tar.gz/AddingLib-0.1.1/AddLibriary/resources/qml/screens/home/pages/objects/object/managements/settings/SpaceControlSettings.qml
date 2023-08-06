import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/components/911/DS3" as DS3


Parts.DeviceSettings {
    id: popup

    Parts.CommonSettings {
        property int savedFalsePressFilter

        Component.onCompleted: {
            savedFalsePressFilter = device.false_press_filter - 1
        }

        Connections {
            target: app

            onActionSuccess: {
                if (falsePressFilterCombobox.currentIndex != popup.savedFalsePressFilter) {
                    application.informationPopup({
                        0: tr.press_space_control_apply_settings,
                        1: tr.long_press_space_control_apply_settings,
                        2: tr.double_press_space_control_apply_setting
                    }[savedFalsePressFilter])
                }
            }
        }

        settingsForChangesChecker: [
            userAssociatedCombobox.currentIndex,
            groupAssociatedCombobox.currentIndex,
            panicButton.checked,
            ifPanic.checked,
            falsePressFilterCombobox.currentIndex
        ]
        generateSettings: () => {
            var settings = {
                "common_part": {
                    "name": {"name": deviceName.atomInput.text.trim()},
                },
                "panic_enabled": panicButton.checked,
                "siren_triggers": ifPanic.checked ? [1] : [],
                "false_press_filter": falsePressFilterCombobox.currentIndex + 1,
            }

            if (roomsCombobox.currentIndex >= 0) {
                var room = rooms.get_room(roomsCombobox.currentIndex)
                settings["common_part"]["room_id"] = room.id
            }

            if (hub.firmware_version_dec >= 207000 || (hub.firmware_version_dec >= 206000 && hub.groups_enabled)) {
                if (userAssociatedCombobox.currentIndex == 0) {
                    settings["associated_user_id"] = "00000000"
                } else {
                    settings["associated_user_id"] = users.normalized_users.user_ids[userAssociatedCombobox.currentIndex - 1]
                }
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

            // Temporary solution for backward compatibility
            settings["_refactored"] = true

            return settings
        }

        Column {
            width: parent.width

            enabled: devEnable

            DS3.SettingsContainer {
                Settings.GroupAssociatedCombobox { id: groupAssociatedCombobox }
                Settings.UserAssociated { id: userAssociatedCombobox }
                Settings.PanicButton { id: panicButton }
                Settings.FalsePressFilter { id: falsePressFilterCombobox }
            }

            DS3.Spacing {
                height: 24

                visible: ifPanic.visible
            }

            DS3.TitleSection {
                isCaps: true
                forceTextToLeft: true
                isBgTransparent: true
                text: tr.alert_with_a_siren
                visible: ifPanic.visible
            }

            DS3.SettingsContainer {
                Settings.IfPanic {
                    id: ifPanic

                    visible: panicButton.checked
                }
            }

            DS3.Spacing {
                height: 24
            }
        }

        DS3.SettingsContainer {
            Parts.ManualNav {}
            Parts.BypassButtonNav {}
        }
    }
}
