import QtQuick 2.7
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/911/DS3/" as DS3

Rectangle {
    property var all_buses: management.fibra_devices.get_fibra_buses()
    property var general_status: all_buses.buses_state

    Connections {
        target: management

        onDevicesChanged: {
            if (hub.max_power_test_state == "TEST_NOT_STARTED") {
                buttonBar.hasComment = false
                buttonBar.button.enabled = true
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

        headerText: tr.bus_power_test_title
        isRound: false
        showBackArrow: true
        showCloseIcon: false

        onBackAreaClicked: {
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/wires/WiresSettings.qml")
        }
    }

    DS3.ScrollView {
        width: parent.width
        height: infoContainer.height > 344 ? 344 : infoContainer.height

        anchors {
            fill: undefined
            top: navBarModal.bottom
            bottom: buttonBar.top
            horizontalCenter: parent.horizontalCenter
        }

        padding: 24

        DS3.InfoContainer {
            id: infoContainer

            imageType: DS3.InfoContainer.ImageType.BigImage
            imageSource: {
                return {
                    "OK": "qrc:/resources/images/Athena/fibra/BusesPowerTestGood.svg",
                    "POWER_IS_LOW": "qrc:/resources/images/Athena/fibra/BusesPowerTestProblems.svg",
                    "POWER_IS_LOST": "qrc:/resources/images/Athena/fibra/BusesPowerTestBad.svg"
                }[general_status]
            }

            titleComponent.text: {
                return {
                    "OK": tr.bus_test_success_title,
                    "POWER_IS_LOW": tr.bus_test_partially_success_title,
                    "POWER_IS_LOST": tr.bus_test_unsuccess_title
                }[general_status]
            }

            descComponent.text: {
                return {
                    "OK": tr.bus_test_passed_success_descr,
                    "POWER_IS_LOW": tr.bus_test_partially_success_descr,
                    "POWER_IS_LOST": tr.bus_test_unsuccess_descr
                }[general_status]
            }
        }

        DS3.Spacing {
            height: 40
        }

        DS3.SettingsContainer {
            width: parent.width
            height: resultsListView.contentHeight

            anchors.horizontalCenter: parent.horizontalCenter

            visible: general_status != "OK"

            ListView {
                id: resultsListView

                width: parent.width
                height: contentHeight

                model: all_buses.buses.length
                spacing: 1
                interactive: false
                delegate: DS3.SettingsNavigationTitlePrimaryStatus {
                    property var current_bus: all_buses.buses[index]

                    height: 68

                    title: util.insert(tr.bus_number_desktop, [current_bus["number"]])
                    subtitle: {
                        return {
                            "OK": tr.bus_state_success_pass,
                            "POWER_IS_LOW": tr.bus_state_partially_pass,
                            "POWER_IS_LOST": tr.bus_state_not_pass
                        }[current_bus["bus_state"]]
                    }

                    subtitleColor: {
                        return {
                            "OK": ui.ds3.figure.positiveContrast,
                            "POWER_IS_LOW": ui.ds3.figure.warningContrast,
                            "POWER_IS_LOST": ui.ds3.figure.attention
                        }[current_bus["bus_state"]]
                    }

                    onEntered: {
                        loader.setSource(
                            "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/wires/wires_test/WireTestResultsForBus.qml",
                            {"bus_data": all_buses.buses[index], "management": management}
                        )
                    }
                }
            }
        }
    }

    DS3.ButtonBar {
        id: buttonBar

        anchors.bottom: parent.bottom

        buttonText: tr.reset_power_test_results
        hasBackground: true
        hasComment: true
        commentText: util.insert(tr.last_tested_desktop, [hub.latest_power_test_date])

        button.onClicked: {
            app.hub_management_module.device_command(hub, 32)
            commentText = tr.resetting_results
            button.enabled = false
        }
    }
}