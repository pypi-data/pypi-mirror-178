import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/" as DS3

Rectangle {
    Connections {
        target: management

        onDevicesChanged: {
            if (hub.max_power_test_state == "TEST_NOT_STARTED") {
                loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/wires/wires_test/WireTestStart.qml")
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

    DS3.InfoContainer {
        id: infoContainer

        anchors {
            top: navBarModal.bottom
            topMargin: 24
        }

        imageType: DS3.InfoContainer.ImageType.PlugImage
        imageSource: "qrc:/resources/images/Athena/fibra/ShortCircuit-XL.svg"
        titleComponent.text: hub.bus_status.includes("SHORT_CIRCUIT_PRESENT") ?
            tr.power_test_short_circuit_impossible_title :
            tr.interrupt_due_overcurrent_title
        descComponent.text: hub.bus_status.includes("SHORT_CIRCUIT_PRESENT") ?
            tr.power_test_short_circuit_impossible_descr :
            tr.interrupt_due_overcurrent_descr
    }

    DS3.ButtonBar {
        id: buttonBar

        anchors.bottom: parent.bottom

        visible: !hub.bus_status.includes("SHORT_CIRCUIT_PRESENT")
        buttonText: tr.reset_power_test_results
        hasBackground: true
        hasComment: true
        commentText: util.insert(tr.last_tested_desktop, [hub.latest_power_test_date])


        button.onClicked: {
            app.hub_management_module.device_command(hub, 32)
        }
    }
}