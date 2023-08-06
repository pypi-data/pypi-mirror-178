import QtQuick 2.13
import QtQuick.Controls 2.12
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/js/images.js" as Images


DS3Popups.PopupStep {
    property var sideMargin: 24
    property var state: device.state
    property var outdoor: {
        return device.obj_type == "13" || device.obj_type == "18"
    }
    property var curtain: {
        return device.obj_type == "06"
    }
    property var dualcurtain: {
        return device.obj_type == "1a"
    }

    Component.onDestruction: {
        if (["DETECTION_AREA_TEST", "WAIT_DETECTION_AREA_TEST_START"].includes(state)) {
            app.hub_management_module.device_command(device, 4)
        }
    }

    DS3.Spacing {
        height: 24
    }

    DS3.Text {
        anchors.horizontalCenter: parent.horizontalCenter

        text: tr.detection_zone_test
        style: ui.ds3.text.title.LBold
    }

    DS3.Spacing {
        height: 48
    }

    Image {
        id: signalTestImage

        width: sourceSize.width
        height: sourceSize.height

        anchors.horizontalCenter: parent.horizontalCenter

        source: Images.get_image(device.obj_type, "Large", device.color)
    }

    DS3.Spacing {
        height: 24
    }

    DS3.Text {
        id: deviceNameLabel

        width: parent.width - 2 * sideMargin

        anchors.horizontalCenter: parent.horizontalCenter

        text: device.info_name
        style: ui.ds3.text.title.SBold
        horizontalAlignment: Text.AlignHCenter
    }

    DS3.Spacing {
        height: 48
    }

    DS3.Text {
        id: deviceState

        anchors.horizontalCenter: parent.horizontalCenter

        horizontalAlignment: Text.AlignHCenter
        text: {
            if (!device.online) {
                return tr.offline
            }
            if (device.state == "NO_DEVICE_STATE_INFO" || device.state == "PASSIVE" || device.state == "ACTIVE") {
                return tr.ready
            }
            if (device.state == "WAIT_DETECTION_AREA_TEST_START") {
                return tr.starting_test
            }
            if (device.state == "WAIT_DETECTION_AREA_TEST_END") {
                return tr.stopping_test
            }
            if (device.state == "DETECTION_AREA_TEST") {
                return tr.test_in_progress
            }
            if (
            [
            "RADIO_CONNECTION_TEST",
            "WAIT_RADIO_CONNECTION_TEST_START",
            "WAIT_RADIO_CONNECTION_TEST_END",
            "WAIT_RADIO_CHANNEL_TEST_START",
            "RADIO_CHANNEL_TEST",
            "WAIT_RADIO_CHANNEL_TEST_END"
            ].includes(state))
            {
                return tr.another_test_in_progress
            }
            return tr.ready
        }
        color: {
            if (!device.online ||
             [
             "WAIT_RADIO_CONNECTION_TEST_START",
             "WAIT_RADIO_CONNECTION_TEST_END",
             "RADIO_CONNECTION_TEST",
             "WAIT_RADIO_CHANNEL_TEST_START",
             "RADIO_CHANNEL_TEST",
             "WAIT_RADIO_CHANNEL_TEST_END"
             ].includes(state)) {
                return ui.colors.disabled
            }
            return ui.colors.interactive
        }
        bottomPadding: 40
        style: ui.ds3.text.title.MBold
    }

    footer: Column {
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
            if (!device.online ||
            [
             "WAIT_DETECTION_AREA_TEST_START",
             "WAIT_DETECTION_AREA_TEST_END",
             "RADIO_CONNECTION_TEST",
             "WAIT_RADIO_CONNECTION_TEST_START",
             "WAIT_RADIO_CONNECTION_TEST_END",
             "WAIT_RADIO_CHANNEL_TEST_START",
             "RADIO_CHANNEL_TEST",
             "WAIT_RADIO_CHANNEL_TEST_END"
             ].includes(state))
            {
                startButton.enabled = false
                stopButton.enabled = false
            }
            else {
                startButton.enabled = true
                stopButton.enabled = true
            }
            if (
            ![                               // condition for changed button
             "WAIT_DETECTION_AREA_TEST_START",
             "WAIT_DETECTION_AREA_TEST_END",
             "DETECTION_AREA_TEST"
            ].includes(state))
            {
                startButton.visible = true
                stopButton.visible = false
            }
            else {
                startButton.visible = false
                stopButton.visible = true
            }
        }

        spacing: 12

        DS3.ButtonContained {
            id: startButton

            width: parent.width - sideMargin * 2

            anchors.horizontalCenter: parent.horizontalCenter

            text: {
                if (outdoor || dualcurtain) return tr.start_full_test
                return tr.start
            }
            enabled: device.online
            visible: !["WAIT_DETECTION_AREA_TEST_START",
                       "WAIT_DETECTION_AREA_TEST_END",
                       "WAIT_RADIO_CONNECTION_TEST_END",
                       "WAIT_RADIO_CHANNEL_TEST_END",
                       "DETECTION_AREA_TEST"
                      ].includes(state)

            onClicked: {
                startButton.visible = false
                stopButton.enabled = false
                stopButton.visible = true
                if (outdoor || curtain || dualcurtain) {
                    app.hub_management_module.device_command(device, 11)
                } else {
                    app.hub_management_module.device_command(device, 3)
                }
            }
        }

        DS3.ButtonContained {
            id: stopButton

            width: parent.width - sideMargin * 2

            anchors.horizontalCenter: parent.horizontalCenter

            text: tr.stop
            visible: !startButton.visible
            enabled: device.online

            onClicked: {
                stopButton.enabled = true
                app.hub_management_module.device_command(device, 4)
            }
        }

        DS3.ButtonContained {
            id: firstButton

            width: parent.width - sideMargin * 2

            anchors.horizontalCenter: parent.horizontalCenter

            visible: outdoor || dualcurtain
            enabled: startButton.visible && startButton.enabled

            text: dualcurtain ? tr.test_upper_sensors : tr.test_upper_sensor

            onClicked: {
                startButton.visible = false
                stopButton.enabled = false
                stopButton.visible = true
                app.hub_management_module.device_command(device, 12)
            }
        }

        DS3.ButtonContained {
            id: secondButton

            width: parent.width - sideMargin * 2

            anchors.horizontalCenter: parent.horizontalCenter

            visible: outdoor || dualcurtain
            enabled: startButton.visible && startButton.enabled

            text: dualcurtain ? tr.test_lower_sensors : tr.test_lower_sensor

            onClicked: {
                startButton.visible = false
                stopButton.enabled = false
                stopButton.visible = true
                app.hub_management_module.device_command(device, 13)
            }
        }

        DS3.ButtonContained {
            id: thirdButton

            width: parent.width - sideMargin * 2

            anchors.horizontalCenter: parent.horizontalCenter

            visible: outdoor || dualcurtain
            enabled: startButton.visible && startButton.enabled && (outdoor || dualcurtain) && device.antimasking

            text: tr.test_anti_masking

            onClicked: {
                startButton.visible = false
                stopButton.visible = true
                stopButton.enabled = false
                app.hub_management_module.device_command(device, 14)
            }
        }

        DS3.ButtonContained {
            id: maskingButton

            width: parent.width - sideMargin * 2

            anchors.horizontalCenter: parent.horizontalCenter

            visible: curtain && device.has_antimasking
            enabled: {
                return startButton.visible && startButton.enabled && curtain && device.antimasking
            }

            text: tr.test_anti_masking

            onClicked: {
                startButton.visible = false
                stopButton.visible = true
                app.hub_management_module.device_command(device, 14)
            }
        }

        DS3.Spacing {
            height: 24
        }
    }
}