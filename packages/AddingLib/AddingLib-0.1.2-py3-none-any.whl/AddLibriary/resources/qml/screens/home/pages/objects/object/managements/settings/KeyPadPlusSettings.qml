import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups


// Because we need to change header in child components
DS3Popups.PopupMultistep {
    id: popup

//  QObject of device
    property var device: null
//  Whether device is enabled
    property var devEnable: hub.online && device.online

    width: 500

    maxStepHeight: maxPopupHeight - headerItem.height - footerItem.height
    height: maxPopupHeight
    closePolicy: currentStepIndex == 0 ? Popup.CloseOnEscape : Popup.NoAutoClose

    firstStepComponent: Parts.CommonSettings {
        id: keyPadPlusSettings

        settingsForChangesChecker: [
            groupAssociatedCombobox.currentIndex,
            accessProfileCombobox.currentIndex,
            armInversion.checked,
            functionCombobox.currentIndex,
            fastArm.checked,
            blocking.checked,
            blockTimeCombobox.currentText,
            brightness.value,
            volume.value,
            ifSecurityButton.checked,
            nfcEnabled.checked
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
                "nfc_enabled": nfcEnabled.checked,
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

            if (armInversion.enabled) {
                settings["arm_inversion"] = armInversion.checked
            }

            // Temporary solution for backward compatibility
            settings["_refactored"] = true

            return settings
        }

        header: DS3.NavBarModal {
            headerText: keyPadPlusSettings.title
        }

        Column {
            width: parent.width

            enabled: devEnable

            DS3.SettingsContainer {
                Settings.GroupAssociatedCombobox { id: groupAssociatedCombobox }
                Settings.AccessProfileCombobox { id: accessProfileCombobox }
                Settings.Password { id: password }
                Settings.DuressPassword { id: duress_password }
                Settings.StarButtonFunctionCombobox {
                    id: functionCombobox

                    currentIndex: (device.star_button_function === 0) ?
                        device.star_button_function :
                        device.star_button_function - 1
                }
                Settings.FastArm { id: fastArm }
                Settings.Blocking { id: blocking }
                Settings.BlockTimeCombobox { id: blockTimeCombobox }
                Settings.Brightness { id: brightness }
                Settings.Volume {
                    id: volume

                    title: tr.volume_keypad_buttons
                }
                Settings.NfcEnabled { id: nfcEnabled }
                Settings.ArmInversion { id: armInversion }
            }

            DS3.Comment {
                text: hub.groups_enabled ? tr.arm_inversion_groups_info : tr.arm_inversion_info
                visible: armInversion.visible
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
                Parts.DeviceFormattingNav {}
            }
            Parts.ManualNav {}
            Parts.BypassButtonNav {}
        }
    }
}