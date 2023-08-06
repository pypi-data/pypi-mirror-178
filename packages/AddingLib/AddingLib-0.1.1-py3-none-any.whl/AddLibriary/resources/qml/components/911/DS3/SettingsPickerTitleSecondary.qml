import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3


// Custom DS combobox
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
//  Whether the combobox needs to scroll to the chosen index
    property bool scrollToChosenWhenOpened: false

    /* ---------------------------------------------------- */
    /* desktop tests */
    property var accessibleTitleName: ""
    property var accessibleItemNamePrefix: ""
    /* ---------------------------------------------------- */

    Component.onCompleted: if (cancelBinding) currentIndex = currentIndex

    width: parent.width
    height: contentItem.height

    model: []
    delegate: ItemDelegate {
        id: itemDelegate

        width: combobox.width
        height: 40

        Rectangle {
            anchors.fill: parent

            color: combobox.highlightedIndex == index ? ui.ds3.bg.high : ui.ds3.bg.highest
        }

        contentItem: DS3.Text {
            anchors {
                verticalCenter: parent.verticalCenter
                left: parent.left
                leftMargin: 16
            }

            style: ui.ds3.text.body.MRegular
            text: suffix ? modelData + suffix : modelData
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
        }

        /* ---------------------------------------------------- */
        /* desktop tests */
        Accessible.name: combobox.accessibleItemNamePrefix ? combobox.accessibleItemNamePrefix + "_" + modelData : ""
        Accessible.description: combobox.accessibleItemNamePrefix ? "<button enabled=" + Accessible.checkable + ">" + modelData + "</button>" : ""
        Accessible.role: Accessible.Button
        Accessible.checkable: visible && enabled
        Accessible.onPressAction: {
            if (!Accessible.checkable) return
            combobox.currentIndex = index
            combobox.activated(index)
        }
        /* ---------------------------------------------------- */
    }

    indicator: DS3.Icon {
        anchors {
            right: combobox.right
            rightMargin: 16
            verticalCenter: combobox.verticalCenter
        }

        source: "qrc:/resources/images/Athena/common_icons/ActionArrow.v3.svg"
        rotation: popup.visible ? 180 : 0

        Behavior on rotation {
            NumberAnimation {
                duration: 200
            }
        }
    }

    contentItem: Item {
        height: atomTitle.height + 24

        anchors {
            left: parent.left
            right: indicator.left
            margins: 16
        }

        DS3.AtomTitle {
            id: atomTitle

            width: parent.width

            anchors.verticalCenter: parent.verticalCenter
            opacity: combobox.enabled ? 1 : 0.5
            subtitle: suffix ? combobox.displayText + suffix : combobox.displayText
            isPrimary: false
            subtitleItem.hasElide: true

            /* ---------------------------------------------------- */
            /* desktop tests */
            Accessible.name: combobox.accessibleTitleName
            Accessible.description: title
            Accessible.role: Accessible.Paragraph
            /* ---------------------------------------------------- */
        }
    }

    background: Rectangle {
        color: ui.ds3.bg.highest
    }

    popup: Popup {
        width: combobox.width
        height: popup.visible ? Math.min(contentItem.implicitHeight, 350) : 0

        padding: 0
        y: combobox.height - 8

        contentItem: DS3.ScrollView {
            onContentHeightChanged: {
                if (contentHeight != 0 && scrollToChosenWhenOpened) scrollToIndex(combobox.highlightedIndex)
            }

            function scrollToIndex(index) {
                let moveTo = 40 * (index - 1)
                scrollBar.scrollTo(moveTo)
            }

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
                color: ui.backgrounds.overlay
                source: back
            }

            Rectangle {
                id: back

                anchors.fill: parent

                color: ui.backgrounds.highest
                radius: 12
            }
        }
    }

    DS3.MouseArea {
        acceptedButtons: Qt.NoButton
    }
}
