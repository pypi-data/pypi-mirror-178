import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/911/"
import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    id: systemState

    clip: true
    color: ui.colors.dark4
    Layout.fillWidth: parent
    Layout.preferredHeight: visible ? 56 : 0

    property bool interconnectButtonVisible: false
    property bool restoreButtonVisible: false
    property bool interconnectDelayButtonVisible: false

    visible: companyAccess.OBJECT_CARD_SYSTEM_STATE

    function change_item_visible() {
        if (companyAccess.OBJECT_CARD_SYSTEM_STATE) {
            visible = true
            return
        }

        if (interconnectButtonVisible || restoreButtonVisible || interconnectDelayButtonVisible) {
            visible = true
        } else {
            visible = false
        }
    }

    onInterconnectButtonVisibleChanged: {
        change_item_visible()
    }

    onRestoreButtonVisibleChanged: {
        change_item_visible()
    }

    onInterconnectDelayButtonVisibleChanged: {
        change_item_visible()
    }

    Row {
        id: rowButtons

        height: parent.height - 24
        spacing: 16

        anchors {
            verticalCenter: parent.verticalCenter
            left: systemState.left
            leftMargin: 18
        }

        InterconnectButton { }

        InterconnectDelayButton { }

        RestoreAlarmButton { }

    }
}