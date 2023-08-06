import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/"

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/js/images.js" as Images
import "qrc:/resources/qml/components/911/DS" as DS
import "qrc:/resources/qml/components/911/DS3/" as DS3


AjaxPopup {
    id: popup

    width: 336
    height: 430

    modal: true
    focus: true

    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    property var management: null
    property var device: null
    property var hub_id: ""
    property var sideMargin: 24

    Rectangle {
        width: 336
        height: 430

        radius: 12
        color: ui.backgrounds.base

        DS3.NavBarModal {
            id: deleteDeviceBar
            headerText: tr.unpair_device
            onClosed: () => {
                popup.close()
            }

            /* -------------------------------------------- */
            /* desktop tests */
            accessibleIcoName: "delete-device_" + device.id + "_close_button"
            accessibleTextName: "delete-device_" + device.id + "_header_text"
            /* -------------------------------------------- */
        }

        Image {
            id: imageRect

            width: 128
            height: 128

            source: {
                if (device.obj_type == "26") {
                    return Images.get_image(device.wire_input_type != 2 ? "26-wired-intrusion" : "26-wired-tamper", "Medium")
                }
                if (device.obj_type == "1d") {
                    return Images.get_image(device.obj_type, "Medium", device.input_type, device.custom_alarm_available_v2 ? device.custom_alarm_S2 : device.custom_alarm)
                }
                if (device.obj_type != "28") {
                    return Images.get_image(device.obj_type, "Medium", device.color, "TAMPER_ALARM", device.subtype)
                }
                return Images.get_image(device.device_type != 2 ? "28-keypad-yavir" : "28-reader-yavir", "Medium")
            }

            anchors {
                top: deleteDeviceBar.bottom
                topMargin: sideMargin + 8
                horizontalCenter: parent.horizontalCenter
            }

            /* ---------------------------------------------------- */
            /* desktop tests */
            Accessible.name: "delete-device_" + device.id + "_image"
            Accessible.description: source
            Accessible.role: Accessible.Graphic
            /* ---------------------------------------------------- */
        }

        DS3.Text {
            id: deviceNameLabel

            style: ui.ds3.text.body.MRegular
            text: device.name
            horizontalAlignment: Text.AlignHCenter

            anchors {
                top: imageRect.bottom
                topMargin: 16
                horizontalCenter: parent.horizontalCenter
            }

            /* ---------------------------------------------------- */
            /* desktop tests */
            Accessible.name: "delete-device_" + device.id + "_name"
            Accessible.description: text
            Accessible.role: Accessible.Paragraph
            /* ---------------------------------------------------- */
        }

        DS3.Text {
            id: roomNameLabel

            horizontalAlignment: Text.AlignHCenter
            style: ui.ds3.text.body.SRegular
            text: device.room_name || ""
            color: ui.ds3.figure.nonessential

            anchors {
                top: deviceNameLabel.bottom
                horizontalCenter: parent.horizontalCenter
            }

            /* ---------------------------------------------------- */
            /* desktop tests */
            Accessible.name: "delete-device_" + device.id + "_room"
            Accessible.description: text
            Accessible.role: Accessible.Paragraph
            /* ---------------------------------------------------- */
        }

        DS3.Text {
            id: infoLabel

            width: parent.width - 24

            style: ui.ds3.text.body.SRegular
            text: util.insert(tr.you_are_about_to_delete_device_all_settings_will_be_erased_continue, [device.name])
            horizontalAlignment: Text.AlignHCenter
            wrapMode: Text.WordWrap
            color: ui.ds3.figure.nonessential

            anchors {
                top: roomNameLabel.bottom
                topMargin: 32
                horizontalCenter: parent.horizontalCenter
            }

            /* ---------------------------------------------------- */
            /* desktop tests */
            Accessible.name: "delete-device_" + device.id + "_warning"
            Accessible.description: text
            Accessible.role: Accessible.Paragraph
            /* ---------------------------------------------------- */
        }

        DS3.ButtonContained {
            id: deleteButton

            width: parent.width - sideMargin * 2

            anchors {
                bottom: parent.bottom
                bottomMargin: sideMargin
                horizontalCenter: parent.horizontalCenter
            }
            text: tr.delete

            onClicked: {
                Popups.please_wait_popup()

                var settings = {}
                if (device.obj_type == 25) {
                    app.hub_management_module.delete_camera(device, hub_id)
                } else if (device.obj_type == 26) {
                    // wired input
                    settings["external_contact_mode"] = 1
                    app.hub_management_module.apply_update(management, device, settings)
                } else if (device.obj_type == 27) {
                    // wired siren
                    settings["enabled"] = false
                    app.hub_management_module.apply_update(management, device, settings)
                } else if (device.obj_type == 28) {
                    // access control
                    settings["enabled"] = false
                    app.hub_management_module.apply_update(management, device, settings)
                } else if (device.obj_type == 29) {
                    app.hub_management_module.delete_access_key(device.id)
                } else {
                    app.hub_management_module.delete_device(device, hub_id)
                }
            }

            /* ---------------------------------------------------- */
            /* desktop tests */
            Accessible.name: "delete-device_" + device.id + "_button"
            Accessible.description: "<button enabled=" + Accessible.checkable + ">" + text + "</button>"
            Accessible.role: Accessible.Button
            Accessible.checkable: visible && enabled
            Accessible.onPressAction: {
                if (!Accessible.checkable) return
                deleteButton.clicked(true)
            }
            /* ---------------------------------------------------- */
        }
    }

    Connections {
        target: app

        onActionSuccess: {
            popup.close()
        }
    }
}