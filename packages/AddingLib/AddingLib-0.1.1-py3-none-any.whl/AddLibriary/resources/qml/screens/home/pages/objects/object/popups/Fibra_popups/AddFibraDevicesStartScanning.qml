import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/" as DS3

Rectangle {
    Component.onCompleted: {
        startScanningTimer.start()
    }

    width: 360
    height: 704

    color: ui.backgrounds.base
    radius: 12

    DS3.NavBarModal {
        id: navBarModal

        headerText: tr.bus_devices_adding_title

        onClosed: () => {
            mainFibraPopup.close()
        }
    }

    DS3.InfoContainerImageLoader {
        id: mainInfoContainer

        anchors {
            top: navBarModal.bottom
            topMargin: 24
            horizontalCenter: parent.horizontalCenter
        }

        titleComponent.text: tr.bus_scanning_title
        descComponent.text: tr.bus_scanning_descr
        imageComponent.spinner.visible: true
    }

    DS3.InfoContainer {
        id: secondaryInfoContainer

        property var counterOfFoundDevices: 0

        Connections {
            target: app

            onFoundFibraDevice: {
                secondaryInfoContainer.counterOfFoundDevices += 1
            }
        }

        anchors {
            top: mainInfoContainer.bottom
            topMargin: 24
            horizontalCenter: parent.horizontalCenter
        }

        titleComponent.text: util.insert(tr.x_devices_found_desktop, [counterOfFoundDevices.toString()])
        titleComponent.textStyle: ui.ds3.text.title.XSBold
        visible: counterOfFoundDevices
    }

    Timer {
        id: startScanningTimer

        interval: 1000 * 2

        onTriggered: {
            if (hub.scan_status == "SCAN_NOT_STARTED") {
                app.hub_management_module.scan_fibra_devices("START")
            } else {
                app.rpc.fibraScannedDevices.get_all_scanned_devices_from_rpc(hub.hub_id)
            }
        }
    }
}