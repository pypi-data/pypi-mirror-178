import QtQuick 2.12

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/components/911/DS3" as DS3


Parts.DeviceSettings {
    Parts.CommonSettings {
        settingsForChangesChecker: [
            currentProtection.checked,
            voltageProtection.checked,
            lockupRelayModeCombobox.currentIndex,
            lockupRelayTimeCombobox.currentIndex,
            contactNormStateCombobox.currentIndex,
            indication.checked,
            indicationBrightnessCombobox.currentIndex
        ]
        generateSettings: () => {
            var settings = {
                "common_part": {
                    "name": {"name": deviceName.atomInput.text.trim()},
                },
                "current_protection_enabled": currentProtection.checked,
                "voltage_protection_enabled": voltageProtection.checked,
                "lockup_relay_mode": lockupRelayModeCombobox.currentIndex + 1,
                "lockup_relay_time_seconds": parseInt(lockupRelayTimeCombobox.currentText),
                "contact_normal_state": contactNormStateCombobox.currentIndex + 1,
                "indication_enabled": indication.checked,
            }

            if (roomsCombobox.currentIndex >= 0) {
                var room = rooms.get_room(roomsCombobox.currentIndex)
                settings["common_part"]["room_id"] = room.id
            }

            if (device.brightness_available && indication.checked) {
                settings["indication_brightness"] = indicationBrightnessCombobox.currentIndex + 1
            }

            /*
            If <(0x46) lockupRelayMode> was changed -> save empty <(0x3F) armingActions>

            <(0x3F) armingActions> case:
            https://ajaxsystems.atlassian.net/wiki/spaces/AC/pages/1366393146/Scripts.Reaction.UX
            */
            if (lockupRelayModeCombobox.currentIndex != device.lockup_relay_mode - 1) {
                settings["actions_on_arming"] = []
            }

            // Temporary solution for backward compatibility
            settings["_refactored"] = true

            return settings
        }

        Column {
            width: parent.width

            enabled: devEnable

            DS3.SettingsContainer {
                Settings.CurrentProtection { id: currentProtection }
                Settings.VoltageProtection { id: voltageProtection }
                Settings.LockupRelayModeCombobox {
                    id: lockupRelayModeCombobox

                    visible: device.is_pulse_mode_available
                }
                Settings.LockupRelayTimeCombobox {
                    id: lockupRelayTimeCombobox

                    visible: lockupRelayModeCombobox.currentText == tr.pulse && device.is_pulse_mode_available
                }
                Settings.ContactNormStateCombobox {
                    id: contactNormStateCombobox

                    visible: device.is_pulse_mode_available
                }
                Settings.Indication { id: indication }
                Settings.IndicationBrightnessCombobox { id: indicationBrightnessCombobox }
            }

            DS3.Spacing {
                height: 24
            }

            DS3.SettingsContainer {
                Parts.ScenariosNav {
                    onEntered: {
                        var settings = {
                            "common_part": {
                                "name": {"name": deviceName.atomInput.text.trim()},
                            },
                            "current_protection_enabled": currentProtection.checked,
                            "voltage_protection_enabled": voltageProtection.checked,
                            "lockup_relay_mode": lockupRelayModeCombobox.currentIndex + 1,
                            "lockup_relay_time_seconds": parseInt(lockupRelayTimeCombobox.currentText),
                            "contact_normal_state": contactNormStateCombobox.currentIndex + 1,
                            "indication_enabled": indication.checked,
                            "_params": {
                                "alt_action_success": true,
                            },
                        }

                        if (roomsCombobox.currentIndex >= 0) {
                            var room = rooms.get_room(roomsCombobox.currentIndex)
                            settings["common_part"]["room_id"] = room.id
                        }

                        if (device.brightness_available && indication.checked) {
                            settings["indication_brightness"] = indicationBrightnessCombobox.currentIndex + 1
                        }

                        /*
                        If <(0x46) lockupRelayMode> was changed -> save empty <(0x3F) armingActions>

                        <(0x3F) armingActions> case:
                        https://ajaxsystems.atlassian.net/wiki/spaces/AC/pages/1366393146/Scripts.Reaction.UX
                        */
                        if (lockupRelayModeCombobox.currentIndex != device.lockup_relay_mode - 1) {
                            settings["actions_on_arming"] = []
                        }

                        app.hub_management_module.apply_update(management, device, settings)
                    }
                }
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
            }
            Parts.ManualNav {}
            Parts.BypassButtonNav {}
        }
    }
}