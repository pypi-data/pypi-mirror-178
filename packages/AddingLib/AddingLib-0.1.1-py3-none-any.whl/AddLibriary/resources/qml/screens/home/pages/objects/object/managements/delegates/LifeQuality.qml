import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


CommonPart {
    height: 72 + spreadInfo.height

    Item {
        id: spreadInfo

        width: parent.width - 32
        height: visible ? row.height + 24 : 0

        anchors {
            horizontalCenter: parent.horizontalCenter
            bottom: parent.bottom
        }

        visible: !device.are_all_sensors_broken && device.online

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
                text: tr.data_receiving_progress
                visible: device.is_in_waiting_for_data
            }

            Row {
                visible: !device.is_in_waiting_for_data

                spacing: 4

                DS3.BadgeStatusIconsText {
                    text: temperature_converter.new(
                        device.actual_temperature, "metric", 1
                    ).convert("auto").addSign().value
                    status: ui.ds3.status[device.temperature_color_status]
                    visible: !device.hardware_malfunction.includes("TEMPERATURE_AND_HUMIDITY_SENSOR")
                }

                DS3.BadgeStatusIconsText {
                    icon: "qrc:/resources/images/Athena/common_icons/Humidity-S.svg"
                    text: `${device.actual_humidity}%`
                    status: ui.ds3.status[device.humidity_color_status]
                    visible: !device.hardware_malfunction.includes("TEMPERATURE_AND_HUMIDITY_SENSOR")
                }

                DS3.BadgeStatusIconsText {
                    text: `${device.actual_co2} ${tr.ppm_co_level_value}`
                    status: ui.ds3.status[device.co2_color_status]
                    visible: !device.hardware_malfunction.includes("CO2_SENSOR")
                }
            }
        }
    }
}
