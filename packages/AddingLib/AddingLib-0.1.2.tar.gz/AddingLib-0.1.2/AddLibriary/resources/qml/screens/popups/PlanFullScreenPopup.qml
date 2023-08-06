import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/events/parts"


AjaxPopup {
    id: popup
    objectName: "planFullScreenPopup"
    width: application.width - 180
    height: application.height - 180
    closePolicy: Popup.CloseOnEscape

    modal: true
    focus: true

    anchors.centerIn: parent

    property var url: ""

    background: Rectangle {
        color: ui.colors.black
        opacity: 0.8
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y

        Image {
            source: "qrc:/resources/images/icons/a-delete-button.svg"
            sourceSize.width: 56
            sourceSize.height: 56
            anchors {
                top: parent.top
                topMargin: 32
                right: parent.right
                rightMargin: 32
            }

            Custom.HandMouseArea {
                onClicked: {
                    popup.close()
                }
            }
        }
    }

    contentItem: Item {
        anchors.fill: parent

        MouseArea {
            anchors.fill: parent
        }

        Image {
            fillMode: Image.PreserveAspectFit
            source: popup.url
            anchors.fill: parent
        }
    }
}
