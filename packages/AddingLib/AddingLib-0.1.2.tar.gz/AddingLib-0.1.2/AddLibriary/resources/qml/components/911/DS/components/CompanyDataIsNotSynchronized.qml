import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS" as DS


Rectangle {
    width: application.width
    height: 50

    color: ui.colors.warningContrast

    signal entered

    DS.Text {
        text: tr.pro_desktop_banner_info_conflict
        size: 12
        line: 16
        color: ui.colors.inverted

        anchors.centerIn: parent
    }

    DS.ButtonRegular {
        anchors {
            right: parent.right
            rightMargin: 86
            verticalCenter: parent.verticalCenter
        }

        text: tr.pro_desktop_banner_button_conflict
        color: ui.colors.inverted
        isOutline: true

        onClicked: entered()
    }
}
