import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3

Rectangle {
//  Text of the comment
    property alias atomTitle: atomTitle
//  Text of the first subtitle
    property alias firstSubtitle: firstSubtitle
//  Text of the second subtitle
    property alias secondSubtitle: secondSubtitle
//  Text of the third subtitle
    property alias thirdSubtitle: thirdSubtitle
//  Icon of the first icon
    property alias firstIcon: firstIcon
//  Icon of the second icon
    property alias secondIcon: secondIcon

    width: parent.width
    height: textRow.height + atomTitle.height + 24

    color: ui.ds3.bg.high

    DS3.AtomTitle {
        id: atomTitle

        width: parent.width

        anchors {
            top: parent.top
            topMargin: 12
            left: parent.left
            leftMargin: 16
            right: parent.right
            rightMargin: 16
        }

        isPrimary: true
        isBold: isPrimary
        opacity: enabled ? 1 : 0.3
    }

    Row {
        id: textRow

        height: 20

        anchors {
            top: atomTitle.bottom
            left: parent.left
            leftMargin: 16
            right: parent.right
            rightMargin: 16
        }

        opacity: enabled ? 1 : 0.3
        spacing: 4

        DS3.Text {
            id: firstSubtitle

            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.secondary
        }

        Item {
            width: 20
            height: 20

            DS3.Icon {
                id: firstIcon

                anchors.centerIn: parent
            }
        }

        DS3.Text {
            id: secondSubtitle

            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.secondary
        }

        Item {
            width: 20
            height: 20

            DS3.Icon {
                id: secondIcon

                anchors.centerIn: parent
            }
        }

        DS3.Text {
            id: thirdSubtitle

            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.secondary
        }
    }
}