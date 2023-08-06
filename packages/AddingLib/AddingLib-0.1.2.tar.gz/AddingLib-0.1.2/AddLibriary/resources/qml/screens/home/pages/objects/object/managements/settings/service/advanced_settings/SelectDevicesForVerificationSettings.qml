import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
    id: selectDevicesScreen

    color: ui.ds3.bg.base

    property var devices_model: null
    property var verifying: get_devices()
    property var mode: null

    property var devices_len: {
        return devices_model.length
    }

    property var emptyImage: null
    property var parentRect: null
    property var callback: () => {}
    property var sideMargin: 24

    function get_devices() {
        var devices = []
        for(var child in devicesView.contentItem.children) {
            let deviceItem = devicesView.contentItem.children[child]
            if (deviceItem.objectName == "delegate") {
                var dev = devices_model.get(deviceItem.indexRef)
                var choice = deviceItem.checked
                var old = deviceItem.old_state
                devices.push([dev.name, dev.device_id, choice])
            }
        }
        return devices
    }

    DS3.NavBarModal {
        id: selectDevicesBar

        headerText: tr.devices
        showBackArrow: true
        isRound: false
        showCloseIcon: false

        onBackAreaClicked: {
            selectDevicesScreen.callback()
            selectDeviceLoader.setSource("")
        }
    }

    DS3.ScrollView {
        anchors {
            fill: undefined
            top: selectDevicesBar.bottom
            bottom: saveButton.top
            left: parent.left
            right: parent.right
        }

        padding: sideMargin

        DS3.InfoContainer {
            anchors.horizontalCenter: parent.horizontalCenter

            imageType: DS3.InfoContainer.ImageType.PlugImage
            imageSource: "qrc:/resources/images/Athena/PD_compliant/DoubleButton-XL.svg"
            descComponent.text: tr.no_devices_for_alarm_confirmation
            visible: !devices_model.length
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            SelectDevicesView {
                id: devicesView

                selectDevicesRect: selectDevicesScreen
                devicesModel: devices_model
                getDevices: get_devices
            }
        }
    }

    DS3.ButtonBar {
        id: saveButton

        anchors {
            bottom: parent.bottom
            horizontalCenter: parent.horizontalCenter
        }

        buttonText: tr.remember_selected_desktop
        hasBackground: true
        visible: devices_model.length

        button.onClicked: {
            if (mode == "verificationMode") {
                parentRect.verifying = get_devices().sort()
            } else {
                parentRect.holdUpVerifying = get_devices().sort()
            }
            selectDevicesScreen.callback()
            selectDeviceLoader.setSource("")
        }
    }
}
