import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"

AjaxPopup {
    id: popup
    objectName: "textPopup"
    width: 320
    height: 36 + rect.height + 12 + 48

    parent: ApplicationWindow.contentItem

    closePolicy: Popup.NoAutoClose

    property string title: ""
    property string text: ""

    Rectangle {
        width: 320
        height: 130
        anchors.fill: parent
        color: ui.colors.dark1
        radius: 4
        border.width: 0.1
        border.color: ui.colors.dark4
        opacity: 0.999
        focus: true

        Keys.onReturnPressed: {
            popup.close()
        }

        Keys.onEnterPressed: {
            popup.close()
        }

        Column {
            anchors.fill: parent

            Item {
                width: parent.width
                height: textTitle.height + 20

                Text {
                    id: textTitle

                    width: parent.width - 10
                    text: title
                    color: ui.colors.white
                    wrapMode: Text.WordWrap
                    horizontalAlignment: Text.AlignHCenter
                    font.family: roboto.name
                    font.pixelSize: 14
                    anchors.centerIn: parent
                }
            }

            Item {
                id: rect
                width: parent.width
                height: textLabel.contentHeight + 28
                Text {
                    id: textLabel

                    width: parent.width - 10
                    wrapMode: Text.WordWrap
                    horizontalAlignment: Text.AlignHCenter
                    text: popup.text
                    color: ui.colors.white
                    opacity: 0.7
                    font.family: roboto.name
                    font.pixelSize: 12
                    anchors.centerIn: parent
                }
                Rectangle {
                    id: backgroundText
                    anchors.fill: parent
                    color: "white"
                    opacity: 0.5
                    visible: false
                }
                ToolTip {
                    id: tooltip
                    parent: parent

                    contentItem: Text {
                        text: tr.copied
                        font.family: roboto.name
                        font.pixelSize: 12
                        color: ui.colors.light1
                    }

                    background: Rectangle {
                        color: ui.colors.dark4
                        radius: 4
                        border {
                            width: 1
                            color: ui.colors.green1
                        }
                    }
                }

                MouseArea {
                    anchors.fill: parent
                    visible: __debug__

                    onClicked: {
                        util.set_clipboard_text(textLabel.text)
                        tooltip.show("", 500)
                    }

                    onPressed: {
                        backgroundText.visible = true
                    }

                    onExited: {
                        backgroundText.visible = false
                    }
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
                color: ui.colors.white
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