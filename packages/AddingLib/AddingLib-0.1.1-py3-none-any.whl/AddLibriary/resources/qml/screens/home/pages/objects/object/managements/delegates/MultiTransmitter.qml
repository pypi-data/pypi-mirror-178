import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911" as Custom
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/"
import "qrc:/resources/qml/components/desktop"
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups

CommonPart {
    id: delegate

    property var hidden: true
    property var trueIndex: index
    property var currentTab: {
        if (appUser.company_id) return equipment.currentTab
        return hubSidebar.currentTab
    }
    property alias mtrDevices: mtrDevices

    height: currentTab == "DEVICES" ? mtrDevices.height + 104 + (!hidden && mtrDevices.model.length > 0) : 72

    flow.anchors {
        top: flow.parent.top
        topMargin: 48
        bottom: undefined
        bottomMargin: 0
    }


    Rectangle {
        id: resetPowerButton

        width: 40
        height: 24

        anchors {
            right: parent.right
            rightMargin: 64
            top: parent.top
            topMargin: 25
        }

        visible: device.fire_alarm_is_detected && !parent.rexDeleg
        opacity: enabled ? 1 : 0.4
        radius: 12
        color: "transparent"
        enabled: {
            if (!device.online || !hub.online) return false

            // wtf, no interconnect access info (company installer case)
            if (appUser.company_id && !hub.current_user.device_edit_access) return false

            return true
        }

        Image {
            width: 40
            height: 24

            source: "qrc:/resources/images/icons/ic-reset.png"
        }

        MouseArea {
            id: mouseArea

            anchors.fill: parent

            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor

            onClicked: {
                var popup = DesktopPopups.reset_power_for_fire_devices(function() {
                    app.hub_management_module.device_command(device, 22);
                },
                [{"id": device.device_id, "name": device.name, "wired_fire_devices": device.wired_fire_devices}],
                management)

                popup.onResetPower.connect(function() {
                    popup.destroy()
                    popup = null
                });
            }
        }

        states: State {
            name: "pressed"; when: mouseArea.pressed
            PropertyChanges { target: resetPowerButton; scale: 0.9 }
        }

        transitions: Transition {
            NumberAnimation { properties: "scale"; duration: 200; easing.type: Easing.InOutQuad }
        }
    }

    Item {
        width: parent.width
        height: 32

        anchors {
            top: parent.top
            topMargin: 72
        }

        visible: currentTab == "DEVICES"

        Rectangle {
            width: parent.width
            height: 1

            color: ui.colors.white
            opacity: 0.1
        }

        Custom.FontText {
            width: contentWidth
            height: contentHeight

            anchors {
                left: parent.left
                leftMargin: 16
                verticalCenter: parent.verticalCenter
            }

            text: tr.devices
            color: ui.colors.light3
            font.pixelSize: 12
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignLeft
        }

        Custom.FontText {
            width: contentWidth
            height: contentHeight

            anchors {
                right: triangleItem.left
                verticalCenter: parent.verticalCenter
            }

            text: device ? device.devices.length : ""
            color: ui.colors.light3
            font.pixelSize: 12
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignRight
        }

        Item {
            id: triangleItem

            width: 32
            height: 32

            anchors {
                right: parent.right
                rightMargin: 16
                verticalCenter: parent.verticalCenter
            }

            Custom.Triangle {
                anchors.centerIn: parent

                rotation: delegate.hidden ? 0 : 180
                colorTriangle: ui.colors.green1
            }
        }

        Custom.HandMouseArea {
            onClicked: {
                delegate.hidden = !delegate.hidden
            }
        }
    }
    ListView {
        id: mtrDevices

        width: parent.width
        height: parent.hidden ? 0 : contentHeight

        anchors.bottom: parent.bottom

        clip: true
        currentIndex: -1
        interactive: false
        boundsBehavior: Flickable.StopAtBounds
        model: device.devices

        onCurrentIndexChanged: {
            devicesItem.device = mtrDevices.model.get(mtrDevices.currentIndex)
            if (devicesItem.device == null) return
            deviceLoader.setSource(devicesItem.device.device_view, {"device": devicesItem.device})
        }

        delegate: Rectangle {
            id: deviceDelegateMt

            property var settingsVisible: !devices.withoutSettingIcon

            width: parent.width
            height: 72 + (mtrDevices.model.length - 1 != index)

            color: ui.colors.black

            Custom.RoundedRect {
                width: parent.width
                height: 72

                radius: 10
                color: mtrDevices.currentIndex == index ? ui.colors.black : ui.colors.dark3

                topRightCorner: false  // (index == 0 && devices.list.currentIndex == delegate.trueIndex) || (index > 0 && index - 1 == mtrDevices.currentIndex)
                bottomRightCorner: false  // (index < mtrDevices.model.length - 1 && index + 1 == mtrDevices.currentIndex)

                Custom.HandMouseArea {
                    onClicked: {
                        devices.resetMtrDevicesIndex()
                        devices.list.currentIndex = -1
                        mtrDevices.currentIndex = index
                    }
                }
            }

            IconSettings { visible: settingsVisible }

            Loader {
                id: loader

                width: parent.width
                height: 72

                anchors.top: parent.top

                source: device ? device.delegate : ""
            }
        }

        footer: Footer {
            id: mtrFooter

            height: visible ? 72 : 0

            roundRect.color: ui.colors.dark3

            btn {
                color: "white"
                text: tr.add_device

                backgroundItem {
                    color: ui.colors.dark4
                    border.width: 0
                }
            }

            Rectangle {
                id: spacer

                width: parent.width
                height: mtrFooter.visible ? 1 : 0

                color: ui.colors.black
            }

            topRightCorner: false  // mtrDevices.currentIndex == mtrDevices.model.length - 1 && mtrDevices.model.length > 0
            bottomRightCorner: {
                return false

                var prevDev = devices.list.model.get(devices.list.currentIndex - 1)
                return prevDev && prevDev.class_name == "multi_transmitter"
            }

            visible: {
                if (!hub.online) return false
                if (!device.online) return false
                if (hub.two_stage_arming_status) return false
                if (hub.state == "ARMED" || hub.state == "NIGHT_MODE") return false
                if (!hub.current_user.device_edit_access) return false
                return true
            }

            btn.onClicked: {
                if (!device.wired_inputs.length) {
                    Popups.text_popup(tr.wired_devices_max_title_copy, tr.wired_devices_max_description)
                    return
                }
                if (!rooms.length) {
                    Popups.text_popup(tr.please_add_at_least_one_room_first, tr.please_add_at_least_one_room_first_descr)
                    return
                }
                Popups.add_multitransmitter_device_popup(management.filtered_rooms.get_index(device), device)
            }
        }

        Connections {
            target: devices

            onResetMtrDevicesIndex: {
                mtrDevices.currentIndex = -1
            }
        }
    }
}

