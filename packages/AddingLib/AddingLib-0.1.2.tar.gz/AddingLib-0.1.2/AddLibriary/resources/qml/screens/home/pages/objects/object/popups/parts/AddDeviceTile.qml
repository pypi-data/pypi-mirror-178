import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/popups/"
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups
import "qrc:/resources/qml/components/911/DS3" as DS3

Item {

    property alias text: deviceType.text
    property alias image: deviceImage.source
    property alias selected: frame.border.width

    /* ---------------------------------------------------- */
    /* desktop tests */
    property var accessibleImageName: ""
    property var accessibleImageDescription: ""

    property var accessibleTextName: ""
    property var accessibleTextDescription: ""

    property var accessibleAreaName: ""
    property var accessibleAreaDescription: ""
    /* ---------------------------------------------------- */

    width: 180
    height: 250

    Rectangle {
        id: frame

        anchors.fill: parent

        clip: true
        color: ui.ds3.bg.high
        radius: 14
        border.color: ui.ds3.figure.interactive
        border.width: 0

        Image {
            id: deviceImage

            width: 128
            height: 128

            anchors {
                horizontalCenter: parent.horizontalCenter
                top: parent.top
                topMargin: 10
            }

            /* ---------------------------------------------------- */
            /* desktop tests */
            Accessible.name: accessibleImageName
            Accessible.description: accessibleImageDescription
            Accessible.role: Accessible.Graphic
            /* ---------------------------------------------------- */
        }

        DS3.Text {
            id: deviceType

            width: 120
            height: 35

            anchors {
                bottom: parent.bottom
                bottomMargin: 20
                horizontalCenter: parent.horizontalCenter
            }

            horizontalAlignment: Text.AlignHCenter
            style: ui.ds3.text.body.LRegular
            color: ui.ds3.figure.interactive

            /* ---------------------------------------------------- */
            /* desktop tests */
            Accessible.name: accessibleTextName
            Accessible.description: accessibleTextDescription
            Accessible.role: Accessible.Paragraph
            /* ---------------------------------------------------- */
        }
        MouseArea {
            id: addDeviceArea

            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor

            onEntered: {
                frame.border.width = 1
            }
            onExited: {
                frame.border.width = 0
            }

            onClicked: {
                if (!management.filtered_rooms.length) {
                    Popups.text_popup(tr.please_add_at_least_one_room_first, tr.please_add_at_least_one_room_first_descr)
                    return
                }
                if (deviceType.text == tr.add_access_device) {
                    var device = popup.management.devices.fake_cards_block()
                    if (!device.is_kpp_kpc_here) {
                        if (!device.is_kpp_here() && device.kpp_count && !device.kpc_count) {
                            Popups.text_popup(tr.turn_on_nfc_info, tr.turn_on_nfc_in_kpp)
                        } else if (!device.is_kpc_here() && device.kpc_count && !device.kpp_count) {
                            Popups.text_popup(tr.turn_on_nfc_info, tr.turn_on_nfc_in_kpc)
                        } else {
                            Popups.text_popup(tr.turn_on_nfc_info, tr.turn_on_nfc_in_kpp_kpc)
                        }
                    } else {
                        popup.close()
                        addAccessCardPopup("")
                    }
                    return
                }

                if (hub.groups_enabled && !groups.length) {
                    Popups.text_popup(tr.information, tr.please_add_at_least_one_group_first)
                    return
                }

                if (deviceType.text == tr.add_device) {
                    if (["SCAN_STARTED", "DEVICES_FOUND"].includes(hub.scan_status)) {
                        DesktopPopups.popupByPath("qrc:/resources/qml/screens/home/pages/objects/object/popups/Fibra_popups/FibraScanningInterruptPopup.qml", {"hub": hub})
                        return
                    }
                    if (hub.max_power_test_state == "TEST_IN_PROGRESS") {
                        DesktopPopups.popupByPath("qrc:/resources/qml/screens/home/pages/objects/object/popups/Fibra_popups/WireTestInterruptPopup.qml", {"hub": hub})
                        return
                    }
                    addDevicePopup(hub, roomIndex)
                }
                if (deviceType.text == tr.add_bus_devices) {
                    if (hub.max_power_test_state == "TEST_IN_PROGRESS") {
                        DesktopPopups.popupByPath("qrc:/resources/qml/screens/home/pages/objects/object/popups/Fibra_popups/WireTestInterruptPopup.qml", {"hub": hub})
                        return
                    }
                    if (hub.bus_status.includes("SHORT_CIRCUIT_PRESENT")) {
                        Popups.popupByPath("qrc:/resources/qml/screens/home/pages/objects/object/popups/Fibra_popups/AddFibraDeviceShortCircuitOnBus.qml")
                        return
                    }
                    addFibraDevicePopup(hub, roomIndex)
                }
                if (deviceType.text == tr.add_camera) { addCommonCameraPopup(roomIndex, management.filtered_rooms) }
                if (deviceType.text == tr.add_wire_device) { addWireInputPopup(roomIndex, popup.management) }
                if (deviceType.text == tr.add_wire_siren) { addWireSirenPopup(roomIndex, popup.management) }
                if (deviceType.text == tr.add_access_contol) { addYavirAccessControlPopup(roomIndex, popup.management) }
                popup.close()
            }
        }

        /* ---------------------------------------------------- */
        /* desktop tests */
        Accessible.name: accessibleAreaName
        Accessible.description: "<button enabled=" + Accessible.checkable + ">" + accessibleAreaDescription + "</button>"
        Accessible.role: Accessible.Button
        Accessible.checkable: visible && enabled
        Accessible.onPressAction: {
            if (!Accessible.checkable) return
            addDeviceArea.clicked(true)
        }
        /* ---------------------------------------------------- */
    }
}