import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911" as Custom
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/"
import "qrc:/resources/qml/components/desktop"
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups
import "qrc:/resources/js/images.js" as Images

CommonPart {
    id: delegate

    property var hidden: true
    property var trueIndex: index
    property var currentTab: {
        if (appUser.company_id) return equipment.currentTab
        return hubSidebar.currentTab
    }

    height: currentTab == "DEVICES" || currentTab == "ROOMS" ? outputsList.height + 104 : 72

    flow.anchors {
        top: flow.parent.top
        topMargin: 48
        bottom: undefined
        bottomMargin: 0
    }

    Item {
        width: parent.width
        height: 32

        anchors {
            top: parent.top
            topMargin: 72
        }

        visible: currentTab == "DEVICES" || currentTab == "ROOMS"

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

            text: tr.outputs
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

            text: outputsList.model.length
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
        id: outputsList

        width: parent.width
        height: parent.hidden ? 0 : contentHeight

        anchors.bottom: parent.bottom

        clip: true
        spacing: 1
        currentIndex: -1
        interactive: false
        boundsBehavior: Flickable.StopAtBounds

        onCurrentIndexChanged: {
            try {devicesItem.device = device} catch (e) {}
            try {roomsDevicesItem.device = device} catch (e) {}
            deviceLoader.setSource(device.device_view, {"device": device})
        }

        model: [1, 2, 3, 4, 5, 6, 7, 8]

        delegate: Rectangle {
            id: outputDelegate

            width: parent.width
            height: 72

            color: ui.colors.black

            Custom.RoundedRect {
                width: parent.width
                height: 72

                radius: 10
                color: outputsList.currentIndex == index ? ui.colors.black : ui.colors.dark3

                Custom.HandMouseArea {
                    onClicked: {
                        devices.resetMtrDevicesIndex()
                        devices.list.currentIndex = -1
                        outputsList.currentIndex = index
                    }
                }
            }

            IconSettings {
                visible: deviceDelegate.settingsVisible
                bridgeOutput: model.modelData
            }

            Item {
                id: wrapper

                width: 72
                height: 72

                opacity: (device && hub && device.online && hub.online) ? 1 : 0.6

                Image {
                    anchors.centerIn: parent

                    sourceSize.width: 40
                    sourceSize.height: 40
                    source: Images.bridgeOutputs(device._get_alarm_type(model.modelData), "Small")
                }

                Column {
                    width: delegate.width - (deviceDelegate.settingsVisible ? 144 : 88)
                    spacing: 2

                    anchors {
                        left: wrapper.right
                        leftMargin: 12
                        verticalCenter: parent.verticalCenter
                    }

                    Custom.FontText {
                        id: deviceName

                        width: parent.width

                        anchors.left: parent.left

                        text: util.insert(tr.output_number, [model.modelData])
                        color: ui.colors.light1
                        textFormat: Text.AutoText
                        elide: Text.ElideRight
                    }

                    Custom.FontText {
                        id: outputType

                        width: parent.width

                        anchors.left: parent.left

                        text: {
                            return {"NOT_ASSIGNED_OUTPUT": tr.not_assigned_output,
                                    "INTRUSION_ALARM": tr.burglary_alarm,
                                    "FIRE_ALARM": tr.fire_alarm,
                                    "MEDICAL_ALARM": tr.medical_alarm,
                                    "PANIC_ALARM": tr.panic_alarm,
                                    "ALARM": tr.any_alarm,
                                    "MALFUNCTION": tr.malfunction,
                                    "BRIDGE_LOST_EXT_POWER": tr.lost_external_power_vhfBridge,
                                    "BRIDGE_BATTERY_LOW": tr.low_battery_vhfBridge,
                                    "HUB_LOST_EXT_POWER": tr.lost_external_power_hub,
                                    "HUB_BATTERY_LOW": tr.low_battery_hub,
                                    "TAMPER_ALARM": tr.lid_state,
                                    "SECURITY_STATE": tr.arm_disarm_state,
                                    "CONFIRMED_ALARM": tr.confirmed_intrusion_alarm,
                                    "CONFIRMED_HU_ALARM": tr.confirmed_hold_up_alarm,
                                    "BRIDGE_JWL_CONN_LOST": tr.connection_via_jeweller_lost_vhfBridge,
                                }[device._get_alarm_type(model.modelData)]
                        }
                        color: ui.colors.light1
                        textFormat: Text.AutoText
                        font.pixelSize: 12
                        opacity: 0.4
                        elide: Text.ElideRight
                    }
                }
            }
        }
        Connections {
            target: devices

            onResetMtrDevicesIndex: {
                outputsList.currentIndex = -1
            }
        }
    }
}

