import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/js/images.js" as Images


DS3Popups.PopupStep {
    id: deviceStep

    default property alias content: contentContainer.data
//  Default settings. There are common settings that are used in all devices. Defined here to avoid repeated code.
    property var defaultSettings: {
        const settings = {"name": deviceName.atomInput.text.trim()}
        if (roomsCombobox.visible)
            settings["room_id"] = rooms.get_room(roomsCombobox.currentIndex).room_id
        return settings
    }
//  Footer button click callback. By, default send update object command.
    property var saveButtonClickCallback: (withClosing=true) => {
        if (!defaultSettings["name"])
            return Popups.text_popup(tr.information, tr.the_name_field_cannot_be_blank)

        let deviceSettings = generateSettings()

        if (!deviceSettings)
            return

        if (!!deviceSettings["_refactored"]) {
            delete deviceSettings["_refactored"]

            Popups.waitPopup(app.actionSuccess, withClosing ? close : undefined)
            app.hub_management_module.apply_update(management, device, deviceSettings)
            return true
        }

        let settings = Object.assign(defaultSettings, deviceSettings)

        Popups.waitPopup(app.actionSuccess, withClosing ? close : undefined)
        app.hub_management_module.update_object_settings(device, settings)
        return true
    }
//  Abstract function to collect device settings. Reimplement it in device.
    property var generateSettings: () => {return {}}
//  If custom device image component is needed
    property Component deviceImageComponent: DS3.DeviceHeaderInfo {
        imagePath: {
            if (device.obj_type == "28") {
                return Images.get_image(device.device_type != 2 ? "28-keypad-yavir" : "28-reader-yavir", "Large")
            }
            if (device.obj_type == "26") {
                return Images.get_image(device.input_is_tamper == 1 ? "26-wired-tamper" : "26-wired-intrusion", "Large")
            }
            if (device.obj_type == "1d") {
                return Images.get_image(device.obj_type, "Large", device.input_type, device.custom_alarm)
            }
            if (device.obj_type == "44") {
                return Images.get_image(device.obj_type, "Large", device.panel_color, null, device.subtype)
            }
            return Images.get_image(device.obj_type, "Large", device.color, "TAMPER_ALARM", device.subtype)
        }
    }
//  Reference to the custom deviceImage item
    readonly property alias deviceImageItem: deviceImageLoader.item
//  Reference to room combobox
    property alias roomsCombobox: roomsCombobox
//  Reference to name field
    property alias deviceName: deviceName
//  Reference to unpair button
    property alias unpairButton: unpairButton
//  List of settings for ChangesChecker
    property var settingsForChangesChecker: []
//  Alias for changesChecker
    property alias changesChecker: changesChecker

    sidePadding: 24
    title: device.name

    DS3.Spacing {
        height: 24
    }

    Loader {
        id: deviceImageLoader

        width: parent.width
        height: childrenRect.height

        sourceComponent: deviceImageComponent
    }

    DS3.Spacing {
        height: !!deviceImageComponent.height ? 24 : 0
    }

    DS3.SettingsContainer {
        width: parent.width

        enabled: devEnable

        Settings.Name { id: deviceName }
        Settings.Room { id: roomsCombobox }
    }

    DS3.Spacing {
        height: 24
    }

    Column {
        id: contentContainer

        width: parent.width
    }

    DS3.Spacing {
        height: 24
    }

    Parts.UnpairDevice { id: unpairButton }

    DS3.Spacing {
        height: 24
    }

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [deviceName.atomInput.text.trim(), roomsCombobox.currentIndex, ...settingsForChangesChecker]
    }

    footer: DS3.ButtonBar {
        id: saveButton

        width: parent.width

        enabled: changesChecker.hasChanges
        hasBackground: true
        button.text: tr.save

        button.onClicked: {
            saveButtonClickCallback()
        }
    }
}