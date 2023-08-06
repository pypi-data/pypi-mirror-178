import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    id: editBlock
    Layout.fillWidth: true
    Layout.minimumHeight: 56
    Layout.preferredHeight: Layout.minimumHeight

    color: "transparent"
    border.width: 0
    border.color: ui.colors.white
    opacity: enabled ? 1 : 0.3

    property var name: ""
    property var contentData: null
    property var collapsed: editBlock.Layout.preferredHeight == editBlock.Layout.minimumHeight
    property alias blockLoader: blockLoader
    property alias blockAnim: blockAnim

    ParallelAnimation {
        id: blockAnim

        PropertyAnimation {
            target: editBlock
            to: editBlock.Layout.preferredHeight == editBlock.Layout.minimumHeight ? editBlock.Layout.maximumHeight : editBlock.Layout.minimumHeight
            duration: 300
            property: "Layout.preferredHeight"
        }

        PropertyAnimation {
            target: viewTriangle
            to: editBlock.Layout.preferredHeight == editBlock.Layout.minimumHeight ? 180 : 0
            duration: 300
            property: "rotation"
        }
    }

    Rectangle {
        width: parent.width
        height: 1
        color: ui.colors.white
        opacity: 0.1
    }

    RowLayout {
        clip: true
        anchors.fill: parent

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredWidth: 11

            Item {
                id: blockHeader
                width: parent.width
                height: 40
                anchors {
                    top: parent.top
                    topMargin: 16
                }

                Custom.FontText {
                    width: parent.width
                    height: 30
                    font.pixelSize: 20
                    text: editBlock.name
                    font.weight: Font.Light
                    color: ui.colors.middle3
                    anchors.verticalCenter: parent.verticalCenter
                }

                Item {
                    width: 40
                    height: parent.height
                    anchors.right: parent.right

                    Custom.Triangle {
                        id: viewTriangle
                        rotation: 180
                        anchors.centerIn: parent
                    }

                    Custom.HandMouseArea {
                        onClicked: {
                            blockAnim.start()
                        }
                    }
                }
            }

            Item {
                id: blockBody
                width: parent.width
                height: parent.height - blockHeader.height
                anchors.top: blockHeader.bottom

                Loader {
                    id: blockLoader
                    anchors.fill: parent
                    sourceComponent: editBlock.contentData
                }
            }
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredWidth: 7
        }
    }

    Component.onCompleted: {
        blockAnim.start()
        editBlock.Layout.preferredHeight = Qt.binding(function(){
            return editBlock.Layout.maximumHeight
        })
    }
}
