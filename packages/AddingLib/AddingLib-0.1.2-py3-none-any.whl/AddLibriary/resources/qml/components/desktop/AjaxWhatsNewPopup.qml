import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/"


AjaxPopup {
    id: popup
    width: 360
    height: bodyRect.height

    modal: true
    focus: true

    property var information: null

    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    Rectangle {
        id: bodyRect
        width: parent.width
        radius: 8
        color: "#252525"

        border.width: 1
        border.color: "#1a1a1a"

        height: {
            var viewHeight = closeItem.height + notFoundText.height + listView.contentHeight + actionItem.height + 30
            return viewHeight > 500 ? 500 : viewHeight
        }

        Item {
            id: closeItem
            width: parent.width
            height: 48
            anchors.top: parent.top

            Text {
                width: parent.width
                text: tr.whats_new
                color: ui.colors.light1
                font.pixelSize: 18
                font.family: roboto.name
                font.weight: Font.Light
                horizontalAlignment: Text.AlignHCenter
                wrapMode: Text.WordWrap
                anchors.centerIn: parent
            }
        }

        View {
            width: popup.width
            anchors {
                top: closeItem.bottom
                topMargin: 15
                bottom: actionItem.top
                bottomMargin: 15
            }

            Item {
                anchors.fill: parent
                visible: !information || !information.data

                Text {
                    id: notFoundText
                    width: parent.width - 64
                    height: parent.visible ? contentHeight : 0
                    text: tr.minor_bug_fixes_app_update
                    color: ui.colors.light1
                    opacity: 0.8
                    font.family: roboto.name
                    font.pixelSize: 13
                    font.weight: Font.Light
                    horizontalAlignment: Text.AlignHCenter
                    wrapMode: Text.WordWrap
                    anchors {
                        top: parent.top
                        horizontalCenter: parent.horizontalCenter
                    }
                }
            }

            ListView {
                id: listView
                anchors.fill: parent
                model: information.data

                delegate: Item {
                    width: listView.width
                    height: textH1.height + textH2.height + textP.height + textLi.height + textA.height

                    Text {
                        id: textH1
                        width: parent.width - 64
                        visible: modelData.mode == "h1" ? true : false
                        height: modelData.mode == "h1" ? contentHeight + 15 : 0
                        text: modelData.text
                        color: ui.colors.light1
                        font.family: roboto.name
                        font.pixelSize: 18
                        font.weight: Font.ExtraBold
                        horizontalAlignment: Text.AlignHCenter
                        wrapMode: Text.WordWrap
                        anchors.centerIn: parent
                    }

                    Text {
                        id: textH2
                        width: parent.width - 64
                        visible: modelData.mode == "h2" ? true : false
                        height: modelData.mode == "h2" ? contentHeight + 15 : 0
                        text: "•  " + modelData.text
                        color: ui.colors.light1
                        font.family: roboto.name
                        font.pixelSize: 16
                        font.weight: Font.Bold
                        horizontalAlignment: Text.AlignLeft
                        wrapMode: Text.WordWrap
                        anchors {
                            verticalCenter: parent.verticalCenter
                            left: parent.left
                            leftMargin: 25
                        }
                    }

                    Text {
                        id: textP
                        width: parent.width - 64
                        visible: modelData.mode == "p" ? true : false
                        height: modelData.mode == "p" ? contentHeight + 15 : 0
                        text: modelData.text
                        color: ui.colors.light1
                        opacity: 0.8
                        font.family: roboto.name
                        font.pixelSize: 13
                        font.weight: Font.Light
                        horizontalAlignment: Text.AlignLeft
                        wrapMode: Text.WordWrap
                        anchors {
                            verticalCenter: parent.verticalCenter
                            left: parent.left
                            leftMargin: 25
                        }
                    }

                    Text {
                        id: textLi
                        width: parent.width - 64
                        visible: modelData.mode == "li" ? true : false
                        height: modelData.mode == "li" ? contentHeight + 5 : 0
                        text: "    •  " + modelData.text
                        color: ui.colors.light1
                        opacity: 0.8
                        font.family: roboto.name
                        font.pixelSize: 13
                        font.weight: Font.Light
                        horizontalAlignment: Text.AlignLeft
                        wrapMode: Text.WordWrap
                        anchors {
                            verticalCenter: parent.verticalCenter
                            left: parent.left
                            leftMargin: 25
                        }
                    }

                    Text {
                        id: textA
                        width: parent.width - 64
                        visible: modelData.mode == "a" ? true : false
                        height: modelData.mode == "a" ? contentHeight + 15 : 0
                        text: "<style>a:link { color: '#60e3ab'; }</style><u><a href='" + modelData.link + "'>" + modelData.text + "</a></u>"
                        color: ui.colors.green1
                        font.family: roboto.name
                        font.pixelSize: 14
                        font.weight: Font.Light
                        textFormat: Text.RichText
                        horizontalAlignment: Text.AlignHCenter
                        wrapMode: Text.WordWrap
                        anchors.centerIn: parent
                    }

                    MouseArea {
                        anchors.fill: textA
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: {
                            Qt.openUrlExternally(modelData.link)
                        }
                    }
                }
            }
        }

        Item {
            id: actionItem
            width: parent.width
            height: 48

            anchors.bottom: parent.bottom

            Rectangle {
                anchors.top: parent.top
                height: 1
                width: parent.width
                color: ui.colors.light1
                opacity: 0.1
            }

            Text {
                anchors.centerIn: parent
                text: tr.ok
                color: ui.colors.green1
                font.family: roboto.name
                font.pixelSize: 14
                font.weight: Font.Light
                width: parent.width
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
            }

            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: {
                    popup.close()
                }
            }
        }
    }
}