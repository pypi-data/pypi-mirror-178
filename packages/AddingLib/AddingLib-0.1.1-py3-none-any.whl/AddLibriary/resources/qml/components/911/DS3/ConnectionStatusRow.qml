import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


Row {
    // Icon statuses
    enum IconStatus {
        OK,
        Fail,
        Loading
    }
//  To change the first icon between first and second images. Can be ok, fail or loading
    property var firstIconStatus: DS3.ConnectionStatusRow.IconStatus.OK
//  To change the second icon between second and third images. Can be ok, fail or loading
    property var secondIconStatus: DS3.ConnectionStatusRow.IconStatus.Fail

    width: parent.width
    height: 88

    anchors.horizontalCenter: parent.horizontalCenter

    spacing: 16

    DS3.Icon {
        source: "qrc:/resources/images/Athena/views_icons/AddHub.Illustration.svg"
        color: ui.ds3.figure.base
    }

    Item {
        width: 24
        height: 24

        anchors.verticalCenter: parent.verticalCenter

        DS3.Spinner {
            size: DS3.Spinner.ImageSize.M

            visible: firstIconStatus == DS3.ConnectionStatusRow.IconStatus.Loading
        }

        DS3.Select {
            checked: true
            isRound: true
            visible: firstIconStatus == DS3.ConnectionStatusRow.IconStatus.OK
        }

        DS3.Icon {
            source: "qrc:/resources/images/Athena/common_icons/CrossCircleFilled-M.svg"
            color: ui.ds3.figure.attention
            visible: firstIconStatus == DS3.ConnectionStatusRow.IconStatus.Fail
        }
    }

    DS3.Icon {
        source: "qrc:/resources/images/Athena/views_icons/Router.Illustration.svg"
        color: ui.ds3.figure.base
    }

    Item {
        width: 24
        height: 24

        anchors.verticalCenter: parent.verticalCenter

        DS3.Spinner {
            size: DS3.Spinner.ImageSize.M

            visible: secondIconStatus == DS3.ConnectionStatusRow.IconStatus.Loading
        }

        DS3.Select {
            checked: true
            isRound: true
            visible: secondIconStatus == DS3.ConnectionStatusRow.IconStatus.OK
        }

        DS3.Icon {
            source: "qrc:/resources/images/Athena/common_icons/CrossCircleFilled-M.svg"
            color: ui.ds3.figure.attention
            visible: secondIconStatus == DS3.ConnectionStatusRow.IconStatus.Fail
        }
    }

    DS3.Icon {
        source: "qrc:/resources/images/Athena/views_icons/Connections.Illustration.svg"
        color: ui.ds3.figure.base
    }
}