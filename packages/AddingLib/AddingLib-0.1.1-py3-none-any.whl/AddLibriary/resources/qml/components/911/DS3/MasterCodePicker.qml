import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3


// version: Athena 4.6
ComboBox {
    id: combobox

//  child component
    property alias atomTitle: atomTitle
//  Use this for adding suffix
    property string suffix: ""
// Use this for adding comment
    property string commentText: ""
//  Whether to cancel property binding
    property bool cancelBinding: true
//  Whether need to change list view
    property alias contentList: contentList
//  Width of the sheet action part
    property var sheetActionWidth: Math.max(combobox.width, 200)
//  Custom highlighted index for focus on suggestion
    property var customHighlightedIndex: combobox.highlightedIndex
//  The country phone code model
    property var codeModel: {}
//  The text displayed as the code
    property var codeText: combobox.displayText + suffix

    Component.onCompleted: if (cancelBinding) currentIndex = currentIndex

    width: 50 + (codeText.length - 4) * 10
    height: contentItem.height

    model: Object.keys(codeModel)
    opacity: enabled ? 1 : 0.3

    delegate: ItemDelegate {
        id: itemDelegate

        width: sheetActionWidth
        height: 40

        Rectangle {
            anchors.fill: parent

            color: customHighlightedIndex == index ? ui.ds3.bg.high : ui.ds3.bg.highest
        }

        contentItem: DS3.Text {
            anchors {
                verticalCenter: parent.verticalCenter
                left: parent.left
                leftMargin: 16
            }

            style: ui.ds3.text.body.MRegular
            text: `(${modelData}) ${codeModel[modelData]}`
            hasElide: true
            rightPadding: 30
        }

        DS3.Icon {
            anchors {
                right: parent.right
                rightMargin: 16
                verticalCenter: parent.verticalCenter
            }

            visible: combobox.currentIndex == index
            source: "qrc:/resources/images/Athena/common_icons/Shape.svg"
        }

        DS3.MouseArea {
            acceptedButtons: Qt.NoButton

            onContainsMouseChanged: {
                if (containsMouse) {
                    customHighlightedIndex = index
                }
            }
        }
    }

    indicator: DS3.Icon {
        anchors {
            right: combobox.right
            verticalCenter: combobox.verticalCenter
        }

        source: "qrc:/resources/images/Athena/common_icons/Picker-XS.svg"
        rotation: popup.visible ? 180 : 0

        Behavior on rotation {
            NumberAnimation {
                duration: 200
            }
        }
    }

    contentItem: Item {
        height: atomTitle.height

        anchors {
            left: parent.left
            right: indicator.left
            rightMargin: 2
        }

        DS3.AtomTitle {
            id: atomTitle

            width: parent.width
            height: 16

            anchors.verticalCenter: parent.verticalCenter

            opacity: combobox.enabled ? 1 : 0.3
            title: codeText
            titleItem {
                color: ui.ds3.figure.base
                style: ui.ds3.text.body.LRegular
            }
        }
    }

    background: Rectangle {
        color: ui.ds3.figure.transparent
    }

    popup: Popup {
        width: sheetActionWidth
        height: popup.visible ? Math.min(contentItem.implicitHeight, 350) : 0

        padding: 0
        y: combobox.height + 8

        contentItem: DS3.ScrollView {
            padding: 0

            ListView {
                id: contentList

                width: parent.width
                implicitHeight: contentHeight

                clip: true
                spacing: 1
                model: combobox.popup.visible ? combobox.delegateModel : null
                currentIndex: combobox.highlightedIndex
                interactive: false
            }

            DS3.Spacing {
                height: 8

                visible: !!commentText
            }

            DS3.Comment {
                id: comment

                width: combobox.width

                anchors {
                    left: parent.left
                    leftMargin: 16
                    right: parent.right
                    rightMargin: 16
                }

                text: commentText
                visible: !!commentText
            }

            DS3.Spacing {
                height: 8

                visible: !!commentText
            }

            Rectangle {
                id: roundedMask

                width: bgRectangle.width
                height: bgRectangle.height

                visible: false
                radius: 12
                layer.enabled: true
            }

            layer.enabled: true
            layer.samplerName: "maskSource"
            layer.effect: ShaderEffect {
                property var colorSource: roundedMask
                property real contentWidth: popup.width
                property real contentHeight: popup.height

                //fragmentShader: util.shaders.round_corners
            }
        }

        background: Rectangle {
            id: bgRectangle

            color: ui.ds3.bg.high
            radius: 12

            DropShadow {
                anchors.fill: back

                verticalOffset: 1
                radius: parent.radius
                samples: 30
                color: ui.ds3.bg.overlay
                source: back
            }

            Rectangle {
                id: back

                anchors.fill: parent

                color: ui.ds3.bg.high
                radius: 12
            }
        }
    }

    DS3.MouseArea {
        acceptedButtons: Qt.NoButton
    }
}
