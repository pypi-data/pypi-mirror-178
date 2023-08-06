import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml" as Root


Rectangle {
    Connections {
        target: app.rpc.fibraScannedDevices

        onIncomingScannedDevices: {
            loading.visible = false
        }

        onGetScannedDeviceError: {
            mainFibraPopup.close()
        }
    }

    width: 500
    height: 704

    color: ui.backgrounds.base
    radius: 12

    Root.ContextLoader {
        id: fibraScannedDevicesView

        anchors.fill: parent

        visible: !loading.visible
        contextTarget: app.fibraScannedDevicesView
    }

    Rectangle {
        id: loading

        anchors.fill: parent

        color: ui.ds3.bg.base
        radius: 12

        DS3.Spinner {
            anchors.centerIn: parent
        }
    }
}