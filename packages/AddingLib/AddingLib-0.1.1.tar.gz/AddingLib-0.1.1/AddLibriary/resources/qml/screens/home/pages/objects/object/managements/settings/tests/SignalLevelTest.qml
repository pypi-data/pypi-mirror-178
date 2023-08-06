import QtQuick 2.13
import QtQuick.Controls 2.12
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups


DS3Popups.PopupStep {
    property var chimesItem: null
    property var sideMargin: 24

    Component.onDestruction: {
        if (["RADIO_CONNECTION_TEST", "WAIT_RADIO_CONNECTION_TEST_START"].includes(device.state)) {
            app.hub_management_module.device_command(device, 2)
        }
    }

    sidePadding: 24

    header: DS3.NavBarModal {
        showBackArrow: true

        onBackAreaClicked: { goBack() }
    }

    DS3.Spacing {
        height: 24
    }

    DS3.Text {
        anchors.horizontalCenter: parent.horizontalCenter

        text: tr.signal_level_test
        style: ui.ds3.text.title.LBold
    }

    DS3.Spacing {
        height: 48
    }

    Item {
        width: 65
        height: 60

        anchors.horizontalCenter: parent.horizontalCenter

        Image {
            id: signalTestImage

            anchors.fill: parent

            y: 100
            source: {
                if (device.signal_strength == "NO_SIGNAL") {
                    return "qrc:/resources/images/desktop/icons/ic-no-signal@2x.png"
                }
                if (device.signal_strength == "WEAK") {
                    return "qrc:/resources/images/desktop/icons/ic-signal-1@2x.png"
                }
                if (device.signal_strength == "NORMAL") {
                    return "qrc:/resources/images/desktop/icons/ic-signal-2@2x.png"
                }
                if (device.signal_strength == "STRONG") {
                    return "qrc:/resources/images/desktop/icons/ic-signal-3@2x.png"
                }
                return "qrc:/resources/images/desktop/icons/ic-no-signal@2x.png"
            }
        }

        LevelAdjust {
            anchors.fill: signalTestImage

            source: signalTestImage
            maximumOutput: ui.ds3.figure.interactive
        }
    }

    DS3.Spacing {
        height: 24
    }

    DS3.Text {
        id: deviceNameText

        anchors.horizontalCenter: parent.horizontalCenter

        text: device.info_name
        horizontalAlignment: Text.AlignHCenter
        style: ui.ds3.text.body.MRegular
        y: 165
    }

    DS3.Spacing {
        height: 24
    }

    DS3.ProgressCountdownM {
        id: testTimer

        anchors.horizontalCenter: parent.horizontalCenter
    }

    DS3.Spacing {
        height: 48
    }

    DS3.Text {
        id: deviceState

        anchors.horizontalCenter: parent.horizontalCenter

        text: {
            if (!device.online) return tr.offline
            return {
                "NO_DEVICE_STATE_INFO": tr.ready,
                "PASSIVE": tr.ready,
                "NO_DEVICE_STATE_INFO": tr.ready,
                "ACTIVE": tr.ready,
                "WAIT_RADIO_CONNECTION_TEST_START": tr.starting_test,
                "WAIT_RADIO_CONNECTION_TEST_END": tr.stopping_test,
                "RADIO_CONNECTION_TEST": tr.test_in_progress,
                "WAIT_DETECTION_AREA_TEST_START": tr.another_test_in_progress,
                "WAIT_DETECTION_AREA_TEST_END": tr.another_test_in_progress,
                "DETECTION_AREA_TEST": tr.another_test_in_progress,
                "WAIT_RADIO_CHANNEL_TEST_START": tr.another_test_in_progress,
                "RADIO_CHANNEL_TEST": tr.another_test_in_progress,
                "WAIT_RADIO_CHANNEL_TEST_END": tr.another_test_in_progress,
            }[device.state]
        }

        color: {
            if (!device.online || [
                "WAIT_DETECTION_AREA_TEST_START",
                "WAIT_DETECTION_AREA_TEST_END",
                "DETECTION_AREA_TEST",
                "WAIT_RADIO_CHANNEL_TEST_START",
                "RADIO_CHANNEL_TEST",
                "WAIT_RADIO_CHANNEL_TEST_END"
            ].includes(device.state)) {
                return ui.colors.disabled
            }
            return ui.colors.interactive
        }
        style: ui.ds3.text.title.MBold
        horizontalAlignment: Text.AlignHCenter
        bottomPadding: 80
    }

    footer: Column {
        //Device state
        property var state: device.state

        Connections {
            target: app

            onActionFailed: {
                startButton.visible = true
                startButton.enabled = true
                stopButton.visible = false
            }
        }

        onStateChanged: {
            if (!device.online || [
                "WAIT_RADIO_CONNECTION_TEST_START",
                "WAIT_RADIO_CONNECTION_TEST_END",
                "WAIT_DETECTION_AREA_TEST_START",
                "WAIT_DETECTION_AREA_TEST_END",
                "DETECTION_AREA_TEST",
                "RADIO_CHANNEL_TEST",
                "WAIT_RADIO_CHANNEL_TEST_START",
                "WAIT_RADIO_CHANNEL_TEST_END"
            ].includes(device.state)) {
                startButton.enabled = false
                stopButton.enabled = false
            }
            else {
                startButton.enabled = true
                stopButton.enabled = true
            }

            if (["NO_DEVICE_STATE_INFO", "PASSIVE"].includes(device.state)) {
                startButton.visible = true
                stopButton.visible = false
            }

            // set appropriate status text
            if (!device.online) {
                testTimer.ready = false
                deviceState.text = tr.offline
            }
            if (["PASSIVE", "NO_DEVICE_STATE_INFO", "ACTIVE"].includes(device.state)) {
                testTimer.ready = true
                testTimer.stop()
                deviceState.text = tr.ready
            }
            else if (device.state == "WAIT_RADIO_CONNECTION_TEST_START") {
                deviceState.text = tr.starting_test
            }
            else if (device.state == "WAIT_RADIO_CONNECTION_TEST_END") {
                testTimer.stop()
                deviceState.text = tr.stopping_test
            }
            else if (device.state == "RADIO_CONNECTION_TEST") {
                testTimer.start()
                deviceState.text = tr.test_in_progress
            }
            else if ([
                "WAIT_DETECTION_AREA_TEST_START",
                "WAIT_DETECTION_AREA_TEST_END",
                "DETECTION_AREA_TEST",
                "WAIT_RADIO_CHANNEL_TEST_START",
                "RADIO_CHANNEL_TEST",
                "WAIT_RADIO_CHANNEL_TEST_END"
            ].includes(device.state)) {
                testTimer.ready = false
                deviceState.text = tr.another_test_in_progress
            }
            else {
                testTimer.ready = true
                deviceState.text = tr.ready
            }
        }

        DS3.ButtonContained {
            id: startButton

            width: parent.width - sideMargin * 2

            anchors.horizontalCenter: parent.horizontalCenter

            text: tr.start
            visible: !["WAIT_RADIO_CONNECTION_TEST_START", "RADIO_CONNECTION_TEST", "WAIT_RADIO_CONNECTION_TEST_END"].includes(device.state)
            enabled: device.online && !["WAIT_RADIO_CONNECTION_TEST_START", "WAIT_RADIO_CONNECTION_TEST_END"].includes(device.state)

            onClicked: {
                startButton.visible = false
                stopButton.visible = true
                stopButton.enabled = false
                app.hub_management_module.device_command(device, 1)
            }
        }

        DS3.ButtonContained {
            id: stopButton

            width: parent.width - sideMargin * 2

            anchors.horizontalCenter: parent.horizontalCenter

            text: tr.stop
            visible: !startButton.visible
            enabled: device.online && ![
                    "NO_DEVICE_STATE_INFO",
                    "PASSIVE",
                    "WAIT_RADIO_CONNECTION_TEST_START",
                    "WAIT_RADIO_CONNECTION_TEST_END"
                ].includes(device.state)

            onClicked: {
                stopButton.visible = false
                startButton.visible = true
                startButton.enabled = false
                app.hub_management_module.device_command(device, 2)
            }
        }

        DS3.Spacing {
            height: 24
        }
    }
}