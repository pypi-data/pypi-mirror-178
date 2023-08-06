import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/popups/"
import "qrc:/resources/qml/screens/home/pages/objects/object/popups/parts" as Parts
import "qrc:/resources/js/images.js" as Images

AjaxPopup {
    id: popup

    property string state: ""
    property int roomIndex: 0
    property var from_devices: true
    property var management: null
    property var hub: management ? management.devices.hub : null

    width: application.width
    height: application.height

    focus: true
    modal: true

    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    Rectangle {
        id: popupBody

        width: addDevicesRow.width + 32
        height: 334

        anchors.centerIn: parent

        color: ui.ds3.bg.highest
        focus: true
        radius: 12

        AjaxPopupCloseHeader {
            id: closeItem
            label: tr.add_device

            /* -------------------------------------------- */
            /* desktop tests */
            accessibleIcoName: "add-device_close_button"
            accessibleTextName: "add-device_header_text"
            accessibleAreaName: "add-device_header_area"
            /* -------------------------------------------- */
        }

        Row {
            id: addDevicesRow

            anchors {
                top: closeItem.bottom
                left: parent.left
                topMargin: 20
                leftMargin: 16
            }
            spacing: 8

            Parts.AddDeviceTile {
                id: addDevice

                visible: hub.hub_type != "YAVIR"
                text: tr.add_device
                image: Images.get_image("02", "Large", "WHITE")

                /* ---------------------------------------------------- */
                /* desktop tests */
                accessibleImageName: "add-device_device_image"
                accessibleImageDescription: image

                accessibleTextName: "add-device_device_text"
                accessibleTextDescription: text

                accessibleAreaName: "add-device_device_area"
                accessibleAreaDescription: "click on add-device_device"
                /* ---------------------------------------------------- */
            }

            Parts.AddDeviceTile {
                id: addFibraDevice

                text: tr.add_bus_devices
                visible: hub.hub_type == "HUB_FIBRA"
                image: "qrc:/resources/images/Athena/fibra/FibraScanningImage.png"

                /* ---------------------------------------------------- */
                /* desktop tests */
                accessibleImageName: "add-device_bus_image"
                accessibleImageDescription: image

                accessibleTextName: "add-device_bus_text"
                accessibleTextDescription: text

                accessibleAreaName: "add-device_bus_area"
                accessibleAreaDescription: "click on add-device_bus"
                /* ---------------------------------------------------- */
            }

            Parts.AddDeviceTile {
                id: addCamera

                text: tr.add_camera
                image: "qrc:/resources/images/desktop/defaults/default-camera.png"

                /* ---------------------------------------------------- */
                /* desktop tests */
                accessibleImageName: "add-device_camera_image"
                accessibleImageDescription: image

                accessibleTextName: "add-device_camera_text"
                accessibleTextDescription: text

                accessibleAreaName: "add-device_camera_area"
                accessibleAreaDescription: "click on add-device_camera"
                /* ---------------------------------------------------- */
            }

            Parts.AddDeviceTile {
                id: addWireInput

                visible: (hub.hub_type == "YAVIR" || hub.hub_type == "YAVIR_PLUS") ? true : false
                enabled: popup.management.devices.available_wire_inputs.length
                opacity: enabled ? 1 : 0.4
                text: tr.add_wire_device
                image: "qrc:/resources/images/desktop/delegates/YavirWiredDevice/YavirWiredDeviceLarge.png"

                /* ---------------------------------------------------- */
                /* desktop tests */
                accessibleImageName: "add-device_wire-input_image"
                accessibleImageDescription: image

                accessibleTextName: "add-device_wire-input_text"
                accessibleTextDescription: text

                accessibleAreaName: "add-device_wire-input_area"
                accessibleAreaDescription: "click on add-device_wire-input"
                /* ---------------------------------------------------- */
            }

            Parts.AddDeviceTile {
                id: addWireSiren

                text: tr.add_wire_siren
                image: "qrc:/resources/images/desktop/delegates/YavirSiren/YavirSirenLarge.png"
                visible: hub.hub_type == "YAVIR" || hub.hub_type == "YAVIR_PLUS"
                enabled: popup.management.devices.available_wire_sirens.length
                opacity: enabled ? 1 : 0.4

                /* ---------------------------------------------------- */
                /* desktop tests */
                accessibleImageName: "add-device_wire-siren_image"
                accessibleImageDescription: image

                accessibleTextName: "add-device_wire-siren_text"
                accessibleTextDescription: text

                accessibleAreaName: "add-device_wire-siren_area"
                accessibleAreaDescription: "click on add-device_wire-siren"
                /* ---------------------------------------------------- */
            }

            Parts.AddDeviceTile {
                id: addWireKeypad

                text: tr.add_access_contol
                image: {
                    hub.firmware_version_dec < 208100 ?
                    "qrc:/resources/images/desktop/delegates/YavirReader/YavirReaderLarge.png" :
                    "qrc:/resources/images/desktop/delegates/YavirKeyPad/YavirKeyPadLarge.png"
                }
                visible: hub.hub_type == "YAVIR" || hub.hub_type == "YAVIR_PLUS"
                enabled: {
                    hub.firmware_version_dec >= 207002 ?
                    true :
                    devices.available_yavir_access_controls.length
                }
                opacity: enabled ? 1 : 0.4

                /* ---------------------------------------------------- */
                /* desktop tests */
                accessibleImageName: "add-device_wire-keypad_image"
                accessibleImageDescription: image

                accessibleTextName: "add-device_wire-keypad_text"
                accessibleTextDescription: text

                accessibleAreaName: "add-device_wire-keypad_area"
                accessibleAreaDescription: "click on add-device_wire-keypad"
                /* ---------------------------------------------------- */
            }

            Parts.AddDeviceTile {
                id: addAccessCard

                text: tr.add_access_device
                image: "qrc:/resources/images/desktop/delegates/PassTag/PassTagLarge.png"
                visible: popup.management.devices.fake_cards_block().count_keypads_with_nfc && popup.from_devices
                enabled: true
                opacity: enabled ? 1 : 0.4

                /* ---------------------------------------------------- */
                /* desktop tests */
                accessibleImageName: "add-device_card_image"
                accessibleImageDescription: image

                accessibleTextName: "add-device_card_text"
                accessibleTextDescription: text

                accessibleAreaName: "add-device_card_area"
                accessibleAreaDescription: "click on add-device_card"
                /* ---------------------------------------------------- */
            }
        }
    }
}