import QtQuick 2.13
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/" as Custom


Item {
    id: headerItem

    property alias checkText: checkText
    property var headerTitle

    width: parent.width
    height: 48

    Rectangle {
        id: header

        width: parent.width
        height: 32

        color: ui.colors.dark4

        Custom.FontText {
            anchors {
                verticalCenter: parent.verticalCenter
                left: parent.left
                leftMargin: 24
            }

            text: headerTitle
            font.pixelSize: 14
            color: ui.colors.white
        }

        Custom.FontText {
            id: checkText

            anchors {
                verticalCenter: parent.verticalCenter
                right: parent.right
                rightMargin: 24
            }

            text: tr.check_all
            color: ui.colors.green1

            Custom.HandMouseArea {
                onClicked: {
                    availableGroupsList.toggleAll()
                }
            }
        }
    }

    Rectangle {
        width: parent.width
        height: 2

        anchors.bottom: header.bottom

        color: ui.colors.black
    }
}
