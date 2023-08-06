import QtQuick 2.7
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/911/DS3/" as DS3

Rectangle {
    property var testStatus: hub.max_power_test_state

    Connections {
        target: management

        onDevicesChanged: {
            if (testStatus == "TEST_FINISHED_SUCCESSFULLY") {
                loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/wires/wires_test/WireTestResults.qml")
            } else if (testStatus == "TEST_FINISHED_WITH_SC" || hub.bus_status.includes("SHORT_CIRCUIT_PRESENT")) {
                loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/wires/wires_test/WireTestShortCircuit.qml")
            }
        }

        onWireTestStarted: {
            stopButton.button.enabled = true
            stopButton.commentText = tr.test_in_progress
            updateButtonsTimer.running = false
        }

        onWireTestEnded: {
            startButton.button.enabled = true
            startButton.commentText = tr.ready
        }
    }

    anchors.fill: parent

    color: ui.ds3.bg.base

    DS3.NavBarModal {
        id: navBarModal

        anchors.top: parent.top

        isRound: false
        headerText: tr.bus_power_test_title
        showBackArrow: true
        showCloseIcon: false

        onBackAreaClicked: {
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/wires/WiresSettings.qml")
        }
    }

    DS3.InfoContainerImageLoader {
        id: infoContainer

        property var approximateTestTime: Math.max(
            Math.ceil(hub.frame_length * 8 / 60 / 5) * 5,
            5
        )

        anchors {
            top: navBarModal.bottom
            topMargin: 24
        }

        titleComponent.text:  testStatus == "TEST_IN_PROGRESS" ? tr.test_in_progress : tr.ready_for_test
        descComponent.text: testStatus == "TEST_IN_PROGRESS" ? util.insert(tr.bus_power_test_in_progress, [approximateTestTime]) : tr.buses_power_test_descr1
        imageComponent.spinner.visible: testStatus == "TEST_IN_PROGRESS"
    }

    DS3.InfoContainer {
        id: infoContainerRedText

        anchors.top: infoContainer.bottom

        descComponent.text: tr.buses_power_test_descr2
        descComponent.color: ui.ds3.figure.attention
        visible: testStatus != "TEST_IN_PROGRESS"
    }

    DS3.ButtonBar {
        id: startButton

        anchors.bottom: parent.bottom

        visible: testStatus != "TEST_IN_PROGRESS"
        buttonText: tr.start
        hasComment: true
        commentText: testStatus == "TEST_IN_PROGRESS"? tr.test_in_progress : tr.ready
        commentIcon: "qrc:/resources/images/Athena/common_icons/Info-Grey-S.svg"

        button.onClicked: {
            app.hub_management_module.device_command(hub, 33)
            startButton.button.enabled = false
            commentText = tr.starting_test
            updateButtonsTimer.running = true
        }
    }

    DS3.ButtonBar {
        id: stopButton

        anchors.bottom: parent.bottom

        button.isOutline: true
        visible: testStatus == "TEST_IN_PROGRESS"
        buttonText: tr.stop_test
        hasComment: true
        commentText: testStatus == "TEST_IN_PROGRESS"? tr.test_in_progress: tr.ready
        commentIcon: "qrc:/resources/images/Athena/common_icons/Info-Grey-S.svg"

        button.onClicked: {
            stopButton.button.enabled = false
            commentText = tr.stopping_test
            app.hub_management_module.device_command(hub, 32)
        }
    }

    Timer {
        id: updateButtonsTimer

        interval: 5000
        repeat: false
        triggeredOnStart: false
        running: false

        onTriggered: {
            startButton.button.enabled = true
            startButton.commentText = tr.ready
        }
    }
}