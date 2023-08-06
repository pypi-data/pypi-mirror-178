import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts

Parts.DeviceSettings {
    Parts.CommonSettings {
        generateSettings: () => {
            var settings = {
                "name": {"name": deviceName.atomInput.text.trim()},
            }

            if (roomsCombobox.currentIndex >= 0) {
                settings["room_id"] = rooms.get_room(roomsCombobox.currentIndex).id
            }

            // Temporary solution for backward compatibility
            settings["_refactored"] = true

            return settings
        }
    }
}
