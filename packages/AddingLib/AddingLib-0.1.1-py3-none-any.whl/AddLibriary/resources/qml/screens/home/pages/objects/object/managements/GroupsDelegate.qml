import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
    property var settingsVisible: false

    Connections {
        target: groups.list

        onCurrentIndexChanged: {
            if (groups.list.currentIndex == -1 || groups.list.currentIndex != index) return

            var result = management.filtered_group_devices.set_filter(group.group_id)
            if (!result) {
                var currentDevice = listViewDevices.list.model.get(listViewDevices.list.currentIndex)
                if (currentDevice && groupsDevicesItem.device && currentDevice.id != groupsDevicesItem.device.id) {
                    listViewDevices.list.currentIndexChanged()
                }
                return
            }

            result = listViewDevices.list.model.length > 0 ? 0 : -1

            if (listViewDevices.list.currentIndex == result) {
                listViewDevices.list.currentIndexChanged()
            } else {
                listViewDevices.list.currentIndex = result
            }
        }
    }

    Component.onCompleted: {
        if (index == 0) list.currentIndex = index
    }

    width: parent.width
    height: 73

    color: ui.colors.black

    Custom.RoundedRect {
        id: container

        anchors.fill: parent

        color: list.currentIndex == index ? ui.colors.black : ui.colors.dark1
        radius: 10
        bottomRightCorner: false
        topRightCorner: false

        DS3.BadgeAttention {
            anchors {
                left: container.left
                top: container.top
            }

            visible: group.issue_count > 0
            text: group.issue_count
            opacity: !hub.online ? 0.6 : 1
        }

        Custom.RoundImage {
            id: imageItem

            imageWidthHeight: 64
            imageSource: group.small_image_link
        }

        Custom.FontText {
            width: settingsVisible ? parent.width - 144 : parent.width - 104

            anchors {
                verticalCenter: parent.verticalCenter
                left: imageItem.right
                leftMargin: 16
            }

            text: group.name
            color: ui.colors.light3
            wrapMode: Text.NoWrap
            elide: Text.ElideRight
            textFormat: Text.PlainText
            maximumLineCount: 1
            opacity: !hub.online ? 0.6 : 1
        }

        Custom.HandMouseArea {
            onClicked: {
                list.currentIndex = index
            }
        }
    }

    IconSettings {
        deviceSettings: false
        groupSetting: true
        visible: settingsVisible
    }
}