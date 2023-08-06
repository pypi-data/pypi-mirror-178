import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
    id: settingsSingleSelection

//  Whether need to change atomTitle
    property alias atomTitle: atomTitle
//  Whether selected or not
    property bool checked: false
//  Whether clicked on item
    property var switchChecked: () => {checked = !checked}

    width: parent.width
    height: atomTitle.height + 24

    color: ui.ds3.bg.highest

    DS3.AtomTitle {
        id: atomTitle

        anchors {
            left: parent.left
            right: checkIcon.left
            margins: 16
            verticalCenter: parent.verticalCenter
        }
        titleColor: ui.ds3.figure.base
    }

    DS3.Select {
        id: checkIcon

        anchors {
            right: parent.right
            margins: 16
            verticalCenter: parent.verticalCenter
        }

        checked: settingsSingleSelection.checked
        cancelBinding: false
        hasBackground: true
    }

    DS3.MouseArea {
        onClicked: switchChecked()
    }
}