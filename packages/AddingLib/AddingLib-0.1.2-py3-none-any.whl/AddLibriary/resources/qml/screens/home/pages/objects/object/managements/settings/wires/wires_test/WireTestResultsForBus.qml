import QtQuick 2.7
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/911/DS3/" as DS3

Rectangle {
    property var management: null
    property var bus_data: null

    Connections {
        target: management

        onDevicesChanged: {
            if (hub.max_power_test_state == "TEST_NOT_STARTED") {
                loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/wires/wires_test/WireTestStart.qml")
            } else if (hub.max_power_test_state == "TEST_FINISHED_WITH_SC") {
                loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/wires/wires_test/WireTestShortCircuit.qml")
            }
        }
    }

    anchors.fill: parent

    color: ui.ds3.bg.base

    DS3.NavBarModal {
        id: navBarModal

        anchors.top: parent.top

        isRound: false
        headerText: util.insert(tr.bus_test_number_desktop, [bus_data["number"]])
        showBackArrow: true
        showCloseIcon: false

        onBackAreaClicked: {
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/wires/wires_test/WireTestResults.qml")
        }
    }

    DS3.ScrollView {
        width: parent.width
        height: settingsContainer.height > 344 ? 344 : settingsContainer.height

        anchors {
            fill: undefined
            top: navBarModal.bottom
            bottom: parent.bottom
        }

        padding: 24

        Rectangle {
            id: helpText

            width: parent.width
            height: 72

            anchors.horizontalCenter: parent.horizontalCenter

            radius: 12
            color: ui.ds3.bg.high
            visible: bus_data.bus_state != "OK"
            
            DS3.Text {
                anchors {
                    fill: parent
                    margins: 16
                }

                text: tr.bus_device_test_need_more_power_descr
                style: ui.ds3.text.body.MRegular
            }
        }

        DS3.Spacing {
            height: 40

            visible: helpText.visible
        }

        DS3.SettingsContainer {
            id: settingsContainer

            width: parent.width
            height: resultsForBusListView.contentHeight

            anchors.horizontalCenter: parent.horizontalCenter

            ListView {
                id: resultsForBusListView

                width: parent.width
                height: contentHeight

                model: bus_data.devices.length
                spacing: 1
                interactive: false
                delegate: DS3.DeviceRegular {

                    property var current_device: management.devices.get_by_id(bus_data.devices[index])

                    width: parent.width
                    height: 104

                    deviceType: current_device.obj_type
                    deviceColor: {
                        if (current_device) {
                            return current_device.color
                        }
                        return "WHITE"
                    }
                    atomTitle.title: current_device.name
                    atomTitle.subtitle: {
                        return {
                            "NO_DATA": tr.no_data_full,
                            "OK": tr.bus_device_test_enough_power,
                            "POWER_IS_LOW": tr.bus_device_test_need_more_power,
                            "POWER_IS_LOST": tr.bus_device_test_no_power
                        }[current_device.max_power_test_result]
                    }

                    atomTitle.subtitleColor: {
                        return {
                            "NO_DATA": ui.ds3.figure.secondary,
                            "OK": ui.ds3.figure.positiveContrast,
                            "POWER_IS_LOW": ui.ds3.figure.warningContrast,
                            "POWER_IS_LOST": ui.ds3.figure.attention
                        }[current_device.max_power_test_result]
                    }
                }
            }
        }
    }
}