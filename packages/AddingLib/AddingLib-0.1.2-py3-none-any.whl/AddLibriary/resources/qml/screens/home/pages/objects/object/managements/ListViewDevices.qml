import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.ListView {
    id: devices

    property var withoutSettingIcon: false
    property var colorMagic: false
    property var reindexNeeded: true

    signal resetMtrDevicesIndex()

    /* ------------------------------------------------ */
    /* desktop tests */
    property var accessiblePrefix: ""
    /* ------------------------------------------------ */

    Component.onCompleted: {
        management.resetCurrentIndexes()
    }

    Connections {
        target: management

        onResetCurrentIndexes: {
            if (!devices.reindexNeeded) return
            if (devices.list.model.length > 0 && devices.list.model.get(0).class_name == "hub") {
                devices.reindexNeeded = false
                devices.list.currentIndex = 0
            } else {
                devices.list.currentIndex = -1
            }
        }
    }

    contentPadding: 0
    list {
        spacing: 1
        cacheBuffer: 20000
        model: []
        delegate: DeviceDelegate {
            selectedColor: devices.reindexNeeded && devices.colorMagic ? ui.colors.dark1 : ui.colors.black
            settingsVisible: !withoutSettingIcon

            /* ------------------------------------------------ */
            /* desktop tests */
            accessiblePrefix: devices.accessiblePrefix ? devices.accessiblePrefix + "_device_" + device.id : ""
            /* ------------------------------------------------ */
        }
    }
}
