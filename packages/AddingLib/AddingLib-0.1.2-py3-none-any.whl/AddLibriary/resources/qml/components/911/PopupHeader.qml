import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom


Custom.RoundedRect {
    id: header
    color: ui.colors.dark3
    topLeftCorner: true
    topRightCorner: true

    property var title: ""
    property alias closeArea: closeArea
    property alias headerTitle: headerTitle

    property var zoneHeight: 80

    /* -------------------------------------------- */
    /* desktop tests */
    property var accessibleIcoName: ""
    property var accessibleTextName: ""
    /* -------------------------------------------- */

    RowLayout {
        spacing: 10
        anchors.fill: parent

        Rectangle {
            color: "transparent"
            Layout.fillWidth: true
            Layout.fillHeight: true

            Custom.FontText {
                id: headerTitle
                text: header.title
                width: parent.width
                color: ui.colors.light3
                font.pixelSize: 16
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignLeft
                anchors {
                    left: parent.left
                    leftMargin: 28
                    verticalCenter: parent.verticalCenter
                }

                /* ------------------------------------------------ */
                /* desktop tests */
                Accessible.name: header.accessibleTextName
                Accessible.description: text
                Accessible.role: Accessible.Paragraph
                /* ------------------------------------------------ */
            }
        }

        Rectangle {
            color: "transparent"
            Layout.fillHeight: true
            Layout.minimumWidth: header.zoneHeight
            Layout.maximumWidth: header.zoneHeight

            Image {
                id: closeAreaImage

                source: "qrc:/resources/images/icons/a-delete-button.svg"
                sourceSize.width: 40
                sourceSize.height: 40
                anchors.centerIn: parent

                Custom.HandMouseArea {
                    id: closeArea

                    /* -------------------------------------------- */
                    /* desktop tests */
                    Accessible.name: header.accessibleIcoName
                    Accessible.description: "<button enabled=" + Accessible.checkable + ">" + closeAreaImage.source + "</button>"
                    Accessible.role: Accessible.Button
                    Accessible.checkable: visible && enabled
                    Accessible.onPressAction: {
                        if (!Accessible.checkable) return
                        closeArea.clicked(true)
                    }
                    /* -------------------------------------------- */
                }
            }
        }
    }
}