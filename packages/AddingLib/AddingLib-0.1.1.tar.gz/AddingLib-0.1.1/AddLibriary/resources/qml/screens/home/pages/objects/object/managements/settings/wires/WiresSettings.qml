import QtQuick 2.7
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups

Rectangle {
    property int roomIndex: 0

    anchors.fill: parent

    color: ui.ds3.bg.base

    DS3.NavBarModal {
        id: navBarModal

        anchors.top: parent.top

        isRound: false
        headerText: tr.wires_settings
        showCloseIcon: false
    }

    Column {
        width: parent.width

        anchors.top: navBarModal.bottom

        padding: 24

        DS3.SettingsSwitch {
            id: powerOnWires

            width: parent.width - 48

            enabled: devEnable
            title: tr.wires_power_state
            radius: 12
            checked: hub.bus_status.includes("POWERED_ON")
            isDanger: hub.bus_status.includes("SHORT_CIRCUIT_PRESENT")
            cancelBinding: false

            onSwitched: () => {
                if (checked) {
                    app.hub_management_module.device_command_for_buses_power([])
                } else {
                    app.hub_management_module.device_command_for_buses_power([
                        "BUS_1",
                        "BUS_2",
                        "BUS_3",
                        "BUS_4",
                        "BUS_5",
                        "BUS_6",
                        "BUS_7",
                        "BUS_8",
                    ])
                }
            }

            Connections {
                target: app

                onPowerOnWiresActive: {
                    powerOnWires.checked = true
                }
                onPowerOnWiresInactive: {
                    powerOnWires.checked = false
                }
            }
        }

        DS3.Comment {
            width: parent.width - 48

            text: tr.buses_supply_interrupted_short_circuit
            itemsColor: ui.ds3.figure.attention
            visible: powerOnWires.checked && hub.bus_status.includes("SHORT_CIRCUIT_PRESENT")
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width - 48

            visible: powerOnWires.checked

            DS3.SettingsNavigationTitlePrimary {
                title: tr.bus_power_test_title
                icon: "qrc:/resources/images/Athena/settings_icons/WirePowerSettings-L.svg"

                onEntered: {
                    if (["SCAN_STARTED", "DEVICES_FOUND"].includes(hub.scan_status)) {
                        Popups.popupByPath("qrc:/resources/qml/screens/home/pages/objects/object/popups/Fibra_popups/FibraScanningInterruptPopup.qml", {"hub": hub})
                        return
                    }
                    if (management.fibra_devices.length == 0) {
                        loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/wires/wires_test/WireTestNoDevices.qml")
                    } else if (hub.bus_status.includes("SHORT_CIRCUIT_PRESENT") || hub.max_power_test_state == "TEST_FINISHED_WITH_SC") {
                        loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/wires/wires_test/WireTestShortCircuit.qml")
                    } else if (hub.max_power_test_state == "TEST_FINISHED_SUCCESSFULLY") {
                        loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/wires/wires_test/WireTestResults.qml")
                    } else {
                        loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/wires/wires_test/WireTestStart.qml")
                    }
                }
            }

            DS3.SettingsNavigationTitlePrimary {
                title: tr.add_bus_devices
                icon: "qrc:/resources/images/Athena/common_icons/AddSettings-L.svg"

                onEntered: {
                    if (!management.filtered_rooms.length) {
                        Popups.text_popup(tr.please_add_at_least_one_room_first, tr.please_add_at_least_one_room_first_descr)
                        return
                    }
                    if (hub.bus_status.includes("SHORT_CIRCUIT_PRESENT")) {
                        Popups.popupByPath("qrc:/resources/qml/screens/home/pages/objects/object/popups/Fibra_popups/AddFibraDeviceShortCircuitOnBus.qml")
                        return
                    }
                    if (hub.max_power_test_state == "TEST_IN_PROGRESS") {
                        Popups.popupByPath("qrc:/resources/qml/screens/home/pages/objects/object/popups/Fibra_popups/WireTestInterruptPopup.qml", {"hub": hub})
                        return
                    }
                    Popups.popupByPath("qrc:/resources/qml/screens/home/pages/objects/object/popups/Fibra_popups/AddFibraDevicePopup.qml", {"hub": hub, "roomIndex": roomIndex})
                }
            }
        }
    }
}