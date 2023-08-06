import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    id: gbr
    color: companyStack.color

    RowLayout {
        anchors.fill: parent
        spacing: 8

        Item {
            Layout.alignment: Qt.AlignTop | Qt.AlignLeft
            Layout.fillWidth: true
            Layout.fillHeight: true

            ColumnLayout {
                id: gbrLayout
                anchors.fill: parent
                spacing: 0

                Panel {
                    id: panel
                }

                GbrList {
                    id: gbrList
                }
            }

            Rectangle {
                anchors.fill: parent
                color: ui.colors.black
                opacity: 0.5
                visible: infoGbrComponent.editMode

                Custom.HandMouseArea {
                    cursorShape: Qt.ArrowCursor
                }
            }
        }

        Info {
            id: infoGbrComponent
        }
    }
}