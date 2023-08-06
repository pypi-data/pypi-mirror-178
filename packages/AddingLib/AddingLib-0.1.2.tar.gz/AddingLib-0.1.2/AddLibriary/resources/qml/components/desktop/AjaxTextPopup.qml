import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/DS3" as DS3

AjaxPopup {
    id: popup
    objectName: "textPopup"
    width: 320
    height: 36 + textLabelWrapper.height + 12 + 48

    parent: ApplicationWindow.contentItem

    property string title: ""
    property string text: ""

    Rectangle {
        width: 320
        height: 130
        anchors.fill: parent
        color: "#393939"
        radius: 4
        border.width: 0.1
        border.color: "#1a1a1a"
        opacity: 0.999
        focus: true

        Keys.onPressed: {
            popup.close()
        }

        Column {
            anchors.fill: parent

            Item {
                id: textTitleWrapper

                width: parent.width
                height: textTitle.height + 8

                DS3.Text {
                    id: textTitle

                    width: parent.width - 12

                    text: title
                    anchors.centerIn: parent
                    style: ui.ds3.text.body.MBold
                    horizontalAlignment: Text.AlignHCenter
                }
            }

            Item {
                id: textLabelWrapper
                width: parent.width
                height: textLabel.contentHeight
                anchors.horizontalCenter: parent.horizontalCenter

                DS3.Text {
                    id: textLabel

                    width: parent.width - 12

                    style: ui.ds3.text.body.SRegular
                    text: popup.text
                    horizontalAlignment: Text.AlignHCenter
                    anchors.centerIn: parent
                }
            }
        }

        MouseArea {
            width: parent.width
            height: 48

            anchors.bottom: parent.bottom

            Rectangle {
                height: 1
                width: parent.width
                opacity: 0.1
                color: ui.colors.light1
                anchors.top: parent.top
            }

            Text {
                anchors.centerIn: parent
                font.family: roboto.name
                font.pixelSize: 12
                color: ui.colors.green1
                text: "OK"
            }

            onClicked: {
                popup.close()
            }
        }
    }
}
