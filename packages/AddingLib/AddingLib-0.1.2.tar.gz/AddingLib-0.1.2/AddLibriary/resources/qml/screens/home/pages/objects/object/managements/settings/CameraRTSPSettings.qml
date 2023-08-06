import QtQuick 2.12

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups


Parts.DeviceSettings {
    Parts.CommonSettings {
        Connections {
            target: app

            onAltActionSuccess: {
                /* save base info -> altActionSuccess -> save stream data -> actionSuccess -> close popup */

                app.hub_management_module.edit_stream_data({
                    "hub_id": hub.hub_id,
                    "camera_id": device.id,
                    "service_id": device.service_id,
                    "service_type": device.stream_settings.service_type,
                    "stream_data_url": url.atomInput.text.trim(),
                })
            }
        }

        settingsForChangesChecker: [
            url.atomInput.text.trim(),
        ]

        generateSettings: () => {
            var settings = {
                "name": {"name": deviceName.atomInput.text.trim()},
                "_params": {
                    "alt_action_success": true,
                },
            }

            if (roomsCombobox.currentIndex >= 0) {
                settings["room_id"] = rooms.get_room(roomsCombobox.currentIndex).id
            }

            return settings
        }

        saveButtonClickCallback: () => {
            if (!deviceName.atomInput.text.trim()) {
                Popups.text_popup(tr.information, tr.the_name_field_cannot_be_blank)
                return
            }

            if (!url.atomInput.text.trim()) {
                Popups.text_popup(tr.information, tr.please_fill_in_all_of_the_required_fields)
                return
            }

            let settings = generateSettings()

            Popups.please_wait_popup()
            app.hub_management_module.apply_update(management, device, settings)
            return false
        }

        DS3.SettingsContainer {
            enabled: devEnable

            Settings.StreamUrl { id: url }
        }
    }
}
