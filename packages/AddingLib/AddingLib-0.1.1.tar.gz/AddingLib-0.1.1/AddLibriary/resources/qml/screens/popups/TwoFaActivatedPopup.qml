import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/"

AjaxPopup {
    id: popup

    width: 328
    height: 290

    modal: true
    focus: true

    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    Rectangle {
        width: parent.width
        height: column.height + 88

        color: ui.colors.dark3
        radius: 8

        Column {
            id: column

            width: parent.width
            anchors.top: parent.top

            Item {
                width: parent.width
                height: 80

                Item {
                    id: closeItem

                    width: 80
                    height: parent.height
                    anchors.right: parent.right

                    Image {
                        id: iconClose

                        source: "qrc:/resources/images/icons/a-delete-button.svg"
                        sourceSize.width: 40
                        sourceSize.height: 40
                        anchors.centerIn: parent
                    }

                    MouseArea {
                        id: mouseAreaClose
                        anchors.fill: iconClose
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: popup.close()
                    }
                }
            }

//          ------------ logo ----------

            Item {
                id: ajaxLogoItem

                width: parent.width
                height: 66

                Image {
                    id: ajaxLogo
                    source: "qrc:/resources/images/desktop/logo/logo@2x.png"
                    width: 68
                    height: 50
                    anchors.horizontalCenter: parent.horizontalCenter
                }
            }

//          --------- text info ---------

            Item {
                id: infoItem

                width: parent.width
                height: infoText.height

                Text {
                    id: infoText

                    width: parent.width - 64
                    height: contentHeight

                    text: tr.desktop_2af_activated
                    color: ui.colors.light1
                    font.family: roboto.name
                    font.pixelSize: 16
                    font.bold: true
                    horizontalAlignment: Text.AlignHCenter
                    wrapMode: Text.WordWrap

                    anchors.centerIn: parent
                }
            }
        }
    }
}