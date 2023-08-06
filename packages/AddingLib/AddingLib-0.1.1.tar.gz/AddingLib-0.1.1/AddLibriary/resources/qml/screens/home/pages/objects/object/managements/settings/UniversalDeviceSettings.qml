import QtQuick 2.12

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/components/911/DS3" as DS3


Parts.DeviceSettings {
    Parts.CommonSettings {
        function hex2bin(hex) {
            return (parseInt(hex, 16).toString(2)).padStart(32, "0");
        }

        function reverseString(str) {
            return str.split('').reverse().join('')
        }

        settingsForChangesChecker: [
            debugModeButton.checked,
            settingsField.atomInput.text
        ]
        generateSettings: () => {
            var settings = {
                "common_part": {
                    "name": {"name": deviceName.atomInput.text.trim()},
                },
                "device_debug_enabled": debugModeButton.checked,
            }

            if (roomsCombobox.currentIndex >= 0) {
                var room = rooms.get_room(roomsCombobox.currentIndex)
                settings["common_part"]["room_id"] = room.id
            }

            settings["settings"] = []
            var binNumber = reverseString(parseInt(settingsField.atomInput.text, 16).toString(2))
            for (var i = 1; i <= binNumber.length; i++) {
                if (Number(binNumber[i-1])) {
                    settings["settings"].push(i)
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
                DS3.SettingsSwitch {
                    id: debugModeButton

                    title: "Debug Mode"
                    checked: device.device_debug_enabled
                }

                Rectangle {
                    width: parent.width
                    height: settingsField.height + 20

                    color: ui.ds3.bg.highest

                    DS3.InputSingleLine {
                        id: settingsField

                        atomInput {
                            label: "Settings (hex)"
                            text: device.settingsHex
                            validator: RegExpValidator { regExp: /[0-9a-fA-F]+/ }

                            onTextChanged: {
                                atomInput.text = util.validator(atomInput.text, 8)
                            }
                        }
                    }

                    DS3.Comment {
                        width: parent.width - 32

                        anchors {
                            bottom: parent.bottom
                            horizontalCenter: parent.horizontalCenter
                        }

                        text: {
                            if (!settingsField.atomInput.text) return ""
                            var hex = hex2bin(settingsField.atomInput.text)
                            var new_hex = hex.slice(0, 8) + "  " + hex.slice(8, 16) + "  " + hex.slice(16, 24) + "  " + hex.slice(24, 32)
                            return new_hex
                        }
                    }
                }

                Rectangle {
                    width: parent.width
                    height: statusesField.height + 20

                    color: ui.ds3.bg.highest

                    DS3.InputSingleLine {
                        id: statusesField

                        atomInput {
                            label: "Statuses (hex)"
                            text: device.statusesHex
                            readOnly: true
                            required: false
                        }
                    }

                    DS3.Comment {
                        width: parent.width - 32

                        anchors {
                            bottom: parent.bottom
                            horizontalCenter: parent.horizontalCenter
                        }

                        text: {
                            if (!statusesField.atomInput.text) return ""
                            var hex = hex2bin(statusesField.atomInput.text)
                            var new_hex = hex.slice(0, 8) + "  " + hex.slice(8, 16) + "  " + hex.slice(16, 24) + "  " + hex.slice(24, 32)
                            return new_hex
                        }
                    }
                }

                Rectangle {
                    width: parent.width
                    height: alarmsField.height + 20

                    color: ui.ds3.bg.highest

                    DS3.InputSingleLine {
                        id: alarmsField

                        atomInput {
                            label: "Alarms (hex)"
                            text: device.alarmsHex
                            readOnly: true
                            required: false
                        }
                    }

                    DS3.Comment {
                        width: parent.width - 32

                        anchors {
                            bottom: parent.bottom
                            horizontalCenter: parent.horizontalCenter
                        }

                        text: {
                            if (!alarmsField.atomInput.text) return ""
                            var hex = hex2bin(alarmsField.atomInput.text)
                            var new_hex = hex.slice(0, 8) + "  " + hex.slice(8, 16) + "  " + hex.slice(16, 24) + "  " + hex.slice(24, 32)
                            return new_hex
                        }
                    }
                }
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            Column {
                width: parent.width

                enabled: devEnable
                spacing: 1

                Parts.TestSignalLevelNav {}
                Parts.TestZoneNav {}
            }
            Parts.BypassButtonNav {}
        }
    }
}