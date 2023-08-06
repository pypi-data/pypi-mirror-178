import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/hub/"

AjaxPopup {
    id: popup
    width: updateBody.width
    height: updateBody.height

    property var info: null

    Rectangle {
        id: updateBody
        width: 360
        height: {
            var viewHeight = closeItem.height + header.height + listView.contentHeight + startArea.height + 30
            return viewHeight > 700 ? 700 : viewHeight
        }
        anchors.fill: parent
        color: "#252525"
        radius: 4
        border.width: 0.1
        border.color: "#1a1a1a"
        opacity: 0.999
        focus: true

        AjaxPopupCloseHeader {
            id: closeItem
            label: tr.attention
        }


        Item {
            id: header
            width: parent.width
            height: 32
            anchors {
                top: closeItem.bottom
                horizontalCenter: parent.horizontalCenter
            }

            Text {
                id: headerText
                width: parent.width
                text: tr.New_update_available_desktop + "  " + info.version
                color: ui.colors.light1
                font.family: roboto.name
                font.pixelSize: 16
                textFormat: Text.RichText
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
                anchors.centerIn: parent
            }
        }

        View {
            width: parent.width
            height: listView.contentHeight
            anchors {
                top: header.bottom
                topMargin: 15
                bottom: startArea.top
                bottomMargin: 15
            }

            ListView {
                id: listView
                anchors.fill: parent
                model: info.changelog
                delegate: Item {
                    width: listView.width
                    height: delegateText.height + 8

                    Text {
                        id: delegateText
                        width: parent.width - 64
                        height: contentHeight
                        text: "•  " + modelData
                        color: ui.colors.light1
                        font.family: roboto.name
                        font.pixelSize: 14
                        font.weight: Font.Light
                        horizontalAlignment: Text.AlignLeft
                        wrapMode: Text.WordWrap
                        anchors {
                            verticalCenter: parent.verticalCenter
                            left: parent.left
                            leftMargin: 32
                        }
                    }
                }
            }
        }

        MouseArea {
            id: startArea
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
                font.pixelSize: 14
                color: ui.colors.green1
                text: tr.Download_install_restart_desktop
            }

            onClicked: {
                client.start_update_installation()
                popup.close()
            }
        }
    }
}