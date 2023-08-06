import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/911/DS3/" as DS3

Rectangle {
    property var settingsVisible: false

    Connections {
        target: rooms.list

        onCurrentIndexChanged: {
            if (rooms.list.currentIndex == -1 || rooms.list.currentIndex != index) return

            var result = management.filtered_room_devices.set_filter(room.room_id)
            if (!result) {
                var currentDevice = listViewDevices.list.model.get(listViewDevices.list.currentIndex)
                if (currentDevice && roomsDevicesItem.device && currentDevice.id != roomsDevicesItem.device.id) {
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
    height: 73 + airMonitoringInfo.height

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
            visible: room.issue_count > 0
            text: room.issue_count
            opacity: hub.online ? 1 : 0.3
        }

        Custom.RoundImage {
            id: imageItem

            anchors {
                verticalCenter: undefined
                top: parent.top
                topMargin: 4
            }

            imageWidthHeight: 64

            imageSource: room.big_image_link
            imageRoundings: 2
        }

        Custom.FontText {
            width: settingsVisible ? parent.width - 144 : parent.width - 104

            anchors {
                top: parent.top
                topMargin: 15
                left: imageItem.right
                leftMargin: 16
            }

            text: room.name
            color: ui.colors.light3
            wrapMode: Text.NoWrap
            elide: Text.ElideRight
            textFormat: Text.PlainText
            maximumLineCount: 1
            opacity: hub.online ? 1 : 0.6
        }

        Row {
            id: infoIcons

            anchors {
                bottom: parent.bottom
                bottomMargin: 15
                left: imageItem.right
                leftMargin: 16
            }

            opacity: hub.online ? 1 : 0.6
            spacing: 8

            Repeater {
                id: iconRepeater

                model: temperatureText.visible ?  // Because we have small delegate ;(
                    room.room_status_icons_list.slice(0, 7) :
                    room.room_status_icons_list.slice(0, 8)

                DS3.Icon {
                    source: iconRepeater.model[index].source
                    color: ui.ds3.figure[iconRepeater.model[index].color]
                }
            }

            DS3.Text {
                id: temperatureText

                height: 16

                text: {
                    settings.measure_system == "imperial" ?
                    Math.round(room.temperature * 9 / 5 + 32) + "℉" :
                    room.temperature + "℃"
                }
                color: ui.ds3.figure.secondary
                style: ui.ds3.text.body.MRegular
                visible: room.temperature && !room.has_lq_with_data
            }
        }

        Custom.HandMouseArea {
            onClicked: {
                list.currentIndex = index
            }
        }
    }

    Item {
        id: airMonitoringInfo

        width: parent.width - 32
        height: visible ? row.height + 24 : 0

        anchors {
            horizontalCenter: parent.horizontalCenter
            bottom: parent.bottom
        }

        visible: room.has_lq_with_data && !!row.width

        Rectangle {
            width: parent.width
            height: 1

            color: ui.ds3.bg.high
        }

        Row {
            id: row

            height: childrenRect.height

            anchors.verticalCenter: parent.verticalCenter

            spacing: 4

            DS3.BadgeStatusIconsText {
                visible: !!text
                text: !!room.actual_temperature
                    ? temperature_converter.new(
                        room.actual_temperature, "metric", 1
                    ).convert("auto").addSign().value
                    : ""
            }

            DS3.BadgeStatusIconsText {
                visible: !!text
                icon: "qrc:/resources/images/Athena/common_icons/Humidity-S.svg"
                text: !!room.actual_humidity ? `${room.actual_humidity}%` : ""
            }

            DS3.BadgeStatusIconsText {
                visible: !!text
                text: !!room.actual_co2 ? `${room.actual_co2} ${tr.ppm_co_level_value}` : ""
                status: ui.ds3.status[room.co2_color_status]
            }
        }
    }

    IconSettings {
        deviceSettings: false
        visible: settingsVisible
    }
}