import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
    id: settingsNavigation

//  Title of the settings
    property alias title: atomTitle.title
//  Subtitle of the settings
    property alias subtitle: atomTitle.subtitle
//  Athena status
    property var status: ui.ds3.status.DEFAULT
//  Color defined based on the status
    readonly property var statusColor: ({
        [ui.ds3.status.DEFAULT]: ui.ds3.figure.base,
        [ui.ds3.status.WARNING]: ui.ds3.figure.warningContrast,
        [ui.ds3.status.ATTENTION]: ui.ds3.figure.attention,
        [ui.ds3.status.HAZARD]: ui.ds3.figure.hazard,
        [ui.ds3.status.NOT_IMPORTANT]: ui.ds3.figure.nonessential,
    })[status]
//  Left icon
    property alias leftIcon: leftIcon

//  On settings navigation clicked
    signal entered

    width: parent.width
    height: atomTitle.height + 24

    color: ui.ds3.bg.highest

    DS3.MouseArea {
        onClicked: parent.entered()
    }

    DS3.Icon {
        id: leftIcon

        width: 24
        height: 24

        anchors {
            left: parent.left
            leftMargin: 16
            verticalCenter: parent.verticalCenter
        }

        opacity: enabled ? 1 : 0.3
        color: ui.ds3.figure.base
    }

    DS3.AtomTitle {
        id: atomTitle

        anchors {
            left: leftIcon.source != '' ? leftIcon.right : parent.left
            right: rightBlock.right
            margins: 16
            verticalCenter: parent.verticalCenter
        }

        isPrimary: false
        opacity: enabled ? 1 : 0.3
        subtitleColor: statusColor
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