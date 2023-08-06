import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
    id: settingsNavigation

//  Title of the settings
    property alias title: atomTitle.title
//  Subtitle of the settings
    property alias subtitle: atomTitle.subtitle
//  Color of the subtitle text
    property alias subtitleColor: atomTitle.subtitleColor

//  On settings navigation clicked
    signal entered

    width: parent.width
    height: atomTitle.height + 24

    color: ui.ds3.bg.highest

    DS3.MouseArea {
        onClicked: parent.entered()
    }

    DS3.AtomTitle {
        id: atomTitle

        anchors {
            left: parent.left
            right: rightBlock.left
            margins: 16
            verticalCenter: parent.verticalCenter
        }

        opacity: enabled ? 1 : 0.3
    }

    DS3.Icon {
        id: rightBlock

        anchors {
            right: parent.right
            margins: 16
            verticalCenter: parent.verticalCenter
        }

        source: "qrc:/resources/images/Athena/common_icons/ChevronRight-S.svg"
        opacity: enabled ? 1 : 0.3
    }
}